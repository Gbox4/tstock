#include <stdio.h>
#include <wchar.h>
#include <locale.h>


int main() {
    printf("\x1b[31mhello\n");
    printf("\x1b[32mhello\n");
    printf("\x1b[0mhello\n");

    return(0);
}