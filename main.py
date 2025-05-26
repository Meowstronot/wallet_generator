from utils.eth_wallet import eth_wallet_generator
import os
from colorama import Fore, Style
from rich.console import Console
from rich.panel import Panel


if __name__ == "__main__":

    def print_banner():
        os.system('cls' if os.name == 'nt' else 'clear')
        console = Console()
        banner = """[bold green]                                                          
                    █░█░█ ▄▀█ █░░ █░░ █▀▀ ▀█▀   █▀▀ █▀▀ █▄░█ █▀▀ █▀█ ▄▀█ ▀█▀ █▀█ █▀█
                    ▀▄▀▄▀ █▀█ █▄▄ █▄▄ ██▄ ░█░   █▄█ ██▄ █░▀█ ██▄ █▀▄ █▀█ ░█░ █▄█ █▀▄                                                                                                                                 
        [/bold green] """
        console.print(Panel(banner, title="[bold yellow]Simple Wallet Generator[/bold yellow]",
                            title_align="center",
                            subtitle="By Meowstronot (Khisan)", subtitle_align="center", 
                            border_style="cyan", width=100))

    def main_menu():

        print_banner()
        menu = ["Generate Ethereum Wallets",
                "Exit"]

        print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "Main Menu :" + Style.RESET_ALL)
        for i, option in enumerate(menu, start=1):
            print(f"{Fore.GREEN + Style.BRIGHT}{i:>6}.{Style.RESET_ALL} {option}")
        
        while True:
            try:
                input_chain = int(input(f"Select an option {Fore.GREEN + Style.BRIGHT}[1 to {len(menu)}]{Style.RESET_ALL}: "))
                if 1 <= input_chain <= len(menu):
                    if input_chain == len(menu):
                        print(Fore.YELLOW + "Exiting the program..." + Style.RESET_ALL)
                        exit()
                    break
                else:
                    print(Fore.RED + f"Please enter a number [1 to {len(menu)}]" + Style.RESET_ALL)
            except ValueError:
                print(Fore.RED + f"Invalid input. Please enter a number [1 to {len(menu)}]" + Style.RESET_ALL)
        
        while True: 
            try: 
                num_wallets = int(input("Enter the number of wallets to generate : "))
                if num_wallets > 0:
                    break
                else:
                    print(Fore.RED + "Please enter a positive number." + Style.RESET_ALL)
            except ValueError:
                print(Fore.RED + "Invalid input. Please enter a valid number." + Style.RESET_ALL)
        
        while True:
            file_name = input(f"Enter the name of the file to save the wallets (without format file): ")
            if file_name.strip() == "":
                file_name = menu[input_chain - 1].split()[1]+ "_wallets"
                break
            elif len(file_name) > 0:
                break
            else:
                print(Fore.RED + "File name cannot be empty." + Style.RESET_ALL)

        result_print = (f"You selected to generate {Fore.GREEN + Style.BRIGHT}{num_wallets}{Style.RESET_ALL} wallets"
                f" for {Fore.GREEN + Style.BRIGHT}{menu[input_chain - 1].split()[1]} Network{Style.RESET_ALL}.\n")

        return input_chain, num_wallets, result_print, file_name

    generator = eth_wallet_generator()
    input_chain, num_wallets, result_print, file_name = main_menu()
    print_banner()
    print(result_print)

    wallets = generator.generate_batch_eth_wallets(num_wallets=num_wallets)
    generator.export_wallets_to_csv(wallets, filename=file_name)
    generator.export_wallets_to_excel(wallets, filename=file_name)
    print("")