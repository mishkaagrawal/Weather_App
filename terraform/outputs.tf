# ----------------------------
# GKE Cluster Information
# ----------------------------
output "cluster_name" {
  description = "Name of the created GKE cluster"
  value       = google_container_cluster.weather_cluster.name
}

output "cluster_location" {
  description = "Region or zone where the cluster is deployed"
  value       = google_container_cluster.weather_cluster.location
}

output "cluster_endpoint" {
  description = "Endpoint (IP address) of the GKE cluster"
  value       = google_container_cluster.weather_cluster.endpoint
}

output "cluster_master_version" {
  description = "Master (control plane) Kubernetes version"
  value       = google_container_cluster.weather_cluster.min_master_version
}

output "cluster_ca_certificate" {
  description = "Base64-encoded public CA certificate for the cluster"
  value       = google_container_cluster.weather_cluster.master_auth[0].cluster_ca_certificate
  sensitive   = true
}

# ----------------------------
# Node Pool Information
# ----------------------------
output "node_pool_name" {
  description = "Name of the GKE node pool"
  value       = google_container_node_pool.weather_nodes.name
}

output "node_pool_machine_type" {
  description = "Machine type used in the node pool"
  value       = google_container_node_pool.weather_nodes.node_config[0].machine_type
}


# ----------------------------
# Helpful Connection Command
# ----------------------------
output "gcloud_get_credentials_command" {
  description = "Command to authenticate kubectl with the GKE cluster"
  value = "gcloud container clusters get-credentials ${google_container_cluster.weather_cluster.name} --region ${google_container_cluster.weather_cluster.location} --project ${var.project_id}"
}


output "service_account_email" {
  value = google_service_account.weather_k8s_sa.email
}
