# He thong 5G Core tren nen tang OpenStack (NFV)

Day la do an cua minh ve viec trien khai cac Network Function (NF) cho mang 5G Core. He thong nay chay tren OpenStack, dung Kubernetes de quan ly cac service va co tinh nang tu dong scale, giam sat.

## Cac thanh phan chinh

- **Source code (`src/`)**: 
  - Co cac service nhu AMF, SMF, UPF, Auth, Orchestrator...
  - Code Python (FastAPI), dung PostgreSQL de luu database.
- **Trien khai (`deployments/`)**:
  - `terraform/`: Dung de tao may ao (VM) va mang tren OpenStack.
  - `ansible/`: Dung de cai dat nhanh Kubernetes len cac VM do.
  - `k8s/`: Cac file YAML de chay service tren K8s.
- **Giam sat (`observability/`)**: Co Prometheus de theo doi thong so va Alertmanager de bao thong bao.

## Cach chay dự án

1. **Buoc 1 - Infra**: Chay Terraform de tao moi truong OpenStack.
   ```bash
   cd deployments/terraform/envs/prod
   terraform init && terraform apply
   ```
2. **Buoc 2 - Cai K8s**: Dung Ansible de setup cluster.
   ```bash
   cd deployments/ansible
   ansible-playbook -i inventory.ini install_k8s.yml
   ```
3. **Buoc 3 - Chay 5G Core**:
   ```bash
   # Tao secret truoc (rat quan trong, de bao mat)
   kubectl apply -f deployments/k8s/secrets.yaml
   # Sau do apply het cac file trong k8s folder
   kubectl apply -f deployments/k8s/
   ```

## Luu y
- May ao Ubuntu dung user: `leanhduc`.
- Database Postgres dung username: `duckle`, password: `anhduc2005`.
- Moi thong tin bao mat deu duoc de trong `secrets.yaml`, khong nen sua truc tiep trong code.

---
*Project nay minh tu lam va tim hieu, co tham khao cac tai lieu tren mang.*
