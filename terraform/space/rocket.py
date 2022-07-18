from random import randrange, random
from time import sleep
import globals

class Rocket:

    ################################################
    # O CONSTRUTOR DA CLASSE NÃO PODE SER ALTERADO #
    ################################################
    def __init__(self, type):
        self.id = randrange(1000)
        self.name = type
        if(self.name == 'LION'):
            self.fuel_cargo = 0
            self.uranium_cargo = 0
            

    def nuke(self, planet): # Permitida a alteração

        with globals.semaforo_planeta[planet.name.lower()]: # Só permite que 2 nukes explodam por vez
            if planet.terraform <= 0: #Foguetes orbitando um planeta totalmente terraformado se detonam
                return
            planet.terraform -= self.damage() #causa dano ao planeta
            globals.semaforo_limite_foguetes_ativos.release() # depois que o foguet explodiu, libera para a criação de outra thread de foguete

            if not(globals.mutex_polo_norte[planet.name.lower()].locked()): #Se o mutex do polo norte desse planeta não estiver trancado:
                with globals.mutex_polo_norte[planet.name.lower()]: #mutex que protege o polo norte do planeta
                    print(f"[EXPLOSION] - The {self.name} ROCKET reached the planet {planet.name} on North Pole")
                    return
            else: # se o polo norte já estiver sendo explodido:
                with globals.mutex_polo_norte[planet.name.lower()]: #mutex que protege o polo sul do planeta
                    print(f"[EXPLOSION] - The {self.name} ROCKET reached the planet {planet.name} on South Pole")
                    return
    
    def voyage(self, planet): # Permitida a alteração (com ressalvas)

        # Essa chamada de código (do_we_have_a_problem e simulation_time_voyage) não pode ser retirada.
        # Você pode inserir código antes ou depois dela e deve
        # usar essa função.

        if self.name == "LION": # o tempo de viagem da terra até a lua é insignificante então será ignorado
            
            failure =  self.do_we_have_a_problem()

            if failure == True: #em caso de falha:
                globals.semaforo_limite_foguetes_ativos.release() #libera um espaço para criação de outra thread foguete 
                return #finaliza

            else:
                
                with globals.mutex_armazenamento['MOON']: #Mutex que protege armazem da lua
                    globals.get_bases_ref()['moon'].fuel += self.fuel_cargo #abastece a lua com combustível carregado pelo LION
                    globals.get_bases_ref()['moon'].uranium += self.uranium_cargo #abastece a lua com urânio carregado pelo LION
                    
                    if globals.get_bases_ref()['moon'].fuel > globals.get_bases_ref()['moon'].constraints[1]: #se chegar mais material do que pode ser armazenado 
                        globals.get_bases_ref()['moon'].fuel = globals.get_bases_ref()['moon'].constraints[1] # o resto é descartado

                    if globals.get_bases_ref()['moon'].uranium > globals.get_bases_ref()['moon'].constraints[0]: #se chegar mais material do que pode ser armazenado
                        globals.get_bases_ref()['moon'].uranium = globals.get_bases_ref()['moon'].constraints[0] # o resto é descartado
                    globals.semaforo_limite_foguetes_ativos.release()   #libera um espaço para criação de outra thread foguete           
                    return#finaliza
     

        self.simulation_time_voyage(planet)
        failure =  self.do_we_have_a_problem()

        if failure == True: #em caso de falha:
            globals.semaforo_limite_foguetes_ativos.release() #libera um espaço para criação de outra thread foguete 
         
        else:
            self.nuke(planet)
        
        


    ####################################################
    #                   ATENÇÃO                        # 
    #     AS FUNÇÕES ABAIXO NÃO PODEM SER ALTERADAS    #
    ###################################################
    def simulation_time_voyage(self, planet):
        if planet.name == 'MARS':
            sleep(2) # Marte tem uma distância aproximada de dois anos do planeta Terra.
        else:
            sleep(5) # IO, Europa e Ganimedes tem uma distância aproximada de cinco anos do planeta Terra.

    def do_we_have_a_problem(self):
        if(random() < 0.15):
            if(random() < 0.51):
                self.general_failure()
                return True
            else:
                self.meteor_collision()
                return True
        return False
            
    def general_failure(self): # Missão fracassada. Sinaliza para o envio de outro foguete (sinalização feita em Voyage ou do_we_have_a_problem)
        print(f"[GENERAL FAILURE] - {self.name} ROCKET id: {self.id}")
    
    def meteor_collision(self): # Missão fracassada. Sinaliza para o envio de outro foguete (sinalização feita em Voyage ou do_we_have_a_problem)
        print(f"[METEOR COLLISION] - {self.name} ROCKET id: {self.id}")

    def successfull_launch(self, base): #Missão bem sucedida. Sinaliza para o envio de outro foguete
        if random() <= 0.1:
            print(f"[LAUNCH FAILED] - {self.name} ROCKET id:{self.id} on {base.name}")
            globals.semaforo_limite_foguetes_ativos.release() #Alteração necessária
            return False
        return True
    
    def damage(self):
        return random()

    def launch(self, base, planet):
        if(self.successfull_launch(base)):
            print(f"[{self.name} - {self.id}] launched from {base.name}.")
            self.voyage(planet)        
