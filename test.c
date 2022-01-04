// Gabe Banks
// 1/3/22
// APCSP CS50 Unit Final Project

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

#include <wchar.h>
#include <locale.h>

double map(double x, double l1, double h1, double l2, double h2);
int main(int argc, char *argv[]);


double map(double x, double l1, double h1, double l2, double h2) {
    return (((x-l1)/(h1-l1)) * (h2-l2)) + l2;
}

int main(int argc, char *argv[]) {

    setlocale(LC_CTYPE, "");

    int maxX = 10;
    int maxY = 10;
    int i = 0;
    int j = 0;

    char graph[maxY][maxX];

    for (i = 0; i < maxY; i++) {
        for (j = 0; j < maxX; j++) {
            graph[i][j] = ' ';
        }
    }
    

    for (i=0; i<maxX; i++) {
        graph[0][i] = '─';
        graph[maxY-1][i] = '─';
    } 

    // char x[] = "----------";

    // strcpy(graph[0], x);
    // strcpy(graph[maxY-1], x);

    for (i=0; i<maxY; i++) {
        printf("%s\n", graph[i]);
    }
}