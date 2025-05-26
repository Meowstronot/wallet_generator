from utils.eth_wallet import eth_wallet_generator
import os

os.system('cls' if os.name == 'nt' else 'clear')

generator = eth_wallet_generator()
wallets = generator.generate_batch_eth_wallets(num_wallets=1)
generator.export_wallets_to_csv(wallets, filename="1_eth_wallets")
generator.export_wallets_to_excel(wallets, filename="1_eth_wallets")