from langchain.utilities import SQLDatabase
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage
from langchain.agents.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.agents import AgentType, create_sql_agent
from dotenv import load_dotenv
from langchain.prompts.chat import ChatPromptTemplate
import os
import openai


def main():
    # Prompt
    final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", 
         """
         You are a helpful AI assistant expert in identifying the relevant topic from user's question about Customers, Orders and Line Items and then querying SQL Database to find answer.
         Use following context to create the SQL query. Context:
         Orders table contains information about sales orders placed by customers. O_ORDERDATE columns tells the date when the order was placed. O_CUSTKEY is a foreing key to table CUSTOMER column C_CUSTKEY. 
         O_TOTALPRICE is total amount of the order.
         Lineitem table contains information about products in an order. L_ORDERKEY is a foreing key to table ORDERS column O_ORDERKEY. L_QUANTITY is the number of products in an order.
         Customer table contains information about customers. C_CUSTKEY is a primary key. C_NAME is the name of the customer. C_ADDRESS is the address of the customer.
        """
         ),
        ("user", "{question}\n ai: "),
    ]
)

    load_dotenv()

    # Snmowflake parameters
    snowflake_url = os.getenv("SNOWFLAKE_URL")
    username = os.getenv("SNOWFLAKE_USERNAME")
    password = os.getenv("SNOWFLAKE_PASSWORD")
 
    # OpenAI parameters
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.azure_endpoint = os.getenv("AZURE_ENDPOINT")
    openai.api_key = os.getenv("OPENAI_API_KEY")


    # Connect to snowflake, and pass tables that we want to sample / query 
    snowflake_url = 'snowflake://{user}:{password}@{account_identifier}/SNOWFLAKE_SAMPLE_DATA/TPCH_SF1'.format(
        user=username,
        password=password,
        account_identifier=snowflake_url,
    )
    print(snowflake_url)
    try:
        db = SQLDatabase.from_uri(snowflake_url,sample_rows_in_table_info=3, include_tables=["customer","orders","lineitem"])
    except Exception as e:
        print(e)
        exit(1)

    # Azure OpenAI model
    model = AzureChatOpenAI(
        openai_api_version="2023-07-01-preview",
        azure_deployment="gpt4pre",
        )

    # Make sure model works
    message = HumanMessage(content="Translate this sentence from English to Spanish. I love programming.")
    reply = model([message])
    print(reply)

    # Create toolkit
    sql_toolkit = SQLDatabaseToolkit(db=db, llm=model)
    sql_toolkit.get_tools()

    sqldb_agent = create_sql_agent(
    llm=model,
    toolkit=sql_toolkit,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
    )   

    sqldb_agent.run(final_prompt.format(
        question="How many orders ocurred in december 1997?"
  ))


if __name__ == "__main__":
    main()
