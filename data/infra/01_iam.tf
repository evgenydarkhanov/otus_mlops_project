### IAM RESOURCES ###

resource "yandex_iam_service_account" "sa" {
  name        = var.yc_service_account_name
  folder_id   = var.yc_folder_id
  description = "Service account for S3 Object Storage"

  # защищаем от удаления
  lifecycle {
    prevent_destroy = true
  }
}

resource "yandex_resourcemanager_folder_iam_member" "sa_roles" {
  folder_id = var.yc_folder_id
  role      = "storage.admin"
  member    = "serviceAccount:${yandex_iam_service_account.sa.id}"

  # защищаем от удаления
  lifecycle {
    prevent_destroy = true
  }
}
