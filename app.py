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

data_ind={'CONSERVACIÓN DE SUELOS': {'descripción': ['Al menos 3 prácticas de conservación'],
  'observación': [{'texto': 'Uso de materia orgánica',
    'tipo': 'options',
    'opciones': ['Si', 'No']},
   {'texto': 'Trinchos; barreras; para evitar la pérdida de suelo',
    'tipo': 'options',
    'opciones': ['Si', 'No']},
   {'texto': 'Suelo cubierto durante al menos 10 meses del año',
    'tipo': 'options',
    'opciones': ['Si', 'No']},
   {'texto': 'Trazado con curvas a nivel',
    'tipo': 'options',
    'opciones': ['Si', 'No']}]},
 'CONSERVACIÓN Y PROTECCIÓN DE LA BIODIVERSIDAD': {'descripción': ['Al menos 3 prácticas de conservación.'],
  'observación': [{'texto': 'Practica la caza',
    'tipo': 'options',
    'opciones': ['Si', 'No']},
   {'texto': 'Se tienen barreras vivas alrededor de la finca',
    'tipo': 'options',
    'opciones': ['Si', 'No']},
   {'texto': 'Siembra árboles como hábitat para las aves',
    'tipo': 'options',
    'opciones': ['Si', 'No']},
   {'texto': 'Tienen corredores biológicos en la finca',
    'tipo': 'options',
    'opciones': ['Si', 'No']}]},
 'SEGURIDAD ALIMENTARIA': {'descripción': ['Productos agropecuarios generado para el autoconsumo.'],
  'observación': [{'texto': 'Productos',
    'tipo': 'multi',
    'opciones': ['Ninguno', 'Frutas', 'Verduras', 'Hortalizas', 'Legumbres', 'Maíz', 'Ganado vacuno', 'Ganado porcino', 'Apicultura', 'Avicola']}]},
 'USO DE BIOINSUMOS': {'descripción': ['Prepara al menos 3 bioinsumos para uso en la finca.'],
  'observación': [{'texto': 'Biofertilizantes',
    'tipo': 'options',
    'opciones': ['Si', 'No']},
   {'texto': 'Abonos orgánicos', 'tipo': 'options', 'opciones': ['Si', 'No']},
   {'texto': 'Uso de microorganismos de montaña',
    'tipo': 'options',
    'opciones': ['Si', 'No']},
   {'texto': 'Biocontroladores',
    'tipo': 'options',
    'opciones': ['Si', 'No']}]},
 'AGUA': {'descripción': ['Al menos 3 prácticas de conservación'],
  'observación': [{'texto': 'Las fuentes de agua se encuentran protegidas',
    'tipo': 'options',
    'opciones': ['Si', 'No']},
   {'texto': 'Se genera vertimientos propios en la finca',
    'tipo': 'options',
    'opciones': ['Si', 'No']},
   {'texto': 'Tiene tratamiento de aguas residuales en la finca',
    'tipo': 'options',
    'opciones': ['Si', 'No']},
   {'texto': 'Cosecha de agua en la finca.',
    'tipo': 'options',
    'opciones': ['Si', 'No']}]},
 'USO DE AGROQUÍMICOS': {'descripción': ['Cultivos que dependen de agroquímicos'],
  'observación': [{'texto': 'Usa agroquímicos',
    'tipo': 'options',
    'opciones': ['Si', 'No']},
   {'texto': 'De manera permanente',
    'tipo': 'options',
    'opciones': ['Si', 'No']},
   {'texto': 'De manera esporádica y como último recurso',
    'tipo': 'options',
    'opciones': ['Si', 'No']}]},
 'PARTICIPACIÓN FAMILIAR': {'descripción': ['Participación de los integrantes de la familia en las labores de la finca y capacitaciones'],
  'observación': [{'texto': 'Participa solo la propietaria (o)',
    'tipo': 'options',
    'opciones': ['Si', 'No']},
   {'texto': 'Participa más de un integrante de la familia',
    'tipo': 'options',
    'opciones': ['Si', 'No']},
   {'texto': 'Participa toda la familia',
    'tipo': 'options',
    'opciones': ['Si', 'No']}]}}

data={'SEMILLA DE MAÍZ AMARILLO': {'cantidad': ['Cantidad de semilla entregada en kilos'],
  'observación': [{'texto': 'Cuántos kilos sembró', 'tipo': 'numeric'},
   {'texto': 'Cuántas cosechas lleva', 'tipo': 'numeric'},
   {'texto': 'Cuántos kilos ha cosechado', 'tipo': 'numeric'},
   {'texto': 'Cómo fue el desarrollo', 'tipo': 'options',
    'opciones': ['Bueno', 'Regular', 'Malo']},
   {'texto': 'Qué otra variedad de maíz tiene', 'tipo': 'multi',
    'opciones': ['Ninguno', 'Blanco', 'Otro']}]},
 'SEMILLA DE FRÍJOL': {'cantidad': ['Cantidad de semilla entregada en kilos'],
  'observación': [{'texto': 'Cuántos kilos sembró', 'tipo': 'numeric'},
   {'texto': 'Cuántas cosechas lleva', 'tipo': 'numeric'},
   {'texto': 'Cuántos kilos ha cosechado', 'tipo': 'numeric'},
   {'texto': 'Cómo fue el desarrollo', 'tipo': 'options',
    'opciones': ['Bueno', 'Regular', 'Malo']},
   {'texto': 'Qué otra variedad de fríjol tiene', 'tipo': 'multi',
    'opciones': ['Ninguno', 'Caupi', 'Bolones', 'Cargamanto', 'Otro']}]},
 'ESTACAS BANCO DE FORRAJE': {'cantidad': ['Cantidad de estacas de Botón de oro',
   'Cuántas estacas de Nacedero',
   'Cuántas estacas de Matarratón'],
  'observación': [
   {'texto': 'Cuántas estacas sembradas prendieron', 'tipo': 'numeric'},
   {'texto': 'Cuál es el estado actual del banco de forraje', 'tipo': 'options',
    'opciones': ['Bueno', 'Regular', 'Malo']},
   {'texto': 'Continúa su propagación',
    'tipo': 'options',
    'opciones': ['Si', 'No']}]},
 'ARBOLES FRUTALES': {'cantidad': ['Cantidad de tipo Injerto',
   'Cantidad de tipo Nativos'],
  'observación': [{'texto': 'Cuántos arboles se desarrollaron',
    'tipo': 'numeric'},
   {'texto': 'En qué estado están',
    'tipo': 'options',
    'opciones': [ 'Bueno', 'Regular', 'Malo']},
   {'texto': 'Número de árboles vivos', 'tipo': 'numeric'}]},
 'COLINO DE PLÁTANO': {'cantidad': ['Cantidad sembrada de Plátano'],
  'observación': [
   {'texto': 'Cuántos colinos de plátano plantaron', 'tipo': 'numeric'},
   {'texto': 'Cuántos colinos de plátano murieron', 'tipo': 'numeric'}]},
 'COLINO DE BANANO': {'cantidad': ['Cantidad sembrada de Banano'],
  'observación': [
   {'texto': 'Cuántos colinos de banano plantaron', 'tipo': 'numeric'},
   {'texto': 'Cuántos colinos de banano murieron', 'tipo': 'numeric'}]},
 'COLINO DE GUAYABO': {'cantidad': ['Cantidad sembrada de Guayabo'],
  'observación': [
   {'texto': 'Cuántos colinos de guayabo plantaron', 'tipo': 'numeric'},
   {'texto': 'Cuántos colinos de guayabo murieron', 'tipo': 'numeric'}]},
 'SOBRE DE SEMILLAS DE HORTALIZAS': {'cantidad': ['Cantidad de sobres entregados'], 
  'observación': [
   {'texto': 'Cuántas veces ha sembrado', 'tipo': 'numeric'},
   {'texto': 'Continúa sembrando', 'tipo': 'options', 'opciones':['Si', 'No']},
   {'texto': 'Continúa sembrando cada cuanto (meses)','tipo': 'numeric'}]},
 'BANDEJA DE GERMINACIÓN': {'cantidad': ['Bandejas de germinación entregadas'],
  'observación': [
   {'texto': 'Se ha utilizado la bandeja de germinación', 'tipo': 'options', 'opciones':['Si', 'No']},
   {'texto': 'En qué estado está', 'tipo': 'options', 'opciones':['Bueno', 'Regular', 'Malo', 'No se utilizó']}]},
 'FUMIGADORA MANUAL': {'observación': [{'texto': 'Fumigadora Manual entregada', 'tipo': 'text'},
   {'texto': 'Fue utilizada con Bioinsumos Orgánicos', 'tipo': 'options', 'opciones':['Si', 'No']},
   {'texto': 'Cómo ha sido el funcionamiento', 'tipo': 'options', 'opciones': [ 'Bueno', 'Regular', 'Malo']}]},
 'PASTO VETIVER': {'cantidad': ['Cantidad entregada de pasto vetiver'],
   'observación': [{'texto': 'Se implementó la siembra', 'tipo': 'options', 'opciones':['Si', 'No']},
   {'texto': 'Se desarrolló bien en el campo', 'tipo': 'options', 'opciones':['Si', 'No']},
   {'texto': 'Qué manejo le ha dado', 'tipo': 'text'}]},
 'COMPOSTERA': {'observación':[{'texto': 'Los materiales fueron utilizados para', 'tipo':'options','opciones': ['Construir compostera nueva', 'Mejoramiento de compostera existente', 'No se utilizaron en compostera'] },
     {'texto': 'Cuántas láminas de zinc ha utilizado en la compostera', 'tipo':'numeric'},
                               {'texto': 'Cuántos bultos de cemento ha utilizado en la compostera', 'tipo':'numeric'},
                               {'texto': 'Cuánto amarre ha utilizado en la compostera', 'tipo':'numeric'}]},
 'ABONO ORGÁNICO': {'cantidad': ['Cantidad entregada de abonos orgánicos en kilos'],
    'observación':[{'texto': 'Qué cantidad ha utilizado', 'tipo':'numeric'}]}}

hoy=datetime.today()

clean={
  "GEN-Fecha": hoy,
  "GEN-O-Municipio": None,
  "GEN-O-Cuenca":None,
  "GEN-Vereda": None,
  "GEN-DAR": None,
  "GEN-Finca": None,
  "GEN-Beneficiario": None,
  "GEN-O-Vigencia": None,
  "GEN-Recibe la visita": None,
  "GEN-O-Propietario": None,
  "IND-CDS-O-Uso de materia orgánica": None,
  "IND-CDS-O-Trinchos; barreras; para evitar la pérdida de suelo": None,
  "IND-CDS-O-Suelo cubierto durante al menos 10 meses del año": None,
  "IND-CDS-O-Trazado con curvas a nivel": None,
  "IND-CYPDLB-O-Practica la caza": None,
  "IND-CYPDLB-O-Se tienen barreras vivas alrededor de la finca": None,
  "IND-CYPDLB-O-Siembra árboles como hábitat para las aves": None,
  "IND-CYPDLB-O-Tienen corredores biológicos en la finca": None,
  "IND-SA-MUL-Productos": [],
  "IND-UDB-O-Biofertilizantes": None,
  "IND-UDB-O-Abonos orgánicos": None,
  "IND-UDB-O-Uso de microorganismos de montaña": None,
  "IND-UDB-O-Biocontroladores": None,
  "IND-A-O-Las fuentes de agua se encuentran protegidas": None,
  "IND-A-O-Se genera vertimientos propios en la finca": None,
  "IND-A-O-Tiene tratamiento de aguas residuales en la finca": None,
  "IND-A-O-Cosecha de agua en la finca.": None,
  "IND-UDA-O-Usa agroquímicos": None,
  "IND-UDA-O-De manera permanente": None,
  "IND-UDA-O-De manera esporádica y como último recurso": None,
  "IND-PF-O-Participa solo la propietaria (o)": None,
  "IND-PF-O-Participa más de un integrante de la familia": None,
  "IND-PF-O-Participa toda la familia": None,
  "IM-SDMA-N-Cantidad de semilla entregada en kilos": None,
  "IM-SDMA-N-Cuántos kilos sembró": None,
  "IM-SDMA-N-Cuántas cosechas lleva": None,
  "IM-SDMA-N-Cuántos kilos ha cosechado": None,
  "IM-SDMA-O-Cómo fue el desarrollo": None,
  "IM-SDMA-M-Qué otra variedad de maíz tiene": [],
  "IM-SDF-N-Cantidad de semilla entregada en kilos": None,
  "IM-SDF-N-Cuántos kilos sembró": None,
  "IM-SDF-N-Cuántas cosechas lleva": None,
  "IM-SDF-N-Cuántos kilos ha cosechado": None,
  "IM-SDF-O-Cómo fue el desarrollo": None,
  "IM-SDF-M-Qué otra variedad de fríjol tiene": [],
  "IM-EBDF-N-Cantidad de estacas de Botón de oro": None,
  "IM-EBDF-N-Cuántas estacas de Nacedero": None,
  "IM-EBDF-N-Cuántas estacas de Matarratón": None,
  "IM-EBDF-N-Cuántas estacas sembradas prendieron": None,
  "IM-EBDF-O-Cuál es el estado actual del banco de forraje": None,
  "IM-EBDF-O-Continúa su propagación": None,
  "IM-AF-N-Cantidad de tipo Injerto": None,
  "IM-AF-N-Cantidad de tipo Nativos": None,
  "IM-AF-N-Cuántos arboles se desarrollaron": None,
  "IM-AF-O-En qué estado están": None,
  "IM-AF-N-Número de árboles vivos": None,
  "IM-CDP-N-Cantidad sembrada de Plátano": None,
  "IM-CDP-N-Cuántos colinos de plátano plantaron": None,
  "IM-CDP-N-Cuántos colinos de plátano murieron": None,
  "IM-CDB-N-Cantidad sembrada de Banano": None,
  "IM-CDB-N-Cuántos colinos de banano plantaron": None,
  "IM-CDB-N-Cuántos colinos de banano murieron": None,
  "IM-CDG-N-Cantidad sembrada de Guayabo": None,
  "IM-CDG-N-Cuántos colinos de guayabo plantaron": None,
  "IM-CDG-N-Cuántos colinos de guayabo murieron": None,
  "IM-SDSDH-N-Cantidad de sobres entregados": None,
  "IM-SDSDH-N-Cuántas veces ha sembrado": None,
  "IM-SDSDH-O-Continúa sembrando": None,
  "IM-SDSDH-N-Continúa sembrando cada cuanto (meses)": None,
  "IM-BDG-N-Bandejas de germinación entregadas": None,
  "IM-BDG-O-Se ha utilizado la bandeja de germinación": None,
  "IM-BDG-O-En qué estado está": None,
  "IM-FM-Fumigadora Manual entregada": None,
  "IM-FM-O-Fue utilizada con Bioinsumos Orgánicos": None,
  "IM-FM-O-Cómo ha sido el funcionamiento": None,
  "IM-PV-N-Cantidad entregada de pasto vetiver": None,
  "IM-PV-O-Se implementó la siembra": None,
  "IM-PV-O-Se desarrolló bien en el campo": None,
  "IM-PV-Qué manejo le ha dado": None,
  "IM-C-O-Los materiales fueron utilizados para": None,
  "IM-C-N-Cuántas láminas de zinc ha utilizado en la compostera": None,
  "IM-C-N-Cuántos bultos de cemento ha utilizado en la compostera": None,
  "IM-C-N-Cuánto amarre ha utilizado en la compostera": None,
  "IM-AO-N-Cantidad entregada de abonos orgánicos en kilos": None,
  "IM-AO-N-Qué cantidad ha utilizado": None,
  "RS-O-Ha entregado semillas a vecino": None,
  "RS-Nombre del Vecino 1": "",
  "RS-Nombre del Vecino 2": "",
  "RS-O-Intención de articularse al Mercado Agroecológico": None,
  "RS-Compromiso frente al proceso": None,
  "RS-Cuál semilla ha entregado a vecinos": [],
  "RS-Finca del Vecino 1": "",
  "RS-Finca del Vecino 2": "",
  "RS-O-Intención de articularse a Proceso Educativo": None,
  "RS-Observaciones": None,
  "FIR-Fecha de Firma": hoy,
  "FIR-Nombre de quién firma": None,
  "FIR-Cédula de quién firma": None
}

#sig={}

#for i in data.keys():
#    sig[siglas(i)]=i

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

    titulo(1,"Seguimiento Seguridad Alimentaria")

    titulo(2,"Información General")
    infoA=st.columns(3)
    with infoA[0]:
        resul["GEN-Fecha"]=st.date_input("Fecha de Visita", value="today", format="DD-MM-YYYY", key="GEN-Fecha").strftime('%Y-%m-%d %H:%M:%S')
        resul["GEN-O-Municipio"]=st.selectbox("Municipio", sorted(['ALCALA ', 'ULLOA ', 'CARTAGO', 'OBANDO', 'LA VICTORIA', 'ZARZAL', 'OBANDO', 'ANSERMANUEVO', 'EL AGUILA', 'ANSERMANUEVO', 'ARGELIA', 'EL CAIRO']), index=None, key="GEN-O-Municipio")

    with infoA[1]:
        resul["GEN-O-Cuenca"]=st.selectbox("Cuenca", sorted(['LA VIEJA ', 'OBANDO', 'CAÑAVERAL', 'CHANCOS', 'GARRAPATAS']),index=None, key="GEN-O-Cuenca")
        resul["GEN-Vereda"]=st.text_input("Vereda", value=None, key="GEN-Vereda")
            

    with infoA[2]:
        resul["GEN-DAR"]=st.selectbox("DAR", ["NORTE"], index=None,key="GEN-DAR")
        resul["GEN-Finca"]=st.text_input("Finca", value=None, key="GEN-Finca")


    infoB=st.columns(2)
    with infoB[0]:
        resul["GEN-Beneficiario"]=st.text_input("Beneficiario(a)", value=None, key="GEN-Beneficiario")
        resul["GEN-O-Vigencia"]=st.selectbox("Vigencia", [2020, 2021, 2022], index=None, key="GEN-O-Vigencia")
    with infoB[1]:
        resul["GEN-Recibe la visita"]=st.text_input("Quien recibe la visita", value=None, key="GEN-Recibe la visita")
        resul["GEN-O-Propietario"]=st.selectbox("Estado de la propiedad", ["El mismo dueño", "Cambio de propietario"], index=None,  key="GEN-O-Propietario")
    
    
    st.markdown('---')
    st.markdown(" ")

###
### INDICADORES
###
    titulo(2,"Indicadores")

    st.markdown(" ")

    head=st.columns(3)
    with head[0]:
        st.markdown("**Indicador**")
    with head[1]:
        st.markdown("**Descripción**")
    with head[2]:
        st.markdown("**Observaciones**") 
    st.markdown('---')

    for ind in data_ind.keys():
        si=siglas(ind)
        cols=st.columns(3)
        cols[0].write(ind)
        if "descripción" in data_ind[ind]:
            descrip=data_ind[ind]["descripción"][0]
            with cols[1]:
                st.write(descrip)
        if "observación" in data_ind[ind]:
            observaciones=data_ind[ind]["observación"]
            with cols[2]:
                for obs in observaciones:
                    if obs["tipo"] == "options":
                        resul[("IND-"+si+"-O-"+obs["texto"]).strip()]=st.selectbox(obs["texto"],index=None, options=obs["opciones"], key=("IND-"+si+"-O-"+obs["texto"]).strip())
                    if obs["tipo"] == "multi":
                        resul[("IND-"+si+"-MUL-"+obs["texto"]).strip()]=st.multiselect(obs["texto"], options=obs["opciones"], key=("IND-"+si+"-MUL-"+obs["texto"]).strip())
                    if obs["tipo"] == "text":
                        resul[("IND-"+si+"-"+obs["texto"]).strip()]=st.text_input(obs["texto"], value=None, key=("IND-"+si+"-"+obs["texto"]).strip())
                    if obs["tipo"] == "numeric":
                        resul[("IND-"+si+"-N-"+obs["texto"]).strip()]=st.number_input(obs["texto"], value=None, key=("IND-"+si+"-N-"+obs["texto"]).strip())
        st.markdown('---')

    st.markdown(" ")



####
####


###
### INSUMOS
###
    titulo(2,"Insumos o Materiales")

    st.markdown(" ")

    head=st.columns(3)
    with head[0]:
        st.markdown("**Descripción**")
    with head[1]:
        st.markdown("**Cantidad**")
    with head[2]:
        st.markdown("**Observaciones**") 
    st.markdown('---')

    for insu in data.keys():
        si=siglas(insu)
        cols=st.columns(3)
        cols[0].write(insu)
        if "cantidad" in data[insu]:
            cantidades=data[insu]["cantidad"]
            with cols[1]:
                for can in cantidades:
                    resul[("IM-"+si+"-N-"+can).strip()]=st.number_input(can,value=None, key="IM-"+si+"-N-"+can)
        if "observación" in data[insu]:
            observaciones=data[insu]["observación"]
            with cols[2]:
                for obs in observaciones:
                    if obs["tipo"] == "options":
                        resul[("IM-"+si+"-O-"+obs["texto"]).strip()]=st.selectbox(obs["texto"],index=None, options=obs["opciones"], key=("IM-"+si+"-O-"+obs["texto"]).strip())
                    if obs["tipo"] == "text":
                        resul[("IM-"+si+"-"+obs["texto"]).strip()]=st.text_input(obs["texto"], value=None, key=("IM-"+si+"-"+obs["texto"]).strip())
                    if obs["tipo"] == "numeric":
                        resul[("IM-"+si+"-N-"+obs["texto"]).strip()]=st.number_input(obs["texto"], value=None, key=("IM-"+si+"-N-"+obs["texto"]).strip())
                    if obs["tipo"] == "multi":
                        resul[("IM-"+si+"-M-"+obs["texto"]).strip()]=st.multiselect(obs["texto"], options=obs["opciones"], key=("IM-"+si+"-M-"+obs["texto"]).strip())
        st.markdown('---')

    st.markdown(" ")


    titulo(2,"Retribución solidaria")
    st.markdown(" ")
    benefA=st.columns(2)
    with benefA[0]:
        resul["RS-O-Ha entregado semillas a vecino"]=st.selectbox("El beneficiario manifiesta haber entregado semillas a un vecino de su vereda", ["Si","No"], index=None, key="RS-O-Ha entregado semillas a vecino")
        resul["RS-Nombre del Vecino 1"]=st.text_input("Nombre del Vecino 1",  key="RS-Nombre del Vecino 1")
        resul["RS-Nombre del Vecino 2"]=st.text_input("Nombre del Vecino 2", key="RS-Nombre del Vecino 2")
        resul["RS-O-Intención de articularse al Mercado Agroecológico"]=st.selectbox("El beneficiario manifiesta la intención de articularse al proceso de Mercado Agroecológico", ["Si","No"], index=None,  key="RS-O-Intención de articularse al Mercado Agroecológico")
        resul["RS-Compromiso frente al proceso"]=st.text_input("Compromiso frente al proceso", value=None, key="RS-Compromiso frente al proceso")
    with benefA[1]:
        resul["RS-Cuál semilla ha entregado a vecinos"]=st.multiselect("Cuál semilla ha entregado a vecinos", ["Ninguno","Maíz", "Frijol", "Hortalizas", "Otras"], key="RS-Cuál semilla ha entregado a vecinos")
        resul["RS-Finca del Vecino 1"]=st.text_input("Finca del Vecino 1", key="RS-Finca del Vecino 1")
        resul["RS-Finca del Vecino 2"]=st.text_input("Finca del Vecino 2", key="RS-Finca del Vecino 2")
        resul["RS-O-Intención de articularse a Proceso Educativo"]=st.selectbox("El beneficiario manifiesta la intención de articularse al proceso en la Institución educativa", ["Si","No"], index=None, key="RS-O-Intención de articularse a Proceso Educativo")
        resul["RS-Observaciones"]=st.text_input("Observaciones", value=None, key="RS-Observaciones")

    st.markdown('---')

    st.markdown(" ")
    titulo(3,"Firma")

    firma=st.columns(3)
    with firma[0]:
        resul["FIR-Fecha de Firma"]=st.date_input("Fecha de Firma", value="today", format="DD-MM-YYYY", key="FIR-Fecha de Firma").strftime('%Y-%m-%d %H:%M:%S')
    with firma[1]:    
        resul["FIR-Nombre de quién firma"]=st.text_input("Nombre de quién firma", value=None,  key="FIR-Nombre de quién firma")
    with firma[2]:    
        resul["FIR-Cédula de quién firma"]=st.number_input("Cédula de quién firma", value=None, step=1, key="FIR-Cédula de quién firma")



    #submitted = st.form_submit_button("ENVIAR",type='primary',use_container_width=True, on_click=disable, disabled=st.session_state.disabled)
    submitted = st.button("ENVIAR",type='primary',use_container_width=True, on_click=disable ,disabled=st.session_state.disabled)

    if submitted:
        faltantes=[]
        for i in resul.keys():
            if  i not in ["FIR-Fecha de Firma","GEN-Fecha","encuestador", "RS-Finca del Vecino 1","RS-Finca del Vecino 2", "RS-Nombre del Vecino 1","RS-Nombre del Vecino 2"]:
                if resul[i]==clean[i]:
                    faltantes.append(i.split('-')[-1]) 
        if len(faltantes) > 0:
            fal=', '.join(faltantes)
            st.session_state.error = True
            titulo(6, "⚠️ ¡Cuidado! ⚠️")
            st.warning(f"⚠️ Faltan los siguientes campos: {fal} ⚠️")

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





