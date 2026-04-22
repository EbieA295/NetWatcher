from flask import Flask, render_template
from scanner import scan_network, scan_ports
from datetime import datetime

app = Flask(__name__)

# Daftar MAC Address perangkat yang kamu kenal
MY_DEVICES = [
    "8e:b3:45:f8:ee:8a", 
    "4c:6f:9c:43:c2:79"
]

# List untuk mencegah log duplikat dalam satu sesi
ALREADY_LOGGED = []

def log_unknown_device(device):
    if device['mac'] not in ALREADY_LOGGED:
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("logs.txt", "a") as f:
            f.write(f"[{waktu}] ALERT: Perangkat Asing! IP: {device['ip']}, MAC: {device['mac']}, Vendor: {device['vendor']}\n")
        ALREADY_LOGGED.append(device['mac'])

@app.route('/')
def index():
    # Sesuaikan segment IP dengan jaringanmu
    target_ip = "192.168.100.142/24" 
    hasil_scan = scan_network(target_ip)
    
    for d in hasil_scan:
        # Menjalankan fungsi port scanner yang baru kita buat
        d['open_ports'] = scan_ports(d['ip'])
        
        # Cek status keamanan
        if d['mac'].lower() in [m.lower() for m in MY_DEVICES]:
            d['status'] = "Known"
        else:
            d['status'] = "Unknown"
            log_unknown_device(d)
            
    return render_template('index.html', devices=hasil_scan)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)