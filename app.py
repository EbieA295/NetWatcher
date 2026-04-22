from flask import Flask, render_template
from scanner import scan_network, scan_ports
from datetime import datetime
import requests # Pastikan sudah install: pip install requests

app = Flask(__name__)

# === KONFIGURASI TELEGRAM ===
TOKEN = "8264579816:AAEueazwYNlD6AlR1zbRbWRMhbdhoB0tndA"
CHAT_ID = "7569339743"

# Daftar MAC Address yang dikenal
MY_DEVICES = [
    "8e:b3:45:f8:ee:8a", 
    "4c:6f:9c:43:c2:79"
]

ALREADY_LOGGED = []

def send_telegram_alert(device):
    """Mengirim pesan notifikasi ke HP lewat Telegram"""
    waktu = datetime.now().strftime('%H:%M:%S')
    # Format pesan menggunakan Markdown agar terlihat rapi
    pesan = (
        f"🚨 *PENYUSUP TERDETEKSI!*\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🌐 *IP:* `{device['ip']}`\n"
        f"🆔 *MAC:* `{device['mac']}`\n"
        f"🏢 *Vendor:* {device['vendor']}\n"
        f"🔌 *Port:* {device['open_ports']}\n"
        f"⏰ *Jam:* {waktu}\n"
        f"━━━━━━━━━━━━━━━"
    )
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": pesan,
        "parse_mode": "Markdown"
    }
    
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Gagal kirim Telegram: {e}")

def log_unknown_device(device):
    if device['mac'] not in ALREADY_LOGGED:
        # 1. Simpan ke file logs.txt
        waktu_log = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("logs.txt", "a") as f:
            f.write(f"[{waktu_log}] ALERT: {device['ip']} - {device['mac']}\n")
        
        # 2. Tembak notifikasi ke HP
        send_telegram_alert(device)
        
        # 3. Tandai agar tidak spam
        ALREADY_LOGGED.append(device['mac'])

@app.route('/')
def index():
    target_ip = "192.168.100.1/24" 
    hasil_scan = scan_network(target_ip)
    
    for d in hasil_scan:
        d['open_ports'] = scan_ports(d['ip'])
        
        if d['mac'].lower() in [m.lower() for m in MY_DEVICES]:
            d['status'] = "Known"
        else:
            d['status'] = "Unknown"
            log_unknown_device(d)
            
    return render_template('index.html', devices=hasil_scan)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)