# Makefile

.PHONY: all
.DEFAULT_GOAL: help

.PHONY: clean
clean: ## Remove temporary cache/coverage files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache .coverage

.PHONY: help
help: ## Show make target documentation
	@awk -F ':|##' '/^[^\t].+?:.*?##/ {\
	printf "\033[36m%-30s\033[0m %s\n", $$1, $$NF \
	}' ${MAKEFILE_LIST}

.PHONY: prebuild
prebuild: clean ## Install or upgrade environment dependencies like Poetry
	python -m pip install --upgrade pip setuptools wheel
	python -m pip install poetry==1.7.1

.PHONY: build
build: prebuild ## Install dependencies
	python -m poetry install --no-root

.PHONY: test
test: ## Execute test cases
	python -m poetry run pytest

.PHONY: lint
lint: ## Run lint
	python -m poetry run pylint ./server

.PHONY: imgbuild
DOCKER_USERNAME ?= user
ENV ?= local
imgbuild: ## Build docker image
	docker build -t $(DOCKER_USERNAME)/santander-consumer-transactions-app-$(ENV):latest .

.PHONY: imgpush
DOCKER_USERNAME = user
ENV ?= local 
imgpush: ## Push docker image to container registry
	docker push $(DOCKER_USERNAME)/santander-consumer-transactions-app-$(ENV):latest

.PHONY: datafetch
datafetch: ## Fetch raw data from kaggle
	mkdir -p ~/.kaggle
	cp -r ./kaggle.json ~/.kaggle/
	chmod 600 ~/.kaggle/kaggle.json
	python -m poetry run kaggle competitions download -c santander-customer-transaction-prediction -p ./data/raw/
	unzip ./data/raw/santander-customer-transaction-prediction.zip -d ./data/raw
	rm -rf ./data/raw/santander-customer-transaction-prediction.zip

.PHONY: runserver
runserver: ## Run inference server on local
	python -m poetry run python -m server

.PHONY: checkmodelhash
checkmodelhash:
	python -m poetry run python -m utils.check_hash

.PHONY: mlflow
mlflow: ## Run mlflow ui
	python -m poetry run mlflow ui

.PHONY: kfolds
kfolds: ## Run kfolds split on raw data
	python -m poetry run python -m ml.create_folds

.PHONY: train
TRAINING_DATA ?= data/raw/train_folds.csv
TEST_DATA ?= data/raw/test.csv
MODEL = lightgbm
train: ## Train classifier
	FOLD=0 MODEL=$(MODEL) TRAINING_DATA=$(TRAINING_DATA) TEST_DATA=$(TEST_DATA) python -m poetry run python -m ml.train
	FOLD=1 MODEL=$(MODEL) TRAINING_DATA=$(TRAINING_DATA) TEST_DATA=$(TEST_DATA) python -m poetry run python -m ml.train
	FOLD=2 MODEL=$(MODEL) TRAINING_DATA=$(TRAINING_DATA) TEST_DATA=$(TEST_DATA) python -m poetry run python -m ml.train
	FOLD=3 MODEL=$(MODEL) TRAINING_DATA=$(TRAINING_DATA) TEST_DATA=$(TEST_DATA) python -m poetry run python -m ml.train
	FOLD=4 MODEL=$(MODEL) TRAINING_DATA=$(TRAINING_DATA) TEST_DATA=$(TEST_DATA) python -m poetry run python -m ml.train

.PHONY: predict
TEST_DATA ?= data/raw/test.csv
MODEL =
predict: ## Run classifier on test set
	MODEL=$(MODEL) TEST_DATA=$(TEST_DATA) python -m poetry run python -m ml.predict

.PHONY: stagemodel
MODEL =  
stagemodel: ## Stage model for deployment
	cp models/$(MODEL) staged/clf.pkl

.PHONY: cleanmodels
cleanmodels: ## Clean stashed models
	rm -rf models/*

.PHONY: runstreamlit
runstreamlit: ## Run streamlit app locally
	python -m pip install -r requirements.txt
	DEPLOYED_TARGET=http://localhost:8000 BACKUP_TARGET=http://localhost:8000 python -m streamlit run streamlit_app.py
