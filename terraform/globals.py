<<<<<<< HEAD
from multiprocessing import Semaphore
from threading import Lock
=======
from msilib.schema import Condition
from multiprocessing import Semaphore
from threading import Lock, Condition
>>>>>>> origin/HEAD

#  A total alteração deste arquivo é permitida.
#  Lembre-se de que algumas variáveis globais são setadas no arquivo simulation.py
#  Portanto, ao alterá-las aqui, tenha cuidado de não modificá-las. 
#  Você pode criar variáveis globais no código fora deste arquivo, contudo, agrupá-las em
#  um arquivo como este é considerado uma boa prática de programação. Frameworks como o Redux,
#  muito utilizado em frontend em libraries como o React, utilizam a filosofia de um store
#  global de estados da aplicação e está presente em sistemas robustos pelo mundo.

<<<<<<< HEAD
#A FAZER:
#  SEMAFOROS BINÁRIOS PARA LEITURA DO PROGRESSO DE TERRAFORMING DE CADA PLANETA (1 SATELITE)/(PLANETA)
#  SEMAFORO DE 2 PARA A O ENVIO DE OGIVAS PARA O MESMO PLANETA (como um dos foguetes pode explodir no meio do caminho, este semaforo vai poder ser liberado se falhar para mandarem outro no lugar ou se detonar)
#  SEMAFORO BINÁRIO PARA A DETONAÇÃO DE APENAS UMA OGIVA POR VEZ EM CADA PLANETA
#  

#Declarando dicionário de Lock() para acesso ao armazem de urânio e combustível de cada base onde a chave é o nome da base
mutex_armazenamento = {'ALCANTARA': Lock(), 'CANAVERAL CAPE': Lock(), 'MOSCOW': Lock(), 'MOON': Lock()}
mutex_mina_urânio = Lock()
mutex_mina_combustivel = Lock()
satelites_de_leitura = {'mars': Lock(), 'io':Lock(), 'ganimedes': Lock(), 'europa': Lock()}
semaforo_planeta = {'mars': Semaphore(2), 'io': Semaphore(2), 'ganimedes': Semaphore(2), 'europa': Semaphore(2)} #satelites
mutex_polo_norte = {'mars': Lock(), 'io':Lock(), 'ganimedes': Lock(), 'europa': Lock()}
mutex_polo_sul = {'mars': Lock(), 'io':Lock(), 'ganimedes': Lock(), 'europa': Lock()}


=======


# Declarando dicionário de Lock() para acesso ao armazem de urânio e combustível de cada base onde a chave é o nome da base
mutex_armazenamento = {'ALCANTARA': Lock(), 'CANAVERAL CAPE': Lock(), 'MOSCOW': Lock(), 'MOON': Lock()}
# Mutex para acesso a mina de urãnio
mutex_mina_urânio = Lock()
# Mutex para acesso a mina de urãnio
mutex_mina_combustivel = Lock()
# Dicionário de Lock() para leitura de habitabilidade de cada planeta
satelites_de_leitura = {'mars': Lock(), 'io':Lock(), 'ganimedes': Lock(), 'europa': Lock()}
# Dicionários de Semaforos para limitar a quantidade de explosões simultâneas em um planeta
semaforo_planeta = {'mars': Semaphore(2), 'io': Semaphore(2), 'ganimedes': Semaphore(2), 'europa': Semaphore(2)}
# Mutex para garantir que apenas 1 explosão por vez ocorrera no polo norte de um planeta
mutex_polo_norte = {'mars': Lock(), 'io':Lock(), 'ganimedes': Lock(), 'europa': Lock()}
# Mutex para garantir que apenas 1 explosão por vez ocorrera no polo norte de um planeta
mutex_polo_sul = {'mars': Lock(), 'io':Lock(), 'ganimedes': Lock(), 'europa': Lock()}


semaforo_limite_foguetes_ativos = Semaphore(200) #Pra evitar que o computador exploda

>>>>>>> origin/HEAD
release_system = False
mutex_print = Lock()
planets = {}
bases = {}
mines = {}
simulation_time = None

def acquire_print():
    global mutex_print
    mutex_print.acquire()

def release_print():
    global mutex_print
    mutex_print.release()

def set_planets_ref(all_planets):
    global planets
    planets = all_planets

def get_planets_ref():
    global planets
    return planets

def set_bases_ref(all_bases):
    global bases
    bases = all_bases

def get_bases_ref():
    global bases
    return bases

def set_mines_ref(all_mines):
    global mines
    mines = all_mines

def get_mines_ref():
    global mines
    return mines

<<<<<<< HEAD
def set_release_system(): #Libera a execução da simulação
    global release_system
    release_system = True

def get_release_system(): #Retorna se a simulação está sendo executada
=======
def set_release_system():
    global release_system
    release_system = True

def get_release_system():
>>>>>>> origin/HEAD
    global release_system
    return release_system

def set_simulation_time(time):
    global simulation_time
    simulation_time = time

def get_simulation_time():
    global simulation_time
    return simulation_time

def get_locks_armazem():
    global mutex_armazenamento #tem que fazer isso?
    return mutex_armazenamento

<<<<<<< HEAD
def get_lock_mina_uranio():
    global mutex_mina_urânio #tem que fazer isso?
    return mutex_mina_urânio  

def get_lock_mina_combustivel():
    global mutex_mina_combustivel #tem que fazer isso?
    return mutex_mina_combustivel

=======
>>>>>>> origin/HEAD
