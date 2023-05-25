
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

//int gValue = 0;
// pthread_mutex_t gMtx;
// pthread_mutexattr_t attrs;

// Função imprime resultados na correção do exercício -- definida em helper.c
void imprimir_resultados(int n, int** results);

// Função escrita por um engenheiro
// Soluçao: compute() retorna o enesimo elemento da sequencia de Fibonacci.
// Existem varios exemplos para implementa-la, este usa variaveis privadas 
// à funçao e um retorno, eliminando a necessidade de mutex.
// gValue também não será necessaria?
int compute(int arg) {
    if (arg < 2){
        return arg;
    } else {
        // Fn = Fn-1 + Fn-2
        return (compute(arg-1)+ compute(arg-2));
    }
}

// Função wrapper que pode ser usada com pthread_create() para criar uma 
// thread que retorna o resultado de compute(arg
void* compute_thread(void* arg) {
    int value  = 0;
    value = compute(*((int*)arg));
    int* ret = malloc(sizeof(int));
    // pthread_mutex_lock(&gMtx); 
    *ret = value;
    // pthread_mutex_unlock(&gMtx);
    return ret;
}


int main(int argc, char** argv) {
    // Temos n_threads?
    if (argc < 2) {
        printf("Uso: %s n_threads x1 x2 ... xn\n", argv[0]);
        return 1;
    }
    // n_threads > 0 e foi dado um x para cada thread?
    int n_threads = atoi(argv[1]);
    if (!n_threads || argc < 2+n_threads) {
        printf("Uso: %s n_threads x1 x2 ... xn\n", argv[0]);
        return 1;
    }

    //Inicializa o mutex
    // pthread_mutexattr_init(&attrs);
    // pthread_mutexattr_settype(&attrs, PTHREAD_MUTEX_RECURSIVE);
    // pthread_mutex_init(&gMtx, &attrs);

    int args[n_threads];
    int* results[n_threads];
    pthread_t threads[n_threads];
    //Cria threads repassando argv[] correspondente
    for (int i = 0; i < n_threads; ++i)  {
        args[i] = atoi(argv[2+i]);
        pthread_create(&threads[i], NULL, compute_thread, &args[i]);
    }
    // Faz join em todas as threads e salva resultados
    for (int i = 0; i < n_threads; ++i)
        pthread_join(threads[i], (void**)&results[i]);

    // Não usaremos mais o mutex
    // pthread_mutexattr_destroy(&attrs);
    // pthread_mutex_destroy(&gMtx);

    // Imprime resultados na tela
    // Importante: deve ser chamada para que a correção funcione
    imprimir_resultados(n_threads, results);

    // Faz o free para os resultados criados nas threads
    for (int i = 0; i < n_threads; ++i) 
        free(results[i]);
    
    return 0;
}
