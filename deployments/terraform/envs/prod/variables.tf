variable "openstack_auth_url" {
  description = "The authentication URL for OpenStack"
  type        = string
}

variable "openstack_region" {
  description = "The region for OpenStack"
  type        = string
  default     = "RegionOne"
}

variable "openstack_user_name" {
  description = "The username for OpenStack"
  type        = string
}

variable "openstack_password" {
  description = "The password for OpenStack"
  type        = string
  sensitive   = true
}

variable "openstack_tenant_name" {
  description = "The project/tenant name for OpenStack"
  type        = string
}
