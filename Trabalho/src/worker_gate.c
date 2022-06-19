#include <stdlib.h>
#include <pthread.h>
#include "worker_gate.h"
#include "globals.h"
#include "config.h"
#include <semaphore.h>
pthread_mutex_t mutex_insere_fila; //mutex para inserir um aluno no fim da fila. 
pthread_mutex_t mutex_decrementa_alunos; //mutex para evitar datarace na subtração de number_students.
pthread_mutex_t mutex_ler_fila; //mutex para garantir que exclusão mutua na leitura e escrita da frente da fila.



void worker_gate_look_queue()
{

    //Enquanto a fila esta vazia, não deixa continuar. Isto serve para que o worker_gate não tente realizar operações sobre uma fila vazia
    pthread_mutex_lock(&mutex_ler_fila); 
    while(globals_get_queue()->_length == 0); 
    pthread_mutex_unlock(&mutex_ler_fila);
    return;
}

void worker_gate_remove_student()
{
    //Remove o primeiro estudante da fila e o insere no buffet.
    //pthread_mutex_lock(&mutex_ler_fila); 
    student_t *student = queue_remove(globals_get_queue());
    //pthread_mutex_unlock(&mutex_ler_fila);
    buffet_t *buffets = globals_get_buffets();
    buffet_queue_insert(buffets, student);
    //printf("Removi o estudante %d da fila do Ru\n\n", student-> _id);
}

void worker_gate_look_buffet()
{
    // Olha para onde tem lugar livre no buffet e define para onde o próximo aluno a entrar no buffet deve ir.
    pthread_mutex_lock(&mutex_ler_fila);
    student_t *student = globals_get_queue()->_first->_student;
    pthread_mutex_unlock(&mutex_ler_fila);
    buffet_t *buffets = globals_get_buffets();
    int num_buffets = globals_get_buffets_number();

    while(1){
        // Atribui o primeiro aluno da fila a um buffet e fila.
        for(int i = 0; i < num_buffets; i++){ 
            /*Verifica se a primeira posição da fila esquerda está livre*/
            if(pthread_mutex_trylock(&buffets[i].mutex_posicao_left[0]) == 0){  //tenta dar lock na primeira posição da fila a esquerda (está disponível)
                student->left_or_right = 'L'; 
                student->_id_buffet = i;            
                return;
            }
            //se primeira posição da esquerda não está livre vai para a fila direita
            else if(pthread_mutex_trylock(&buffets[i].mutex_posicao_right[0]) == 0){  //tenta dar lock na primeira posição da fila a direita (está disponível?)
                student->left_or_right = 'R';       
                student->_id_buffet = i;         
                return;
            }
        }
        // Repete o laço enquanto não encontrar um lugar vago nos buffets.
    }    

}

void *worker_gate_run(void *arg)
{

    int number_students;

    number_students = *((int *)arg);

    while (number_students > 1)
    {
        worker_gate_look_queue(); //Ve se a fila não esta vazia
        worker_gate_look_buffet(); //Olha para ver se e onde tem lugar vazio nas primeiras posições dos buffets e define onde o primeiro estudante da fila vai.
        worker_gate_remove_student(); //tira o estudante da fila e o insere no buffet.
        pthread_mutex_lock(&mutex_decrementa_alunos); 
        number_students--; //reduz o numero de estudantes da fila.
        pthread_mutex_unlock(&mutex_decrementa_alunos);
        //msleep(5000); /* Pode retirar este sleep quando implementar a solução! */
    }
    globals_set_students(0);
    printf("\n\nAcabou gente na fila externa\n\n");
    pthread_exit(NULL);
}

void worker_gate_init(worker_gate_t *self)
{
    int number_students = globals_get_students();
    int number_of_tables = globals_get_tables_number();
    pthread_mutex_init(&mutex_insere_fila, 0);
    pthread_mutex_init(&mutex_decrementa_alunos, 0);
    pthread_mutex_init(&mutex_ler_fila, 0);
    for (int i = 0; i < number_of_tables; i++)
    {
        sem_init(&globals_get_table()[i].sem_lugares, 0, globals_get_seats_number()); //ATENÇÃO: TEM QUE DESTRUIR ESSA PORRA.
        pthread_mutex_init(&globals_get_table()[i].mutex_decremento_lugares, 0);
        
    }
    pthread_create(&self->thread, NULL, worker_gate_run, &number_students);
}

void worker_gate_finalize(worker_gate_t *self)
{   
    pthread_mutex_destroy(&mutex_insere_fila);
    pthread_mutex_destroy(&mutex_decrementa_alunos);
    pthread_mutex_destroy(&mutex_ler_fila);
    for (int i = 0; i < globals_get_buffets_number(); i++)
    {
        pthread_mutex_destroy(&globals_get_buffets()[i].mutex_trocar_comida);

        for(int j= 0; j< 5; j++){
            pthread_mutex_destroy(&globals_get_buffets()[i].mutex_posicao_left[j]);
            pthread_mutex_destroy(&globals_get_buffets()[i].mutex_posicao_right[j]);
        }
    }
    pthread_join(self->thread, NULL);
    free(self);
}

void worker_gate_insert_queue_buffet(student_t *student)
{

    pthread_mutex_lock(&mutex_insere_fila);
    queue_insert(globals_get_queue(), student); //insere um estudante na fila pro buffet.
    pthread_mutex_unlock(&mutex_insere_fila);

}