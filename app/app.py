import streamlit as st
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

# Konfigurasi endpoint Jena Fuseki
FUSEKI_ENDPOINT = "http://34.34.221.164:3030/pratisentana1/sparql"

st.set_page_config(page_title="Kamus Aksara Kawi", layout="wide")
st.title("📖 Kamus Aksara Kawi (Terhubung ke Jena Fuseki)")

# Fungsi untuk SPARQL query
def query_fuseki(sparql_query):
    sparql = SPARQLWrapper(FUSEKI_ENDPOINT)
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results["results"]["bindings"]

if "selected_items" not in st.session_state:
    st.session_state["selected_items"] = []

# Tampilan keyboard aksara kawi
with st.expander("⌨️ Keyboard Aksara Kawi Lengkap", expanded=True):
    st.write("Klik tombol untuk menyusun kata dalam Aksara Kawi:")

    # Define character sets
    nglegena = {
        "ꦲ": "ha", "ꦤ": "na", "ꦕ": "ca", "ꦫ": "ra", "ꦏ": "ka",
        "ꦢ": "da", "ꦠ": "ta", "ꦱ": "sa", "ꦮ": "wa", "ꦭ": "la",
        "ꦥ": "pa", "ꦝ": "dha", "ꦗ": "ja", "ꦪ": "ya", "ꦚ": "nya",
        "ꦩ": "ma", "ꦒ": "ga", "ꦧ": "ba", "ꦛ": "tha", "ꦔ": "nga"
    }
    sandhangan_swara = {
        "ꦶ": "i (wulu)", "ꦸ": "u (suku)", "ꦺ": "é (taling)",
        "ꦺꦴ": "o (taling tarung)", "ꦼ": "e (pepet)"
    }
    sandhangan_panyigeg = {
        "ꦃ": "-h (wignyan)", "ꦁ": "-ng (cecak)", "ꦂ": "-r (layar)",
        "꧀": " (pangkon)"
    }
    aksara_khusus = {
        "ꦎꦀ": "Om"
    }

    # Use tabs for better organization
    tab1, tab2, tab3 = st.tabs(
        ["Aksara Nglegena (Konsonan Dasar)", "Sandhangan (Vokal & Lainnya)", "Aksara Khusus"])

    with tab1:
        st.subheader("Aksara Nglegena")
        # Display consonants in rows for better layout
        chunk_size = 5
        nglegena_items = list(nglegena.items())
        for i in range(0, len(nglegena_items), chunk_size):
            chunk = nglegena_items[i:i + chunk_size]
            cols = st.columns(chunk_size)
            for j, (aksara, latin) in enumerate(chunk):
                with cols[j]:
                    button_label = f"{aksara}\n({latin})"
                    if st.button(button_label, key=f"key_{aksara}", help=f"Masukkan {latin}", use_container_width=True):
                        st.session_state["input_kawi"] += aksara

    with tab2:
        st.subheader("Sandhangan Swara (Vokal)")
        cols = st.columns(len(sandhangan_swara))
        for i, (aksara, latin) in enumerate(sandhangan_swara.items()):
            with cols[i]:
                button_label = f"{aksara}\n({latin})"
                if st.button(button_label, key=f"key_{aksara}", help=f"Masukkan {latin}", use_container_width=True):
                    st.session_state["input_kawi"] += aksara

        st.subheader("Sandhangan Panyigeg Wanda (Akhiran Suku Kata)")
        cols = st.columns(len(sandhangan_panyigeg))
        for i, (aksara, latin) in enumerate(sandhangan_panyigeg.items()):
            with cols[i]:
                button_label = f"{aksara}\n({latin})"
                if st.button(button_label, key=f"key_{aksara}", help=f"Masukkan {latin}", use_container_width=True):
                    st.session_state["input_kawi"] += aksara

    with tab3:
        st.subheader("Aksara Khusus")
        cols = st.columns(len(aksara_khusus))
        for i, (aksara, latin) in enumerate(aksara_khusus.items()):
            with cols[i]:
                button_label = f"{aksara}\n({latin})"
                if st.button(button_label, key=f"key_{aksara}", help=f"Masukkan {latin}", use_container_width=True):
                    st.session_state["input_kawi"] += aksara

    # Add a clear button for convenience
    if st.button("Hapus Input", use_container_width=True):
        st.session_state["input_kawi"] = ""

# Input dari pengguna
st.subheader("🔡 Terjemahkan Aksara Kawi ↔ Latin")
input_kawi = st.text_input("Masukkan Aksara Kawi", key="input_kawi", disabled=True)
input_latin = st.text_input("Masukkan Kata Latin (misal: Ka)")

def load_all_items():
    sparql_all = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX : <http://pratisentana.org/ontology#>

        SELECT ?kawi ?translit ?terjemahan WHERE {
            ?entry a :BarisPrasasti ;
                  :memilikiTeksAksara ?aksara ;
                  :memilikiTransliterasi ?translitNode ;
                  :memilikiTerjemahan ?terjemahanNode .

            ?aksara rdf:value ?kawi .
            FILTER (lang(?kawi) = "jv-x-krama")

            ?translitNode rdf:value ?translit .
            FILTER (lang(?translit) = "jv-Latn")

            ?terjemahanNode rdf:value ?terjemahan .
            FILTER (lang(?terjemahan) = "id")
        }
    """
    results = query_fuseki(sparql_all)
    st.session_state["selected_items"] = results

# Load once
if not input_kawi and not input_latin:
    load_all_items()

# Terjemahkan dari Aksara Kawi
if input_kawi:
    sparql = f"""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX : <http://pratisentana.org/ontology#>

        SELECT ?kawi ?translit ?terjemahan WHERE {{
            ?entry a :BarisPrasasti ;
                   :memilikiTeksAksara ?aksara ;
                   :memilikiTransliterasi ?translitNode ;
                   :memilikiTerjemahan ?terjemahanNode .

            ?aksara rdf:value ?kawi .
            FILTER (lang(?kawi) = "jv-x-krama" && CONTAINS(str(?kawi), "{input_kawi}"))

            ?translitNode rdf:value ?translit .
            FILTER (lang(?translit) = "jv-Latn")

            ?terjemahanNode rdf:value ?terjemahan .
            FILTER (lang(?terjemahan) = "id")
        }}
    """
    results = query_fuseki(sparql)
    if results:
        st.session_state["selected_items"] = results
    else:
        st.warning("Tidak ditemukan terjemahan untuk aksara tersebut.")

# Terjemahkan dari Latin ke Aksara
elif input_latin:
    sparql = f"""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX : <http://pratisentana.org/ontology#>

        SELECT ?kawi ?translit ?terjemahan WHERE {{
            ?entry a :BarisPrasasti ;
                   :memilikiTeksAksara ?aksara ;
                   :memilikiTransliterasi ?translitNode ;
                   :memilikiTerjemahan ?terjemahanNode .

            ?aksara rdf:value ?kawi .
            FILTER (lang(?kawi) = "jv-x-krama")

            ?translitNode rdf:value ?translit .
            FILTER (lang(?translit) = "jv-Latn")

            ?terjemahanNode rdf:value ?terjemahan .
            FILTER (lang(?terjemahan) = "id" && LCASE(str(?terjemahan)) = LCASE("{input_latin}"))
        }}
    """
    results = query_fuseki(sparql)
    if results:
        st.session_state["selected_items"] = results
    else:
        st.warning("Tidak ditemukan aksara untuk arti tersebut.")
        
if st.button("🔄 Tampilkan Semua Entri"):
    load_all_items()

st.subheader("📋 Hasil Pencarian / Semua Data")

results_display = st.session_state.get("selected_items", [])

if results_display:
    df = pd.DataFrame([
        {
            "Aksara Kawi": r.get("kawi", {}).get("value", "-"),
            "Transliterasi": r.get("translit", {}).get("value", "-"),
            "Terjemahan": r.get("terjemahan", {}).get("value", "-")
        }
        for r in results_display
    ])
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("Tidak ada data yang ditampilkan.")