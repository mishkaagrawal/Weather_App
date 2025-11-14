# Weather App

A cloud-native weather dashboard application built with Python, deployed on **Google Kubernetes Engine (GKE)**, using **Docker** and **Terraform** for infrastructure management.

---

## Features

- Displays current weather information for any city.
- Built with Python Flask for backend and HTML templates for frontend.
- Deployed on a scalable Kubernetes cluster.
- Infrastructure is managed via Terraform.
- CI/CD pipeline automates build, Docker image push, Terraform apply, and Kubernetes deployment.

---

## Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML/CSS (Flask templates)
- **Containerization:** Docker
- **Infrastructure as Code:** Terraform
- **Orchestration:** Kubernetes (GKE)
- **CI/CD:** GitHub Actions
- **Cloud Provider:** Google Cloud Platform (GCP)

---

## Project Structure
weather-function/
├── Dockerfile
├── main.py
├── requirements.txt
├── weather-dashboard/
│ ├── app.py
│ └── templates/
│ └── weather.html
├── terraform/
│ ├── main.tf
│ ├── variables.tf
│ ├── outputs.tf
│ ├── node_pool.tf
│ └── providers.tf
├── kubernetes/
│ ├── deployment.yaml
│ ├── service.yaml
│ └── hpa.yaml
└── .github/workflows/
└── google.yml