### PROVIDER VARIBLES AND SHARED VARIABLES ###
variable "yc_zone" {
  description = "The availability zone to use for resources"
  type        = string
}

variable "yc_token" {
  description = "The OAuth token for Yandex Cloud"
  type        = string
}

variable "yc_cloud_id" {
  description = "The ID of the Yandex Cloud"
  type        = string
}

variable "yc_folder_id" {
  description = "The ID of the Yandex Cloud folder"
  type        = string
}

variable "yc_ssh_public_key_path" {
  description = "Path to the public key file"
  type        = string
}

variable "yc_ssh_private_key_path" {
  description = "Path to the private key file"
  type        = string
}

### IAM VARIABLES ###
variable "yc_service_account_name" {
  description = "The name of the service account to create"
  type        = string
}

### NETWORK VARIABLES ###
variable "yc_network_name" {
  description = "Name of the network"
  type        = string
}

variable "yc_subnet_name" {
  description = "Name of the subnet"
  type        = string
}

variable "yc_subnet_range" {
  description = "IDR block for the subnet"
  type        = string
}

### STORAGE VARIABLES ###
variable "yc_bucket_name" {
  description = "The name of the storage bucket to create"
  type        = string
}

variable "yc_bucket_size" {
  description = "The size of the storage bucket to create"
  type        = number
}

variable "yc_default_storage_class" {
  description = "The class of the storage bucket to create"
  type        = string
}

### VIRTUAL MACHINE VARIABLES ###
variable "yc_disk_name" {
  description = "The name of the disk to create"
  type        = string
}

variable "yc_disk_type" {
  description = "The type of disk to create"
  type        = string
}

variable "yc_image_id" {
  description = "ID of the image for the virtual machine"
  type        = string
}

variable "yc_vm_name" {
  description = "Name of the virtual machine"
  type        = string
}

variable "yc_platform_id" {
  description = "The platform ID for the VM"
  type        = string
}

variable "yc_vm_cores" {
  description = "The number of CPU cores for the VM"
  type        = number
}

variable "yc_vm_memory" {
  description = "The amount of memory (GB) for the VM"
  type        = number
}

variable "common_voice_dataset" {
  description = "Dataset link"
  type        = string
}

variable "common_voice_api_key" {
  description = "Common voice API key"
  type        = string
}
