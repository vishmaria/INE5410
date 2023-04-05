from time import sleep
from random import randint
from threading import Thread, Lock, Condition
from concurrent.futures import ThreadPoolExecutor

def produtor(n):
  global buffer
  for i in range(10):
    sleep(randint(0,2))           # fica um tempo produzindo...
    item = 'item ' + str(i) + ' da thread ' + str(n)
    with lock:
      if len(buffer) == tam_buffer:
        print('>>> Buffer cheio. Produtor ira aguardar.')
        lugar_no_buffer.wait()    # aguarda que haja lugar no buffer
      buffer.append(item)
      print('Produzido %s (ha %i itens no buffer)' % (item,len(buffer)))
      item_no_buffer.notify()

def consumidor():
  global buffer
  for i in range(10):
    with lock:
      if len(buffer) == 0:
        print('>>> Buffer vazio. Consumidor ira aguardar.')
        item_no_buffer.wait()   # aguarda que haja um item para consumir 
      item = buffer.pop(0)
      print('Consumido %s (ha %i itens no buffer)' % (item,len(buffer)))
      lugar_no_buffer.notify()
    sleep(randint(0,2))         # fica um tempo consumindo...

buffer = []
lista_produtores = []
lista_consumidores = []
num_thread = 2
tam_buffer = 5
lock = Lock()
lugar_no_buffer = Condition(lock)
item_no_buffer = Condition(lock)
for i in range(num_thread):
  lista_produtores.append(Thread(target=produtor,args=(i,)))
  lista_consumidores.append(Thread(target=consumidor))
  lista_produtores[i].start()
  lista_consumidores[i].start()
for i in range(num_thread):
  lista_produtores[i].join()
  lista_consumidores[i].join()