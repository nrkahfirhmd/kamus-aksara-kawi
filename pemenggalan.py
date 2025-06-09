import pandas as pd

# Pemetaan sederhana Latin ke aksara Jawa Unicode (pendekatan Kawi)
aksara_jawa_map = {
    "nya": "ꦚ", "nga": "ꦔ",
    "ka": "ꦏ", "ga": "ꦒ",
    "ca": "ꦕ", "ja": "ꦗ",
    "ta": "ꦠ", "da": "ꦢ", "na": "ꦤ",
    "pa": "ꦥ", "ba": "ꦧ", "ma": "ꦩ",
    "ya": "ꦪ", "ra": "ꦫ", "la": "ꦭ", "wa": "ꦮ",
    "sa": "ꦱ", "ha": "ꦲ",
    "a": "ꦄ", "i": "ꦆ", "u": "ꦈ", "e": "ꦌ", "o": "ꦎ"
}

# Fungsi konversi transliterasi Latin ke aksara Jawa Unicode
def latin_to_aksara_jawa(translit):
    result = []
    translit = str(translit).lower()
    words = translit.split()
    for word in words:
        aksara_word = ""
        i = 0
        while i < len(word):
            # Cek 3 huruf dulu
            if i + 2 < len(word) and word[i:i+3] in aksara_jawa_map:
                aksara_word += aksara_jawa_map[word[i:i+3]]
                i += 3
            # Cek 2 huruf
            elif i + 1 < len(word) and word[i:i+2] in aksara_jawa_map:
                aksara_word += aksara_jawa_map[word[i:i+2]]
                i += 2
            # Cek 1 huruf
            elif word[i] in aksara_jawa_map:
                aksara_word += aksara_jawa_map[word[i]]
                i += 1
            else:
                aksara_word += word[i]  # fallback: karakter apa adanya
                i += 1
        result.append(aksara_word)
    return " ".join(result)

# Baca file CSV asli
input_path = "Prasasti Pratisentana 1.csv"
df = pd.read_csv(input_path, delimiter=";")

# Terapkan konversi ke seluruh baris
df["teks_aksara"] = df["transliterasi"].apply(latin_to_aksara_jawa)

# Simpan ke file baru
output_path = "Prasasti_Pratistentana1_aksara_terisi.csv"
df.to_csv(output_path, index=False, sep=";")

print(f"File berhasil disimpan ke: {output_path}")