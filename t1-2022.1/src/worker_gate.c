#include <stdlib.h>

#include "worker_gate.h"
#include "globals.h"
#include "config.h"



void worker_gate_look_queue()
{
    /* Verificar se há alunos na fila */
}

void worker_gate_remove_student()
{
    /* Permite 1 estudante sair da fila dos estudantes 
    e entrar na fila do buffet por vez */
}

void worker_gate_look_buffet()
{
    /* Verifica se o buffet está cheio */

}

void *worker_gate_run(void *arg)
{
    int all_students_entered;
    int number_students;

    number_students = *((int *)arg);
    all_students_entered = number_students > 0 ? FALSE : TRUE;

    while (all_students_entered == FALSE)
    {
        worker_gate_look_queue();
        worker_gate_look_buffet();
        worker_gate_remove_student();
        msleep(5000); /* Pode retirar este sleep quando implementar a solução! */
    }

    pthread_exit(NULL);
}

void worker_gate_init(worker_gate_t *self)
{
    int number_students = globals_get_students();
    pthread_create(&self->thread, NULL, worker_gate_run, &number_students);
}

void worker_gate_finalize(worker_gate_t *self)
{
    pthread_join(self->thread, NULL);
    free(self);
}

void worker_gate_insert_queue_buffet(student_t *student)
{
    /* estudante entra na fila do buffet */
}