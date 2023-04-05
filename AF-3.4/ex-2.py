from time import sleep
from random import randint
from threading import Thread, Semaphore, BoundedSemaphore

def produtor():
  global buffer
  for i in range(10):
    sem_produtor.acquire()
    sleep(randint(0,2))           # fica um tempo produzindo...
    item = 'item ' + str(i)
    # verifica se há lugar no buffer
    buffer.append(item)
    print('Produzido %s (ha %i itens no buffer)' % (item,len(buffer)))
    sem_consumidor.release()

def consumidor():
  global buffer
  for i in range(10):
    # aguarda que haja um item para consumir 
    sem_consumidor.acquire()
    item = buffer.pop(0)
    print('Consumido %s (ha %i itens no buffer)' % (item,len(buffer)))
    sleep(randint(0,2))         # fica um tempo consumindo...
    sem_produtor.release() 

buffer = []
tam_buffer = 3
# cria semáforos
sem_produtor = BoundedSemaphore(value=tam_buffer)
sem_consumidor = Semaphore(value=0)
produtor = Thread(target=produtor) 
consumidor = Thread(target=consumidor) 
produtor.start()
consumidor.start()
produtor.join()
consumidor.join() 