# Weather App

This project implements a serverless, event-driven, fully automated microservice on Google Cloud Platform (GCP) with:

•	Serverless ingestion using Cloud Scheduler + Cloud Function

•	Storage on Cloud Storage

•	AI-based weather insights using Vertex AI (Gemini)

•	Modern UI deployed on GKE

•	Complete automation using Terraform + GitHub Actions CI/CD

•	Secure secrets with Secret Manager

•	Least-privilege IAM roles

•	Dockerized deployment with Kubernetes

### The final application is hosted at:

http://34.93.229.19/

<img width="2370" height="1521" alt="image" src="https://github.com/user-attachments/assets/c1ba63f9-4e54-47fa-8cbe-71c64d7fe1c5" />
<img width="1633" height="1648" alt="image" src="https://github.com/user-attachments/assets/6b126a32-a2f1-4802-ae40-e02afd4a1085" />


## 1.Project Objective

To build a scalable, cost-efficient microservice that:

•	Automatically collects weather data every 30 minutes

•	Enriches it using GenAI (Vertex AI Gemini)

•	Stores it in Cloud Storage

•	Visualizes processed insights in a modern web UI

•	Uses Terraform for infrastructure

•	Uses Docker + Kubernetes + GKE for the UI layer

•	Delivers fully automated deployment using CI/CD

 

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
 ├── requirements.txt
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


# STEPS:

### Set Project ID
-export PROJECT_ID="mishka-cme-project"

### Create GCP Project
-gcloud projects create $PROJECT_ID --name="CME Weather Pipeline Project"

### Set Current Project
-gcloud config set project $PROJECT_ID

<img width="3199" height="1581" alt="image" src="https://github.com/user-attachments/assets/02f99ba8-081c-4abe-b7e9-1888fab10952" />

### Create Storage Bucket

1. Set Bucket Name
-export BUCKET_NAME="${PROJECT_ID}-weather-data"

2. Create GCS Bucket
-gsutil mb -l asia-south1 gs://$BUCKET_NAME/

<img width="3187" height="1582" alt="image" src="https://github.com/user-attachments/assets/5808c413-efc2-45d4-a530-27fd6430ef52" />

<img width="3199" height="310" alt="image" src="https://github.com/user-attachments/assets/293c945c-c3a1-4514-9bfd-ba69ce5f3f54" />

### Create Pub/Sub Topic

Create Weather Topic
-gcloud pubsub topics create weather-topic

### Deploy Cloud Function

Deploy the Weather Ingestion Function

gcloud functions deploy weather_ingest \
  --runtime=python311 \
  --region=asia-south1 \
  --gen2 \
  --trigger-topic=weather-topic \
  --set-env-vars "BUCKET_NAME=${PROJECT_ID}-weather-data,API_KEY=YOUR_OPENWEATHERMAP_API_KEY" \
  --entry-point=hello_world
  
### Create Cloud Scheduler Job

Trigger Function Every 30 Minutes

gcloud scheduler jobs create pubsub weather-job \
  --schedule="*/30 * * * *" \
  --time-zone="Asia/Kolkata" \
  --topic=weather-topic \
  --message-body="Trigger weather update"

### IAM Permissions

Grant Pub/Sub Subscriber Role

gcloud projects add-iam-policy-binding mishka-cme-project \
  --member="serviceAccount:574573355783-compute@developer.gserviceaccount.com" \
  --role="roles/pubsub.subscriber"


<img width="2636" height="1410" alt="image" src="https://github.com/user-attachments/assets/636b38a3-0188-474e-b8be-7ec721f70ed1" />

### Flask App Setup (Local)

Install Flask
pip install flask

### Enable Vertex AI + Install GenAI SDK

1.Enable API
-gcloud services enable aiplatform.googleapis.com

2.Install Google GenAI SDK
-pip install google-genai

<img width="3162" height="1580" alt="image" src="https://github.com/user-attachments/assets/630580da-d113-4596-bc33-2de999567e04" />

### Build & Deploy Container to Cloud Run

1.Build Docker Image

gcloud builds submit --tag gcr.io/mishka-cme-project/weatherapp


2.Deploy on Cloud Run

gcloud run deploy weatherapp \
  --image gcr.io/mishka-cme-project/weatherapp \
  --platform managed \
  --region asia-south1 \
  --allow-unauthenticated

<img width="2583" height="104" alt="image" src="https://github.com/user-attachments/assets/34fc55a3-78fc-47df-a0f3-27922b9ce18f" />

<img width="3168" height="1579" alt="image" src="https://github.com/user-attachments/assets/742de7f8-60a4-44c2-acd6-68f844bcf116" />

### Infrastructure Deployment via Terraform

terraform init

terraform plan

terraform apply

### Deploy to GKE (For Visualization App)

1.Apply Kubernetes Deployment
-kubectl apply -f k8s/deployment.yaml

2.Apply Kubernetes Service
-kubectl apply -f k8s/service.yaml

3.Apply Horizontal Pod Autoscaler
-kubectl apply -f k8s/hpa.yaml

<img width="2227" height="1585" alt="image" src="https://github.com/user-attachments/assets/c5bda211-6262-447d-9f90-919de0ae293a" />



<img width="1699" height="352" alt="image" src="https://github.com/user-attachments/assets/638426c0-7a5d-465c-8664-9c2651b9c96f" />

<img width="3153" height="1619" alt="image" src="https://github.com/user-attachments/assets/4d6aae1c-e545-4323-bb60-ef6f0b6e563d" />

<img width="2876" height="1341" alt="image" src="https://github.com/user-attachments/assets/f1421ae3-d406-4aee-9356-7fc918dd2109" />


## Github Actions
<img width="3187" height="1576" alt="image" src="https://github.com/user-attachments/assets/e8bd64eb-22a5-4476-86c5-8ecec3a89cb2" />

### Secrets
<img width="3190" height="1564" alt="image" src="https://github.com/user-attachments/assets/fa546909-3671-4fb8-ac7a-807f1f8876b9" />


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
