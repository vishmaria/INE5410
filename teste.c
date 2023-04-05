#include <stdio.h>
#include <string.h>
typedef struct {
    float x, y;
} ponto_t;
int main() {
    ponto_t q = {23.0, 27.0};
    ponto_t* p = &q;
    p->x++;
}