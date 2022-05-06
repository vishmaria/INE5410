#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <stdio.h>


//       (pai)      
//         |        
//    +----+----+
//    |         |   
// filho_1   filho_2


// ~~~ printfs  ~~~
// pai (ao criar filho): "Processo pai criou %d\n"
//    pai (ao terminar): "Processo pai finalizado!\n"
//  filhos (ao iniciar): "Processo filho %d criado\n"

// Obs:
// - pai deve esperar pelos filhos antes de terminar!


int main(int argc, char** argv) {

    // ....

    /*************************************************
     * Dicas:                                        *
     * 1. Leia as intruções antes do main().         *
     * 2. Faça os prints exatamente como solicitado. *
     * 3. Espere o término dos filhos                *
     *************************************************/
    pid_t filho1, filho2;
   /* if (filho1 >= 0){
        if (filho1 ==0){
            printf("Processo filho %d criado\n", getpid());
            wait(NULL);
        }
        else {
            printf("Processo pai criou %d\n", filho1);
            filho2 = fork();
            wait(NULL);
        }
    }*/

    for (int i = 0; i < 2; i++) {
        filho1 = fork();
        if (filho1 >= 0){
            if (filho1 == 0){
                printf("Processo filho %d criado\n", getpid());
                break;
            }
            else{
               printf("Processo pai criou %d\n", filho1);
               wait(NULL);
               if (i == 1) printf("Processo pai finalizado!\n");   
            }
        }
    }
    

     
    return 0;
}
