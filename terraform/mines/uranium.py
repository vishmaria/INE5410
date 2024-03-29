from threading import Thread
from random import randint
from time import sleep

import globals


######################################################################
#                                                                    #
#              Não é permitida a alteração deste arquivo!            #
#                                                                    #
######################################################################

class StoreHouse(Thread):

    def __init__(self, unities, location, constraint):
        Thread.__init__(self)
        self.unities = unities
        self.location = location
        self.constraint = constraint

    def print_store_house(self):
        print(f"🔨 - [{self.location}] - {self.unities} uranium unities are produced.")

    def produce(self):
        with globals.mutex_mina_combustivel:
            if(self.unities < self.constraint):
                self.unities+=15
<<<<<<< HEAD
                #self.print_store_house()
=======
                self.print_store_house() #Se for possível deletar esse print o código vai muito mais rápido
>>>>>>> origin/HEAD
        sleep(0.001)
        

    def run(self):
<<<<<<< HEAD
=======

>>>>>>> origin/HEAD
        globals.acquire_print()
        self.print_store_house()
        globals.release_print()

        while(globals.get_release_system() == False):
            pass

        while(True):
            self.produce()