import streamlit as st

from pygwalker.api.streamlit import StreamlitRenderer, init_streamlit_comm


from supabase import create_client, Client

from authenticate import Authenticate

from datetime import datetime

import os

import pandas as pd

import plotly.express as px

st.set_page_config(layout="wide", page_title="📊_Explorador")

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def titulo(num,tit):
    st.markdown(f'<h{num} style="text-align: center;">{tit}</h{num}>',unsafe_allow_html=True)

def encab(tit):
    st.markdown(f'<p style="text-align: center;"><strong>{tit}</strong></p>',unsafe_allow_html=True)

d1,d2=supabase.table("cvc").select("*").execute()
df=pd.DataFrame.from_dict(d1[1],orient='columns')
df.drop_duplicates(subset="GEN-Beneficiario", keep='last', inplace=True, ignore_index=False)

authenticator = Authenticate("supa_auth", url, key)

authentication_status, email= authenticator.login('Bienvenido', 'main')
if authentication_status:

    c1, c2, c3 =  st.columns([4.5,1.8,1])
    with c3:
        authenticator.logout('Salir', 'main')

    pregx=None
    pregy=None
    pregc=None
    pregs=None

    titulo(1,"Explorador de Datos")

    st.write(f"Hay un total de **{len(df)} encuestas**")

    st.divider()

    init_streamlit_comm()

    @st.cache_resource
    def get_pyg_renderer() -> "StreamlitRenderer":
        # When you need to publish your app to the public, you should set the debug parameter to False to prevent other users from writing to your chart configuration file.
        return StreamlitRenderer(df, spec="./gw_config.json", debug=False)
    
    renderer = get_pyg_renderer()

    renderer.render_explore()


elif authentication_status is False:
    st.error("Error, usuario y/o contraseña invalidos")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)





