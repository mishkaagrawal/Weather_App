variable "project_id" {
  description = "GCP project ID"
  default     = "mishka-cme-project"
}

variable "region" {
  description = "Region for GKE cluster"
  default     = "asia-south1"
}

variable "cluster_name" {
  description = "Name of the GKE cluster"
  default     = "weather-gke-cluster"
}


variable "weather_api_key" {
  type      = string
  sensitive = true
}

variable "service_account_key" {
  type      = string
  sensitive = true
}

variable "k8s_sa_name" {
  default = "weather-k8s-sa"
}
