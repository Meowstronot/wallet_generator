import pandas as pd
from eth_account import Account
from mnemonic import Mnemonic
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from colorama import Fore, Style
import os, secrets


class eth_wallet_generator:
    def __init__(self):
        self.name_file = "eth_wallet"  # Default filename for exporting wallets
        
    def logger(self, header:str, header_color, message: str, end="\n"):
        print(f"{header_color}[{header.center(8)}]{Style.RESET_ALL} | {message}", end=end)


    def create_eth_wallet(self):

        random_bytes1 = secrets.token_bytes(32)
        random_bytes2 = os.urandom(32)
        combined_entropy = random_bytes1 + random_bytes2

        mnemo = Mnemonic("english")
        seed = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=combined_entropy,  # Entropy gabungan digunakan sebagai salt
            iterations=100000
        ).derive(b"Secure Seed Phrase")  # Teks bisa diganti sesuai kebutuhan
        seed_phrase = mnemo.to_mnemonic(seed)
        
        Account.enable_unaudited_hdwallet_features()
        account = Account.from_mnemonic(seed_phrase)
        private_key = "0x"+account.key.hex()
        address = account.address

        return address, private_key, seed_phrase

    def generate_batch_eth_wallets(self, num_wallets:int=10)-> list:
        """
        Generate a batch of Ethereum wallets.

        Args:
            num_wallets (int, optional): The number of wallets to generate. Defaults to 10.

        Returns:
            list: A list of dictionaries containing wallet information.
        Each dictionary contains:
                - address: The Ethereum address of the wallet.
                - private_key: The private key of the wallet.
                - seed_phrase_24: The 24-word seed phrase for the wallet.
        """
        wallets = []
        self.logger("Status", header_color=Fore.CYAN + Style.BRIGHT, 
                    message=f"Generating {num_wallets} Ethereum wallets...")
        for i in range(num_wallets):
            address, private_key, seed_phrase = self.create_eth_wallet()
            wallets.append({
                            "address": address,
                            "private_key": private_key,
                            "seed_phrase_24": seed_phrase
                            })
            self.logger(header=f"{i+1}/{num_wallets}", header_color=Fore.BLUE + Style.BRIGHT, 
                        message=f"Wallet {i+1} created: Address {address[:6]}***{address[-6:]}", end="\r")
        print("")
        self.logger("Status", header_color=Fore.CYAN + Style.BRIGHT,
                    message=f"Successfully generated {num_wallets} Ethereum wallets.")
        
        return wallets

    def export_wallets_to_csv(self, wallets: list, filename: str =None):

        if not os.path.exists("results"):
            self.logger("Status", header_color=Fore.CYAN + Style.BRIGHT,
                        message=f"Creating results folder...")
            os.makedirs("results")

        if filename is None:
            filename = self.name_file
        filepath = os.path.join(os.getcwd(), f"results/{filename}.csv")

        df = pd.DataFrame(wallets)
        df.to_csv(filepath, index=False)
        self.logger("Status", header_color=Fore.CYAN + Style.BRIGHT,
                    message=f"Successfully export {len(df)} wallets to {Fore.GREEN + Style.BRIGHT}{filename}.csv{Style.RESET_ALL}, check results folder.")

    def export_wallets_to_excel(self, wallets: list, filename: str =None):

        if not os.path.exists("results"):
            self.logger("Status", header_color=Fore.CYAN + Style.BRIGHT,
                        message=f"Creating results folder...")
            os.makedirs("results")
    
        if filename is None:
            filename = self.name_file
        filepath = os.path.join(os.getcwd(), f"results/{filename}.xlsx")

        df = pd.DataFrame(wallets)
        df.to_excel(filepath, index=False)
        self.logger("Status", header_color=Fore.CYAN + Style.BRIGHT,
                    message=f"Successfully export {len(df)} wallets to {Fore.GREEN + Style.BRIGHT}{filename}.xlsx{Style.RESET_ALL}, check results folder.")
