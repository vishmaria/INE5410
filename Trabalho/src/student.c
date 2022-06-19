#include <time.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdio.h>
#include <semaphore.h>
#include "student.h"
#include "config.h"
#include "worker_gate.h"
#include "globals.h"
#include "table.h"

void* student_run(void *arg)
{
    student_t *self = (student_t*) arg;
    table_t *tables  = globals_get_table();

    worker_gate_insert_queue_buffet(self);
    while(self->_buffet_position < 0); //enquanto não entrou em um buffet. Não pode se servir.
    student_serve(self);
    student_seat(self, tables);
    msleep(500);
    student_leave(self, tables);

    pthread_exit(NULL);
};

void student_seat(student_t *self, table_t *table)
{
    int num_tables = globals_get_tables_number();
    while(1){
        for(int i = 0; i < num_tables; i++){ //FALTA GARANTIR QUE DOIS CARAS NÃO SENTEM NO MESMO LUGAR (obs: por que é gay)
            if(table[i]._empty_seats > 0){
                //estudante senta numa mesa e diminui número de lugares vazios
                sem_wait(&table[i].sem_lugares);//isso poderia garantir que os caras não estão sentando no mesmo lugar.
                pthread_mutex_lock(&globals_get_table()[i].mutex_decremento_lugares);
                table[i]._empty_seats--;
                self-> _id_table = table[i]._id;
                pthread_mutex_unlock(&globals_get_table()[i].mutex_decremento_lugares);
                /*printf("\n\n self-id_table: %d  table-id %d", self->_id_table, table[i]._id);
                
                printf("\n aluno: %d esta comendo na mesa %d\n",self->_id, table[i]._id);
                printf("Restam %d lugares vazios na mesa %d\n\n", table[i]._empty_seats, table[i]._id);*/
                return;
            }
        }
    }
    
}

void student_serve(student_t *self)
{
    int i = 0;
    while(i<5){
        //printf("estudante %d, buffet %d, fila %c , posicao %d \n",self->_id, self->_id_buffet, self->left_or_right, self->_buffet_position);
        if(self->_wishes[i] == 1){
            if(globals_get_buffets()[self->_id_buffet]._meal[i] < 2){
              pthread_mutex_lock(&globals_get_buffets()[i].mutex_trocar_comida); // se faltou comida em uma bacia, espera até o chefe destravar.
            }
            globals_get_buffets()[self->_id_buffet]._meal[i]--;
           printf("Aluno %d pegou comida %d, ainda tem %d refeicoes\n", self->_id, i, globals_get_buffets()[self->_id_buffet]._meal[i]);
        }
        buffet_next_step(globals_get_buffets(), self);
        //msleep(1000);
    i++;
    }

}

void student_leave(student_t *self, table_t *table)
{
    int num_tables = globals_get_tables_number();
     for(int i = 0; i < num_tables; i++){ 
        //estudante sai e aumenta número de lugares vazios:
        if (self-> _id_table == table[i]._id){
            table[i]._empty_seats++;
            sem_post(&table[i].sem_lugares);//isso poderia garantir que os caras não estão sentando no mesmo lugar.
            //printf("O aluno %d saiu. mesa %d valor atual de empty seat: %d\n", self-> _id, table[i]._id, table[i]._empty_seats);
            return;
            
        }
    }
    //FALTA MANDAR OS CARAS IREM EMBORA E DEPOIS DISSO PROCURAR OS MUTEXES E SEMAFOROS QUE PRECISAM SER DESTRUIDOS.
}

/* --------------------------------------------------------- */
/* ATENÇÃO: Não será necessário modificar as funções abaixo! */
/* --------------------------------------------------------- */

student_t *student_init()
{
    student_t *student = malloc(sizeof(student_t));
    student->_id = rand() % 1000;
    student->_buffet_position = -1;
    int none = TRUE;
    for (int j = 0; j <= 4; j++)
    {
        student->_wishes[j] = _student_choice();
        if(student->_wishes[j] == 1) none = FALSE;
    }

    if(none == FALSE){
        /* O estudante só deseja proteína */
        student->_wishes[3] = 1;
    }

    return student;
};

void student_finalize(student_t *self){
    free(self);
};


pthread_t students_come_to_lunch(int number_students)
{
    pthread_t lets_go;
    pthread_create(&lets_go, NULL, _all_they_come, &number_students);
    return lets_go;
}

/**
 * @brief Função (privada) que inicializa as threads dos alunos.
 * 
 * @param arg 
 * @return void* 
 */
void* _all_they_come(void *arg)
{
    int number_students = *((int *)arg);
    
    student_t *students[number_students];

    for (int i = 0; i < number_students; i++)
    {
        students[i] = student_init();                                               /* Estudante é iniciado, recebe um ID e escolhe o que vai comer*/
    }

    for (int i = 0; i < number_students; i++)
    {
        pthread_create(&students[i]->thread, NULL, student_run, students[i]);       /*  Cria as threads  */
    }

    for (int i = 0; i < number_students; i++)
    {
        pthread_join(students[i]->thread, NULL);                                    /*  Aguarda o término das threads   */
    }

    for (int i = 0; i < number_students; i++)
    {
        student_finalize(students[i]);                                              /*  Libera a memória de cada estudante  */
    }

    pthread_exit(NULL);
}

/**
 * @brief Função que retorna as escolhas dos alunos, aleatoriamente (50% para cada opção)
 *        retornando 1 (escolhido) 0 (não escolhido). É possível que um aluno não goste de nenhuma opção
 *         de comida. Nesse caso, considere que ele ainda passa pela fila, como todos aqueles que vão comer.
 * @return int 
 */
int _student_choice()
{
    float prob = (float)rand() / RAND_MAX;
    return prob > 0.51 ? 1 : 0;
}