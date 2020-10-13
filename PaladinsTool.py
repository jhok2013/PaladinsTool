from random import seed
from random import randint
from json import load, dumps
from pathlib import Path

class PaladinsTool(object):
    '''

    ''' 
    champion_dict: dict
    start_board: str = ( 
        f"\nWelcome to the Paladins Champion Selector\n"
        f"=========================================\n"
        f"Commands\n"
        f"========\n"
        f"1. Select random character\n"
        f"2. Change champion settings\n"
        f"3. Save changes\n"
        f"4. Reset changes\n"
        f"5. Show start menu\n"
        f"6. Quit"
    )
    champion_menu: str = (
        f"Champion Menu\n"
        f"=============\n"
        f"1. Set champion availability\n"
        f"2. Set all champions\n"
        f"3. See champion\n"
        f"4. See all champions\n"
        f"5. Show menu again\n"
        f"6. Go back"
    )
    def __init__(self):
        '''

        '''
        self._path = Path.home().cwd().joinpath('champions.json')
        self._f = open(self._path, "r+")
        self.champion_dict: dict = load(self._f)
    
    def __quit(self):
        '''

        '''
        self._f.close()
        goodbye_message: str = "Goodbye and thank you."
        print(goodbye_message)
        quit()
    
    def __save(self):
        '''

        '''
        self._f.seek(0)
        self._f.write(dumps(self.champion_dict))
        self._f.truncate()
        print("Saved changes!")
    
    def __reset(self):
        '''

        '''
        self._f.close()
        self._f = open(self._path, "r+")
        self.champion_dict = load(self._f)
        print("Changes reset!")

    def choose_random_champion(self) -> bool:
        '''

        '''
        ran_successfully: bool = False
        available_dict: dict = {int(k): v for (k,v) in self.champion_dict.items() if v['available'] == True}
        if available_dict:
            print("Choosing random champion")
            print("=========================")
            available_ids: list = list(available_dict.keys())
            seed()
            amount: int = len(available_ids)
            champion_index: int = randint(1, amount - 1)
            champion: str = available_dict[available_ids[champion_index]]['name']
            print(f"Your next champion is {champion}. Have fun!")
        else:
            champion = "No champions are available."
        ran_successfully = True
        return ran_successfully

    def set_available_champions(self) -> bool:
        '''

        '''
        ran_successfully: bool = False
        champion_name: str = str(input("\nEnter champion name: "))
        available = input("Enter availability: ")
        available = True if available == 'True' else False
        for i in self.champion_dict:
            if self.champion_dict[i]['name'] == champion_name:
                self.champion_dict[i]['available'] = available
                ran_successfully = True
                print(f"{champion_name} set to {'available' if available == True else 'unavailable'}")
        return ran_successfully

    def set_all(self) -> bool:
        '''

        '''
        available = input("Enter availability: ")
        available = True if available == 'True' else False
        for ok, ov in self.champion_dict.items():
            if ov['available'] != available:
                ov['available'] = available
        ran_successfully = True
        print(f"All champions set to {'available' if available == True else 'unavailable'}")
        return ran_successfully

    def see_champion(self) -> bool:
        '''

        '''
        champion_name: str
        ran_successfully: bool = False
        try:
            champion_name = str(input("Enter champion name: ")) 
            print('')
            for k, v in self.champion_dict.items():
                if v['name'] == champion_name:
                    print("ID   Name    Role    Available")
                    print("===============================")
                    print(f"{k}   {v['name']}   {v['role']}   {v['available']}")
                    ran_successfully = True
        except Exception as e:
            print("Invalid champion name.")

        return ran_successfully
    
    def show_champions(self) -> bool:
        '''

        '''
        message: str
        ran_successfully: bool = False
        available = input("Enter availability: ")
        available = True if available == 'True' else False
        selected_dict: dict = {int(k): v for (k,v) in self.champion_dict.items() if v['available'] == available}
        if selected_dict:
            print("ID   Name    Role    Available")
            print("===============================")
            for k, v in self.champion_dict.items():
                print(f"{k}.   {v['name']}   {v['role']}   {v['available']}")
        else:
            print("No champions are available.")
        ran_successfully = True
        return ran_successfully
    
    def print_champion_menu(self):
        '''

        '''
        print(self.champion_menu)
    
    def print_start_menu(self):
        '''

        '''
        print(self.start_board)
    
    def set_availability_interactive(self) -> bool:
        '''

        '''
        ran_successfully: bool = False
        
        command_dict: dict = {
            1: self.set_available_champions,
            2: self.set_all,
            3: self.see_champion,
            4: self.show_champions,
            5: self.print_champion_menu,
            6: self.command_parser
        }
        print(self.champion_menu)
        command: int = 0
        while command != 6:
            print('')
            while True:
                try:
                    command = int(input("Enter command: "))
                    if command < 1 or command > 6:
                        raise ValueError
                    else:
                        execute = command_dict.get(command)
                        execute()
                    break
                except ValueError as e:
                    self.print_champion_menu()
                    print('')
                    print("Please enter a valid number.\n")
        ran_successfully = True
        return ran_successfully

    def command_parser(self) -> None:
        '''

        '''
        command_dict = {
            1: self.choose_random_champion,
            2: self.set_availability_interactive,
            3: self.__save,
            4: self.__reset,
            5: self.print_start_menu,
            6: self.__quit
        }
        command: int = 0
        print(self.start_board)
        while command != 6:
            print('')
            while True:
                try:
                    command = int(input("Enter command: "))
                    if command < 1 or command > 6:
                        raise ValueError
                    else:
                        execute = command_dict.get(command)
                        execute()
                    break
                except ValueError as e:
                    self.print_start_menu()
                    print('')
                    print("Please enter a valid number.\n")

    def main(self):
        '''

        '''
        self.command_parser()

if __name__ == "__main__":
    PaladinsTool().main()