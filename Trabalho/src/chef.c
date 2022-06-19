#include <stdlib.h>
#include "globals.h"
#include "chef.h"
#include "config.h"

//variável global para o buffet que precisa de reposição de alimento
int *refeicao_repor = NULL; 

void *chef_run()
{
    while (TRUE)
    {
        chef_check_food();
        //msleep(5000); /* Pode retirar este sleep quando implementar a solução! */
    }
    
    pthread_exit(NULL);
}


void chef_put_food()
{
    //Comida volta a quantidade máxima
    *refeicao_repor = 40;
    return;    
}
void chef_check_food()
{
    int num_buffets = globals_get_buffets_number();
    //evita que a função tente vericar os buffets antes que sejam inicializados:
    if(globals_get_buffets() == NULL) return;
        for(int i = 0; i< num_buffets; i++){
            //se o mutex foi trancado por outra função pode por comida:
            if((pthread_mutex_trylock(&globals_get_buffets()[i].mutex_trocar_comida)) == -1){ 
                printf("TRAVEI TODO O BUFFET\n");
                 for(int x = 0; x<5;x++){                                               
                    if(globals_get_buffets()[i]._meal[x] < 2){ // verifica em qual posição da fila está faltando comida.
                        //informa a comida faltante e chama o chefe para colocar mais:
                        refeicao_repor = &globals_get_buffets()[i]._meal[x];
                        chef_put_food();
                        //libera a fila trancada.
                        pthread_mutex_unlock(&globals_get_buffets()[i].mutex_trocar_comida);
                        printf("TROCANDO A BACIA DE COMIDA %d\n", x); //FIX: DELETAR ANTES DE ENVIAR
                        
                        break;
                    }
                    }
                
            }
            //check_food() trancou o mutex em vez do estudante, deve liberar:
            else pthread_mutex_unlock(&globals_get_buffets()[i].mutex_trocar_comida);
        }
    
}

/* --------------------------------------------------------- */
/* ATENÇÃO: Não será necessário modificar as funções abaixo! */
/* --------------------------------------------------------- */

void chef_init(chef_t *self)
{
    pthread_create(&self->thread, NULL, chef_run, NULL);
}

void chef_finalize(chef_t *self)
{
    pthread_join(self->thread, NULL);
    free(self);
}