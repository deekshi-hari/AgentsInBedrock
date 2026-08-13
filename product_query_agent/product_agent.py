import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.tools import tool
from langchain.agents import create_agent
from datas.products import PRODUCTS
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
        model="gemini-flash-latest",
        temperature=0.7,
        api_key=GOOGLE_API_KEY,
    )


@tool
def get_product_info(name: str) -> str:
    """Look up product information by name and return a formatted string with the product's price and description."""
    product_info = PRODUCTS.get(name.lower())
    if product_info:
        return str(product_info)
    return f"Sorry, we don't have information about '{name}'."

@tool
def get_product_rating(name: str) -> str:
    """Look up product rating by name and return a formatted string with the product's rating."""
    product_info = PRODUCTS.get(name.lower())
    if product_info:
        return f"The rating for '{name}' is {product_info['rating']}."
    return f"Sorry, we don't have information about '{name}'."

agent = create_agent(
    model=llm,
    tools=[get_product_info],
    system_prompt="You are a helpful assistant that provides product information about a tech store."
)

agent2 = create_agent(
    model=llm,
    tools=[get_product_info, get_product_rating],
    system_prompt="You are a helpful assistant that provides product information about a tech store."
)

def ask(question: str) -> str:
    """Ask the agent a question and return the response."""
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})
    print(result["messages"][-1].text)

def ask_proc_details(question: str) -> str:
    """Ask the agent with product rating tool a question and return the response."""
    result = agent2.invoke({"messages": [{"role": "user", "content": question}]})
    print(result["messages"][-1].text)

# ask("What is the price and description of the wireless headphones?")

ask_proc_details("how do people like smart watch?")