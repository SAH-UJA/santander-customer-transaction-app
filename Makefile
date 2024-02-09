# Makefile

.PHONY: all
.DEFAULT_GOAL: help

.PHONY: clean
clean: ## Remove temporary cache/coverage files
	rm -rf __pycache__ .pytest_cache .coverage

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
	poetry run pytest --cov

.PHONY: imgbuild
imgbuild:
	docker build -t ${{ secrets.DOCKER_USERNAME }}/santander-consumer-transactions-app:latest .

.PHONY: imgpush
imgpush:
	docker push ${{ secrets.DOCKER_USERNAME }}/santander-consumer-transactions-app:latest