#include <stdlib.h>
#include "globals.h"

queue_t *students_queue = NULL;
table_t *table = NULL;
buffet_t *buffets_ref = NULL;

int students_number;
int tables_number;
int buffets_number;
int seats_number;

void globals_set_seats_number(int x){
    seats_number = x;
    return;
}

int globals_get_seats_number(){
    return seats_number;
}

void globals_set_buffets_number(int x){
    buffets_number = x;
    return;
}

int globals_get_buffets_number(){
    return buffets_number;
}

void globals_set_tables_number(int x){
    tables_number = x;
    return;
}

int globals_get_tables_number(){
    return tables_number;
}

void globals_set_queue(queue_t *queue)
{
    students_queue = queue;
}

queue_t *globals_get_queue()
{
    return students_queue;
}

void globals_set_table(table_t *t)
{
    table = t;
}

table_t *globals_get_table()
{
    return table;
}


void globals_set_students(int number)
{
    students_number = number;
}

int globals_get_students()
{
    return students_number;
}

void globals_set_buffets(buffet_t *buffets)
{
    buffets_ref = buffets;
}

buffet_t *globals_get_buffets()
{
    return buffets_ref;
}


/**
 * @brief Finaliza todas as variáveis globais que ainda não foram liberadas.
 *  Se criar alguma variável global que faça uso de mallocs, lembre-se sempre de usar o free dentro
 * dessa função.
 */
void globals_finalize()
{
    free(table);
}