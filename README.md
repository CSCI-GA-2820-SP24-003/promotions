# NYU DevOps Spring 24 Promotions Squad

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)
[![Build Status](https://github.com/CSCI-GA-2820-SP24-003/promotions/actions/workflows/ci.yml/badge.svg)](https://github.com/CSCI-GA-2820-SP24-003/promotions/actions)
[![BDD Tests](https://github.com/CSCI-GA-2820-SP24-003/promotions/actions/workflows/bdd.yml/badge.svg)](https://github.com/CSCI-GA-2820-SP24-003/promotions/actions/workflows/bdd.yml)
[![codecov](https://codecov.io/gh/CSCI-GA-2820-SP24-003/promotions/graph/badge.svg?token=Y8JOEKTXJX)](https://codecov.io/gh/CSCI-GA-2820-SP24-003/promotions)

## Overview
This is the Promotions repository of the back-end of an e-Commerce Website as a collection of RESTful services. The Promotions Squad handles deals on products (Eg: 20 % discount, buy 1 get 1 etc.). You can use this link to access our service: https://promotions-anoushka21-dev.apps.sandbox-m2.ll9k.p1.openshiftapps.com/.

## Database Schema

| Column          | Data type | Details     |
|-----------------|-----------|-----------------|
| id              | `<integer>` | Primary key which is an unique identifier for the promotion      |
| name        | `<string>` | Name of the promotion |
| start_date  | `<date>`  | The start date of the promotion|
| duration       | `<integer>`  | Number of days for which the promotion is valid |
| rule      | `<string>`  | Rule describing the promotion|
| product_id    | `<integer>`  | Describes the product on which the promotion is applied|
| promotion_type    | `<enum>`  | Describes the type of promotion-AMOUNT_DISCOUNT,PERCENTAGE_DISCOUNT, BXGY or UNKNOWN|
 status   | `<boolean>`  | Describes if promotion is activated or not|

## RESTful API Endpoints

Detailed API information could be access at endpoint `/apidocs`.

| Method         | URL | Details     |
|-----------------|-----------|-----------------|
| `POST`             | `/promotions` |  Create a new promotion      |
| `GET`       | `/promotions/<int:promotion_id>` | Reads the promotion with id `promotion_id`  |
| `DELETE`  | `/promotions/<int:promotion_id>`  | Deletes the promotion with id `promotion_id` |
| `GET`     | `/promotions`  | Lists all the promotions. We can also query or filter the promotions using name, promotion_type, product_id, start_date, and status|
| `PUT`   | `/promotions/<int:promotions_id>`  | Updates existing promotion with id `promotion_id`|
| `PUT`   | `/promotions/<int:promotions_id>/activate`  | Activates existing promotion with id  `promotion_id`|
| `PUT`   | `/promotions/<int:promotions_id>/deactivate`  | Deactivates existing promotion with id  `promotion_id`|

## Run the service localy

You could run `make test` to run the TDD tests.

You could use `make lint` to run the pylint.

You could use `honcho start` to start the service, and it will run at `localhost:8080`. Then, you could run `behave` to run the BDD tests.

You could use `make cluster` followed by `kubectl apply -f k8s` to deploy our service locally and then run BDD test `behave` to check it.

## License

Copyright (c) 2016, 2024 [John Rofrano](https://www.linkedin.com/in/JohnRofrano/). All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the New York University (NYU) masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by [John Rofrano](https://cs.nyu.edu/~rofrano/), Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.

## TODO
<details>
  <summary> ORIGINAL TEMPLATE</summary>
  
  This is a skeleton you can use to start your projects

## Overview

This project template contains starter code for your class project. The `/service` folder contains your `models.py` file for your model and a `routes.py` file for your service. The `/tests` folder has test case starter code for testing the model and the service separately. All you need to do is add your functionality. You can use the [lab-flask-tdd](https://github.com/nyu-devops/lab-flask-tdd) for code examples to copy from.

## Automatic Setup

The best way to use this repo is to start your own repo using it as a git template. To do this just press the green **Use this template** button in GitHub and this will become the source for your repository.

## Manual Setup

You can also clone this repository and then copy and paste the starter code into your project repo folder on your local computer. Be careful not to copy over your own `README.md` file so be selective in what you copy.

There are 4 hidden files that you will need to copy manually if you use the Mac Finder or Windows Explorer to copy files from this folder into your repo folder.

These should be copied using a bash shell as follows:

```bash
    cp .gitignore  ../<your_repo_folder>/
    cp .flaskenv ../<your_repo_folder>/
    cp .gitattributes ../<your_repo_folder>/
```

## Contents

The project contains the following:

```text
.gitignore          - this will ignore vagrant and other metadata files
.flaskenv           - Environment variables to configure Flask
.gitattributes      - File to gix Windows CRLF issues
.devcontainers/     - Folder with support for VSCode Remote Containers
dot-env-example     - copy to .env to use environment variables
pyproject.toml      - Poetry list of Python libraries required by your code

service/                   - service python package
├── __init__.py            - package initializer
├── config.py              - configuration parameters
├── models.py              - module with business models
├── routes.py              - module with service routes
└── common                 - common code package
    ├── cli_commands.py    - Flask command to recreate all tables
    ├── error_handlers.py  - HTTP error handling code
    ├── log_handlers.py    - logging setup code
    └── status.py          - HTTP status constants

tests/                     - test cases package
├── __init__.py            - package initializer
├── test_cli_commands.py   - test suite for the CLI
├── test_models.py         - test suite for business models
└── test_routes.py         - test suite for service routes
```

</details>
