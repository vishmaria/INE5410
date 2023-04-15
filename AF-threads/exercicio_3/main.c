#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <stdio.h>
#include <pthread.h>

// Lê o conteúdo do arquivo filename e retorna um vetor E o tamanho dele
// Se filename for da forma "gen:%d", gera um vetor aleatório com %d elementos
//
// +-------> retorno da função, ponteiro para vetor malloc()ado e preenchido
// |
// |         tamanho do vetor (usado <-----+
// |         como 2o retorno)              |
// v                                       v
double *load_vector(const char *filename, int *out_size);

// Avalia se o prod_escalar é o produto escalar dos vetores a e b. Assume-se
// que ambos a e b sejam vetores de tamanho size.
void avaliar(double *a, double *b, int size, double prod_escalar);
typedef struct data_t
{
    double *a;
    double *b;
    double *c;
    int start;
    int end;
    int i;
} data_t;

// Função executada pelas threads:
void *thread(void *arg)
{
    data_t dt = *((data_t *)arg);
    dt.c[dt.i] = 0;
    // A multiplicacao é acumulada no vetor de resultado
    for (size_t i = dt.start; i < dt.end; ++i)
    {
        dt.c[dt.i] += dt.a[i] * dt.b[i];
    }
    pthread_exit(NULL);
}
int main(int argc, char *argv[])
{
    srand(time(NULL));

    // Temos argumentos suficientes?
    if (argc < 4)
    {
        printf("Uso: %s n_threads a_file b_file\n"
               "    n_threads    número de threads a serem usadas na computação\n"
               "    *_file       caminho de arquivo ou uma expressão com a forma gen:N,\n"
               "                 representando um vetor aleatório de tamanho N\n",
               argv[0]);
        return 1;
    }

    // Quantas threads?
    int n_threads = atoi(argv[1]);
    if (!n_threads)
    {
        printf("Número de threads deve ser > 0\n");
        return 1;
    }
    // Lê números de arquivos para vetores alocados com malloc
    int a_size = 0, b_size = 0;
    double *a = load_vector(argv[2], &a_size);
    if (!a)
    {
        // load_vector não conseguiu abrir o arquivo
        printf("Erro ao ler arquivo %s\n", argv[2]);
        return 1;
    }
    double *b = load_vector(argv[3], &b_size);
    if (!b)
    {
        printf("Erro ao ler arquivo %s\n", argv[3]);
        return 1;
    }
    // Garante que entradas são compatíveis
    if (a_size != b_size)
    {
        printf("Vetores a e b tem tamanhos diferentes! (%d != %d)\n", a_size, b_size);
        return 1;
    }
    // Não pode haver mais threads que o tamanho do vetor
    if (n_threads > a_size)
    {
        n_threads = a_size;
    }
    data_t data_threads[n_threads];
    // Cria as threads:
    pthread_t threads[n_threads];
    // Quantas somas cada thread executa
    int sum_thread = a_size / n_threads;

    // Cria vetor do resultado
    double *c = calloc(n_threads, n_threads * sizeof(double));
    double result = 0;

    for (int i = 0; i < n_threads; i++)
    {
        int start = i * sum_thread;
        int end = start + sum_thread;
        if (i == n_threads - 1)
        {
            end = a_size;
        }

        data_threads[i].a = a;
        data_threads[i].b = b;
        data_threads[i].c = c;
        data_threads[i].i = i;
        data_threads[i].start = start;
        data_threads[i].end = end;

        pthread_create(&threads[i], NULL, thread, (void *)&data_threads[i]);
    }

    for (int i = 0; i < n_threads; ++i)
        pthread_join(threads[i], NULL);

    // A soma deve ser computada apos join() para resultado correto
    for (size_t i = 0; i < n_threads; i++)
        result += c[i];
    //    +---------------------------------+
    // ** | IMPORTANTE: avalia o resultado! | **
    //    +---------------------------------+
    avaliar(a, b, a_size, result);

    // Libera memória
    free(a);
    free(b);
    free(c);

    return 0;
}
