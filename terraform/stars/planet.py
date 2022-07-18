from threading import Thread
import globals

class Planet(Thread):

    ################################################
    # O CONSTRUTOR DA CLASSE NÃO PODE SER ALTERADO #
    ################################################
    def __init__(self, terraform,name):
        Thread.__init__(self)
        self.terraform = terraform
        self.name = name

    def nuke_detected(self):
        while(self.terraform > 0):
            before_percentage = self.terraform
            while(before_percentage == self.terraform): #Enquanto não for nukado, não faz nada
                pass
            print(f"[NUKE DETECTION] - The planet {self.name} was bombed. {self.terraform}% UNHABITABLE")

    def print_planet_info(self):
        print(f"🪐 - [{self.name}] → {self.terraform}% UNINHABITABLE")

    def run(self):
        globals.acquire_print()
        self.print_planet_info()
        globals.release_print()

        while(globals.get_release_system() == False):
            pass

        while(True):
            self.nuke_detected()
            if self.terraform < 1:
                print(f"\n\n{self.name} está habitavel\n\n")
                globals.planets.pop(self.name.lower()) #Se um planeta fica habitável ele sai do dicionário de planetas. 
                return #finaliza