import streamlit as st

from supabase import create_client, Client

from authenticate import Authenticate

from datetime import datetime

import os


#from dotenv import find_dotenv, load_dotenv
#ENV_FILE = find_dotenv()
#if ENV_FILE:
#    load_dotenv(ENV_FILE)

st.set_page_config(layout="wide")

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def siglas(x:str):
    r=""
    li=x.split(" ")
    for i in li:
        r=r+i[0]
    return r



data={'SEMILLA DE MAÍZ AMARILLO': {'cantidad': ['Cantidad de semilla entregada en kilos'],
  'observación': [{'texto': 'Cuántos kilos sembró', 'tipo': 'numeric'},
   {'texto': 'Cuántas cosechas lleva', 'tipo': 'numeric'},
   {'texto': 'Cuántos kilos ha cosechado', 'tipo': 'numeric'},
   {'texto': 'Cómo fue el desarrollo', 'tipo': 'text'}]},
 'SEMILLA DE FRÍJOL': {'cantidad': ['Cantidad de semilla entregada en kilos'],
  'observación': [{'texto': 'Cuántos kilos sembró', 'tipo': 'numeric'},
   {'texto': 'Cuántas cosechas lleva', 'tipo': 'numeric'},
   {'texto': 'Cuántos kilos ha cosechado', 'tipo': 'numeric'}]},
 'ESTACAS BANCO DE FORRAJE': {'cantidad': ['Cantidad de estacas de Botón de oro',
   'Cuántas estacas de Nacedero',
   'Cuántas estacas de Matarratón'],
  'observación': [{'texto': 'Cuántas estacas se desarrollaron',
    'tipo': 'numeric'},
   {'texto': 'Cuántas estacas se perdieron', 'tipo': 'numeric'},
   {'texto': 'Cuál es el estado actual del banco de forraje', 'tipo': 'options',
    'opciones': ['---', 'Bueno', 'Regular', 'Malo']},
   {'texto': 'Continúa su propagación',
    'tipo': 'options',
    'opciones': ['---', 'Si', 'No']}]},
 'ARBOLES FRUTALES': {'cantidad': ['Cantidad de tipo Injerto',
   'Cantidad de tipo Nativos'],
  'observación': [{'texto': 'Cuántos arboles se desarrollaron',
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
 'PASTO VETIVER': {'cantidad': ['Cantidad entregada de pasto vetiver']},
 'COMPOSTERA': {'observación':[{'texto': 'Cuántas láminas de zinc ha utilizado en la compostera', 'tipo':'numeric'},
                               {'texto': 'Cuántos bultos de cemento ha utilizado en la compostera', 'tipo':'numeric'},
                               {'texto': 'Cuánto amarre ha utilizado en la compostera', 'tipo':'numeric'}]}}

hoy=datetime.today()

clean={
  "Fecha": hoy,
  "Municipio": "",
  "Cuenca": "",
  "Vereda": "",
  "DAR": "NORTE",
  "Finca": "",
  "Beneficiario": "",
  "Vigencia-O": 2020,
  "Recibe la visita": "",
  "Propietario-O": "---",
  "SDMA-N-Cantidad de semilla entregada en kilos": None,
  "SDMA-N-Cuántos kilos sembró": None,
  "SDMA-N-Cuántas cosechas lleva": None,
  "SDMA-N-Cuántos kilos ha cosechado": None,
  "SDMA-Cómo fue el desarrollo": "",
  "SDF-N-Cantidad de semilla entregada en kilos": None,
  "SDF-N-Cuántos kilos sembró": None,
  "SDF-N-Cuántas cosechas lleva": None,
  "SDF-N-Cuántos kilos ha cosechado": None,
  "EBDF-N-Cantidad de estacas de Botón de oro": None,
  "EBDF-N-Cuántas estacas de Nacedero": None,
  "EBDF-N-Cuántas estacas de Matarratón": None,
  "EBDF-N-Cuántas estacas se desarrollaron": None,
  "EBDF-N-Cuántas estacas se perdieron": None,
  "EBDF-O-Cuál es el estado actual del banco de forraje": "---",
  "EBDF-O-Continúa su propagación": "---",
  "AF-N-Cantidad de tipo Injerto": None,
  "AF-N-Cantidad de tipo Nativos": None,
  "AF-N-Cuántos arboles se desarrollaron": None,
  "AF-O-En qué estado están": "---",
  "AF-N-Número de árboles vivos": None,
  "CDP-N-Cantidad sembrada de Plátano": None,
  "CDP-N-Cuántos racimos de plátano ha cosechado": None,
  "CDP-N-Cuántos colinos de plátano plantaron": None,
  "CDP-N-Cuántos colinos de plátano murieron": None,
  "CDB-N-Cantidad sembrada de Banano": None,
  "CDB-N-Cuántos racimos de banano ha cosechado": None,
  "CDB-N-Cuántos colinos de banano plantaron": None,
  "CDB-N-Cuántos colinos de banano murieron": None,
  "CDG-N-Cantidad sembrada de Guayabo": None,
  "CDG-N-Cuántos racimos de guayabo ha cosechado": None,
  "CDG-N-Cuántos colinos de guayabo plantaron": None,
  "CDG-N-Cuántos colinos de guayabo murieron": None,
  "SDSDH-N-Cantidad de sobres entregados": None,
  "BDG-N-Bandejas de germinación entregadas": None,
  "FM-O-Cómo ha sido el funcionamiento": "---",
  "PV-N-Cantidad entregada de pasto vetiver": None,
  "C-N-Cuántas láminas de zinc ha utilizado en la compostera": None,
  "C-N-Cuántos bultos de cemento ha utilizado en la compostera": None,
  "C-N-Cuánto amarre ha utilizado en la compostera": None,
  "Ha entregado semillas a vecino-O": "---",
  "Nombre del Vecino 1": "",
  "Nombre del Vecino 2": "",
  "Intención de articularse al Mercado Agroecológico-O": "---",
  "Compromiso frente al proceso": "",
  "Cuál semilla ha entregado a vecinos": "",
  "Finca del Vecino 1": "",
  "Finca del Vecino 2": "",
  "Intención de articularse a Proceso Educativo-O": "---",
  "Observaciones": "",
  "Fecha de Firma": hoy,
  "Nombre de quién firma": None,
  "Cédula de quién firma": None
}

sig={}

for i in data.keys():
    sig[siglas(i)]=i

def titulo(num,tit):
    st.markdown(f'<h{num} style="text-align: center;">{tit}</h{num}>',unsafe_allow_html=True)


def disable():
    st.session_state.disabled = True

def denuevo():
    st.session_state.error == False
    st.session_state.disabled = False

def nueva():
    for i in clean:
        st.session_state[i] = clean[i]
    st.session_state.disabled = False
    
    
    


# Initialize disabled for form_submit_button to False
if "disabled" not in st.session_state:
    st.session_state.disabled = False

if "error" not in st.session_state:
    st.session_state.error = False


authenticator = Authenticate("supa_auth", url, key)

authentication_status, email= authenticator.login('Bienvenido', 'main')
if authentication_status:
    cantidadP,count = supabase.table("cvc").select("encuestador").eq("encuestador",email).execute()
    cantP=len(cantidadP[1])
    resul={"encuestador":email}

    c1, c2, c3 = st.columns([6,1.6,0.6])
    with c2:
        st.markdown(f"""{email.split("@")[0]}: **{cantP} encuestas**""")
    with c3:
        authenticator.logout('Salir', 'main')

    titulo(1,"Segimiento Seguridad Alimentaria")

    titulo(2,"Información General")
    infoA=st.columns(3)
    with infoA[0]:
        resul["Fecha"]=st.date_input("Fecha de Visita", value="today", format="DD-MM-YYYY", key="Fecha").strftime('%Y-%m-%d %H:%M:%S')
        resul["Municipio"]=st.text_input("Municipio:", key="Municipio")

    with infoA[1]:
        resul["Cuenca"]=st.text_input("Cuenca:", key="Cuenca")
        resul["Vereda"]=st.text_input("Vereda:", key="Vereda")
            

    with infoA[2]:
        resul["DAR"]=st.text_input("DAR:", value="NORTE", key="DAR")
        resul["Finca"]=st.text_input("Finca:", key="Finca")


    infoB=st.columns(2)
    with infoB[0]:
        resul["Beneficiario"]=st.text_input("Beneficiario(a):", key="Beneficiario")
        resul["Vigencia-O"]=st.selectbox("Vigencia", [2020, 2021, 2022], key="Vigencia-O")
    with infoB[1]:
        resul["Recibe la visita"]=st.text_input("Quien recibe la visita:", key="Recibe la visita")
        resul["Propietario-O"]=st.selectbox("Estado de la propiedad", ["---","El mismo dueño", "Cambio de propietario"], key="Propietario-O")
    
    
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
                    resul[(siglas(insu)+"-N-"+can).strip()]=st.number_input(can,value=None, key=siglas(insu)+"-N-"+can)
        if "observación" in data[insu]:
            observaciones=data[insu]["observación"]
            with cols[2]:
                for obs in observaciones:
                    if obs["tipo"] == "options":
                        resul[(siglas(insu)+"-O-"+obs["texto"]).strip()]=st.selectbox(obs["texto"],options=obs["opciones"], key=siglas(insu)+"-O-"+obs["texto"])
                    if obs["tipo"] == "text":
                        resul[(siglas(insu)+"-"+obs["texto"]).strip()]=st.text_input(obs["texto"], key=siglas(insu)+"-"+obs["texto"])
                    if obs["tipo"] == "numeric":
                        resul[(siglas(insu)+"-N-"+obs["texto"]).strip()]=st.number_input(obs["texto"], value=None, key=siglas(insu)+"-N-"+obs["texto"])
        st.markdown("---")


    titulo(2,"Sobre el Beneficiario")
    benefA=st.columns(2)
    with benefA[0]:
        resul["Ha entregado semillas a vecino-O"]=st.selectbox("El beneficiario manifiesta haber entregado semillas a un vecino de su vereda", ["---","Si","No"], key="Ha entregado semillas a vecino-O")
        resul["Nombre del Vecino 1"]=st.text_input("Nombre del Vecino 1", key="Nombre del Vecino 1")
        resul["Nombre del Vecino 2"]=st.text_input("Nombre del Vecino 2", key="Nombre del Vecino 2")
        resul["Intención de articularse al Mercado Agroecológico-O"]=st.selectbox("El beneficiario manifiesta la intención de articularse al proceso de Mercado Agroecológico", ["---","Si","No"], key="Intención de articularse al Mercado Agroecológico-O")
        resul["Compromiso frente al proceso"]=st.text_input("Compromiso frente al proceso", key="Compromiso frente al proceso")
    with benefA[1]:
        resul["Cuál semilla ha entregado a vecinos"]=st.text_input("Cuál semilla ha entregado a vecinos", key="Cuál semilla ha entregado a vecinos")
        resul["Finca del Vecino 1"]=st.text_input("Finca del Vecino 1", key="Finca del Vecino 1")
        resul["Finca del Vecino 2"]=st.text_input("Finca del Vecino 2", key="Finca del Vecino 2")
        resul["Intención de articularse a Proceso Educativo-O"]=st.selectbox("El beneficiario manifiesta la intención de articularse al proceso en la Institución educativa", ["---","Si","No"], key="Intención de articularse a Proceso Educativo-O")
        resul["Observaciones"]=st.text_input("Observaciones", key="Observaciones")

    st.markdown("---")

    firma=st.columns(3)
    with firma[0]:
        resul["Fecha de Firma"]=st.date_input("Fecha de Firma", value="today", format="DD-MM-YYYY", key="Fecha de Firma").strftime('%Y-%m-%d %H:%M:%S')
    with firma[1]:    
        resul["Nombre de quién firma"]=st.text_input("Nombre de quién firma", key="Nombre de quién firma")
    with firma[2]:    
        resul["Cédula de quién firma"]=st.number_input("Cédula de quién firma", value=None, step=1, key="Cédula de quién firma")



    #submitted = st.form_submit_button("ENVIAR",type='primary',use_container_width=True, on_click=disable, disabled=st.session_state.disabled)
    submitted = st.button("ENVIAR",type='primary',use_container_width=True, on_click=disable ,disabled=st.session_state.disabled)

    if submitted:
        if resul["Nombre de quién firma"] == None:
            st.session_state.error = True
            titulo(6, "⚠️ ¡Cuidado! ⚠️")
            st.warning("⚠️ Faltó el nombre de quién firma. Intente de nuevo ⚠️")
        
        if resul["Cédula de quién firma"] == None:
            st.session_state.error = True
            titulo(6, "⚠️ ¡Cuidado! ⚠️")
            st.warning("⚠️ Faltó el número de cédula de quién firma. Intente de nuevo ⚠️")

        else:
            #data,count=resul,1
            #if len(data.keys())>1:
            ## ENVIAR A SUPABASE
                #st.write(resul)
            data,count = supabase.table("cvc").insert(resul).execute()
            if data[1][0]:
                d=data[1][0]
                titulo(4,"Enviado")
                st.success("Enviado satisfactoriamente")
                st.session_state.error = False
            #    st.write(d)
                #dP,count = supabase.table("cantidad").insert({"perfil":email, "cant":cantP+1}).execute()

            else:
                st.session_state.error = True
                titulo(4,"❌ Error ❌")
                st.error("❌ Ocurrió un error inesperado. Intente de nuevo, no se han enviado los datos del encuestado ❌")

if st.session_state.disabled == True:
    if st.session_state.error == True:
        st.button("INTENAR DE NUEVO", type='primary', on_click=denuevo ,use_container_width=True)
    else:
        st.button("LLENAR NUEVA ENCUESTA", type='primary', on_click=nueva ,use_container_width=True)

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





