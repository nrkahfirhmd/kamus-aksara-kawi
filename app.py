import streamlit as st
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

# Konfigurasi endpoint Jena Fuseki
FUSEKI_ENDPOINT = "http://localhost:3030/pratisentana1/sparql"

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
    st.write("Klik untuk memasukkan aksara:")
    # Using a dictionary to map Kawi script to its Latin transliteration
    aksara_map = {
        "ꦏ": "ka", "ꦠ": "ta", "ꦤ": "na", "ꦧ": "ba", "ꦗ": "ja",
        "ꦒ": "ga", "ꦥ": "pa", "ꦩ": "ma", "ꦚ": "nya", "ꦛ": "tha", "ꦝ": "dha"
    }

    # Create a number of columns equal to the number of characters for a horizontal layout
    cols = st.columns(len(aksara_map))

    # Iterate through each column and place one button
    for i, (aksara, latin) in enumerate(aksara_map.items()):
        with cols[i]:
            # Create a label that includes both the script and its transliteration
            button_label = f"{aksara}"
            if st.button(button_label, key=f"key_{aksara}", help=f"Masukkan aksara {latin}", use_container_width=True):
                # Append the selected character to the input text in session state
                st.session_state["input_kawi"] = st.session_state.get("input_kawi", "") + aksara

# Input dari pengguna
st.subheader("🔡 Terjemahkan Aksara Kawi ↔ Latin")
input_kawi = st.text_input("Masukkan Aksara Kawi", key="input_kawi")
input_latin = st.text_input("Masukkan Kata Latin (misal: Ka)")

# Terjemahkan dari Aksara Kawi
if input_kawi:
    sparql = f"""
      PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
      PREFIX : <http://pratisentana.org/ontology#>

      SELECT ?latin WHERE {{
        # Find the specific Kawi text node based on the input string.
        # Note: The input Kawi string must be an exact match.
        ?kawiText rdf:value "{input_kawi}"@jv-x-krama .

        # Use the central entry to find the connection
        ?entry :memilikiTeksAksara ?kawiText ;
              :memilikiTransliterasi ?translit .

        # Get the value from the correctly linked transliteration node
        ?translit rdf:value ?latin .
      }}
      """
    results = query_fuseki(sparql)
    if results:
        st.success(f"Terjemahan: {results[0]['latin']['value']}")
    else:
        st.warning("Tidak ditemukan terjemahan untuk aksara tersebut.")

# Terjemahkan dari Latin ke Aksara
elif input_latin:
    sparql = f"""
      PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
      PREFIX : <http://pratisentana.org/ontology#>

      SELECT ?kawi WHERE {{
        # Find the central entry that connects the different text forms
        ?entry :memilikiTerjemahan ?terjemah ;
              :memilikiTeksAksara ?kawiText .

        # Filter to find the entry where the Indonesian translation is "{input_latin}"
        ?terjemah rdf:value ?indonesianValue .
        FILTER(str(?indonesianValue) = "{input_latin}")

        # Get the corresponding Kawi script from that same entry
        ?kawiText rdf:value ?kawi .
      }}
      """
    results = query_fuseki(sparql)
    if results:
        st.success(f"Aksara Kawi: {results[0]['kawi']['value']}")
    else:
        st.warning("Tidak ditemukan aksara untuk arti tersebut.")