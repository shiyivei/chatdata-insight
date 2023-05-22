
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



```
async def analyze_prompt(
    prompt: str
): 
    try:

        print("user request:",prompt)
        answer = get_judgment_results(prompt)

        if answer["case_number"] == "1":
                 
            value = query_ethereum_info(prompt)

            res = {
            "question_type": "chain_info",
            "data": value,
            }

            return res
            # return value


        elif answer["case_number"] == "2":
            params = get_binance_prams(prompt)

            symbol = params["symbol"]
            currency="USDT"
            klines= params["k_lines"]
            dataframe = params["dataframe"]

            print("symbol:",symbol)
            print("currency:",currency)
            print("klines:",klines)
            print("dataframe:",dataframe)
            
            data = binance_api.get_historical_price(symbol, currency, klines, dataframe)

            res = {
            "question_type": "binance_data",
            "data": data,
            }


            return res

        elif answer["case_number"] == "3":
                 
            params=get_news_prams(prompt)
            news = news_api.get_top_headlines(params["token_name"])

            
            res = {
            "question_type": "news",
            "data": news,
            }

            return res
           
        else:
            
            print("case_number:",answer["case_number"])
            return "Invalid case_number"  
    
    except Exception as e:

        print("answer failed with information:", str(e))

        res = """We appreciate your question! Sadly, our system isn't able to provide an answer at the moment. Please be assured, we've recorded your query and our committed team is addressing it. As we refine our system, we'll be equipped to answer such questions in the future. We truly value your patience. We'd love to invite you to join our lively community at http://chatdatainsight.com. There, you can help us identify more unanswered questions, or help answer some for the community. As a bonus, you could earn our ecological tokens! Your contribution could greatly impact our services. We'd be thrilled to see you there!"""
        return JSONResponse(status_code=200, content={"message": res})
```

