# ragsql
Retrieval Augmented Generation (RAG) is for me one of the most useful features of Large Language Models (LLMs) (This is my personal opinion). It allows you to ask a LLM questions about your own data.
If you have information in PDFs, Office formats, etc. format I recommend you to try this [repository](https://github.com/Azure-Samples/azure-search-openai-demo)
That example, at this point does not support reading from a SQL database tough, that is why I have started this repository.

## What does it do?
I used the customer,orders,lineitem tables from [TPCH_SF1](https://docs.snowflake.com/en/user-guide/sample-data-tpch)
Then I asked: "How many orders ocurred in december 1997?" , the model (Agent Executor chain) created a sql
```SELECT COUNT(*) FROM orders WHERE o_orderdate >= '1997-12-01' AND o_orderdate < '1998-01-01';```
And returned the count. Very nice, isn't it?

## What do you need

1. A snowflake account (You can get a free trial for 30 days)
2. An Azure OpenAI resource and model deployed 

## How to run it

1. Clone the report to your PC or use CodeSpaces
2. Install the libraries from requirements.txt ```pip install -r requirements.txt```
3. Create a file called .env with the following 
    ```
    SNOWFLAKE_URL = xxxxxx.west-europe.azure
    SNOWFLAKE_USERNAME =  xxxxxx
    SNOWFLAKE_PASSWORD = xxxxxxx
    SNOWFLAKE_ACCOUNT = xxxx.yyyy
    OPENAI_API_TYPE = azure
    OPENAI_API_VERSION = 2023-07-01-preview
    OPENAI_API_KEY = xxxxxxxxxxx
    OPENAI_CHAT_MODEL = gpt4pre
    AZURE_ENDPOINT = https://xxxxx.openai.azure.com/
    OPENAI_API_BASE= https://xxxxx.openai.azure.com/
    ```

    Note: that AZURE_ENDPOINT and OPENAI_API_BASE are identical , will figure out later which one to use.
4. run ```python query.py```

## Change the question
In line 79, you can change the question, soon this will be a parameter.
```question="How many orders ocurred in december 1997?"```

## How does the output look like when you run it:

``` > Entering new AgentExecutor chain...
Action: sql_db_list_tables
Action Input: 
Observation: customer, lineitem, orders
Thought:Now that I know the available tables, I should check the schema of the orders table to verify the names of the columns and to ensure I understand the data types for the O_ORDERDATE column.
Action: sql_db_schema
Action Input: orders
Observation: 
CREATE TABLE orders (
        o_orderkey DECIMAL(38, 0) NOT NULL, 
        o_custkey DECIMAL(38, 0) NOT NULL, 
        o_orderstatus VARCHAR(1) NOT NULL, 
        o_totalprice DECIMAL(12, 2) NOT NULL, 
        o_orderdate DATE NOT NULL, 
        o_orderpriority VARCHAR(15) NOT NULL, 
        o_clerk VARCHAR(15) NOT NULL, 
        o_shippriority DECIMAL(38, 0) NOT NULL, 
        o_comment VARCHAR(79) NOT NULL
)

/*
3 rows from orders table:
o_orderkey      o_custkey       o_orderstatus   o_totalprice    o_orderdate     o_orderpriority o_clerk o_shippriority  o_comment
1       36901   O       173665.47       1996-01-02      5-LOW   Clerk#000000951 0       nstructions sleep furiously among 
2       78002   O       46929.18        1996-12-01      1-URGENT        Clerk#000000880 0        foxes. pending accounts at the pending, silent asymptot
3       123314  F       193846.25       1993-10-14      5-LOW   Clerk#000000955 0       sly final accounts boost. carefully regular ideas cajole carefully. depos
*/
Thought:Now I have confirmed the structure of the orders table and the relevant column names. I can now proceed to construct a query to count the number of orders in December 1997. To do this, I'll need to filter the orders by the O_ORDERDATE column to only include dates within December 1997 and then count the number of rows that match this criterion.

Action: sql_db_query_checker
Action Input: SELECT COUNT(*) FROM orders WHERE o_orderdate >= '1997-12-01' AND o_orderdate < '1998-01-01';
Observation: SQL Query:

Thought:The query has been validated and is correct. I can now execute it to get the number of orders that occurred in December 1997.

Action: sql_db_query
Action Input: SELECT COUNT(*) FROM orders WHERE o_orderdate >= '1997-12-01' AND o_orderdate < '1998-01-01';
Observation: [(19450,)]
Thought:I now know the final answer
Final Answer: There were 19,450 orders that occurred in December 1997.
```

