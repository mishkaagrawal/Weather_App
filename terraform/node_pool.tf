resource "google_container_node_pool" "weather_nodes" {
name = "${var.cluster_name}-pool"
location = var.region
cluster = google_container_cluster.weather_cluster.name


autoscaling {
min_node_count = 0
max_node_count = 3
}


management {
auto_repair = true
auto_upgrade = true
}


node_config {
machine_type = "e2-medium"
preemptible = true
disk_type = "pd-standard"
disk_size_gb = 30


oauth_scopes = ["https://www.googleapis.com/auth/cloud-platform"]
}


depends_on = [google_container_cluster.weather_cluster]
}