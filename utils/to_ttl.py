import csv
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD

# Namespace
BASE = Namespace("http://pratisentana.org/ontology#")
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
LEXINFO = Namespace("http://www.lexinfo.net/ontology/2.0/lexinfo#")
DCTERMS = Namespace("http://purl.org/dc/terms/")

g = Graph()
g.bind("", BASE)
g.bind("rdf", RDF)
g.bind("rdfs", RDFS)
g.bind("xsd", XSD)
g.bind("lexinfo", LEXINFO)
g.bind("dcterms", DCTERMS)

with open("Prasasti_Pratistentana1_aksara_terisi.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    print("Kolom terdeteksi:", reader.fieldnames)  # <--- Debug line

    for row in reader:
        baris_id = row["baris_id"].strip()

        # Aksara asli
        aksara_uri = BASE[f"aksara_{baris_id}"]
        g.add((aksara_uri, RDF.type, BASE.TeksAksara))
        g.add((aksara_uri, RDF.value, Literal(row["teks_aksara"], lang="jv-x-krama")))
        g.add((aksara_uri, LEXINFO.script, BASE.AksaraKawi))
        g.add((aksara_uri, BASE.jumlahKarakter, Literal(len(row["teks_aksara"]), datatype=XSD.integer)))

        # Transliteration
        translit_uri = BASE[f"translit_{baris_id}"]
        g.add((translit_uri, RDF.type, BASE.Transliterasi))
        g.add((translit_uri, RDF.value, Literal(row["transliterasi"], lang="jv-Latn")))
        g.add((translit_uri, BASE.menggunakanAturan, Literal("Aturan Transliterasi Kawi-Latin 2020")))

        # Terjemahan
        terjemah_uri = BASE[f"terjemah_{baris_id}"]
        g.add((terjemah_uri, RDF.type, BASE.Terjemahan))
        g.add((terjemah_uri, RDF.value, Literal(row["terjemahan"], lang="id")))
        g.add((terjemah_uri, BASE.keBahasa, Literal("id")))
        g.add((terjemah_uri, BASE.dariBahasa, Literal("jv")))

# Simpan RDF
g.serialize(destination="pratisentana1.ttl", format="turtle")
print("RDF instance berhasil dibuat untuk aksara, transliterasi, dan terjemahan.")