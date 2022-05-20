#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <stdio.h>

//                          (principal)
//                               |
//              +----------------+--------------+
//              |                               |
//           filho_1                         filho_2
//              |                               |
//    +---------+-----------+          +--------+--------+
//    |         |           |          |        |        |
// neto_1_1  neto_1_2  neto_1_3     neto_2_1 neto_2_2 neto_2_3

// ~~~ printfs  ~~~
//      principal (ao finalizar): "Processo principal %d finalizado\n"
// filhos e netos (ao finalizar): "Processo %d finalizado\n"
//    filhos e netos (ao inciar): "Processo %d, filho de %d\n"

// Obs:
// - netos devem esperar 5 segundos antes de imprmir a mensagem de finalizado (e terminar)
// - pais devem esperar pelos seu descendentes diretos antes de terminar

int main(int argc, char** argv) {

    // ....

    /*************************************************
     * Dicas:                                        *
     * 1. Leia as intruções antes do main().         *
     * 2. Faça os prints exatamente como solicitado. *
     * 3. Espere o término dos filhos                *
     *************************************************/

    pid_t filho1, filho2;
    int n = 2;
    int m = 3;
    for (int i = 0; i < n; i++) {
        filho1 = fork();
        if (filho1 >= 0){
            if (filho1 == 0){
                printf("Processo %d, filho de %d\n", getpid(), getppid());
                for (int c = 0; c < m; c++) {
                    filho2 = fork();
                    if (filho2 >= 0){
                        if (filho2 ==0){
                            printf("Processo %d, filho de %d\n", getpid(), getppid());
                            break;
                        }
                        else{
                            sleep(5);
                            printf("Processo %d finalizado\n", filho2);
                        }
                    }
                }
                break;
            }
            else{
               wait(NULL);
               printf("Processo %d finalizado\n", filho1); 
               if (i == n-1) printf("Processo principal %d finalizado!\n", getpid());   
            }
        }
    }

    return 0;
}
