#include <stdio.h>
#include <stdlib.h>
#define MAX_SIZE 100
// Comparação ascedente
int sortAscending(int * num1, int * num2) {
    return (*num1 - *num2);
}

// Comparação descendente
int sortDescending(int * num1, int * num2) {
    return (*num2 - *num1);
}

// Dividir o array em duas partes
int partition(int * arr, int low, int high, int (* compare)(int *, int *)) {
    int pivot = arr[high];
    int i = low - 1;

    // Elementos a esquerda do pivo são menores que ele e a direita são maiores
    for (int j = low; j <= high - 1; j++) {
        if (compare(&arr[j], &pivot) < 0) {
            i++;
            int temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
        }
    }
    int temp = arr[i+1];
    arr[i+1] = arr[high];
    arr[high] = temp;

    // Retorna a posição do pivô
    return (i + 1);
}

// Implementando quick sort
void quickSort(int * arr, int low, int high, int (* compare)(int *, int *)) {
    // Usa função de dividir para ordenar as duas partes em chamadas recursivas
    if (low < high) {
        int pi = partition(arr, low, high, compare);
        quickSort(arr, low, pi - 1, compare);
        quickSort(arr, pi + 1, high, compare);
    }
}

// Ordenar array
void sort(int * arr, int size, int (* compare)(int *, int *)) {
    quickSort(arr, 0, size - 1, compare);
}

void inputArray(int *array, int size){
    for (int i = 0; i< size; i++){
        printf("Enter array[%d]: ", i);
        // Deve utilizar &array para não ocorrer segmentation fault porque a posição não está inicializada
        scanf("%d", &array[i]);
    } 
}

void printArray (int *array, int size){
    for (int i = 0; i< size; i++) printf("%d, ", array[i]);
    printf("\n");
}
int main(){
    int arr[MAX_SIZE];
    int size;
    /*
    * Input array size and elements.
    */
    printf("Enter array size: ");
    scanf("%d", &size);
    printf("Enter elements in array:\n");
    inputArray(arr, size);
    printf("\n\nElements before sorting: ");
    printArray(arr, size);
    // Sort and print sorted array in ascending order.
    printf("\n\nArray in ascending order: ");
    sort(arr, size, sortAscending);
    printArray(arr, size);
    // Sort and print sorted array in descending order.
    printf("\nArray in descending order: ");
    sort(arr, size, sortDescending);
    printArray(arr, size);

    return 0;
}