#include <stdlib.h>
#include "table.h"
#include "globals.h"


/* --------------------------------------------------------- */
/* ATENÇÃO: Não será necessário modificar as funções abaixo! */
/* --------------------------------------------------------- */

table_t *table_init(int number_of_tables, int seats_per_table)
{
    globals_set_tables_number(number_of_tables);
    globals_set_seats_number(seats_per_table);
    
    table_t *new_tables = malloc(sizeof(table_t) * number_of_tables);
    for (int i = 0; i < number_of_tables; i++)
    {
        new_tables[i]._id = i;
        new_tables[i]._empty_seats = seats_per_table;
        new_tables[i]._max_seats = seats_per_table;
    }

    return new_tables;
}