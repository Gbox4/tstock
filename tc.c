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

    // Check for right number of arguments
    if (argc != 2) {
        printf("Usage: ./tc TICKER\n");
        return 1;
    }

    setlocale(LC_CTYPE, "");

    int maxX = 100;
    int maxY = 30;

    double ath = 99999999;
    double atl = 0;

    char data[10000];
    int i = 0;
    int j = 0;
    char tempPriceStr[50];
    double tempPrice;

    FILE *p;
    int ch;
    char cmd[] = "curl -s \"http://api.marketstack.com/v1/eod?access_key=81febc3f2c33df988a02f8e763e76358&date_from=2021-12-24&date_to=2022-01-03&symbols=";
    strcat(cmd, argv[1]);
    strcat(cmd, "\"");

    p = popen(cmd,"r");

    if( p == NULL)
    {
        puts("Unable to open process");
        return(1);
    }

    while( (ch=fgetc(p)) != EOF) {
        data[i] = ch;
        i++;
    }
    pclose(p);

    printf("%s\n", data);

    // This shouldn't exceed 30 rows, I'm only gonna pull 30 days worth of data
    // Each row is of the shape: [Open, high, low, close]
    double barData[50][4];
    int bari = 0;

    i = 0;
    // looking for either 0=open, 1=high, 2=low, 3=close
    int looking = 0;
    while (data[i] != ']') {
        switch(looking){
            case 0:
                if (data[i-1]=='"' && data[i]=='o' && data[i+1]=='p' && data[i+2]=='e' && data[i+3]=='n' ) {
                    looking = 1;
                    j = i+6;
                    while (data[j] != ',') {
                        tempPriceStr[j-i-6] = data[j];
                        j++;
                    }
                    tempPriceStr[j-i-5] = '\0';
                    tempPrice = atof(tempPriceStr);
                    barData[bari][0] = tempPrice;
                }
                break;
            case 1:
                if (data[i-1]=='"' && data[i]=='h' && data[i+1]=='i' && data[i+2]=='g' && data[i+3]=='h' ) {
                    looking = 2;
                    j = i+6;
                    while (data[j] != ',') {
                        tempPriceStr[j-i-6] = data[j];
                        j++;
                    }
                    tempPriceStr[j-i-5] = '\0';
                    tempPrice = atof(tempPriceStr);
                    barData[bari][1] = tempPrice;
                    if (tempPrice > ath) {
                        ath = tempPrice;
                    }
                }
                break;
            case 2:
                if (data[i-1]=='"' && data[i]=='l' && data[i+1]=='o' && data[i+2]=='w' ) {
                    looking = 3;
                    j = i+5;
                    while (data[j] != ',') {
                        tempPriceStr[j-i-5] = data[j];
                        j++;
                    }
                    tempPriceStr[j-i-4] = '\0';
                    tempPrice = atof(tempPriceStr);
                    barData[bari][2] = tempPrice;
                    if (tempPrice < atl) {
                        atl = tempPrice;
                    }
                }
                break;
            case 3:
                if (data[i-1]=='"' && data[i]=='c' && data[i+1]=='l' && data[i+2]=='o' && data[i+3]=='s' && data[i+4]=='e' ) {
                    looking = 0;
                    j = i+7;
                    while (data[j] != ',') {
                        tempPriceStr[j-i-7] = data[j];
                        j++;
                    }
                    tempPriceStr[j-i-6] = '\0';
                    tempPrice = atof(tempPriceStr);
                    barData[bari][3] = tempPrice;
                    bari++;
                }
                break;

            default:
                printf("ERROR: looking has an invalid value");
        }

        i++;
    }

    int barYLen = bari;
    for(i=0; i<barYLen; i++) {
        printf("%f, %f, %f, %f\n", barData[i][0], barData[i][1], barData[i][2], barData[i][3]);
    }

    char graph[maxY][maxX+1];

    for (i = 0; i < maxY; i++) {
        for (j = 0; j < maxX-1; j++) {
            graph[i][j] = ' ';
        }
        graph[i][maxX-1] = '\0';
    }
    

    for (i=0; i<maxX; i++) {
        graph[0][i] = 'a';
        graph[maxY-1][i] = 'a';
    }

    // Key: a=─, b=┌, c=┐, d=└, e=┘
    wchar_t special;
    char c;
    for (i=0; i<maxY; i++) {
        for (j = 0; j < maxX-1; j++) {
            c = graph[i][j];
            switch(c){
                case 'a':
                    special = 0x2500;
                    printf("%lc", special);
                    break;
                case 'b':
                    special = 0x250c;
                    printf("%lc", special);
                    break;
                case 'c':
                    special = 0x2510;
                    printf("%lc", special);
                    break;
                case 'd':
                    special = 0x2514;
                    printf("%lc", special);
                    break;
                case 'e':
                    special = 0x2518;
                    printf("%lc", special);
                    break;
                default:
                    printf("%c",graph[i][j]);
            }
        }
        printf("\n");
    }

    // for (i=0;i<barYLen;i++) {

    // }

    return(0);
}