# 🛡️ Net-Watcher: Local Network Monitoring Tool

Net-Watcher adalah aplikasi berbasis web yang dirancang untuk memantau perangkat yang terhubung ke jaringan lokal secara real-time. Proyek ini menggabungkan teknik **Network Scanning** dengan antarmuka web yang modern.

## 🚀 Fitur Utama
- **ARP Scanning:** Mendeteksi semua perangkat aktif di subnet jaringan menggunakan library Scapy.
- **Vendor Identification:** Mengintegrasikan MAC Vendor API untuk mengidentifikasi merk perangkat (Apple, Samsung, Huawei, dll).
- **Responsive Dashboard:** Tampilan bersih menggunakan Tailwind CSS.
- **Optimization:** Berjalan efisien pada perangkat dengan spesifikasi rendah (Tested on 4GB RAM).

## 🛠️ Tech Stack
- **Backend:** Python 3, Flask
- **Network Library:** Scapy
- **Frontend:** HTML5, Tailwind CSS
- **API:** MacVendors API

## 📋 Prasyarat
Sistem operasi berbasis Linux (Rekomendasi: Linux Mint/Ubuntu/Kali) dengan Python 3 terinstal.

## 🔧 Cara Instalasi
1. Clone repository ini:
   ```bash
   git clone [https://github.com/EbieA295/NetWatcher.git](https://github.com/EbieA295/NetWatcher.git)
   cd NetWatcher