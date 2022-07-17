from time import sleep
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
                                            
                    if self.uranium > 35 and self.fuel > 100:
                        self.uranium = self.uranium - 35 #

                        if self.name == 'ALCANTARA':
                            self.fuel = self.fuel - 70 #
                            
                        elif self.name == 'MOON':
                            self.fuel = self.fuel - 50 #

                        else:
                            self.fuel = self.fuel - 100 #
                    
                    else:
                        return False

                case 'FALCON':

                    if self.uranium > 35 and self.fuel > 120:
                        self.uranium = self.uranium - 35 #

                        if self.name == 'ALCANTARA':
                            self.fuel = self.fuel - 100 #

                        elif self.name == 'MOON':
                            self.fuel = self.fuel - 90 #

                        else:
                            self.fuel = self.fuel - 120 #
                    else:
                        return False

                case 'LION':
                    if self.uranium > 75 and self.fuel > 235: #235 = 115 combustível pra voar + 120 combustível para reabastecer lua
                        self.uranium = self.uranium - 75 # 75 = carga de urânio para reabastecer lua
                        rocket.uranium_cargo = 75  

                        if self.name == 'ALCANTARA':
                            self.fuel = self.fuel - 220 # 220 = 100 combustível pra voar + 120 combustível para reabastecer lua
                            rocket.fuel_cargo = 220

                        else:
                            self.fuel = self.fuel - 235 #235 = 115 combustível pra voar + 120 combustível para reabastecer lua
                            rocket.fuel_cargo = 235

                    else:
                        return False

                case _:
                    print("Invalid rocket name")
        return True


    def refuel_oil(self):
        #Reestoca base
        if self.name == 'MOON': #a lua não tem acesso as minas da terra. toda a carga vem do foguete LION
            with globals.mutex_armazenamento['MOON']: #Mutex para realizar leitura atômica do armazem da lua
                if self.fuel < 90: #90 por que é a quantidade de combustivel necessária para lançar o maior foguete da Lua
                    pass
        else:
            if self.fuel < self.constraints[1]:
                mina_combustivel = globals.get_mines_ref()['oil_earth']
                with globals.mutex_mina_combustivel:
                        if mina_combustivel.unities >=100: #100 por que é o minimo pra abastecer o foguete médio. Talvez pegar o maior seja melhor
                            mina_combustivel.unities -= 100 #testes revelaram que 100 aparenta ser um bom
                            self.fuel +=100
                            if self.fuel > self.constraints[1]:
                                mina_combustivel.unities += self.fuel - self.constraints[1] #se o carregamento trouxe material demais para o reservatório: devolve o excesso para as minas
                                self.fuel = self.constraints[1]


    def refuel_uranium(self):
        #Reestoca base
        if self.name == 'MOON': #a lua não tem acesso as minas da terra. toda a carga vem do foguete LION
            with globals.mutex_armazenamento['MOON']: #Mutex para realizar leitura atômica do armazem da lua
                if self.uranium < 35: 
                    pass
        else:
            if self.uranium < self.constraints[0]:
                mina_uranio = globals.get_mines_ref()['uranium_earth']
                with globals.mutex_mina_urânio:
                    if mina_uranio.unities >= 100: #35 por que 35 é a carga necessária para uma ogiva.
                        mina_uranio.unities -= 100 
                        self.uranium += 100 # Reabastece
                        if self.uranium > self.constraints[0]:
                            mina_uranio.unities += self.uranium - self.constraints[0]  #se o carregamento trouxe material demais para o reservatório: devolve o excesso para as minas
                            self.uranium = self.constraints[0]

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
                    
                case 2:
                    self.foguetes_estacionados.append(Rocket('FALCON'))#constroi um FALCON

                case 3:
                    self.foguetes_estacionados.append(Rocket('LION')) #constroi um LION
                    
            
            if not(self.base_rocket_resources(self.foguetes_estacionados[self.rockets-1])): #abastece o foguete recém-criado com urânio e combustível
                #print(f"{self.name} não possui os recursos para montar este foguete") #DELETAR
                self.foguetes_estacionados.remove(self.foguetes_estacionados[self.rockets-1]) #Se a base não tem combustível ou urânio o suficiente, o foguete não é abastecido
            else:
                self.rockets += 1


    def launch_rocket(self): #chama a função rocket.launch() com os parametros certinhos. Tem que dar preferência pra lançamento de Lions para a Lua caso seja chamado.
        if self.rockets > 0: # não pode lançar um foguete se não tem nenhum foguete estacionado
            planetas = globals.planets
            satelite = globals.satelites_de_leitura
            alvo = False
            if globals.flag_lua_com_falta:
                for i in self.foguetes_estacionados:
                    #print(i.name)
                    if i.name == 'LION':
                        foguete_selecionado = i
                        alvo = True
                        break
                

            else:        
                if len(planetas)>1:
                    random_target_number = randint(0, len(planetas)-1)
                else:
                    random_target_number = 0
                if self.rockets > 1:
                    num_foguete = randint(0, self.rockets-1) # escolhe aleatóriamente entre os x foguetes estacionados
                    foguete_selecionado = self.foguetes_estacionados[num_foguete]
                else:
                    num_foguete = 0
                    foguete_selecionado = self.foguetes_estacionados[num_foguete]

                
                for i, key in enumerate(planetas.keys()): #enumera as chaves
                    if i == random_target_number: #ao chegar na chave equivalente ao numero gerado aleatóriamente
                        #print(planetas[key].name) #USO PRA DEBUG, DELETAR DEPOIS
                        with satelite[planetas[key].name.lower()]: #ativa o mutex do planeta
                            if planetas[key].terraform > 0: #checa se o planeta ainda deve ser terraformado
                                alvo = planetas[key]       #seta o planeta como alvo para lançamento       
                        break

            
            if (alvo): #se algum alvo foi adquirido:
                if self.name == 'MOON':
                    self.print_space_base_info()
                globals.semaforo_limite_foguetes_ativos.acquire()
                if foguete_selecionado.name == "LION":
                    print("QUERO LANÇAR O LION")
                Thread(target=foguete_selecionado.launch, args=(self, alvo)).start()
                #foguete_selecionado.launch(self, alvo)
                self.foguetes_estacionados.remove(foguete_selecionado) #tira o foguete lançado da lista de foguetes estacionados
                self.rockets -= 1


    def run(self): #Thread dos foguetes [A FAZER]
        self.foguetes_estacionados = []
        globals.acquire_print()
        self.print_space_base_info()
        globals.release_print()
        

        while(globals.get_release_system() == False):
            pass

        while(True):

            
            if(self.uranium < 0 or self.fuel < 0 or self.uranium > self.constraints[0] or self.fuel > self.constraints[1]): #Deletar depois. Só pra debugar
                self.print_space_base_info()
                exit()
            
            self.refuel_oil()
            self.refuel_uranium()
            self.build_rocket()
            self.launch_rocket()
            if globals.planets == {}:
                print("ACABOU")
                exit()
            pass
