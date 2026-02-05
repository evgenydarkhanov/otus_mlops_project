### VIRTUAL MACHINE RESOURCES ###

resource "yandex_compute_disk" "disk" {
  name     = var.yc_disk_name
  type     = var.yc_disk_type
  zone     = var.yc_zone
  image_id = var.yc_image_id
}

resource "yandex_compute_instance" "vm" {
  name        = var.yc_vm_name
  platform_id = var.yc_platform_id
  zone        = var.yc_zone

  resources {
    cores  = var.yc_vm_cores
    memory = var.yc_vm_memory
  }

  boot_disk {
    disk_id = yandex_compute_disk.disk.id
  }

  network_interface {
    subnet_id = yandex_vpc_subnet.subnet.id
    nat       = true
  }

  metadata = {
    ssh-keys  = "ubuntu:${file(var.yc_ssh_public_key_path)}" 
    user-data = templatefile("${path.root}/scripts/user_data.sh", {
      ACCESS_KEY             = yandex_iam_service_account_static_access_key.sa-static-key.access_key
      SECRET_KEY             = yandex_iam_service_account_static_access_key.sa-static-key.secret_key
      S3_BUCKET              = yandex_storage_bucket.data_bucket.bucket
      COMMON_VOICE_DATASET   = var.common_voice_dataset
      COMMON_VOICE_API_KEY   = var.common_voice_api_key
      preprocess_data_base64 = filebase64("${path.root}/../src/preprocess_data.py")
      convert_data_base64    = filebase64("${path.root}/../src/convert_data.py")
    })
  }
}
