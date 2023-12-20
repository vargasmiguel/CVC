import streamlit as st

from supabase import create_client, Client

from authenticate import Authenticate

from datetime import datetime

import os

import pandas as pd

import plotly.express as px

st.set_page_config(layout="wide", page_title="📊_Resultados")

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

secc={'DATOS GENERALES': {'Fecha': 'GEN-Fecha',
  'Municipio': 'GEN-O-Municipio',
  'Cuenca': 'GEN-O-Cuenca',
  'Vereda': 'GEN-Vereda',
  'DAR': 'GEN-DAR',
  'Finca': 'GEN-Finca',
  'Beneficiario': 'GEN-Beneficiario',
  'Vigencia': 'GEN-O-Vigencia',
  'Recibe la visita': 'GEN-Recibe la visita',
  'Propietario': 'GEN-O-Propietario'},
 'INDICADORES': {'CONSERVACIÓN DE SUELOS': {'Uso de materia orgánica': 'IND-CDS-O-Uso de materia orgánica',
   'Trinchos; barreras; para evitar la pérdida de suelo': 'IND-CDS-O-Trinchos; barreras; para evitar la pérdida de suelo',
   'Suelo cubierto durante al menos 10 meses del año': 'IND-CDS-O-Suelo cubierto durante al menos 10 meses del año',
   'Trazado con curvas a nivel': 'IND-CDS-O-Trazado con curvas a nivel'},
  'CONSERVACIÓN Y PROTECCIÓN DE LA BIODIVERSIDAD': {'Practica la caza': 'IND-CYPDLB-O-Practica la caza',
   'Se tienen barreras vivas alrededor de la finca': 'IND-CYPDLB-O-Se tienen barreras vivas alrededor de la finca',
   'Siembra árboles como hábitat para las aves': 'IND-CYPDLB-O-Siembra árboles como hábitat para las aves',
   'Tienen corredores biológicos en la finca': 'IND-CYPDLB-O-Tienen corredores biológicos en la finca'},
  'SEGURIDAD ALIMENTARIA': {'Productos': 'IND-SA-MUL-Productos'},
  'USO DE BIOINSUMOS': {'Biofertilizantes': 'IND-UDB-O-Biofertilizantes',
   'Abonos orgánicos': 'IND-UDB-O-Abonos orgánicos',
   'Uso de microorganismos de montaña': 'IND-UDB-O-Uso de microorganismos de montaña',
   'Biocontroladores': 'IND-UDB-O-Biocontroladores'},
  'AGUA': {'Las fuentes de agua se encuentran protegidas': 'IND-A-O-Las fuentes de agua se encuentran protegidas',
   'Se genera vertimientos propios en la finca': 'IND-A-O-Se genera vertimientos propios en la finca',
   'Tiene tratamiento de aguas residuales en la finca': 'IND-A-O-Tiene tratamiento de aguas residuales en la finca',
   'Cosecha de agua en la finca.': 'IND-A-O-Cosecha de agua en la finca.'},
  'USO DE AGROQUÍMICOS': {'Usa agroquímicos': 'IND-UDA-O-Usa agroquímicos',
   'De manera permanente': 'IND-UDA-O-De manera permanente',
   'De manera esporádica y como último recurso': 'IND-UDA-O-De manera esporádica y como último recurso'},
  'PARTICIPACIÓN FAMILIAR': {'Participa solo la propietaria (o)': 'IND-PF-O-Participa solo la propietaria (o)',
   'Participa más de un integrante de la familia': 'IND-PF-O-Participa más de un integrante de la familia',
   'Participa toda la familia': 'IND-PF-O-Participa toda la familia'}},
 'INSUMOS Y MATERIALES': {'SEMILLA DE MAÍZ AMARILLO': {'Cantidad de semilla entregada en kilos': 'IM-SDMA-N-Cantidad de semilla entregada en kilos',
   'Cuántos kilos sembró': 'IM-SDMA-N-Cuántos kilos sembró',
   'Cuántas cosechas lleva': 'IM-SDMA-N-Cuántas cosechas lleva',
   'Cuántos kilos ha cosechado': 'IM-SDMA-N-Cuántos kilos ha cosechado',
   'Cómo fue el desarrollo': 'IM-SDMA-O-Cómo fue el desarrollo',
   'Qué otra variedad de maíz tiene': 'IM-SDMA-M-Qué otra variedad de maíz tiene'},
  'SEMILLA DE FRÍJOL': {'Cantidad de semilla entregada en kilos': 'IM-SDF-N-Cantidad de semilla entregada en kilos',
   'Cuántos kilos sembró': 'IM-SDF-N-Cuántos kilos sembró',
   'Cuántas cosechas lleva': 'IM-SDF-N-Cuántas cosechas lleva',
   'Cuántos kilos ha cosechado': 'IM-SDF-N-Cuántos kilos ha cosechado',
   'Cómo fue el desarrollo': 'IM-SDF-O-Cómo fue el desarrollo',
   'Qué otra variedad de fríjol tiene': 'IM-SDF-M-Qué otra variedad de fríjol tiene'},
  'ESTACAS BANCO DE FORRAJE': {'Cantidad de estacas de Botón de oro': 'IM-EBDF-N-Cantidad de estacas de Botón de oro',
   'Cuántas estacas de Nacedero': 'IM-EBDF-N-Cuántas estacas de Nacedero',
   'Cuántas estacas de Matarratón': 'IM-EBDF-N-Cuántas estacas de Matarratón',
   'Cuántas estacas sembradas prendieron': 'IM-EBDF-N-Cuántas estacas sembradas prendieron',
   'Cuál es el estado actual del banco de forraje': 'IM-EBDF-O-Cuál es el estado actual del banco de forraje',
   'Continúa su propagación': 'IM-EBDF-O-Continúa su propagación'},
  'ARBOLES FRUTALES': {'Cantidad de tipo Injerto': 'IM-AF-N-Cantidad de tipo Injerto',
   'Cantidad de tipo Nativos': 'IM-AF-N-Cantidad de tipo Nativos',
   'Cuántos arboles se desarrollaron': 'IM-AF-N-Cuántos arboles se desarrollaron',
   'En qué estado están': 'IM-AF-O-En qué estado están',
   'Número de árboles vivos': 'IM-AF-N-Número de árboles vivos'},
  'COLINO DE PLÁTANO': {'Cantidad sembrada de Plátano': 'IM-CDP-N-Cantidad sembrada de Plátano',
   'Cuántos colinos de plátano plantaron': 'IM-CDP-N-Cuántos colinos de plátano plantaron',
   'Cuántos colinos de plátano murieron': 'IM-CDP-N-Cuántos colinos de plátano murieron'},
  'COLINO DE BANANO': {'Cantidad sembrada de Banano': 'IM-CDB-N-Cantidad sembrada de Banano',
   'Cuántos colinos de banano plantaron': 'IM-CDB-N-Cuántos colinos de banano plantaron',
   'Cuántos colinos de banano murieron': 'IM-CDB-N-Cuántos colinos de banano murieron'},
  'COLINO DE GUAYABO': {'Cantidad sembrada de Guayabo': 'IM-CDG-N-Cantidad sembrada de Guayabo',
   'Cuántos colinos de guayabo plantaron': 'IM-CDG-N-Cuántos colinos de guayabo plantaron',
   'Cuántos colinos de guayabo murieron': 'IM-CDG-N-Cuántos colinos de guayabo murieron'},
  'SOBRE DE SEMILLAS DE HORTALIZAS': {'Cantidad de sobres entregados': 'IM-SDSDH-N-Cantidad de sobres entregados',
   'Cuántas veces ha sembrado': 'IM-SDSDH-N-Cuántas veces ha sembrado',
   'Continúa sembrando': 'IM-SDSDH-O-Continúa sembrando',
   'Continúa sembrando cada cuanto (meses)': 'IM-SDSDH-N-Continúa sembrando cada cuanto (meses)'},
  'BANDEJA DE GERMINACIÓN': {'Bandejas de germinación entregadas': 'IM-BDG-N-Bandejas de germinación entregadas',
   'Se ha utilizado la bandeja de germinación': 'IM-BDG-O-Se ha utilizado la bandeja de germinación',
   'En qué estado está': 'IM-BDG-O-En qué estado está'},
  'FUMIGADORA MANUAL': {'Cantidad de fumigadoras manuales entregadas': 'IM-FM-N-Cantidad de fumigadoras manuales entregadas',
   'Fue utilizada con Bioinsumos Orgánicos': 'IM-FM-O-Fue utilizada con Bioinsumos Orgánicos',
   'Cómo ha sido el funcionamiento': 'IM-FM-O-Cómo ha sido el funcionamiento'},
  'PASTO VETIVER': {'Cantidad entregada de pasto vetiver (esquejes)': 'IM-PV-N-Cantidad entregada de pasto vetiver (esquejes)',
   'Se implementó la siembra': 'IM-PV-O-Se implementó la siembra',
   'Se desarrolló bien en el campo': 'IM-PV-O-Se desarrolló bien en el campo',
   'Qué manejo le ha dado': 'IM-PV-O-Qué manejo le ha dado'},
  'COMPOSTERA': {'Los materiales fueron utilizados para': 'IM-C-O-Los materiales fueron utilizados para',
   'Cuántas láminas de zinc ha utilizado en la compostera': 'IM-C-N-Cuántas láminas de zinc ha utilizado en la compostera',
   'Cuántos bultos de cemento ha utilizado en la compostera': 'IM-C-N-Cuántos bultos de cemento ha utilizado en la compostera',
   'Cuánto amarre ha utilizado en la compostera': 'IM-C-N-Cuánto amarre ha utilizado en la compostera'},
  'ABONO ORGÁNICO': {'Cantidad entregada de abonos orgánicos (bultos)': 'IM-AO-N-Cantidad entregada de abonos orgánicos (bultos)',
   'Qué cantidad ha utilizado': 'IM-AO-N-Qué cantidad ha utilizado'}},
 'RETRIBUCIÓN SOCIAL': {'Ha entregado semillas a vecino': 'RS-O-Ha entregado semillas a vecino',
  'Nombre del Vecino 1': 'RS-Nombre del Vecino 1',
  'Nombre del Vecino 2': 'RS-Nombre del Vecino 2',
  'Intención de articularse al Mercado Agroecológico': 'RS-O-Intención de articularse al Mercado Agroecológico',
  'Compromiso frente al proceso': 'RS-Compromiso frente al proceso',
  'Cuál semilla ha entregado a vecinos': 'RS-Cuál semilla ha entregado a vecinos',
  'Finca del Vecino 1': 'RS-Finca del Vecino 1',
  'Finca del Vecino 2': 'RS-Finca del Vecino 2',
  'Intención de articularse a Proceso Educativo': 'RS-O-Intención de articularse a Proceso Educativo',
  'Observaciones': 'RS-Observaciones'},
 'FIRMA': {'Fecha de Firma': 'FIR-Fecha de Firma',
  'Nombre de quién firma': 'FIR-Nombre de quién firma',
  'Cédula de quién firma': 'FIR-Cédula de quién firma'}}

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

    titulo(1,"Visualizador de Resultados")

    st.write(f"Hay un total de **{len(df)} encuestas**")

    st.divider()
    ex=st.columns(4)
    ###
    ###EJE X
    ###
    with ex[0]:
        encab("Eje X")
        sx1=st.selectbox("Categoría", options=secc.keys(), index=None, key="sx1")
        if sx1==None:
            sx2=st.selectbox("Subcategoría", [], index=None, key="sx2")
            sx3=st.selectbox("Pregunta", options=[], index=None, key="sx3")
        elif type(list(secc[sx1].values())[0]) == dict:
            sx2=st.selectbox("Subcategoría", options=secc[sx1].keys(), index=None, key="sx2")
            if sx2 == None:
                sx3=st.selectbox("Pregunta", options=[], index=None, key="sx3")
            else:
                sx3=st.selectbox("Pregunta", options=secc[sx1][sx2].keys(), index=None, key="sx3")
            if sx3 != None:
                pregx=secc[sx1][sx2][sx3]
        else:
            sx2=st.selectbox("Subcategoría", [], index=None, key="sx2")
            sx3=st.selectbox("Pregunta", options=secc[sx1].keys(), index=None, key="sx3")
            if sx3 != None:
                pregx=secc[sx1][sx3]

    ###
    ###EJE Y
    ###
    with ex[1]:
        encab("Eje Y")
        sy1=st.selectbox("Categoría", options=secc.keys(), index=None, key="sy1")
        if sy1==None:
            sy2=st.selectbox("Subcategoría", [], index=None, key="sy2")
            sy3=st.selectbox("Pregunta", options=[], index=None, key="sy3")
        elif type(list(secc[sy1].values())[0]) == dict:
            sy2=st.selectbox("Subcategoría", options=secc[sy1].keys(), index=None, key="sy2")
            if sy2 == None:
                sy3=st.selectbox("Pregunta", options=[], index=None, key="sy3")
            else:
                sy3=st.selectbox("Pregunta", options=secc[sy1][sy2].keys(), index=None, key="sy3")
            if sy3 != None:
                pregy=secc[sy1][sy2][sy3]
        else:
            sy2=st.selectbox("Subcategoría", [], index=None, key="sy2")
            sy3=st.selectbox("Pregunta", options=secc[sy1].keys(), index=None, key="sy3")
            if sy3 != None:
                pregy=secc[sy1][sy3]

    ###
    ### CLASIFICAR
    ###
    with ex[2]:
        encab("Clasificar")
        sc1=st.selectbox("Categoría", options=secc.keys(), index=None, key="sc1")
        if sc1==None:
            sc2=st.selectbox("Subcategoría", [], index=None, key="sc2")
            sc3=st.selectbox("Pregunta", options=[], index=None, key="sc3")
        elif type(list(secc[sc1].values())[0]) == dict:
            sc2=st.selectbox("Subcategoría", options=secc[sc1].keys(), index=None, key="sc2")
            if sc2 == None:
                sc3=st.selectbox("Pregunta", options=[], index=None, key="sc3")
            else:
                sc3=st.selectbox("Pregunta", options=secc[sc1][sc2].keys(), index=None, key="sc3")
            if sc3 != None:
                pregc=secc[sc1][sc2][sc3]
        else:
            sc2=st.selectbox("Subcategoría", [], index=None, key="sc2")
            sc3=st.selectbox("Pregunta", options=secc[sc1].keys(), index=None, key="sc3")
            if sc3 != None:
                pregc=secc[sc1][sc3]

    ###
    ### SOMBREAR
    ###
    with ex[3]:
        encab("Sombrear")
        ss1=st.selectbox("Categoría", options=secc.keys(), index=None, key="ss1")
        if ss1==None:
            ss2=st.selectbox("Subcategoría", [], index=None, key="ss2")
            ss3=st.selectbox("Pregunta", options=[], index=None, key="ss3")
        elif type(list(secc[ss1].values())[0]) == dict:
            ss2=st.selectbox("Subcategoría", options=secc[ss1].keys(), index=None, key="ss2")
            if ss2 == None:
                ss3=st.selectbox("Pregunta", options=[], index=None, key="ss3")
            else:
                ss3=st.selectbox("Pregunta", options=secc[ss1][ss2].keys(), index=None, key="ss3")
            if ss3 != None:
                pregs=secc[ss1][ss2][ss3]
        else:
            ss2=st.selectbox("Subcategoría", [], index=None, key="ss2")
            ss3=st.selectbox("Pregunta", options=secc[ss1].keys(), index=None, key="ss3")
            if ss3 != None:
                pregs=secc[ss1][ss3]
    
    encab("Parámetros")
    p=st.columns(3)
    funcion=p[0].selectbox("Función de agregación", ["Contar", "Sumar", "Promedio", "Minímo", "Máximo"], index=0, key="func")
    bins=p[1].number_input("Bins", value=None, step=1, key="bins")
    autotexto=p[2].selectbox("Tipo de texto", ["Ninguno","Enteros","Una cifra decimal", "Dos cifras decimales"], index=0, key="autotexto")

    fun={"Contar": "count", "Sumar":"sum", "Promedio":"avg", "Minímo":"min", "Máximo":"max"}
    autot={"Ninguno":False,"Enteros":'.0f',"Una cifra decimal":'.1f', "Dos cifras decimales":'.2f'}

    st.divider()
    encab("GRÁFICO")
    if pregx != None:
        fig = px.histogram(df, x=pregx, y=pregy, color=pregc, pattern_shape=pregs, histfunc=fun[funcion], nbins=bins, text_auto=autot[autotexto])
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)


    st.divider()
    encab("DATOS")

    st.dataframe(df)


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





