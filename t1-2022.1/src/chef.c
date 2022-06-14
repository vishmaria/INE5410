#include <stdlib.h>

#include "chef.h"
#include "config.h"

void *chef_run()
{
    /* Insira sua lógica aqui */
    while (TRUE)
    {
        //Permanece olhando os buffets, check_food em cada um
    
        msleep(5000); /* Pode retirar este sleep quando implementar a solução! */
    }
    
    pthread_exit(NULL);
}


void chef_put_food()
{
    /* Bacia vazia, trava a fila, coloca comida e libera*/
}
void chef_check_food()
{
    /* Uma iteração para olhar buffet e uma para as bacias por fila */
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