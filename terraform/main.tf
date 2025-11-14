resource "google_project_service" "enabled_apis" {
  for_each = toset([
    "container.googleapis.com",
    "compute.googleapis.com",
    "iam.googleapis.com",
    "servicenetworking.googleapis.com",
    "secretmanager.googleapis.com"
  ])

  project = var.project_id
  service = each.key
}

# Weather API Key Secret
resource "google_secret_manager_secret" "weather_api_key" {
  secret_id = "weather-api-key"
  replication {
    auto{}
  }
}

resource "google_secret_manager_secret_version" "weather_api_key_version" {
  secret      = google_secret_manager_secret.weather_api_key.id
  secret_data = var.weather_api_key
}

# Service Account JSON Key secret
resource "google_secret_manager_secret" "service_account_key" {
  secret_id = "weather-service-account-key"
  replication {
    auto{}
  }
}

resource "google_secret_manager_secret_version" "service_account_key_version" {
  secret      = google_secret_manager_secret.service_account_key.id
  secret_data = file(var.service_account_key_path)
}

resource "google_service_account" "weather_k8s_sa" {
  account_id   = "weather-k8s-service-account"
  display_name = "Weather App Kubernetes Service Account"
}

############################################
# 6. Grant Secret Accessor Role to K8s Service Account
############################################

resource "google_secret_manager_secret_iam_member" "weather_api_reader" {
  secret_id = google_secret_manager_secret.weather_api_key.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.weather_k8s_sa.email}"
}

resource "google_secret_manager_secret_iam_member" "sa_key_reader" {
  secret_id = google_secret_manager_secret.service_account_key.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.weather_k8s_sa.email}"
}

resource "kubernetes_secret" "weather_secrets" {
  metadata {
    name = "weather-secrets"
    namespace = "default"
  }

  data = {
    WEATHER_API_KEY               = var.weather_api_key
    GOOGLE_APPLICATION_CREDENTIALS = file(var.service_account_key_path)
  }

  type = "Opaque"

  depends_on = [google_container_cluster.weather_cluster]
}


resource "google_container_cluster" "weather_cluster" {
  name     = var.cluster_name
  location = var.region

  remove_default_node_pool = true
  initial_node_count       = 1

  network    = "default"
  subnetwork = "default"

  ip_allocation_policy {}

  cluster_autoscaling {
    enabled = true

    resource_limits {
      resource_type = "cpu"
      minimum       = 1
      maximum       = 4
    }

    resource_limits {
      resource_type = "memory"
      minimum       = 2
      maximum       = 8
    }
  }

  depends_on = [google_project_service.enabled_apis]
}

