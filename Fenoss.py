import os
import re
import json
import requests
import socket
import time
from datetime import datetime

# ==================== KONFIGURASI ====================
CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"BOT_TOKEN": "", "CHAT_ID": ""}

def save_config(token, chat_id):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"BOT_TOKEN": token, "CHAT_ID": chat_id}, f)

config = load_config()
BOT_TOKEN = config.get("BOT_TOKEN", "")
CHAT_ID = config.get("CHAT_ID", "")

# Warna ANSI
R = "\033[1;31m"
G = "\033[1;32m"
Y = "\033[1;33m"
B = "\033[1;34m"
C = "\033[1;36m"
W = "\033[0m"

TARGET_WA_FILE = "target_wa.txt"
TARGET_IP_FILE = "target_ip.txt"
HASIL_FILE = "hasil_ip.txt"

def banner():
    os.system("clear")
    print(f"""{C}
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠁  ⠈⠉⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟         ⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡟            ⠈⢻⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡟     ⢀⣠⣤⣤⣤⣤⣄   ⠹⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⠁    ⠾⣿⣿⣿⣿⠿⠛⠉    ⠘⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡏   ⣤⣶⣤⣉⣿⣿⡯⣀⣴⣿⡗    ⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡇   ⡈  ⠉⣿⣿⣶⡉  ⣀⡀   ⢻⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡇  ⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇   ⢸⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿   ⠉⢉⣽⣿⠿⣿⡿⢻⣯⡍⢁⠄   ⣸⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡄  ⠐⡀⢉⠉ ⠠ ⢉⣉ ⡜    ⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⠿⠁   ⠘⣤⣭⣟⠛⠛⣉⣁⡜     ⠛⠿⣿⣿⣿
⡿⠟⠛⠉⠉       ⠈⢻⣿⡀ ⣿⠏         ⠈⠉
              ⠉⠁ ⠁       
W E L C O M E
TRACK IP BY 
FENOSS SILENCE
=============================================
  📍{Y}TOOLS IP TRACK V2 - BY FENOSS SILENCE{C}
=============================================

{G}[1]{B} Set Token & ID Telegram
{G}[2]{B} Cek IP manual
{G}[3]{B} Cek IP dari file list
{G}[4]{B} Auto-scan dari log server
{G}[5]{B} Lihat hasil sebelumnya
{G}[6]{B} Tambah nomor WhatsApp target
{G}[7]{B} Scan log untuk nomor WA (lacak lokasi)
{G}[8]{B} Track manual (Nomor + IP)
{G}[9]{B} Live Track IP (auto kirim ke Telegram)
{G}[10]{B} Cek IP dari Domain
{G}[11]{B} Export hasil ke JSON
{G}[12]{B} Generate Google Maps Link
{G}[13]{B} Keluar

============================================={W}

 {G}"FENOSS DATANG UNTUK MELINDUNGI YANG LEMAH"
""")

# ==================== TELEGRAM ====================
def set_token():
    global BOT_TOKEN, CHAT_ID
    print(f"{Y}⚙️ KONFIGURASI TELEGRAM{W}")
    token = input(f"{C}Masukkan BOT_TOKEN:{W} ").strip()
    chat_id = input(f"{C}Masukkan CHAT_ID:{W} ").strip()
    if token and chat_id:
        save_config(token, chat_id)
        config = load_config()
        BOT_TOKEN = config.get("BOT_TOKEN", "")
        CHAT_ID = config.get("CHAT_ID", "")
        print(f"{G}✅ Token & ID berhasil disimpan!{W}")
        kirim_telegram("✅ IP Tracker V2 Aktif! Bot siap menerima data.")
    else:
        print(f"{R}⚠️ Token dan ID tidak boleh kosong!{W}")

def kirim_telegram(pesan):
    if not BOT_TOKEN or not CHAT_ID:
        print(f"{R}⚠️ Token atau Chat ID belum diset!{W}")
        return False
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": pesan, "parse_mode": "HTML"}
        r = requests.post(url, data=data, timeout=10)
        if r.status_code == 200:
            print(f"{G}✅ Notifikasi terkirim ke Telegram!{W}")
            return True
        else:
            print(f"{R}⚠️ Gagal kirim: {r.text}{W}")
            return False
    except Exception as e:
        print(f"{R}⚠️ Error: {e}{W}")
        return False

# ==================== CEK IP ====================
def cek_ip(ip, send_telegram=False):
    url = f"http://ip-api.com/json/{ip}"
    try:
        r = requests.get(url, timeout=10).json()
    except:
        print(f"{R}⚠️ Tidak bisa menghubungi API!{W}")
        return None

    if r.get("status") == "success":
        hasil = (
            f"{B}🌐 IP:{W} {r['query']}\n"
            f"{G}🏳 Negara:{W} {r.get('country','-')}\n"
            f"{G}🏙 Wilayah:{W} {r.get('regionName','-')}\n"
            f"{G}🏠 Kota:{W} {r.get('city','-')}\n"
            f"{C}📡 ISP:{W} {r.get('isp','-')}\n"
            f"{C}🔧 Organisasi:{W} {r.get('org','-')}\n"
            f"{C}🔢 ASN:{W} {r.get('as','-')}\n"
            f"{Y}📍 Koordinat:{W} {r.get('lat','-')},{r.get('lon','-')}\n"
            f"{Y}🗺 Maps:{W} https://www.google.com/maps?q={r.get('lat','-')},{r.get('lon','-')}\n"
            "---------------------------"
        )
        print(hasil)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(HASIL_FILE, "a") as f:
            f.write(f"[{timestamp}]\n{hasil}\n\n")
        
        if send_telegram:
            pesan_tg = f"<b>📍 IP Terdeteksi!</b>\n{hasil.replace(chr(27), '')}"
            kirim_telegram(pesan_tg)
        
        return hasil
    else:
        print(f"{R}❌ Gagal cek IP {ip}: {r.get('message','')}{W}")
        return None

def cek_domain():
    domain = input(f"{C}Masukkan domain (contoh: google.com):{W} ").strip()
    try:
        ip = socket.gethostbyname(domain)
        print(f"{G}🔍 Domain {domain} → IP: {ip}{W}")
        return cek_ip(ip)
    except:
        print(f"{R}❌ Gagal resolve domain {domain}{W}")
        return None

def live_track_ip():
    print(f"{Y}📡 Mode Live Tracking (Ctrl+C untuk berhenti){W}")
    if not BOT_TOKEN or not CHAT_ID:
        print(f"{R}⚠️ Set Token & ID Telegram dulu (menu 1)!{W}")
        return
    try:
        while True:
            ip = input(f"{C}Masukkan IP target (atau 'exit'):{W} ").strip()
            if ip.lower() == 'exit':
                break
            hasil = cek_ip(ip, send_telegram=True)
            if hasil:
                print(f"{G}✅ Hasil sudah dikirim ke Telegram{W}")
    except KeyboardInterrupt:
        print(f"\n{Y}⏹️ Live tracking dihentikan{W}")

def auto_scan_log(logfile):
    if not os.path.exists(logfile):
        print(f"{R}⚠️ File log tidak ditemukan.{W}")
        return
    with open(logfile, "r") as f:
        data = f.read()
    ips = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', data)
    unik = sorted(set(ips))
    if not unik:
        print(f"{R}⚠️ Tidak ada IP ditemukan di log.{W}")
        return
    print(f"{Y}📊 Ditemukan {len(unik)} IP unik. Mulai cek...{W}")
    for ip in unik:
        cek_ip(ip)

def scan_log_kirim_telegram():
    if not BOT_TOKEN or not CHAT_ID:
        print(f"{R}⚠️ Set Token & ID Telegram dulu!{W}")
        return
    logfile = input(f"{C}Nama file log (ex: access.log):{W} ").strip()
    if not os.path.exists(logfile):
        print(f"{R}⚠️ File tidak ditemukan.{W}")
        return
    with open(logfile, "r") as f:
        data = f.read()
    ips = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', data)
    unik = sorted(set(ips))
    if not unik:
        print(f"{R}⚠️ Tidak ada IP.{W}")
        return
    print(f"{Y}📊 Ditemukan {len(unik)} IP, mengirim ke Telegram...{W}")
    for ip in unik:
        hasil = cek_ip(ip)
        if hasil:
            kirim_telegram(f"<b>📡 IP dari log:</b>\n{hasil.replace(chr(27), '')}")
            time.sleep(1)
    print(f"{G}✅ Selesai mengirim semua IP{W}")

def tambah_target_wa():
    nomor = input(f"{C}Masukkan nomor WhatsApp target (format: 628xxxx):{W} ")
    if not nomor.startswith("62"):
        print(f"{R}⚠️ Gunakan format internasional, contoh: 6281234567890{W}")
        return
    with open(TARGET_WA_FILE, "a") as f:
        f.write(nomor + "\n")
    print(f"{G}✅ Nomor berhasil ditambahkan!{W}")
    kirim_telegram(f"📢 <b>Nomor WA Target Baru:</b> {nomor}")

def scan_log_nomor_wa():
    if not os.path.exists(TARGET_WA_FILE):
        print(f"{R}⚠️ Belum ada nomor target. Tambahkan dulu dengan menu 6.{W}")
        return
    log = input(f"{C}Masukkan nama file log server (ex: access.log):{W} ")
    if not os.path.exists(log):
        print(f"{R}⚠️ File log tidak ditemukan.{W}")
        return

    with open(log, "r") as f:
        data = f.read()

    with open(TARGET_WA_FILE, "r") as f:
        targets = [t.strip() for t in f.readlines() if t.strip()]

    ditemukan = False
    for nomor in targets:
        if nomor in data:
            print(f"{G}✅ Nomor ditemukan di log: {nomor}{W}")
            baris = [line for line in data.splitlines() if nomor in line]
            for line in baris:
                ip_match = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', line)
                if ip_match:
                    ip = ip_match.group()
                    print(f"{Y}🔎 Lacak lokasi IP: {ip}{W}")
                    hasil = cek_ip(ip)
                    if hasil:
                        kirim_telegram(f"📍 <b>Nomor WA {nomor} ditemukan!</b>\n{hasil.replace(chr(27), '')}")
            ditemukan = True

    if not ditemukan:
        print(f"{R}⚠️ Tidak ada nomor target ditemukan di log.{W}")

def track_manual():
    nomor = input(f"{C}Masukkan nomor WhatsApp:{W} ")
    ip = input(f"{C}Masukkan IP target:{W} ")
    hasil = cek_ip(ip)
    if hasil:
        pesan = f"📱 <b>Track Manual</b>\nNomor: {nomor}\n{hasil.replace(chr(27), '')}"
        kirim_telegram(pesan)
        print(f"{G}✅ Data manual berhasil dikirim!{W}")

def export_json():
    if not os.path.exists(HASIL_FILE):
        print(f"{R}⚠️ Belum ada hasil.{W}")
        return
    data_export = []
    with open(HASIL_FILE, "r") as f:
        content = f.read()
    blocks = content.split("---------------------------")
    for block in blocks:
        if block.strip():
            data_export.append({"raw": block.strip()})
    with open("hasil_export.json", "w") as f:
        json.dump(data_export, f, indent=2)
    print(f"{G}✅ Export ke hasil_export.json berhasil!{W}")

def gen_maps_link():
    lat = input(f"{C}Latitude:{W} ")
    lon = input(f"{C}Longitude:{W} ")
    if lat and lon:
        link = f"https://www.google.com/maps?q={lat},{lon}"
        print(f"{G}🗺 Google Maps: {link}{W}")
        with open(HASIL_FILE, "a") as f:
            f.write(f"[Manual Maps] {link}\n")
    else:
        print(f"{R}⚠️ Koordinat tidak valid{W}")

def lihat_hasil():
    if os.path.exists(HASIL_FILE):
        with open(HASIL_FILE, "r") as f:
            print(f.read())
    else:
        print(f"{R}⚠️ Belum ada hasil disimpan.{W}")

def cek_ip_dari_file():
    file = input(f"{C}Masukkan nama file list IP:{W} ")
    if os.path.exists(file):
        with open(file, "r") as f:
            for ip in f:
                if ip.strip():
                    cek_ip(ip.strip())
    else:
        print(f"{R}⚠️ File tidak ditemukan.{W}")

# ==================== MENU UTAMA ====================
def menu():
    while True:
        banner()
        pilihan = input(f"{C}Pilih menu:{W} ").strip()

        if pilihan == "1":
            set_token()
            input(f"\n{Y}Enter untuk kembali ke menu...{W}")
        elif pilihan == "2":
            ip = input(f"{C}Masukkan IP:{W} ")
            cek_ip(ip)
            input(f"\n{Y}Enter untuk kembali ke menu...{W}")
        elif pilihan == "3":
            cek_ip_dari_file()
            input(f"\n{Y}Enter untuk kembali ke menu...{W}")
        elif pilihan == "4":
            log = input(f"{C}Masukkan nama file log server (ex: access.log):{W} ")
            auto_scan_log(log)
            input(f"\n{Y}Enter untuk kembali ke menu...{W}")
        elif pilihan == "5":
            lihat_hasil()
            input(f"\n{Y}Enter untuk kembali ke menu...{W}")
        elif pilihan == "6":
            tambah_target_wa()
            input(f"\n{Y}Enter untuk kembali ke menu...{W}")
        elif pilihan == "7":
            scan_log_nomor_wa()
            input(f"\n{Y}Enter untuk kembali ke menu...{W}")
        elif pilihan == "8":
            track_manual()
            input(f"\n{Y}Enter untuk kembali ke menu...{W}")
        elif pilihan == "9":
            live_track_ip()
            input(f"\n{Y}Enter untuk kembali ke menu...{W}")
        elif pilihan == "10":
            cek_domain()
            input(f"\n{Y}Enter untuk kembali ke menu...{W}")
        elif pilihan == "11":
            export_json()
            input(f"\n{Y}Enter untuk kembali ke menu...{W}")
        elif pilihan == "12":
            gen_maps_link()
            input(f"\n{Y}Enter untuk kembali ke menu...{W}")
        elif pilihan == "13":
            print(f"{G}👋 Keluar dari program...{W}")
            break
        else:
            print(f"{R}⚠️ Pilihan tidak ada!{W}")
            input(f"\n{Y}Enter untuk kembali...{W}")

if __name__ == "__main__":
    menu()
