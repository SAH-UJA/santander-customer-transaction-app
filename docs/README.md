# Santander Customer Transaction Prediction App
A simple web app to predict if a customer will make a transaction using the famous Santander Customer Transaction Dataset.

# Background
This projects demonstrates a basic MLOps pipeline for a machine learning model using Python and incorporating key DevOps best practices. The model developed in this project is a simple classification model to predict if a customer will make a transaction, using the famous Santander Customer Transaction Dataset.

# Pipeline Components ([Design Diagram](design.jpeg))

* __Experimentation Tracking__: The journey of a model begins on local where data scientist build/train a model. With so many iterations needed to come up with an optimal model performing well on test set, it is essential to have an experimentation tracking server in place. Here's in our design we have used MLFlow which is an open-source well-established tool for experiment/model tracking, logging and registry.

* __Version Control__: With multiple version of the code/data/model committed, it is essential to track the changes and collaborate with other developers. It is therefore essential to have a VCS which in our case is Github (for code versioning) & Git LFS (for model versioning) given these are open-source and have a strong integration. Git LFS is used for storing/versioning Large Files and it is integrated with Git.

* __CI/CD__: The quality of a software depends on the best practices used to build it. CI/CD plays a critical role in building, scanning and deploying the code/model to the target instances so that it can be eventually delivered to the user without failure and manual intervention. The CI/CD service used in this project is Github Action given it is open-source and integrated well with GitHub & has a rich set of Actions.

* __Model Repository__: The models that are to be shipped have to be stored somewhere so that while building a server or for just getting a specific shared model, we can pull it conveniently. Model Repository used in our case is HuggingFace & DockerHub.

* __Container Registry__: Container Registry is used for managing and storing container which can eventually be pulled and run in an orchestration platform. This service should be durable and reliable since it is where the shipped application code/model bundle resides. The Container Registry used in this project is DockerHub given that it is an open-source, reliable and user-friendly tool.

* __Model/Application Monitoring__: Model/Application Monitoring is essential to monitor the health of an application running in production and can often be integrated with alerts/notifications alarming teams in case of failure or downtime. It was essential to have this piece in the design given the hosting service used was unreliable given that it is a free version and the application uptime on that platform depended on the hits on the server.

* __Model serving__: In order to expose an interface on top of a model for users/clients to run inference and get the prediction we need an API server which in our case is FastAPI. FastAPI is an open-source ASGI server written in Python and offers rich set of feature with pretty less learning curve. The FastAPI application runs on Render.com which is a managed hosting platform that has a free tier and provides a range of features like provisioning a Postgres DB, Redis server, Web Servers, Background Jobs, etc. The only downside is that it is a bit unreliable. Due to this we have 2 versions of the API servers deployed. A Kubernetes-based platform would have been more reliable but there wasn't any available for free.

* __User Interface__: UI acts as a first point of contact for users/clients therfore it is essential to design it properly and keep UI/UX principles in mind. The UI built in this project is a simple streamlit app that has allows users to upload a CSV file with all the var info (Refer [../tests/test_data/batch_of_two.csv] for sample data) and on clicking the Get Predictions buttion it hits the deployed API and gets the prediction in a neat dataframe format.


# Quick Setup Guide

This project can be setup on local by simply following the steps below:

## Developer Environment Setup 

### Clone repository
```bash
git clone https://github.com/SAH-UJA/santander-customer-transaction-app.git # Clone the repository
```

### Build dependencies
```bash
make build # Install all the dependencies and packages
```

### Run backend server 
#### Swagger UI can be viewed at /api/v1/docs route
```bash
make runserver # Spins up the FastAPI backend which serves the inference API
```

### Run frontend server
```bash
make runstreamlit # Spins up a Streamlit UI app and uses the backend server running locally
```

## Modeling Workflow

### Fetch data from kaggle 
#### In order to get the data from kaggle, you'd require kaggle.json file that contains the username and the API key to be stored in .kaggle folder in the root of this project
```bash
make datafetch # The raw data gets stored in data/raw/ folder
```

### Split data into kfolds
```bash
make kfolds # This will create 5 folds of data in the data/raw/ folder
```

### Start the MLFlow tracking server
```bash
make mlflow # This will launch mlflow tracking server
```

### Train the model 
#### More models can be added in [ml/dispatcher.py] to use them with this interface
```bash
make train MODEL=lightgbm # This will train lightgbm model on the data folds. Other model available is "randomforest"
```

### Run the model on the test set
```bash
make predict MODEL=lightgbm # This will run inference on the test set and generate the output as a submission.csv in models/ folder
```

### Stage the model for deployment
```bash
make stagemodel MODEL=<FINAL_MODEL>.pkl # This will simple move the <FINAL_MODEL>.pkl file in the models/staged folder
```

### Viewing the final model end-to-end on local
```bash
make runserver
make runstreamlit
```

## Miscellaneous

### Clean the state of the repo i.e. remove __pycache__, .coverage, etc.
```bash
make clean
```

### Run tests 
```bash
make test
```


