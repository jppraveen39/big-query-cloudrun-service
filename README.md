# BigQuery Table Manager on Cloud Run

## Overview
This repository contains a Python-based service deployed on **Google Cloud Run**, which allows users to **create, delete, and retrieve** BigQuery table details.

## Features
- **Create a BigQuery Table**
- **Insert data into the table**
- **Fetch all records from the table**
- **Delete records from the table**

## Prerequisites
Before running the service, ensure you have:
- A **Google Cloud Project** with **BigQuery** and **Cloud Run** enabled.
- **gcloud CLI** installed and authenticated.
- **Docker** installed for building and pushing the container.

## Setup
### 1. **Create a BigQuery Table**
Run the following SQL command to create a table in **BigQuery**:
```sql
CREATE TABLE `igneous-fold-344311.test_dataset.my_table` (
    name STRING,
    age INT64,
    email STRING
);
```
To verify the table, run:
```sql
SELECT * FROM `igneous-fold-344311.test_dataset.my_table`;
```

### 2. **Build and Deploy the Service**
#### **Build the Docker Image**
```sh
docker build -t gcr.io/igneous-fold-344311/my-app:latest .
```

#### **Push the Image to Google Container Registry**
```sh
docker push gcr.io/igneous-fold-344311/my-app:latest
```

#### **Deploy to Cloud Run**
##### **Publicly Accessible Deployment**
```sh
gcloud run deploy my-app \
    --image gcr.io/igneous-fold-344311/my-app:latest \
    --region=us-central1 \
    --project=igneous-fold-344311
```

##### **Private Deployment (Requires Authentication)**
```sh
gcloud run deploy my-app \
    --image gcr.io/igneous-fold-344311/my-app:latest \
    --region=us-central1 \
    --no-allow-unauthenticated \
    --project=igneous-fold-344311
```

## API Endpoints

### **Obtain an Access Token**
Before making requests to the API, get an authentication token by running:
```sh
gcloud auth print-access-token
```

After deployment, your Cloud Run service URL will look like:
```
https://my-app-396977120295.us-central1.run.app
```

### **1. Fetch Records (GET Request)**
```sh
curl -X GET https://my-app-396977120295.us-central1.run.app/fetch \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### **2. Insert Data (POST Request)**
```sh
curl -X POST https://my-app-396977120295.us-central1.run.app/insert \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"name": "Praveen", "age": 25, "email": "praveen2532@gmail.com"}'
```

### **3. Delete Record (DELETE Request)**
```sh
curl -X DELETE https://my-app-396977120295.us-central1.run.app/delete \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"name": "Praveen"}'
```

## Conclusion
This project provides a simple REST API to manage BigQuery tables and is deployed on **Cloud Run** for scalability and ease of use.

Feel free to contribute and improve this repository!

