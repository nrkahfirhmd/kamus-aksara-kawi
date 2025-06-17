import pandas as pd

def latin_to_aksara_jawa(text):
    """
    Fungsi utama untuk mengonversi seluruh teks Latin ke Aksara Jawa.
    Fungsi ini memecah teks menjadi kata-kata dan menerjemahkannya satu per satu.
    """
    # Mengonversi input ke string dan membaginya menjadi beberapa kata
    words = str(text).split(' ')
    jawa_words = []
    for word in words:
        jawa_words.append(transliterate_word(word))
    return ' '.join(jawa_words)

def transliterate_word(word):
    """
    Menerjemahkan satu kata Latin ke Aksara Jawa dengan logika yang benar.
    Fungsi ini menangani konsonan, vokal, dan gabungan konsonan (pasangan).
    """
    # Peta karakter Latin ke Aksara Jawa yang lebih lengkap
    aksara_map = {
        # Konsonan Ngalagena
        'h': 'ꦲ', 'n': 'ꦤ', 'c': 'ꦕ', 'r': 'ꦫ', 'k': 'ꦏ', 'd': 'ꦢ', 
        't': 'ꦠ', 's': 'ꦱ', 'w': 'ꦮ', 'l': 'ꦭ', 'p': 'ꦥ', 'dh': 'ꦝ', 
        'j': 'ꦗ', 'y': 'ꦪ', 'ny': 'ꦚ', 'm': 'ꦩ', 'g': 'ꦒ', 'b': 'ꦧ', 
        'th': 'ꦛ', 'ng': 'ꦔ',
        # Vokal Mandiri (Aksara Swara) - untuk awal kata
        'A': 'ꦄ', 'I': 'ꦆ', 'U': 'ꦈ', 'E': 'ꦌ', 'O': 'ꦎ',
        # Tanda Vokal (Sandhangan)
        'a': '',      # Vokal 'a' sudah inheren, tidak perlu tanda
        'i': 'ꦶ',     # wulu
        'u': 'ꦸ',     # suku
        'e': 'ꦺ',     # taling
        'o': 'ꦼ',     # pepet (untuk 'e' pada "segar")
        # Pemati Vokal
        'pangkon': '꧀',
    }
    vowels = ['a', 'i', 'u', 'e', 'o']
    
    word = word.lower()
    jawa_word = ""
    i = 0

    while i < len(word):
        found_consonant = False
        
        # Cek konsonan 2 huruf (ny, ng, dh, th)
        if i + 1 < len(word) and word[i:i+2] in ['ny', 'ng', 'dh', 'th']:
            syllable = word[i:i+2]
            i += 2
            found_consonant = True
        # Cek konsonan 1 huruf
        elif word[i] not in vowels and word[i] in aksara_map:
            syllable = word[i]
            i += 1
            found_consonant = True
        
        # Jika ditemukan konsonan
        if found_consonant:
            # Cek karakter selanjutnya, apakah vokal atau bukan
            if i < len(word) and word[i] in vowels:
                vowel = word[i]
                # Tambah aksara dasar + sandhangan vokalnya
                jawa_word += aksara_map[syllable] + aksara_map[vowel]
                i += 1
            else:
                # Jika diikuti konsonan lain atau akhir kata, gunakan pangkon
                jawa_word += aksara_map[syllable] + aksara_map['pangkon']
        
        # Jika karakter adalah vokal di awal kata
        elif word[i] in vowels:
            # Gunakan Aksara Swara jika di awal kata
            if len(jawa_word) == 0:
                jawa_word += aksara_map[word[i].upper()]
            else:
                # Ini kasus vokal setelah vokal, untuk saat ini dibiarkan
                jawa_word += aksara_map[word[i].upper()]
            i += 1
        # Karakter tidak dikenal
        else:
            jawa_word += word[i]
            i += 1
            
    # Membersihkan pangkon di akhir kata jika tidak diperlukan
    if jawa_word.endswith(aksara_map['pangkon']):
        # Logika ini bisa lebih kompleks tergantung aturan, 
        # tapi untuk transliterasi umum, pangkon di akhir kata biasanya benar.
        pass
        
    return jawa_word


# --- MAIN SCRIPT ---
# Ganti dengan path file CSV asli Anda jika berbeda
# Untuk contoh ini, kita membaca file yang sudah ada 'transliterasi'-nya
input_path = "Prasasti_Pratistentana1_aksara_terisi.csv"
try:
    df = pd.read_csv(input_path, delimiter=";")
    
    # Terapkan fungsi konversi yang sudah diperbaiki
    df["teks_aksara_fixed"] = df["transliterasi"].apply(latin_to_aksara_jawa)
    
    # Tentukan path file output
    output_path = "Prasasti_Pratistentana1_aksara_terisi_FIXED.csv"
    
    # Hapus kolom yang tidak diperlukan jika ada (misal kolom kosong 'Unnamed')
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    # Simpan ke file CSV baru
    df.to_csv(output_path, index=False, sep=";")
    
    print(f"Konversi berhasil! File baru disimpan di: {output_path}")
    print("\nContoh hasil:")
    print(df[['transliterasi', 'teks_aksara_fixed']].head())

except FileNotFoundError:
    print(f"Error: File tidak ditemukan di path '{input_path}'. Mohon periksa kembali nama dan lokasi file.")
except Exception as e:
    print(f"Terjadi error: {e}")

