# Hệ thống 5G Core trên nền tảng OpenStack (NFV)

Dự án này mình tập trung vào việc triển khai và quản lý mạng 5G Core theo mô hình Cloud-Native, chạy trên hạ tầng OpenStack.

## 1. Bài toán giải quyết
Dự án này mình làm để tìm hiểu cách triển khai một mạng lõi 5G thực tế trên môi trường đám mây (Cloud). Thay vì cài đặt thủ công từng bước rất dễ lỗi, mình tập trung vào:
- **Tự động hóa hoàn toàn**: Dùng Terraform để dựng Infra, Ansible để cài K8s và script để deploy 5G. Mục tiêu là chỉ cần 1 câu lệnh là có cả hệ thống chạy.
- **Vận hành thông minh (SRE)**: Mình tích hợp thêm các kịch bản tự động kiểm tra sức khỏe hệ thống. Nếu một service (như AMF) bị treo, hệ thống sẽ tự phát hiện và khởi động lại hoặc cảnh báo ngay.
- **Tối ưu hóa**: Hệ thống có thể tự scale khi lượng người dùng giả lập tăng cao, đảm bảo mạng không bị nghẽn.

## 2. Mô hình mô phỏng
Mô hình mình xây dựng tập trung vào việc mô phỏng luồng kết nối thực tế trong mạng 5G Core, tuân thủ kiến trúc tách biệt giữa **Luồng điều khiển (Control Plane - CP)** và **Luồng dữ liệu (User Plane - UP)**:

- **Kết nối từ người dùng**: Điện thoại (UE) thông qua trạm phát sóng (gNB) để gửi yêu cầu đăng ký mạng. gNB sẽ giao tiếp trực tiếp với **AMF** (Thành phần quản lý truy cập và di động). Đây là luồng điều khiển chính.
- **Quản lý phiên và Đường truyền**: Khi UE muốn truy cập internet, **AMF** sẽ chuyển tiếp yêu cầu tới **SMF** (Thành phần quản lý phiên) thông qua giao diện **N11**. SMF có nhiệm vụ quyết định cách thức truyền dữ liệu.
- **Xử lý dữ liệu thực tế**: Sau khi có quyết định từ SMF, dữ liệu của người dùng sẽ đi thẳng từ gNB qua **UPF** (Thành phần xử lý dữ liệu người dùng) để ra internet. SMF điều khiển UPF này thông qua giao diện **N4**.
- **Lưu trữ tập trung**: Mọi thông tin về thuê bao, phiên kết nối và cấu hình được lưu trữ thống nhất trong **PostgreSQL** để đảm bảo dữ liệu không bị mất khi các service khởi động lại.
- **Tự động hóa SRE**: Toàn bộ hệ thống được giám sát bởi các script Python. Các script này sẽ thu thập dữ liệu về hiệu năng và trạng thái của AMF, SMF, UPF để tự động xử lý khi có sự cố.

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
