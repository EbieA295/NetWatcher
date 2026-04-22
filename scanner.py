from scapy.all import ARP, Ether, srp
import requests

def get_vendor(mac_address):
    try:
        # Menggunakan API gratis untuk cek merk berdasarkan MAC
        url = f"https://api.macvendors.com/{mac_address}"
        response = requests.get(url, timeout=1) # Timeout 1 detik agar tidak lambat
        if response.status_code == 200:
            return response.text
        return "Unknown"
    except:
        return "N/A"

def scan_network(ip_range):
    arp_request = ARP(pdst=ip_range)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    combined_packet = broadcast / arp_request
    # timeout dinaikkan ke 4 atau 5, dan kita tambahkan retry
    answered_list = srp(combined_packet, timeout=4, retry=1, verbose=False)[0]
    
    devices = []
    for element in answered_list:
        mac = element[1].hwsrc
        # Panggil fungsi vendor
        vendor_name = get_vendor(mac)
        
        devices.append({
            "ip": element[1].psrc, 
            "mac": mac,
            "vendor": vendor_name
        })
    
    return devices