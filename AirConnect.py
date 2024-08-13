import pywifi
from pywifi import const
from time import sleep
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich import box
from art import text2art
import sys

console = Console()

def display_ascii_art():
    app_name = "AirConnect"
    ascii_art = text2art(app_name)
    console.print(f"[bold cyan]{ascii_art}[/bold cyan]")
    console.print("[bold yellow]Find us on GitHub:[/bold yellow] [link=https://github.com/c4nng/AirConnect]Air-Connect on GitHub[/link]")

def scan_wifi():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()
    sleep(2)  # Tarama için biraz zaman tanıyalım
    
    scan_results = iface.scan_results()
    wifi_list = []

    for network in scan_results:
        wifi_list.append({
            "ssid": network.ssid,
            "signal": network.signal,
            "bssid": network.bssid,
            "frequency": network.freq
        })

    return wifi_list

def display_wifi_networks(wifi_networks):
    table = Table(title="Available WiFi Networks", box=box.ROUNDED)
    console.print("")
    table.add_column("Index", style="cyan bold", no_wrap=True)
    table.add_column("SSID", style="cyan bold", no_wrap=True)
    table.add_column("Signal (dBm)", style="magenta bold")
    table.add_column("BSSID", style="green bold")
    table.add_column("Frequency (MHz)", style="yellow bold")

    for idx, network in enumerate(wifi_networks, start=1):
        table.add_row(
            str(idx),
            network['ssid'] or "[Not Broadcasting]",
            str(network['signal']),
            network['bssid'],
            str(network['frequency'])
        )
    
    console.print(table)

def connect_wifi(ssid, password):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    
    iface.disconnect()
    sleep(1)
    
    if iface.status() == const.IFACE_DISCONNECTED:
        profile = pywifi.Profile()
        profile.ssid = ssid
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        profile.cipher = const.CIPHER_TYPE_CCMP
        profile.key = password
        
        iface.remove_all_network_profiles()
        tmp_profile = iface.add_network_profile(profile)
        
        iface.connect(tmp_profile)
        sleep(10)  # Bağlantının gerçekleşmesi için bekleme süresi
        
        if iface.status() == const.IFACE_CONNECTED:
            console.print(f"[bold green]Successfully connected to {ssid}![/bold green]")
            return True
        else:
            console.print(f"[bold red]Failed to connect to {ssid}. Check your password and try again.[/bold red]")
            return False
    else:
        console.print("[bold red]Could not disconnect from current network. Please try again.[/bold red]")
        return False

def get_valid_index(wifi_networks):
    while True:
        user_input = Prompt.ask("[cyan]Select the index of the WiFi network you want to connect to (or press 'q' to quit)[/cyan]").strip()
        
        if user_input.lower() == 'q':
            console.print("[bold red]Exiting program...[/bold red]")
            sys.exit()  # Programı sonlandır
        
        try:
            selected_index = int(user_input)
            if 1 <= selected_index <= len(wifi_networks):
                return selected_index - 1  # 0 tabanlı index
            else:
                console.print(f"[bold red]Index out of range. Please select a number between 1 and {len(wifi_networks)}.[/bold red]")
        except ValueError:
            console.print("[bold red]Invalid input. Please enter a valid number or 'q' to quit.[/bold red]")

def get_valid_password(ssid):
    while True:
        password = Prompt.ask(f"[cyan]Enter the password for {ssid}[/cyan]", password=True)
        if password:
            return password
        else:
            console.print("[bold red]Password cannot be empty. Please enter a valid password.[/bold red]")

def main():
    display_ascii_art()

    while True:
        # WiFi ağlarını tarayalım ve tablo olarak gösterelim
        wifi_networks = scan_wifi()
        display_wifi_networks(wifi_networks)

        # Kullanıcıdan geçerli bir indeks seçmesini isteyelim
        selected_index = get_valid_index(wifi_networks)

        # Seçilen ağın SSID'sini alalım ve geçerli bir şifre isteyelim
        selected_ssid = wifi_networks[selected_index]['ssid']
        password = get_valid_password(selected_ssid)

        # Seçilen ağa bağlanalım
        connect_wifi(selected_ssid, password)
        
        # Yeniden tarama yapmak isteyip istemediğini soralım
        if Prompt.ask("[cyan]Do you want to scan again? (y/n)[/cyan]").strip().lower() != 'y':
            console.print("[bold red]Exiting program...[/bold red]")
            break

if __name__ == "__main__":
    main()
