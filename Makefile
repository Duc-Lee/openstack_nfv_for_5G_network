# Makefile dung de chay nhanh cac lenh trong do an
.PHONY: setup-infra setup-k8s deploy clean build

# 1. Chay Terraform de tao VM
setup-infra:
	cd deployments/terraform/envs/prod && terraform init && terraform apply

# 2. Cai dat K8s cho cac VM vua tao
setup-k8s:
	ansible-playbook -i deployments/ansible/inventory.ini deployments/ansible/install_k8s.yml

# 3. Build docker cho toan bo service
build:
	docker build -t 5g-core-amf:latest src/services/amf
	docker build -t 5g-core-smf:latest src/services/smf
	docker build -t 5g-core-upf:latest src/services/upf
	docker build -t 5g-core-auth:latest src/services/auth_service
	docker build -t 5g-core-orchestrator:latest src/services/orchestrator
	docker build -t 5g-core-infra:latest src/services/infra_manager

# 4. Deploy vao K8s
deploy:
	# Phai tao secret truoc de co pass login database
	kubectl apply -f deployments/k8s/secrets.yaml
	# Sau do apply het config va deployment
	kubectl apply -f deployments/k8s/

# Don dẹp may cai cached
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
