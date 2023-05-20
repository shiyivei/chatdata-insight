
# PolarDash FARM-Stack APP

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
    -> Create a new env. with pyton3 -m venv polardash-backend-env
    -> Activate the virtual env. with source polardash-backend-env/bin/activate 
    -> Install dependencies with <b>pip install -r requierments.txt</b>
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

## Test API Examples

```
http://127.0.0.1:3004/api/integration/request?prompt=Please check what is the ENS associated with the account 0xEf1c6E67703c7BD7107eed8303Fbe6EC2554BF6B
```

```
http://127.0.0.1:3004/api/integration/request?prompt=What news are there about Bitcoin?
```

```
http://127.0.0.1:3004/api/integration/request?prompt=How has Bitcoin performed over the past hour?
```

```
http://137.184.5.217:3004/api/integration/request?prompt=What news are there about Bitcoin?
```

```
http://137.184.5.217:3004/api/integration/request?prompt=can you help me examine the details of this contract: 0xf2A22B900dde3ba18Ec2AeF67D4c8C1a0DAB6aAC?
```

