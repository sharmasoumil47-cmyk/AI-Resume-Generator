import streamlit as st
# streamlit : web based app making 
# lite python framework 

st.title("AI Resume Maker")

st.markdown("""## user can create or download 
AI created Resume based on high ATS score""")


#==============Agent Code ===========
# Step 2: Load Modules
import os
import time
import langchain
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
import pytesseract as pyt
from tavily import TavilyClient
from langchain.messages import SystemMessage, HumanMessage
import numpy as np
import streamlit as st
from langchain_community.document_loaders import PyMuPDFLoader
from PIL import image



#==============API KEY Load ==============
GOOGLE_API_KEY = st.sidebar.text_input("GOOGLE_API_KEY",type ="password")
GROQ_API_KEY = st.sidebar.text_input("GROQ_API_KEY",type ="password")
TAVILY_API_KEY = st.sidebar.text_input("TAVILY_API_KEY",type ="password")

if not(GOOGLE_API_KEY) and not (GROQ_API_KEY) and not(TAVILY_API_KEY):
    st.sidebar.warning("PASS API KEYS")
    st.stop()
else:
    st.success("API KEYS LOADED")
    
#================MODEL BUILDING ===========
model = ChatGoogleGenerativeAI(
    model = 'gemini-3.5-flash-lite',
    google_api_key = GOOGLE_API_KEY
)
def search_recent_news_jobs():
  '''this function helps you to search
  recent news or recent jobs
  related to given search query
  suppose user write Python Developer Jobs
  It should return trending news and jobs link'''
  client = TavilyClient(
      api_key = TAVILY_API_KEY
  )
  return client.search(query)


  # agent creation
from langchain.agents import create_agent
agent = create_agent(
    model = model,
    tools = [search_recent_news_jobs]
)


#==========Prompt Generator ===============
def prompt_generator(agent):
  '''this function help to give detailed prompt
  followed by chain of thoughts and persona prompting,main task is to give detailed prompt to build resume for the students
  or experienced person based on their given personal information  '''

  prompt = '''you are a senior HR resume analyer , main task is to give detailed prompt to build resume for the students
  or experienced person based on their given personal information
  system Instruction i want  model to generate resume in html format , include that in prompt'''

  response = agent.invoke(prompt)
  file_name = 'prompt.py'
  with open(file_name,'w') as f:
    f.write(response.content[-1]['text'])
  return 'prompt file generator Successfully,agent can read it '

prompt_generator(model)

# tool 2
def resume_maker_prompt():
  '''this function just gives
  updated prompt for model '''

  with open("prompt.py",'r') as f:
    prompt = f.read()
  return prompt

resume_maker_prompt()
#=============== UPLOAD IMAGE ===========
uploaded_file = st.sidebar.file_uploader(
    "Choose an image file",
    type = ['jpeg','jpeg','png''webp']
    )
    if uploaded_file is not None:
        try:
             image = Image.open(uploaded_file)

             st.sidebar.image(image,caption ="uploaded image",use_container_width=True)

             if image.mode in ("RGBA",'P')
               image = image.convert.('RGB')
            base_name = os.path.splitext(uploaded_file.name)[0]
            save_path =f"{base_name}.jpg"

            image.save(save_path,"JPEG")
            st.sidebar.success(f" iamge successfully saved as '{save-path}'!)

        except Exception as e:
        st.errror(f"Error processing image:{e}")
        









#============== Generate Resume=========
prompt = '''you are a helpful AI assistant
with job resume maker, your task is to give
html format resume , with proper designing using recent CSS and JS code, with professional design format,
user will upload data and return html format resume
ALways use different color and styling '''

final_prompt = prompt + resume_maker_prompt()
user_info = st.text_input("Enter your  information")
user_details = f"""user details : giver below:-
Resume info : {user_info}
photo : {uploaded_photo}
photo present in the current directory with name as uploaded 
default if not given generate python developer resume"""

query = final_prompt + user_details

if st.button("Generator Resume"):
  with st.spinner("Running Agent......"):
    
    response = agent.invoke({'messages': [{'role':'user','content':query}]})
    code = response['messages'][-1].content[-1]['text']

    # st.markdown(code)
st.html(code,width = "stretch", unsafe_allow_javascript = True) 


