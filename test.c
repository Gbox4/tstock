// Gabe Banks
// 1/3/22
// APCSP CS50 Unit Final Project

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

double map(double x, double l1, double h1, double l2, double h2);
int main(int argc, char *argv[]);


double map(double x, double l1, double h1, double l2, double h2) {
    return (((x-l1)/(h1-l1)) * (h2-l2)) + l2;
}

int main(int argc, char *argv[]) {

    printf("%f\n", map(1, 0,2, 0,3));

    return(0);
}