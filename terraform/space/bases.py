import globals
from threading import Thread
from space.rocket import Rocket
from random import choice, randint

class SpaceBase(Thread):

    ################################################
    # O CONSTRUTOR DA CLASSE NÃO PODE SER ALTERADO #
    ################################################
    def __init__(self, name, fuel, uranium, rockets):
        Thread.__init__(self)
        self.name = name
        self.uranium = 0
        self.fuel = 0
        self.rockets = 0
        self.constraints = [uranium, fuel, rockets]

    def print_space_base_info(self):
        print(f"🔭 - [{self.name}] → 🪨  {self.uranium}/{self.constraints[0]} URANIUM  ⛽ {self.fuel}/{self.constraints[1]}  🚀 {self.rockets}/{self.constraints[2]}")
    
    def base_rocket_resources(self, rocket): #Decrementa estoque de combustivel e urânio. Chama a função de abastecimento depois. (ALTERAÇÕES: rocket_name alterado para o objeto ROCKET)

        with globals.get_locks_armazem()[self.name]: #este lock protege toda a operação de reabastecimento de cada foguete em cada base

            match rocket.name:   #Controle de concorrência é necessário nas linhas que decrementam o próprio estoque já que ele pode estar abastecendo multiplos foguetes
                case 'DRAGON':   #Talvez seja preciso um controle para a leitura também para que ele não leia que pode abastecer enquanto outro já está tirando a quantidade necessária do estoque
                                            
                    if self.uranium > 35 and self.fuel > 50:
                        self.uranium = self.uranium - 35 #
                        rocket.uranium_cargo = 35

                        if self.name == 'ALCANTARA':
                            self.fuel = self.fuel - 70 #
                            rocket.fuel_cargo = 70
                            
                        elif self.name == 'MOON':
                            self.fuel = self.fuel - 50 #
                            rocket.fuel_cargo = 50

                        else:
                            self.fuel = self.fuel - 100 #
                            rocket.fuel_cargo = 100

                case 'FALCON':

                    if self.uranium > 35 and self.fuel > 90:
                        self.uranium = self.uranium - 35 #
                        rocket.uranium_cargo = 35

                        if self.name == 'ALCANTARA':
                            self.fuel = self.fuel - 100 #
                            rocket.fuel_cargo = 100

                        elif self.name == 'MOON':
                            self.fuel = self.fuel - 90 #
                            rocket.fuel_cargo = 90

                        else:
                            self.fuel = self.fuel - 120 #
                            rocket.fuel_cargo = 120

                case 'LION':
                    if self.uranium > 35 and self.fuel > 100:
                        self.uranium = self.uranium - 35 #
                        rocket.uranium_cargo = 35  

                        if self.name == 'ALCANTARA':
                            self.fuel = self.fuel - 100 #
                            rocket.fuel_cargo = 100

                        else:
                            self.fuel = self.fuel - 115 #
                            rocket.fuel_cargo = 115


                case _:
                    print("Invalid rocket name")


    def refuel_oil(self):
        #Reestoca base
        if self.name == 'MOON': #a lua não tem acesso as minas da terra. toda a carga vem do foguete LION
            if self.fuel < 50: #50 por que é a quantidade de combustivel necessária para lançar o maior foguete da Lua
                pass #AQUI SERÁ A SINALIZAÇÃO PARA O ENVIO DE FOGUETES LION PARA LUA
        else:
            if self.fuel < self.constraints[1]:
                mina_combustivel = globals.get_mines_ref()['oil_earth']
                with globals.mutex_mina_combustivel:
                        if mina_combustivel.unities >=100: #100 por que é o minimo pra abastecer o foguete médio. Talvez pegar o maior seja melhor
                            mina_combustivel.unities -= 100
                            self.fuel +=100


    def refuel_uranium(self):
        #Reestoca base
        if self.name == 'MOON': #a lua não tem acesso as minas da terra. toda a carga vem do foguete LION
             if self.uranium < 35:
                pass #SINALIZAÇÃO PARA ENVIO DE FOGUETES LION
        else:
            if self.uranium < self.constraints[0]:
                mina_uranio = globals.get_mines_ref()['uranium_earth']
                with globals.mutex_mina_urânio:
                    if mina_uranio.unities >= 35: #35 por que 35 é a carga necessária para uma ogiva.
                        mina_uranio.unities -= 35 
                        self.uranium += 35 # Reabastece

    def build_rocket(self):
        if self.rockets < self.constraints[2]:
            foguete_construido = randint(1,3)
            #como armazenar esses foguetes? uma lista? acho que sim
            match foguete_construido:
                case 1:
                    pass #constroi um DRAGON
                case 2:
                    pass #constroi um FALCON
                case 3:
                    pass #constroi um LION
            self.rockets += 1
        pass    

    def launch_rocket(self, rocket): #chama a função rocket.launch() com os parametros certinhos. Tem que dar preferência pra lançamento de Lions para a Lua caso seja chamado.
        pass

    def run(self): #Thread dos foguetes [A FAZER]
        globals.acquire_print()
        self.print_space_base_info()
        globals.release_print()
        

        while(globals.get_release_system() == False):
            pass

        while(True):
            self.print_space_base_info()
            self.refuel_oil()
            self.refuel_uranium()
            pass
