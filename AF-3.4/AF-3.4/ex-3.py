from multiprocessing import Process, Queue


def origem(fila1):
    for i in range(10):
        msg = 'Teste ' + str(i)
        # envia mensagem para a ponte pela fila 1
        fila1.put(msg)
        print('Mensagem enviada:', msg)


def ponte(fila1, fila2):
    for i in range(10):
        # recebe mensagem na fila 1
        msg = fila1.get()
        # reenvia mensagem na fila 2
        fila2.put(msg)
        print('Mensagem encaminhada:', msg)


def destino(fila2):
    for i in range(10):
        while fila2.empty() == False:
            msg = fila2.get()
            # recebe mensagem na fila 2
            print('Mensagem recebida:', msg)


if __name__ == '__main__':
    fila1 = Queue()
    fila2 = Queue()

    o = Process(target=origem, args=(fila1,))
    p = Process(target=ponte, args=(fila1, fila2))
    d = Process(target=destino, args=(fila2,))
    # executa os processos
    o.start()
    p.start()
    d.start()
    # aguarda conclusão
    o.join()
    p.join()
    d.join()
    # libera as filas
    # as filas devem ser encerradas por close()
    # seguido de join_thread()
    fila1.close
    fila1.join_thread()

    fila2.close()
    fila2.join_thread()
