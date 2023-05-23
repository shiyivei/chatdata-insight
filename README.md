
# ChatdataInsight APP

Application built with FastAPI, React, and MongoDB. 

You need a mongodb account. 

## Setup MongoDB connection

``` 
    -> Create a .env file and add the following lines: 

    DB_URL = "mongodb+srv://<name>:<password>@..."
    DB_NAME = "PolarDashApp"
    COLLECTION_NAME = "polardash"

```

## Setup backend

In the backend folder
```
    -> Create a new env. with python3 -m venv polardash-backend-env
    -> Activate the virtual env. with source polardash-backend-env/bin/activate 
    -> Install dependencies with <b>pip install -r requirements.txt</b>
    -> Activate the backend with python main.py

```

## Setup frontend

In the frontend folder 
```
    -> Create a new env. with python3 -m venv polardash-frontend-env
    -> Activate the virtual env. with source polardash-frontend-env/bin/activate
    -> Install react app with npm install 
    -> npm install react-router-dom

    -> Run the app with npm start
```

## API Test Examples

### 1 Query on-chain information

```
Please check what is the ENS associated with the account 0xEf1c6E67703c7BD7107eed8303Fbe6EC2554BF6B
```

```
Can you help me examine the details of this contract: 0xf2A22B900dde3ba18Ec2AeF67D4c8C1a0DAB6aAC?
```

### 2 Query transaction data

```
How has Bitcoin performed over the past hour?
```

### 3 Query media news

```
What news are there about Bitcoin?
```
