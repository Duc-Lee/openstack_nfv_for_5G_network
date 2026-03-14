# OpenStack Provider Configuration
provider "openstack" {
  auth_url    = var.openstack_auth_url
  region      = var.openstack_region
  user_name   = var.openstack_user_name
  password    = var.openstack_password
  tenant_name = var.openstack_tenant_name
  domain_name = "Default"
}

# Net cho quan ly
resource "openstack_networking_network_v2" "mgmt_net" {
  name           = "mgmt-net"
  admin_state_up = "true"
}

resource "openstack_networking_subnet_v2" "mgmt_subnet" {
  name       = "mgmt-subnet"
  network_id = openstack_networking_network_v2.mgmt_net.id
  cidr       = "192.168.10.0/24"
}

# Net cho 5G (Control Plane)
resource "openstack_networking_network_v2" "control_net" {
  name           = "control-net"
  admin_state_up = "true"
}

resource "openstack_networking_subnet_v2" "control_subnet" {
  name       = "control-subnet"
  network_id = openstack_networking_network_v2.control_net.id
  cidr       = "10.0.1.0/24"
}

# Net User Plane - eMBB
resource "openstack_networking_network_v2" "embb_net" {
  name           = "embb-net"
  admin_state_up = "true"
}

resource "openstack_networking_subnet_v2" "embb_subnet" {
  name       = "embb-subnet"
  network_id = openstack_networking_network_v2.embb_net.id
  cidr       = "10.0.10.0/24"
}

# Net User Plane - IoT
resource "openstack_networking_network_v2" "iot_net" {
  name           = "iot-net"
  admin_state_up = "true"
}

resource "openstack_networking_subnet_v2" "iot_subnet" {
  name       = "iot-subnet"
  network_id = openstack_networking_network_v2.iot_net.id
  cidr       = "10.0.20.0/24"
}

# Security group
resource "openstack_networking_secgroup_v2" "fiveg_secgroup" {
  name        = "fiveg-secgroup"
  description = "Rules cho 5G va SDN"
}

resource "openstack_networking_secgroup_rule_v2" "sctp_rule" {
  direction         = "ingress"
  ethertype         = "IPv4"
  protocol          = "sctp"
  port_range_min    = 38412
  port_range_max    = 38412
  remote_ip_prefix  = "0.0.0.0/0"
  security_group_id = openstack_networking_secgroup_v2.fiveg_secgroup.id
}

# Cac node K8s
resource "openstack_compute_instance_v2" "k8s_node" {
  count           = 3
  name            = "k8s-node-${count.index}"
  image_name      = "Ubuntu-22.04"
  flavor_name     = "m1.medium"
  security_groups = ["default", openstack_networking_secgroup_v2.fiveg_secgroup.name]

  network {
    name = openstack_networking_network_v2.mgmt_net.name
  }

  network {
    name = openstack_networking_network_v2.control_net.name
  }

  network {
    name = openstack_networking_network_v2.embb_net.name
  }

  network {
    name = openstack_networking_network_v2.iot_net.name
  }
}
