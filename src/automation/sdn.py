import logging
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, set_ev_cls
from ryu.ofproto import ofproto_v1_3
from prometheus_client import start_http_server, Counter
from src.common.config import settings


PROMETHEUS_PORT = settings.PROMETHEUS_PORT
# Prometheus metric
flow_mod_counter = Counter(
    "sdn_flow_mod_total",
    "Flow rule added",
    ["slice"]
)

class FiveGSdnController(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logging.info("Starting 5G slicing SDN controller")
        start_http_server(PROMETHEUS_PORT)
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto
        match = parser.OFPMatch()
        actions = [
            parser.OFPActionOutput(
                ofproto.OFPP_CONTROLLER,
                ofproto.OFPCML_NO_BUFFER
            )
        ]
        self.add_flow(datapath, 0, match, actions, "default")
        # eMBB slice
        embb_match = parser.OFPMatch(
            eth_type=0x0800,
            ipv4_dst="10.45.0.0/16"
        )
        embb_actions = [parser.OFPActionOutput(1)]
        self.add_flow(datapath, 100, embb_match, embb_actions, "embb")
        # IoT slice
        iot_match = parser.OFPMatch(
            eth_type=0x0800,
            ipv4_dst="10.46.0.0/16"
        )
        iot_actions = [parser.OFPActionOutput(2)]
        self.add_flow(datapath, 100, iot_match, iot_actions, "iot")

    def add_flow(self, datapath, priority, match, actions, slice_name):
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto
        instructions = [
            parser.OFPInstructionActions(
                ofproto.OFPIT_APPLY_ACTIONS,
                actions
            )
        ]
        flow_mod = parser.OFPFlowMod(
            datapath=datapath,
            priority=priority,
            match=match,
            instructions=instructions
        )
        datapath.send_msg(flow_mod)
        flow_mod_counter.labels(slice=slice_name).inc()
        logging.info(f"Flow installed for slice: {slice_name}")