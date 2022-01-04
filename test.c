#include <time.h>
#include <stdio.h>
// #include <stdlib.h>


int main() {
    char text[100];
    time_t now = time(NULL); // number of seconds in 4 months
    struct tm *t1 = localtime(&now);

    strftime(text, sizeof(text)-1, "%Y-%m-%d", t1);
    printf("Current Date: %s\n", text);

    now = time(NULL) - 10512000; // number of seconds in 4 months
    struct tm *t2 = localtime(&now);

    strftime(text, sizeof(text)-1, "%Y-%m-%d", t2);
    printf("Current Date: %s\n", text);

    return(0);
}