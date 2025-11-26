# Weather App

This project implements a serverless, event-driven, fully automated microservice on Google Cloud Platform (GCP) with:

Serverless ingestion using Cloud Scheduler + Cloud Function
Storage on Cloud Storage
AI-based weather insights using Vertex AI (Gemini)
Modern UI deployed on GKE
Complete automation using Terraform + GitHub Actions CI/CD
Secure secrets with Secret Manager
Least-privilege IAM roles
Dockerized deployment with Kubernetes

The final application is hosted at:
http://34.93.229.19/


## 1.Project Objective

To build a scalable, cost-efficient microservice that:
 Automatically collects weather data every 30 minutes
 Enriches it using GenAI (Vertex AI Gemini)
 Stores it in Cloud Storage
 Visualizes processed insights in a modern web UI
 Uses Terraform for infrastructure
 Uses Docker + Kubernetes + GKE for the UI layer
 Delivers fully automated deployment using CI/CD
 

## 2.Technologies Used

Compute-Cloud Functions, GKE
AI-Vertex AI Gemini APIs
Storage-Cloud Storage
Scheduling-Cloud Scheduler
IaC-Terraform
Containerization-Docker
CI/CD-GitHub Actions
Secrets-Secret Manager + Kubernetes Secrets


## 3.Project Structure
weather-function/
├── Dockerfile
├── main.py
├── requirements.txt
├── weather-dashboard/
│ ├── app.py
| ├── requirements.txt
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
| ├── cicd.yml
└── README.md


## 4.Final Outcomes

 Fully functional serverless microservice
 AI-powered weather insights
 Live UI running on GKE
 End-to-end automation
 Proper IAM, security, and cost-optimized infrastructure
 Understanding of Terraform, Docker, Kubernetes, GCP, CI/CD, Vertex AI



## 5.Learnings

Serverless compute
Production-grade CI/CD
AI integration
Container orchestration
Secure secrets management
Terraform provisioning
Cloud-native design patterns
