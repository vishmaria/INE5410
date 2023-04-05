from threading import Thread
from time import sleep

import globals


######################################################################
#                                                                    #
#              Não é permitida a alteração deste arquivo!            #
#                                                                    #
######################################################################

class Pipeline(Thread):

    def __init__(self, unities, location, constraint):
        Thread.__init__(self)
        self.unities = unities
        self.location = location
        self.constraint = constraint

    def print_pipeline(self):
        print(
            f"🔨 - [{self.location}] - {self.unities} oil unities are produced."
        )

    def produce(self):
        with globals.mutex_mina_urânio:
            if(self.unities < self.constraint):
                self.unities += 17
<<<<<<< HEAD
                #self.print_pipeline()
        sleep(0.001)

    def run(self):
=======
                self.print_pipeline() #Se for possível deletar esse print o código vai muito mais rápido
        sleep(0.001)

    def run(self):
        
>>>>>>> origin/HEAD
        globals.acquire_print()
        self.print_pipeline()
        globals.release_print()

        while(globals.get_release_system() == False):
            pass

        while(True):
            self.produce()
