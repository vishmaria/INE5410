#include <stdlib.h>
#include "globals.h"
#include "chef.h"
#include "config.h"

void *chef_run()
{
    /* Insira sua lógica aqui */
    while (TRUE)
    {
        chef_check_food();
        chef_put_food();
        //msleep(5000); /* Pode retirar este sleep quando implementar a solução! */
    }
    
    pthread_exit(NULL);
}


void chef_put_food()
{
    /* Insira sua lógica aqui */
}
void chef_check_food()
{
    if(globals_get_buffets() == NULL) return;
        for(int i = 0; i< 2; i++){ //trocar 2 por num_buffets;
            if((pthread_mutex_trylock(&globals_get_buffets()[i].mutex_trocar_comida))){ //se o mutex estiver trancado:
                for(int x = 0; x<5;x++){                                               // verifica em qual posição da fila está faltando comida.
                    if(globals_get_buffets()[i]._meal[x] < 0){ 
                        globals_get_buffets()[i]._meal[x] = 40; //trocar 40 por 20 caso a solução seja dividar cada bacia em duas.
                        printf("TROCANDO A BACIA DE COMIDA\n"); //FIX: DELETAR ANTES DE ENVIAR
                        pthread_mutex_unlock(&globals_get_buffets()[i].mutex_trocar_comida); //libera a fila trancada.
                    }
                }
            }
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