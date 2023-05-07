#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>
#include <time.h>
#include <stdlib.h>

FILE* out;

sem_t semaphore_a, semaphore_b;

// O funcionamento sera similar ao exemplo do slide, onde existe um numero finito de tokens gerenciado pelos posts opostos nas funcoes.
// Nesse caso cada contador inicia com um token, fazendo com que no maximo cada funcao tenha dois tokens para print
// garantindo que a diferenca entra As e Bs em qualquer posicao sempre seja <= 1

void *thread_a(void *args) {
    for (int i = 0; i < *(int*)args; ++i) {
	//      +---> arquivo (FILE*) destino
	//      |    +---> string a ser impressa
	//      v    v
        sem_wait(&semaphore_a);
        fprintf(out, "A");
        // Importante para que vocês vejam o progresso do programa
        // mesmo que o programa trave em um sem_wait().
        fflush(stdout);
        sem_post(&semaphore_b);
    }
    return NULL;
}

void *thread_b(void *args) {
    for (int i = 0; i < *(int*)args; ++i) {
        sem_wait(&semaphore_b);
        fprintf(out, "B");
        fflush(stdout);
        sem_post(&semaphore_a);
    }
    return NULL;
}

int main(int argc, char** argv) {
    if (argc < 2) {
        printf("Uso: %s [ITERAÇÕES]\n", argv[0]);
        return 1;
    }
    int iters = atoi(argv[1]);
    srand(time(NULL));
    out = fopen("result.txt", "w");

    pthread_t ta, tb;

    // Inicia os semaforos com contador em 1.
    sem_init(&semaphore_a, 0, 1);
    sem_init(&semaphore_b, 0, 1);

    // Cria threads
    pthread_create(&ta, NULL, thread_a, &iters);
    pthread_create(&tb, NULL, thread_b, &iters);

    // Espera pelas threads
    pthread_join(ta, NULL);
    pthread_join(tb, NULL);

    // Destroi os semaforos
    sem_destroy(&semaphore_a);
    sem_destroy(&semaphore_b);

    //Imprime quebra de linha e fecha arquivo
    fprintf(out, "\n");
    fclose(out);
  
    return 0;
}