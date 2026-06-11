#!/usr/bin/env python3
"""
Modulo per la scansione della rete e selezione degli host SSH
"""
import socket
import ipaddress
from colorama import Fore

# Colori
GREEN = Fore.GREEN
RED = Fore.RED
RESET = Fore.RESET
BLUE = Fore.BLUE

def scan_network(network_cidr="192.168.122.0/24"):
    """
    Scansiona la rete locale per trovare host con porta 22 aperta
    Restituisce una lista di IP che rispondono sulla porta 22
    """
    ssh_hosts = []
    
    print(f"{BLUE}[*] Scansione della rete {network_cidr} per host SSH...{RESET}")
    print(f"{BLUE}[*] Attendere... la scansione richiede circa 30 secondi{RESET}")
    print("-" * 50)
    
    # Genera tutti gli IP della rete
    network = ipaddress.ip_network(network_cidr, strict=False)
    total_ips = len(list(network.hosts()))
    scanned = 0
    
    for ip in network.hosts():
        ip_str = str(ip)
        scanned += 1
        
        # Mostra progresso ogni 10 IP
        if scanned % 10 == 0:
            print(f"{BLUE}[*] Progresso: {scanned}/{total_ips} IP{RESET}", end="\r")
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((ip_str, 22))
        sock.close()
        
        if result == 0:
            print(f"\n{GREEN}[+] Trovato host SSH: {ip_str}{RESET}")
            ssh_hosts.append(ip_str)
    
    print(f"\n{BLUE}[*] Scansione completata! Trovati {len(ssh_hosts)} host con SSH{RESET}")
    print("-" * 50)
    return ssh_hosts

def select_target(hosts):
    """
    Mostra la lista degli host e permette all'utente di scegliere
    Restituisce l'IP selezionato
    """
    if not hosts:
        print(f"{RED}[-] Nessun host con SSH trovato nella rete.{RESET}")
        return None
    
    print(f"\n{BLUE}Host trovati con porta SSH aperta:{RESET}")
    print("-" * 50)
    
    for i, host in enumerate(hosts, 1):
        print(f"  {GREEN}{i}.{RESET} {host}")
    
    print("-" * 50)
    print(f"{BLUE}0. Esci{RESET}")
    print("-" * 50)
    
    while True:
        try:
            choice = int(input(f"\n{BLUE}[?] Scegli l'host da attaccare (numero): {RESET}"))
            if choice == 0:
                return None
            if 1 <= choice <= len(hosts):
                return hosts[choice - 1]
            else:
                print(f"{RED}[-] Scelta non valida. Inserisci un numero tra 1 e {len(hosts)}{RESET}")
        except ValueError:
            print(f"{RED}[-] Inserisci un numero valido.{RESET}")

def get_target_interactive(network_cidr="192.168.122.0/24"):
    """
    Funzione principale che esegue la scansione e restituisce l'host selezionato
    """
    hosts = scan_network(network_cidr)
    target = select_target(hosts)
    return target