import streamlit as st
from st_pages import hide_pages
from time import sleep
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages
import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.getenv("APP_NAME")
PROJECT_VERSION = os.getenv("PROJECT_VERSION")

#page config
#config
def set_page_config(auth_status):
    if auth_status:
        st.set_page_config(
            page_title=APP_NAME,
            page_icon="📊",
            #layout="centered",
            initial_sidebar_state="auto",
            #menu_items={
            #    'Get Help': 'https://www.extremelycoolapp.com/help',
            #    'Report a bug': "https://www.extremelycoolapp.com/bug",
            #    'About': "# This is a header. This is an *extremely* cool app!"
            #}
        )
    else:
        st.set_page_config(
            page_title=APP_NAME,
            page_icon="📊",
            initial_sidebar_state="collapsed",
        )        


def get_current_page_name():
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("Couldn't get script context")

    pages = get_pages("")

    return pages[ctx.page_script_hash]["page_name"]


def make_sidebar(auth_status, user_info):
    with st.sidebar:
        #st.markdown("<div style='text-align: center;'> 회사 로고 </div>", unsafe_allow_html=True)
        st.logo("/app/src/images/logo_wesleyquest.png", link="http://wesleyquest.com")
        st.markdown(f"<div style='text-align:center;font-size:20px;'><b>📊 {APP_NAME}</b></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align:center;font-size:16px;color:grey;'>{PROJECT_VERSION}</div>", unsafe_allow_html=True)
        st.markdown("")
        st.markdown("""<div style="height:0.5px;border:none;color:#D3D3D3;background-color:#D3D3D3;" /> """, unsafe_allow_html=True)
        #st.markdown("")
        if auth_status == True:
            #st.markdown("<div style='text-align: center;'> 🐱 </div>", unsafe_allow_html=True)
            st.markdown(f"""<div style='text-align: center;'> 🐱 {user_info["username"]} </div>""", unsafe_allow_html=True)
            st.markdown(f"""<div style='text-align: center; color: grey;'> {user_info["email"]} </div>""", unsafe_allow_html=True)
            
            st.markdown("")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("나의정보", use_container_width=True):
                    st.switch_page("pages/my_profile.py")
            with col2:
                if st.button("로그아웃", use_container_width=True):
                    logout()

            #st.markdown("")
            st.markdown("""<div style="height:0.5px;border:none;color:#D3D3D3;background-color:#D3D3D3;" /> """, unsafe_allow_html=True)
            with st.expander("🏠&nbsp; HOME", expanded=True):
                st.page_link("pages/hello.py", label="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 개요")
            with st.expander("🚀&nbsp; APP", expanded=True):
                st.page_link("pages/quiz_generator.py", label="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 한국어 퀴즈 생성")
            with st.expander("📑&nbsp; API Docs", expanded=True):
                st.page_link("pages/api_docs_auth.py", label="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 로그인 API")
                st.page_link("pages/api_docs_quiz.py", label="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 한국어 퀴즈 생성 API")
                st.page_link("pages/api_docs_user.py", label="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 사용자 관리 API (관리자용)")
        elif not auth_status == True:
            st.page_link("main.py", label="로그인")
            st.page_link("pages/signup.py", label="회원가입")

        elif get_current_page_name() != "main":
            # If anyone tries to access a secret page without being logged in,
            # redirect them to the login page
            st.switch_page("main.py")

def logout():
    st.session_state = {}
    st.switch_page("main.py")

