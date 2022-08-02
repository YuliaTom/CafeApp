# About the project

CafeApp is an application for a pop-up cafe that allows to create orders for customers. It stores data in  MySQL database. Users can perform CRUD operations on their data.


## Goals

As a business:

I want to maintain a collection of products & couriers
When a customer makes a new order, I need to create it on the system
I need to be able to update the status of an order
When I exit the app, I need all data to be persisted
When I start the app, I need to load all persisted data
I want to be sure the app has been tested & proven to work well

## Installation

Install Python3 and pip
Create and activate virtual environment (Unix/MacOS):
```bash
python3 -m venv .venv
source .venv/bin/activate
```
Install the requirements:
```bash
pip install -r requirements.txt
```
Install Docker and compose docker-compose.yml
```bash
docker-compose up -d
```
