import csv

prefixes = """@prefix : <http://pratisentana.org/ontology#> .
@prefix lexinfo: <http://www.lexinfo.net/ontology/2.0/lexinfo#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
"""

def make_ttl_entry(row):
    baris_id = row['baris_id']
    aksara = row['teks_aksara']
    translit = row['transliterasi']
    terjemah = row['terjemahan']

    ttl = []

    # Teks Aksara
    ttl.append(f":aksara_{baris_id} a :TeksAksara ; :jumlahKarakter {len(aksara)} ; "
                f"lexinfo:script :AksaraKawi ; rdf:value \"{aksara}\"@jv-x-krama .")

    # Transliterasi
    ttl.append(f":translit_{baris_id} a :Transliterasi ; :menggunakanAturan \"Aturan Transliterasi Kawi-Latin 2020\" ; "
                f"rdf:value \"{translit}\"@jv-Latn .")

    # Terjemahan
    ttl.append(f":terjemah_{baris_id} a :Terjemahan ; :dariBahasa \"jv\" ; :keBahasa \"id\" ; "
                f"rdf:value \"{terjemah}\"@id .")

    # Entry Prasasti
    ttl.append(f":entry_{baris_id} a :BarisPrasasti ; :memilikiTeksAksara :aksara_{baris_id} ; "
                f":memilikiTransliterasi :translit_{baris_id} ; :memilikiTerjemahan :terjemah_{baris_id} .")

    return "\n".join(ttl)

def convert_csv_to_ttl(csv_path, output_path):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        entries = [make_ttl_entry(row) for row in reader]

    with open(output_path, 'w', encoding='utf-8') as ttlfile:
        ttlfile.write(prefixes + "\n\n")
        ttlfile.write("\n\n".join(entries))

# Contoh penggunaan
convert_csv_to_ttl('../data/Prasasti_Pratistentana1_aksara_terisi_FIXED.csv', '../data/pratisentana1.ttl')