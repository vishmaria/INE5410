#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int contador_global = 0;

void loop(n_loops){
    for (int i = 0; i<n_loops;i++){
        contador_global++;
    }
    return 0;
}

int main(int argc, char** argv) {
    int n_threads = atoi(argv[1]);
    int n_loops = atoi(argv[2]);
    pthread_t threads[n_threads];

    for(int i = 0; i < n_threads]; i++){
        pthread_create(&threads[i],NULL, loop, n_loops)
    }

    for (int i = 0; i < n_threads; ++i){
        pthread_join(threads[i], NULL);
    }
    printf("contador: %d\nesperado:", contador_global, n_loops);
}