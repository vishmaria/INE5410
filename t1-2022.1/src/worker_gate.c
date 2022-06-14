#include <stdlib.h>
#include "worker_gate.h"
#include "globals.h"
#include "config.h"
#include <pthread.h>
#include <semaphore.h>

sem_t semaphore_gate; // semáforo de controle de catraca,
pthread_mutex_t mutex_insert_fila;
student_t* student_buffer;


void worker_gate_look_queue()
{
    /* Verificar se há alunos na fila */
    while (globals_get_queue()->_length == 0) msleep(5); //Enquanto não tiver gente ele dorme.
        
}

void worker_gate_remove_student()
{
    /* Permite 1 estudante sair da fila dos estudantes 
    e entrar na fila do buffet por vez */

    //sem_wait(&semaphore_gate); // semaforo nao permite que outro aluno seja retirado da fila antes que o aluno anterior tenha sido colocado em um buffet
    student_buffer = queue_remove(globals_get_queue()); // student_buffer = aluno que passou a catraca e ainda será encaminhado para um buffet

        printf("%d\n", student_buffer -> _id);
    
}

void worker_gate_look_buffet(student_t* student) // Procura um buffet disponível e envia o estudante pra lá.
{
    /* Verifica se o buffet está cheio */
    buffet_t* buffets = globals_get_buffets();
    //sem_wait(&semaphore_gate);
    printf("AAAAAAAAA %d \n\n",buffets[1].queue_left[0]);
    while(1){
        for(int i = 0; i < 2; i++){ // FIX trocar por numero de buffets
            if(!(buffets[i].queue_left[0])){ // queue_left[0] está vazio? 
                student->left_or_right = 'L';
                student->_id_buffet = i; //determina o buffet para qual o aluno vai
                buffet_queue_insert(buffets, student); //insere na fila
                return;
            }
            else if(!(buffets[i].queue_right[0])){
                student->left_or_right = 'R';
                student->_id_buffet = i;
                buffet_queue_insert(buffets, student);
                return;
            } 
        // se não localizou nenhum lugar espera até um estudante sair do buffet
        //sem_wait(&sem_buffet);
        }
    }

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
        worker_gate_remove_student();
        number_students--;
        worker_gate_look_buffet(student_buffer);
        //worker_gate_remove_student(); // um estudante a menos aguardando entrada

        
    }
   // sem_destroy(&sem_buffet); // se todos os estudantes entraram destrói o semáforo
    pthread_exit(NULL);
}

void worker_gate_init(worker_gate_t *self)
{
    int number_students = globals_get_students();
    sem_init(&semaphore_gate, 0, 1);
    pthread_mutex_init(&mutex_insert_fila, 0);
    pthread_create(&self->thread, NULL, worker_gate_run, &number_students);
}

void worker_gate_finalize(worker_gate_t *self)
{
    sem_destroy(&semaphore_gate);
    pthread_join(self->thread, NULL);
    free(self);
}

void worker_gate_insert_queue_buffet(student_t *student)
{
    pthread_mutex_lock(&mutex_insert_fila); // mutex para impedir data-race na inserção na fila.
    queue_insert(globals_get_queue(), student);
    pthread_mutex_unlock(&mutex_insert_fila);

    
    /*buffet_t* buffets = globals_get_buffets();
    printf("id: %d",buffets[1]._id);
    buffet_queue_insert(buffets, student); // insere o aluno em um buffet
    //sem_post(&semaphore_gate); //libera a entrada do próximo aluno.*/

}
    
   