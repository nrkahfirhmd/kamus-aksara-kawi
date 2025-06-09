import streamlit as st
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

# Konfigurasi endpoint Jena Fuseki
FUSEKI_ENDPOINT = "http://localhost:3030/kawi/sparql"

st.set_page_config(page_title="Kamus Aksara Kawi", layout="wide")
st.title("📖 Kamus Aksara Kawi (Terhubung ke Jena Fuseki)")

# Fungsi untuk SPARQL query


def query_fuseki(sparql_query):
    sparql = SPARQLWrapper(FUSEKI_ENDPOINT)
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results["results"]["bindings"]


# Tampilan keyboard aksara kawi
with st.expander("⌨️ Keyboard Aksara Kawi"):
    aksara_list = ["ꦏ", "ꦠ", "ꦤ", "ꦧ", "ꦗ", "ꦒ", "ꦥ", "ꦩ", "ꦚ", "ꦛ", "ꦝ"]
    col1, col2 = st.columns(2)
    with col1:
        st.write("Klik untuk memasukkan aksara:")
        for aksara in aksara_list:
            if st.button(aksara, key=aksara):
                st.session_state["input_kawi"] = st.session_state.get(
                    "input_kawi", "") + aksara

# Input dari pengguna
st.subheader("🔡 Terjemahkan Aksara Kawi ↔ Latin")
input_kawi = st.text_input("Masukkan Aksara Kawi", key="input_kawi")
input_latin = st.text_input("Masukkan Kata Latin (misal: Ka)")

# Terjemahkan dari Aksara Kawi
if input_kawi:
    sparql = f"""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX ex: <http://example.org/>

    SELECT ?label ?arti WHERE {{
        ?s rdfs:label "{input_kawi}" ;
           ex:arti ?arti .
    }}
    """
    results = query_fuseki(sparql)
    if results:
        st.success(f"Terjemahan: {results[0]['arti']['value']}")
    else:
        st.warning("Tidak ditemukan terjemahan untuk aksara tersebut.")

# Terjemahkan dari Latin ke Aksara
elif input_latin:
    sparql = f"""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX ex: <http://example.org/>

    SELECT ?label WHERE {{
        ?s rdfs:label ?label ;
           ex:arti "{input_latin}" .
    }}
    """
    results = query_fuseki(sparql)
    if results:
        st.success(f"Aksara Kawi: {results[0]['label']['value']}")
    else:
        st.warning("Tidak ditemukan aksara untuk arti tersebut.")