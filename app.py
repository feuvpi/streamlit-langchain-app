import os
import streamlit as st
from APIKEY import API_KEY
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain

os.environ['OPENAI_API_KEY'] = API_KEY

# app-framework
st.title("My First App using LangChain")
prompt = st.text_input('Plug in your prompt here')

# Prompt constructor
title_template = PromptTemplate(
    input_variables = ['topic'],
    template="Escreva um roteiro com titulo para um video no youtube sobre {topic}"
)

script_template = PromptTemplate(
    input_variables = ['title'],
    template="Write a youtube video script based om this TITLE: {title}"
)


# Llms
llm = OpenAI(temperature=0.8)
title_chain = LLMChain(llm=llm, prompt=title_template, verbose=True, output_key='title')
script_chain = LLMChain(llm=llm, prompt=script_template, verbose=True, output_key='script')
sequential_chain = SequentialChain(chains=[title_chain, script_chain], input_variables=['topic'], output_variables=['title', 'script'])

if prompt:
    response = sequential_chain({'topic': prompt})
    st.write(response['title'])
    st.write(response['script'])