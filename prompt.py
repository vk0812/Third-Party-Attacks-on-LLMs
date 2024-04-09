# flake8: noqa
from langchain.prompts.prompt import PromptTemplate

API_RESPONSE_PROMPT_TEMPLATE = (
""" 
Here is the response from the API:

{api_response}

Use the response to answer the user question.

Question:{question}"""
)

API_RESPONSE_PROMPT = PromptTemplate(
    input_variables=["api_response", "question"],
    template=API_RESPONSE_PROMPT_TEMPLATE,
)