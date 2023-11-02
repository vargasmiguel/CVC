import streamlit as st

from supabase import create_client, Client

from authenticate import Authenticate

import os


from dotenv import find_dotenv, load_dotenv
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

logo="logo-cvc.png"

st.set_page_config(layout="wide")

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

data={'SEMILLA DE MAÍZ AMARILLO': {'cantidad': ['Cantidad de semilla entregada en kilos'],
  'observación': [{'texto': 'Cuántos kilos sembró', 'tipo': 'numeric'},
   {'texto': 'Cuántas cosechas lleva', 'tipo': 'numeric'},
   {'texto': 'Cuántos kilos ha cosechado', 'tipo': 'numeric'},
   {'texto': 'Cómo fue el desarrollo', 'tipo': 'text'}]},
 'SEMILLA DE FRÍJOL': {'cantidad': ['Cantidad de semilla entregada en kilos'],
  'observación': [{'texto': 'Cuántos kilos sembró', 'tipo': 'numeric'},
   {'texto': 'Cuántas cosechas lleva', 'tipo': 'numeric'},
   {'texto': 'Cuántos kilos ha cosechado', 'tipo': 'numeric'}]},
 'ESTACAS PARA BANCO DE FORRAJE': {'cantidad': ['Cantidad de estacas de Botón de oro',
   'Cuántas estacas de Nacedero',
   'Cuántas estacas de Matarratón'],
  'observación': [{'texto': 'Cuántas estacas sembradas se desarrollo',
    'tipo': 'numeric'},
   {'texto': 'Cuántas estacas se prendieron', 'tipo': 'numeric'},
   {'texto': 'Cuál es el estado actual del banco de forraje', 'tipo': 'text'},
   {'texto': 'Continúa su propagación',
    'tipo': 'options',
    'opciones': ['---', 'Si', 'No']}]},
 'ARBOLES FRUTALES': {'cantidad': ['Cantidad de tipo Injerto',
   'Cantidad de tipo Nativos'],
  'observación': [{'texto': 'Cuántos arboles sembrado se desarrollaron',
    'tipo': 'numeric'},
   {'texto': 'En qué estado están',
    'tipo': 'options',
    'opciones': ['---', 'Bueno', 'Regular', 'Malo']},
   {'texto': 'Número de árboles vivos', 'tipo': 'numeric'}]},
 'COLINO DE PLÁTANO': {'cantidad': ['Cantidad sembrada de Plátano'],
  'observación': [{'texto': 'Cuántos racimos de plátano ha cosechado',
    'tipo': 'numeric'},
   {'texto': 'Cuántos colinos de plátano plantaron', 'tipo': 'numeric'},
   {'texto': 'Cuántos colinos de plátano murieron', 'tipo': 'numeric'}]},
 'COLINO DE BANANO': {'cantidad': ['Cantidad sembrada de Banano'],
  'observación': [{'texto': 'Cuántos racimos de banano ha cosechado',
    'tipo': 'numeric'},
   {'texto': 'Cuántos colinos de banano plantaron', 'tipo': 'numeric'},
   {'texto': 'Cuántos colinos de banano murieron', 'tipo': 'numeric'}]},
 'COLINO DE GUAYABO': {'cantidad': ['Cantidad sembrada de Guayabo'],
  'observación': [{'texto': 'Cuántos racimos de guayabo ha cosechado',
    'tipo': 'numeric'},
   {'texto': 'Cuántos colinos de guayabo plantaron', 'tipo': 'numeric'},
   {'texto': 'Cuántos colinos de guayabo murieron', 'tipo': 'numeric'}]},
 'SOBRE DE SEMILLAS DE HORTALIZAS': {'observación': [{'texto': 'Cantidad de sobres entregados',
    'tipo': 'numeric'}]},
 'BANDEJA DE GERMINACIÓN': {'cantidad': ['Bandejas de germinación entregadas']},
 'FUMIGADORA MANUAL': {'observación': [{'texto': 'Cómo ha sido el funcionamiento',
    'tipo': 'options',
    'opciones': ['---', 'Bueno', 'Regular', 'Malo']}]},
 'PASTO VETIVER': {'cantidad': ['Cantidad entregada de pasto vetiver']}}

def titulo(num,tit):
    st.markdown(f'<h{num} style="text-align: center;">{tit}</h{num}>',unsafe_allow_html=True)


def disable():
    st.session_state.disabled = True

# Initialize disabled for form_submit_button to False
if "disabled" not in st.session_state:
    st.session_state.disabled = False


authenticator = Authenticate("supa_auth", url, key)

authentication_status, email= authenticator.login('Bienvenido', 'main')
if authentication_status:
    cantidadP,count = supabase.table("encuesta").select("email").eq("email",email).execute()
    cantP=len(cantidadP[1])
    resul={"encuestador":email}

    col1, col2, col3 = st.columns([3,1,3])
    with col2:
        st.image("logo-cvc.png",width=200)

    c1, c2, c3 = st.columns([8,1.6,0.6])
    with c2:
        st.markdown(f"""{email.split("@")[0]}: **{cantP} encuestas**""")
    with c3:
        authenticator.logout('Salir', 'main')

    titulo(1,"Segimiento Seguridad Alimentaria - CVC")


    with st.form("encuesta", clear_on_submit=True):

        titulo(2,"Información General")
        infoA=st.columns(3)
        with infoA[0]:
            resul["Fecha"]=st.date_input("Fecha de Visita", value="today", format="DD-MM-YYYY").strftime('%Y-%m-%d %H:%M:%S')
            resul["Municipio"]=st.text_input("Municipio:")

        with infoA[1]:
            resul["Cuenca"]=st.text_input("Cuenca:")
            resul["Vereda"]=st.text_input("Vereda:")
             

        with infoA[2]:
            resul["DAR"]=st.text_input("DAR:")
            resul["Finca"]=st.text_input("Finca:")


        infoB=st.columns(2)
        with infoB[0]:
            resul["Beneficiario"]=st.text_input("Beneficiario(a):")
            resul["Vigencia"]=st.selectbox("Vigencia", [2020, 2021, 2022])
        with infoB[1]:
            resul["Recibe la visita"]=st.text_input("Quien recibe la visita:")
            resul["Propietario"]=st.selectbox("Estado de la propiedad", ["---","El mismo dueño", "Cambio de propietario"])
        
        
        st.markdown("---")
        st.markdown(" ")

        titulo(2,"Insumos o Materiales")

        st.markdown(" ")

        head=st.columns(3)
        with head[0]:
            st.markdown("**Descripción**")
        with head[1]:
            st.markdown("**Cantidad**")
        with head[2]:
            st.markdown("**Observaciones**") 
        st.markdown("---")

        for insu in data.keys():
            cols=st.columns(3)
            cols[0].write(insu)
            if "cantidad" in data[insu]:
                cantidades=data[insu]["cantidad"]
                with cols[1]:
                    for can in cantidades:
                        resul[((insu+"-C-"+can)[:62]).strip()]=st.number_input(can,value=1.1, key=insu+"-C-"+can)
            if "observación" in data[insu]:
                observaciones=data[insu]["observación"]
                with cols[2]:
                    for obs in observaciones:
                        if obs["tipo"] == "options":
                            resul[((insu+"-O-"+obs["texto"])[:62]).strip()]=st.selectbox(obs["texto"],options=obs["opciones"], key=insu+"-O-"+obs["texto"])
                        if obs["tipo"] == "text":
                            resul[((insu+"-O-"+obs["texto"])[:62]).strip()]=st.text_input(obs["texto"], key=insu+"-O-"+obs["texto"])
                        if obs["tipo"] == "numeric":
                            resul[((insu+"-O-"+obs["texto"])[:62]).strip()]=st.number_input(obs["texto"], value=1.1, key=insu+"-O-"+obs["texto"])
            st.markdown("---")

        submitted = st.form_submit_button("ENVIAR",type='primary',use_container_width=True, on_click=disable, disabled=st.session_state.disabled)

        if submitted:
            if resul["Beneficiario"] == None:
                titulo(6, "⚠️ ¡Cuidado! ⚠️")
                st.warning("⚠️ Faltó el beneficiario. Intente de nuevo ⚠️")
            
            elif resul["Finca"] == None:
                titulo(6, "⚠️ ¡Cuidado! ⚠️")
                st.warning("⚠️ Faltó ingresar la finca. Intente de nuevo ⚠️")

            else:
                #data,count=resul,1
                #if len(data.keys())>1:
                ## ENVIAR A SUPABASE
                st.write(resul)
                data,count = supabase.table("cvc").insert(resul).execute()
                if data[1][0]:
                    d=data[1][0]
                    titulo(4,"Enviado")
                    st.success("Enviado satisfactoriamente")
                    st.write(d)
                    #dP,count = supabase.table("cantidad").insert({"perfil":email, "cant":cantP+1}).execute()

                else:
                    titulo(4,"❌ Error ❌")
                    st.error("❌ Ocurrió un error inesperado. Intente de nuevo, no se han enviado los datos del encuestado ❌")

    if st.session_state.disabled == True:
        if st.button("DE NUEVO", type='primary' ,use_container_width=True):
            st.session_state.disabled = False
            st.experimental_rerun()

elif authentication_status is False:
    st.error("Error, usuario y/o contraseña invalidos")





