import os
import streamlit as st
from APIKEY import API_KEY
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

os.environ['OPENAI_API_KEY'] = API_KEY

# app-framework
st.title("My First App using LangChain")
prompt = st.text_input('Plug in your prompt here')

# Prompt constructor
title_template = PromptTemplate(
    input_variable= ['topic'],
    template="Escreva um roteiro com titulo para um video no youtube sobre {topic}"
)
# Llms
llm = OpenAI(temperature=0.8)
title_chain = LLMChain(llm=llm, prompt=title_template)

if prompt:
    response = title_chain.run(topic=prompt)
    st.write(response)