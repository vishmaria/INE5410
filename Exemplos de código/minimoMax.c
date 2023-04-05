#include <stdio.h>
#include <stdlib.h>

typedef struct MinMax
{
    int min;
    int max;
} MinMax;

MinMax *getMinMax (int *array, const int SIZE){
    // Aloca dinamicamente a estrutura:
    MinMax* structure = (MinMax*) malloc(sizeof(MinMax));
    // Iniciar min e max com o primeiro elemento:
    structure->min = array[0];
    structure->max = array[0];
    // Comparação simples de menor/maior
    for (int i = 0; i < SIZE; i++) if(array[i]< structure->min) structure->min = array[i];
    for (int i = 0; i < SIZE; i++) if(array[i]> structure->max) structure->max = array[i]; 

    return structure;
}
int main (void){
    int array[8] = {2, 10, 20, 40, 77, 39, 128, 64};
    // O retorno da função é um ponteiro para a struct
    MinMax* result = getMinMax(array, 8);
    printf ("%d\n%d\n", result->min, result->max);
    // Libera espaço alocado para a estrutura
    free(result);
    return 0;
}