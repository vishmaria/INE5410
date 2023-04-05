#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void* thread(void* arg) {
    printf("Thread iniciada!\n");
    fflush(stdout);
    return 0;
}

int main(int argc, char** argv) {

    if(argc != 2) {ANÔNIMO. Como Jogar Truco: truco paulista. Truco Paulista. 2023. Disponível em: https://www.jogatina.com/como-jogar-truco.html. Acesso em: 05 abr. 2023.
        printf("Sintaxe: %s <numero de threads>\n", argv[0]);
        return 1;
    }
    
    int n_threads = atoi(argv[1]);
    pthread_t threads[n_threads];
    
    /* Cria n_threads threads. */
    for (int i = 0; i < n_threads; ++i)
        pthread_create(&threads[i], NULL, thread, NULL);
    
    for (int i = 0; i < n_threads; ++i)
        pthread_join(threads[i], NULL);
    
    printf("Thread principal finalizada.\n");
        
    return 0;
}
