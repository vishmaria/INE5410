from time import sleep
import globals
<<<<<<< HEAD
=======
import os
>>>>>>> origin/HEAD
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

<<<<<<< HEAD
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
=======
            match rocket.name:

                case 'DRAGON':   
                    #Se tiver recursos o suficiente para abastecer o foguete, abastece                         
                    if self.uranium > 35 and self.fuel > 100:
                        self.uranium = self.uranium - 35 

                        if self.name == 'ALCANTARA':
                            self.fuel = self.fuel - 70 
                            
                        elif self.name == 'MOON':
                            self.fuel = self.fuel - 50 

                        else:
                            self.fuel = self.fuel - 100 
                    #Caso contrário, função retorna falso
                    else:
                        return False

                case 'FALCON':
                    #Se tiver recursos o suficiente para abastecer o foguete, abastece    
                    if self.uranium > 35 and self.fuel > 120:
                        self.uranium = self.uranium - 35 

                        if self.name == 'ALCANTARA':
                            self.fuel = self.fuel - 100 

                        elif self.name == 'MOON':
                            self.fuel = self.fuel - 90 

                        else:
                            self.fuel = self.fuel - 120 
                    #Caso contrário, função retorna falso
                    else:
                        return False

                case 'LION':
                    #Se tiver recursos o suficiente para abastecer o foguete, abastece 
                    if self.uranium > 75 and self.fuel > 235: #235 = 115 combustível pra voar + 120 combustível para reabastecer lua
                        self.uranium = self.uranium - 75 # 75 = carga de urânio para reabastecer lua
                        rocket.uranium_cargo = 75  

                        if self.name == 'ALCANTARA':
                            self.fuel = self.fuel - 220 # 220 = 100 combustível pra voar + 120 combustível para reabastecer lua
                            rocket.fuel_cargo = 220

                        else:
                            self.fuel = self.fuel - 235 #235 = 115 combustível pra voar + 120 combustível para reabastecer lua
                            rocket.fuel_cargo = 235
                    #Caso contrário, função retorna falso
                    else:
                        return False

                case _:
                    print("Invalid rocket name")
        return True
>>>>>>> origin/HEAD


    def refuel_oil(self):
        #Reestoca base
<<<<<<< HEAD
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
=======
        if self.name == 'MOON': #A lua não tem acesso as minas da terra
            pass
        else:
            if self.fuel < self.constraints[1]: # Se a quantidad de combustível é inferior ao limite de combustivel:
                mina_combustivel = globals.get_mines_ref()['oil_earth']
                with globals.mutex_mina_combustivel: # Mutex protege o acesso a mina de combustível
                        if mina_combustivel.unities >=100: # Se a mina de combustivel tem mais que 100 unidades produzidas
                            mina_combustivel.unities -= 100 # Tira 100 unidades de combustível da mina 
                            self.fuel +=100 # Bota 100 unidades de combustível na base
                            if self.fuel > self.constraints[1]: # se o carregamento trouxe material demais para o reservatório:
                                mina_combustivel.unities += self.fuel - self.constraints[1] # devolve o excesso para as minas
                                self.fuel = self.constraints[1] # quantidade de combustível = quantidade máxima de combustível.
>>>>>>> origin/HEAD


    def refuel_uranium(self):
        #Reestoca base
<<<<<<< HEAD
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
        valor_max = 3
        if self.name == 'MOON': #A base lunar não pode construir o foguete LION
            valor_max = 2
        if self.rockets < self.constraints[2]:
            foguete_construido = randint(1,valor_max)
            #como armazenar esses foguetes? uma lista? acho que sim
            match foguete_construido:
                case 1:
                    self.foguetes_estacionados.append(Rocket('DRAGON')) #constroi um DRAGON
                    self.base_rocket_resources(self.foguetes_estacionados[len(self.foguetes_estacionados)-1])
                case 2:
                    self.foguetes_estacionados.append(Rocket('FALCON'))#constroi um FALCON
                    self.base_rocket_resources(self.foguetes_estacionados[len(self.foguetes_estacionados)-1])
                case 3:
                    self.foguetes_estacionados.append(Rocket('LION')) #constroi um LION
                    self.base_rocket_resources(self.foguetes_estacionados[len(self.foguetes_estacionados)-1])
            self.rockets += 1   

    def launch_rocket(self): #chama a função rocket.launch() com os parametros certinhos. Tem que dar preferência pra lançamento de Lions para a Lua caso seja chamado.
        if len(self.foguetes_estacionados)>0: # não pode lançar um foguete se não tem nenhum foguete estacionado
            planetas = globals.get_planets_ref()
            alvo = False
            if len(self.foguetes_estacionados) >1:
                foguete_lançado = randint(0,len(self.foguetes_estacionados)-1)
            else:
                foguete_lançado = 0
            
            if not(globals.satelites_de_leitura['mars'].locked()): #ve se o satelite para ler habitabilidade de marte está disponível
                with globals.satelites_de_leitura['mars']:
                    if planetas['mars'].terraform > 0: #se o planeta ainda não estiver terraformado
                        globals.semaforo_planeta['mars'].acquire() #lança um foguete para marte e tranca o semaforo para o planeta
                        alvo = planetas['mars'] # coloca marte como alvo do foguete

            elif not(globals.satelites_de_leitura['io'].locked()):
                with globals.satelites_de_leitura['io']:
                    if planetas['io'].terraform > 0:
                        globals.semaforo_planeta['io'].acquire()
                        alvo = planetas['io']
            
            elif not(globals.satelites_de_leitura['ganimedes'].locked()):
                with globals.satelites_de_leitura['ganimedes']:
                    if planetas['ganimedes'].terraform > 0:
                        globals.semaforo_planeta['ganimedes'].acquire()
                        alvo = planetas['ganimedes']
            
            elif not(globals.satelites_de_leitura['europa'].locked()):
                with globals.satelites_de_leitura['europa']:
                    if planetas['europa'].terraform > 0:
                        globals.semaforo_planeta['europa'].acquire()
                        alvo = planetas['europa']

            if(alvo == False):         
                return  
            else:    
                self.foguetes_estacionados[foguete_lançado].launch(self, alvo)
                globals.semaforo_planeta[alvo.name.lower()].release() #independente do resultado da missão, o próximo foguete pode ser lançado.
                self.foguetes_estacionados.remove(self.foguetes_estacionados[foguete_lançado]) #tira o foguete lançado da lista de foguetes estacionados
                self.rockets -= 1
        #print("\n\nNÃO TEM FOGUETES\n\n")

    def run(self): #Thread dos foguetes [A FAZER]
=======
        if self.name == 'MOON': #A lua não tem acesso as minas da terra
            pass
        else:
            if self.uranium < self.constraints[0]:
                mina_uranio = globals.get_mines_ref()['uranium_earth']
                with globals.mutex_mina_urânio: # Mutex protege o acesso a mina de urânio
                    if mina_uranio.unities >= 100: # Se a mina de urânio tem mais que 100 unidades produzidas
                        mina_uranio.unities -= 100 # Tira 100 unidades de urânio da mina 
                        self.uranium += 100 # Bota 100 unidades de urânio na base
                        if self.uranium > self.constraints[0]: # se o carregamento trouxe material demais para o reservatório:
                            mina_uranio.unities += self.uranium - self.constraints[0]  # devolve o excesso para as minas
                            self.uranium = self.constraints[0] # quantidade de urânio = quantidade máxima de urânio.

    def build_rocket(self):
        valor_max = 3
        if self.name == 'MOON':
             # Como a base lunar não pode produzir foguetes LION, o valor_max do gerador de número aleatório é limitado em 2 para evitar que um LION seja construido na lua
            valor_max = 2
        if self.rockets < self.constraints[2]: # Se o número atual de foguetes é menor que o limite de foguetes na base:
            foguete_construido = randint(1,valor_max) # gera um número aleatório para decidir qual foguete construir

            match foguete_construido:
                case 1:
                    self.foguetes_estacionados.append(Rocket('DRAGON')) #constroi um DRAGON e o coloca na lista de foguetes prontos pra voar
                    
                case 2:
                    self.foguetes_estacionados.append(Rocket('FALCON'))#constroi um FALCON e o coloca na lista de foguetes prontos pra voar

                case 3:
                    self.foguetes_estacionados.append(Rocket('LION')) #constroi um LION e o coloca na lista de foguetes prontos pra voar
                    
            
            if not(self.base_rocket_resources(self.foguetes_estacionados[self.rockets-1])): # tenta abastecer o foguete recém-criado com urânio e combustível
                #Se a base não tem combustível ou urânio o suficiente, a função retorna FALSE, o foguete não é construido e é removido da lista de foguetes
                self.foguetes_estacionados.remove(self.foguetes_estacionados[self.rockets-1]) 
            else:
                self.rockets += 1


    def launch_rocket(self): # chama a função rocket.launch() com os parametros certinhos.
        if self.rockets > 0: # Se a base tem pelo menos um foguete estacionado:
            planetas = globals.planets
            satelite = globals.satelites_de_leitura
            alvo = False
                
                    
            if len(planetas)>1: # se tem mais de um planeta que ainda deve ser terraformado
                random_target_number = randint(0, len(planetas)-1) #gera um número aleatório para escolher qual planeta será o alvo
            else: #se só tiver um planeta que ainda não foi terraformado, esse planeta será o alvo
                random_target_number = 0

            if self.rockets > 1: # Se a base possui mais de um foguete estacionado:
                num_foguete = randint(0, self.rockets-1) # escolhe aleatóriamente entre os x foguetes estacionados
                foguete_selecionado = self.foguetes_estacionados[num_foguete] #o foguete que será lançado é igual ao foguete na NUM_FOGUETE posição da lista FOGUETES_ESTACIONADOS
            else: # Se a base possui apenas 1 foguete estacionado:
                num_foguete = 0
                foguete_selecionado = self.foguetes_estacionados[num_foguete] #o foguete que será lançado é igual ao foguete na NUM_FOGUETE posição da lista FOGUETES_ESTACIONADOS

            if foguete_selecionado.name == "LION": # se o foguete selecionado for um LION:
                with globals.mutex_armazenamento['MOON']: #Mutex protege a leitura da lua
                    if (globals.get_bases_ref()['moon'].uranium>35 and globals.get_bases_ref()['moon'].fuel > 90):
                        # SE A BASE DECIDIR LANÇAR UM FOGUETE LION MAS A LUA SINALIZAR QUE NÃO PRECISA DE RECURSOS, O FOGUETE NÃO RECEBERA UM ALVO E NÃO SERÁ LANÇADO
                        return
            
            for i, key in enumerate(planetas.keys()): #enumera as chaves
                if i == random_target_number: #ao chegar na chave equivalente ao numero gerado aleatóriamente
                    with satelite[planetas[key].name.lower()]: #ativa o mutex do planeta
                        if planetas[key].terraform > 0: #checa se o planeta ainda deve ser terraformado
                            alvo = planetas[key]       #seta o planeta como alvo para lançamento       
                            break
                
                
            
            if (alvo): #se algum alvo foi adquirido:
                
                globals.semaforo_limite_foguetes_ativos.acquire()
                Thread(target=foguete_selecionado.launch, args=(self, alvo)).start() #Cria a thread do foguete lançado
                self.foguetes_estacionados.remove(foguete_selecionado) #tira o foguete lançado da lista de foguetes estacionados
                self.rockets -= 1


    def run(self):
>>>>>>> origin/HEAD
        self.foguetes_estacionados = []
        globals.acquire_print()
        self.print_space_base_info()
        globals.release_print()
        

<<<<<<< HEAD
        while(globals.get_release_system() == False):
            pass

        while(True):
            #self.print_space_base_info()
=======
        while(globals.get_release_system() == False): #enquanto a simulação não é totalmente inicializada: não faz nada
            pass

        while(True):

            
>>>>>>> origin/HEAD
            self.refuel_oil()
            self.refuel_uranium()
            self.build_rocket()
            self.launch_rocket()
<<<<<<< HEAD
=======
            if globals.planets == {}: #Quando o dicionário de planetas fica vazio significa que todos os planetas estão habitaveis e o processo pode ser finalizado.
                print("TODOS OS PLANETAS ESTÃO TERRAFORMADOS")
                os._exit(os.X_OK) # comando para matar o processo.
>>>>>>> origin/HEAD
            pass
