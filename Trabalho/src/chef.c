#include <stdlib.h>
#include "globals.h"
#include "chef.h"
#include "config.h"

//variável global para a refeição que acabou:
int refeicao_repor; 
//variável global para o buffet que precisa de reposição de alimento:
int buffet_repor;

void *chef_run()
{
    while (TRUE)
    {
        int buffets_vazios = 0;
        chef_check_food();
        for(int i = 0; i<globals_get_buffets_number(); i++){
            if(globals_get_buffets()[i].vazio ==1){
                //Incrementando número de buffets vazios:
                buffets_vazios++;
            }
        }
        //Se todos os buffets estão vazios o chef descansa:
        if(buffets_vazios == globals_get_buffets_number()){
            break;
        }
    }
    
    pthread_exit(NULL);
}


void chef_put_food()
{
//Chef faz post nas refeições do semáforo para repor comida:
    for (int i = 0; i< 40; i++){
        sem_post(&globals_get_buffets()[buffet_repor].sem_meal[refeicao_repor]);
    }
    return;
     
}
void chef_check_food()
{
    int num_buffets = globals_get_buffets_number();
    int enough_meal;
    //Evita que a função tente vericar os buffets antes que sejam inicializados:
    if(globals_get_buffets() == NULL) return;

        for(int i = 0; i< num_buffets; i++){
                 for(int x = 0; x < 5;x++){
                    sem_getvalue(&globals_get_buffets()[i].sem_meal[x], &enough_meal);
                    //Se valor do semáforo é 0, acabou comida:
                    if (enough_meal < 1){
                        refeicao_repor = x;
                        buffet_repor = i;
                        chef_put_food();
                        //Liberar o aluno de se servir só apos reabastecimento:
                        pthread_mutex_unlock(&globals_get_buffets()[i].mutex_trocar_comida);  
                        break;
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