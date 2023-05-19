import os
import streamlit as st
from APIKEY import API_KEY
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory

from langchain.utilities import WikipediaAPIWrapper

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
    input_variables = ['title', 'wikipedia_research'],
    template="Write a youtube video script based om this TITLE: {title} while leveraging this wikipedia research: {wikipedia_research}"
)

# MEmory
title_memory = ConversationBufferMemory(input_key='topic', memory_key='chat_history')
script_memory = ConversationBufferMemory(input_key='title', memory_key='chat_history')


# Llms
llm = OpenAI(temperature=0.8)
title_chain = LLMChain(llm=llm, prompt=title_template, verbose=True, output_key='title', memory=title_memory)
script_chain = LLMChain(llm=llm, prompt=script_template, verbose=True, output_key='script', memory=script_memory)
#sequential_chain = SequentialChain(chains=[title_chain, script_chain], input_variables=['topic'], output_variables=['title', 'script'])

wiki = WikipediaAPIWrapper()

if prompt:
    title = title_chain(topic=prompt)
    wiki_research = wiki.run(prompt)
    script = script_chain(title=title, wikipedia_research=wiki_research)

    #response = sequential_chain({'topic': prompt})
    st.write(response['title'])
    st.write(response['script'])


    with st.expander('Title History'):
        st.info(title_memory.buffer)

    with st.expander('Script History'):
        st.info(script_memory.buffer)

    with st.expander('Wiki Research History'):
        st.info(wiki_research)