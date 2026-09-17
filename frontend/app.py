import streamlit as st
from uuid import uuid4
import requests
import os
import time
from dotenv import load_dotenv
load_dotenv()
BASE_URL=os.getenv('BASE_URL',"http://127.0.0.1:8000")
def generator(content):
    for i in content.split():
        yield i+' '
        time.sleep(0.04)
if 'id' not in st.session_state:
    st.session_state.id=str(uuid4())

st.title('LINKDIN TECHNICAL POST WRITER')
st.write("CAN ONLY READ .py, .js, .md, .txt, .ipynb FILES")
link=st.text_input('enter public github link')
goal=st.text_input('explain what the project does')

if st.button('send') and link and goal:
    payload={'github_repo':link,'id':st.session_state.id,'goal':goal}
    with st.spinner('running'):
        result=requests.post(json=payload,url=f'{BASE_URL}/agent')
        time.sleep(4)
    
    


    if result.ok:
        st.write_stream(generator(result.json()))
    else:
        st.error('something went wrong')

