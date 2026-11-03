
import streamlit as st
import pandas as pd
from google.cloud import firestore
from google.oauth2 import service_account
import json

# =====================================
# CONEXIÓN A FIREBASE
# =====================================

key_dict = json.loads(st.secrets["textkey"])

creds = service_account.Credentials.from_service_account_info(key_dict)

db = firestore.Client(
    credentials=creds,
    project=key_dict["project_id"]
)

dbNames = db.collection("names")

# =====================================
# CREAR NUEVO REGISTRO
# =====================================

st.header("Nuevo registro")

index = st.text_input("Index")
name = st.text_input("Name")

sex = st.selectbox(
    "Select Sex",
    ("F", "M", "Other")
)

submit = st.button("Crear nuevo registro")

if index and name and sex and submit:

    doc_ref = dbNames.document(name)

    doc_ref.set({
        "index": index,
        "name": name,
        "sex": sex
    })

    st.success("Registro insertado correctamente")


# =====================================
# FUNCIÓN PARA BUSCAR NOMBRE
# =====================================

def loadByName(name):

    names_ref = dbNames.where("name", "==", name)

    currentName = None

    for myname in names_ref.stream():
        currentName = myname

    return currentName


# =====================================
# BUSCAR REGISTRO
# =====================================

st.sidebar.subheader("Buscar nombre")

nameSearch = st.sidebar.text_input("Nombre")

btnFiltrar = st.sidebar.button("Buscar")

if btnFiltrar:

    doc = loadByName(nameSearch)

    if doc is None:
        st.sidebar.warning("Nombre no existe")

    else:
        st.sidebar.write(doc.to_dict())


# =====================================
# ELIMINAR REGISTRO
# =====================================

st.sidebar.markdown("---")

btnEliminar = st.sidebar.button("Eliminar")

if btnEliminar:

    deletename = loadByName(nameSearch)

    if deletename is None:
        st.sidebar.warning(f"{nameSearch} no existe")

    else:
        dbNames.document(deletename.id).delete()

        st.sidebar.success("Registro eliminado correctamente")
