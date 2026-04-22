from flask import Flask, render_template
from scanner import scan_network

app = Flask(__name__)

@app.route('/')
def index():
    # Cek IP laptopmu, biasanya 192.168.1.1/24 atau 192.168.100.1/24
    # Ganti string di bawah ini sesuai segment Wi-Fi kamu
    target_ip = "192.168.100.142/24" 
    
    hasil_scan = scan_network(target_ip)
    return render_template('index.html', devices=hasil_scan)

if __name__ == '__main__':
    # Menjalankan server Flask
    app.run(debug=True, host='0.0.0.0', port=5000)