from flask import Flask, render_template
from scanner import scan_network
from datetime import datetime # Import untuk mencatat waktu

app = Flask(__name__)

MY_DEVICES = [
    "8e:b3:45:f8:ee:8a", 
    "4c:6f:9c:43:c2:79"
]

# Tambahkan list kosong di bagian atas (di bawah MY_DEVICES)
ALREADY_LOGGED = []

def log_unknown_device(device):
    # Cek apakah MAC ini sudah pernah dicatat sebelumnya
    if device['mac'] not in ALREADY_LOGGED:
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("logs.txt", "a") as f:
            f.write(f"[{waktu}] ALERT: Perangkat Asing! IP: {device['ip']}, MAC: {device['mac']}, Vendor: {device['vendor']}\n")
        
        # Masukkan ke daftar yang sudah dicatat agar tidak double
        ALREADY_LOGGED.append(device['mac'])

@app.route('/')
def index():
    target_ip = "192.168.100.1/24" 
    hasil_scan = scan_network(target_ip)
    
    for d in hasil_scan:
        if d['mac'].lower() in [m.lower() for m in MY_DEVICES]:
            d['status'] = "Known"
        else:
            d['status'] = "Unknown"
            # Catat ke log jika asing
            log_unknown_device(d)
            
    return render_template('index.html', devices=hasil_scan)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)