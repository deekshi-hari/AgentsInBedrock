import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from Prompts.prompts_call_llm import SYSTEM_PROMPT

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def file_open(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        return content[:900]

USER_PROMPTS = file_open("datas/sample_blood_test.txt")

def call_google_genai():
    llm = ChatGoogleGenerativeAI(
        model="gemini-flash-latest",
        temperature=0.7,
        api_key=GOOGLE_API_KEY
    )

    # print(USER_PROMPTS)

    response = llm.invoke([
        ["system", SYSTEM_PROMPT],
        ["user", USER_PROMPTS]
    ])
    print(response.text)


call_google_genai()