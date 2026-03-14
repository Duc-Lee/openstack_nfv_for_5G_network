# Hệ thống 5G Core trên nền tảng OpenStack (NFV)

Dự án này mình tập trung vào việc triển khai và quản lý mạng 5G Core theo mô hình Cloud-Native, chạy trên hạ tầng OpenStack.

## 1. Bài toán giải quyết
Dự án này mình làm để tìm hiểu cách triển khai một mạng lõi 5G thực tế trên môi trường đám mây (Cloud). Thay vì cài đặt thủ công từng bước rất dễ lỗi, mình tập trung vào:
- **Tự động hóa hoàn toàn**: Dùng Terraform để dựng Infra, Ansible để cài K8s và script để deploy 5G. Mục tiêu là chỉ cần 1 câu lệnh là có cả hệ thống chạy.
- **Vận hành thông minh (SRE)**: Mình tích hợp thêm các kịch bản tự động kiểm tra sức khỏe hệ thống. Nếu một service (như AMF) bị treo, hệ thống sẽ tự phát hiện và khởi động lại hoặc cảnh báo ngay.
- **Tối ưu hóa**: Hệ thống có thể tự scale khi lượng người dùng giả lập tăng cao, đảm bảo mạng không bị nghẽn.

## 2. Mô hình mô phỏng
Mô hình mình xây dựng tuân thủ theo kiến trúc tách biệt giữa **Luồng điều khiển (Control Plane)** và **Luồng dữ liệu (User Plane)** của 3GPP:

```text
[ UE ] <--- Radio ---> [ gNB ]
                         |
           ----------------------------
           |                          |
      (Control Plane)            (User Plane)
           v                          v
        [ AMF ] <---- N11 ----> [ SMF ] <---- N4 ----> [ UPF ]
           |                      |                      |
           -----------------------------------------------
                                  |
                        [ Database (Postgres) ]
```
- **Luồng kết nối**: Điện thoại (UE) kết nối vào trạm phát sóng (gNB). gNB sẽ gửi các yêu cầu đăng ký mạng về **AMF**. 
- **Quản lý phiên**: **SMF** nhận lệnh từ AMF qua giao diện **N11** để thiết lập đường truyền dữ liệu.
- **Xử lý dữ liệu**: Dữ liệu thực tế của người dùng sẽ đi thẳng qua **UPF**. SMF điều khiển UPF thông qua giao diện **N4**.
- **Lưu trữ**: Tất cả thông tin thuê bao và cấu hình được quản lý tập trung trong **PostgreSQL**.

## 3. Các thành phần chính

- **Source code (`src/`)**: 
  - Các service: AMF, SMF, UPF, Auth, Orchestrator...
  - Dùng Python (FastAPI) và PostgreSQL.
- **Triển khai (`deployments/`)**:
  - `terraform/`: Tạo VM và mạng trên OpenStack.
  - `ansible/`: Cài đặt Kubernetes.
  - `k8s/`: Các file YAML chạy service.
- **Giám sát (`observability/`)**: Prometheus, Loki và Alertmanager.

## 4. Cách chạy dự án

1. **Bước 1 - Hạ tầng**:
   ```bash
   cd deployments/terraform/envs/prod
   terraform init && terraform apply
   ```
2. **Bước 2 - Cài K8s**:
   ```bash
   cd deployments/ansible
   ansible-playbook -i inventory.ini install_k8s.yml
   ```
3. **Bước 3 - Triển khai 5G**:
   ```bash
   kubectl apply -f deployments/k8s/secrets.yaml
   kubectl apply -f deployments/k8s/
   ```
