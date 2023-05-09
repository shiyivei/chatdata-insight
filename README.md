
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

