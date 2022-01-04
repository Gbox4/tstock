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
    int maxY = 60;

    double ath = 0;
    double atl = 99999999;

    char data[1000000];
    int i = 0;
    int j = 0;
    char tempPriceStr[50];
    double tempPrice;

    FILE *p;
    int ch;
    char cmd[] = "curl -s \"http://api.marketstack.com/v1/eod?access_key=b1b863864c3e595e1eea256725870434&date_from=2021-08-01&date_to=2021-11-30&symbols=";
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
    double barData[1000][4];
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

    wchar_t graph[maxY][maxX];

    for (i = 0; i < maxY; i++) {
        for (j = 0; j < maxX; j++) {
            graph[i][j] = ' ';
        }
    }

    // Draw top and bottom borders
    for (i=0; i<maxX; i++) {
        graph[0][i] = 0x2500; // 0x2500 = ─
        graph[maxY-1][i] = i%5==0 ? 0x253c : 0x2500;
    }
    // Draw left and right borders
    for (i=0; i<maxY; i++) {
        graph[i][0] = i%5==0 ? 0x253c : '|';
        graph[i][maxX-1] = '|';
    }
    // Draw corners
    graph[0][0] = 0x250c; // 0x250c = ┌
    graph[0][maxX-1] = 0x2510; // 0x2510 = ┐
    graph[maxY-1][0] = 0x2514; // 0x2514 = └
    graph[maxY-1][maxX-1] = 0x2518; // 0x2518 = ┘

    j = 6;
    int low = 4;
    int high = maxY - 4;
    int mlow;
    int mhigh;
    int vpos;
    int tmp;

    int columnColors[maxX]; // 0 = white, 1 = red, 2 = green
    for (i=0; i<maxX; i++) {
        columnColors[i] = 0;
    }

    for (i=0; i < barYLen; i++){
        // map high/low
        mlow = map(barData[i][2], atl, ath, low, high);
        mhigh = map(barData[i][1], atl, ath, low, high);
        // graph[mlow][j] = 0x2588;
        for (vpos=mlow;vpos<=mhigh;vpos++) {
            graph[vpos][j] = '|';
        }

        // map open/close
        mlow = map(barData[i][0], atl, ath, low, high);
        mhigh = map(barData[i][3], atl, ath, low, high);
        if (mlow > mhigh){
            tmp = mlow;
            mlow = mhigh;
            mhigh = tmp;
            columnColors[j] = 1;
        }
        else{
            columnColors[j] = 2;
        }
        // graph[mlow][j] = 0x2588;
        for (vpos=mlow;vpos<=mhigh;vpos++) {
            graph[vpos][j] = 0x2588;
        }

        j++;
    }

    // Draw graph
    wchar_t special;
    for (i=0; i<maxY; i++) {
        printf("\x1b[0m");
        printf(" ");
        for (j = 0; j < maxX; j++) {
            if (i != 0 && i != maxY-1){
                switch (columnColors[j]) {
                case 0:
                    printf("\x1b[0m");
                    break;
                case 1:
                    printf("\x1b[31m");
                    break;
                case 2:
                    printf("\x1b[32m");
                    break;
                
                default:
                    printf("ERROR: Incorrect columncolor\n");
                    break;
                }
            }
            printf("%lc", graph[i][j]);
        }
        printf("\n");
    }

    // for (i=0;i<barYLen;i++) {

    // }

    printf("\n");
    return(0);
}