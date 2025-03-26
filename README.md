# stage0_fran

This repository contains Fran the Facilitator, an API and Echo Chatbot that supports creating, conducting, and recording Design Thinking workshops for stage0. 

This system uses the [Flask](https://flask.palletsprojects.com/en/stable/) API framework, and the [Stage0 Echo](https://github.com/agile-learning-institute/stage0_py_utils/blob/main/ECHO.md) discord chat agent framework.

# Contributing

## Prerequisites

- [Stage0 Developer Edition]() #TODO for now Docker
- [Python](https://www.python.org/downloads/)
- [Pipenv](https://pipenv.pypa.io/en/latest/installation.html)
- [ollama](https://ollama.com/)

### Optional

- [Mongo Compass](https://www.mongodb.com/try/download/compass) - if you want a way to look into the database

## Folder structure for source code

```text
/stage0_fran        Repo Root
│── 📁 docs           OpenAPI Documentation
│── 📁 fran_model     [Fran LLM](./fran_model/README.md) Model & Prompts
│── 📁 stage0_fran    The Fran server
│   ├── 📁 agents         ECHO Agents
│   ├── 📁 routes         Flask routes
│   ├── 📁 services       Business Services
│── 📁 tests          Unittest for stage0_fran
│   ├── 📁 agents         Test for Agents
│   ├── 📁 routes         Test for Routes
│   ├── 📁 services       Test for Services
│   ├── stepci.yaml       API Black Box testing
│── README.md
```

## Install Dependencies

```bash
pipenv install
```

## Run Unit Testing

```bash
pipenv run test
```
NOTE: This excludes the tests with a backing service i.e. testbacking_mentorhub_mongo_io.py which can be run in vscode with the mongodb backing database running. 

## {re}start the containerized database and run the API locally
# NOTE: Not Functional till stage0 developer edition is created
```bash
pipenv run start
```

## Run the API locally (assumes database is already running)

```bash
pipenv run local
```

## Build and run the server Container
This will build the new container, and {re}start the mongodb and API container together.
NOTE: partially functional until stage0 developer edition is there
```bash
pipenv run container
```

## Run StepCI end-2-end testing
NOTE: Assumes the API is running at localhost:8580
```bash
pipenv run stepci
```

## Additional Automation
See the [fran_model README](./fran_model/README.md) for information on additional pipenv scripts. 

# API Testing with CURL

There are quite a few endpoints, see [CURL_EXAMPLES](./CURL_EXAMPLES.md) for all of them.

The [Dockerfile](./Dockerfile) uses a 2-stage build, and supports both amd64 and arm64 architectures. 