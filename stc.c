// Gabe Banks
// 1/3/22
// APCSP CS50 Unit Final Project

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <wchar.h>
#include <locale.h>
#include <time.h>
#include <math.h>

double map(double x, double l1, double h1, double l2, double h2);
int digits(int x, int y);
int main(int argc, char *argv[]);

double map(double x, double l1, double h1, double l2, double h2) {
    return (((x-l1)/(h1-l1)) * (h2-l2)) + l2;
}

int digits(int x, int y){ // call this function with (y=0)
    if (x > 9) {
        return digits(x/10, y+1);
    }
    return y+1;
}

int main(int argc, char *argv[]) {

    // Check for right number of arguments
    if (argc != 2) {
        printf("Usage: stc TICKER\n");
        return 1;
    }

    setlocale(LC_CTYPE, ""); // Set locale for unicode characters

    int maxX = 100;
    int maxY = 40;
    double ath = 0;
    double atl = 99999999;
    char data[1000000];
    int i = 0;
    int j = 0;
    char tempPriceStr[50];
    double tempPrice;

    // Get current date and date of 2 months ago
    char d1[100];
    char d2[100];
    time_t now = time(NULL);
    struct tm *t1 = localtime(&now);
    strftime(d1, sizeof(d1)-1, "%Y-%m-%d", t1);
    now = time(NULL) - 7884000; // number of seconds in 3 months
    struct tm *t2 = localtime(&now);
    strftime(d2, sizeof(d2)-1, "%Y-%m-%d", t2);
    

    // cUrl the API and store the resulting characters in the variable "data"
    FILE *p;
    int ch;
    char cmd[500] = "curl -s \"http://api.marketstack.com/v1/eod?access_key=b1b863864c3e595e1eea256725870434&date_from="; // construct the cUrl command
    strcat(cmd, d2); //     Construct the URL like this because C is an ancient language with no better way of concatenating strings
    strcat(cmd, "&date_to=");
    strcat(cmd, d1);
    strcat(cmd, "&symbols=");
    strcat(cmd, argv[1]);
    strcat(cmd, "\"");
    // printf("%s\n", cmd);
    // return(0);
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

    if (strlen(data) < 100){
        printf("ERROR: Didn't recieve data from API. Is this stock covered by the API?\n");
        return(0);
    }

    // printf("%s\n", data);

    // This shouldn't exceed 30 rows, I'm only gonna pull 30 days worth of data
    // Each row is of the shape: [Open, high, low, close, day]
    double barData[1000][5];
    int bari = 0;
    
    // looking for either 0=open, 1=high, 2=low, 3=close, 4=day
    int looking = 0;
    char tmpDay[2];
    i = 0;
    while (data[i] != ']') { // Scan through returned API data, extract certain parts
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
                    looking = 4;
                    j = i+7;
                    while (data[j] != ',') {
                        tempPriceStr[j-i-7] = data[j];
                        j++;
                    }
                    tempPriceStr[j-i-6] = '\0';
                    tempPrice = atof(tempPriceStr);
                    barData[bari][3] = tempPrice;
                }
                break;
            case 4:
                if (data[i-1]=='"' && data[i]=='d' && data[i+1]=='a' && data[i+2]=='t' && data[i+3]=='e') {
                    looking = 0;
                    tmpDay[0] = data[i+15];
                    tmpDay[1] = data[i+16];
                    tmpDay[2] = '\0';
                    barData[bari][4] = atof(tmpDay);
                    bari++;
                }
                break;

            default:
                printf("ERROR: looking has an invalid value\n");
                return(1);
        }
        i++;
    }

    int barYLen = bari;
    // Reverse the barData
    double barDataRev[1000][5];
    for (i=0; i<barYLen; i++) {
        for (j = 0; j < 5; j++) {
            barDataRev[i][j] = barData[barYLen - i - 1][j];
        }
    }

    // for(i=0; i<barYLen; i++) {
    //     printf("%f, %f, %f, %f, %f\n", barData[i][0], barData[i][1], barData[i][2], barData[i][3], barData[i][4]);
    // }
    maxX = barYLen + 12;

    // Create 2d array of unicode characters that will become the graph
    wchar_t graph[maxY][maxX];
    for (i = 0; i < maxY; i++) { // Clear the array by setting every element to a blank space
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
        graph[i][0] = i%5==0 ? 0x253c : 0x2502;
        graph[i][maxX-1] = 0x2502;
    }
    // Draw corners
    graph[0][0] = 0x250c; // 0x250c = ┌
    graph[0][maxX-1] = 0x2510; // 0x2510 = ┐
    graph[maxY-1][0] = 0x2514; // 0x2514 = └
    graph[maxY-1][maxX-1] = 0x2518; // 0x2518 = ┘

    // Draw graph title
    char upper[10];
    for (i=0; i < strlen(argv[1]); i++) {
        upper[i] = toupper(argv[1][i]);
    }
    upper[i] = '\0';
    char title[50] = "  3 Month Stock Price for $";
    strcat(title, upper);
    strcat(title, "  ");
    graph[0][1] = 0x2524; // ┤
    for (i=0; i < strlen(title); i++) {
        graph[0][i+2] = title[i];
    }
    graph[0][i+2] = 0x251c; // ├

    // Declare variables for drawing candlesticks
    j = 5;
    int low = 4;
    int high = maxY - 4;
    int mlow;
    int mhigh;
    int vpos;
    int tmp;
    // Declare array for keeping track of which columns saw an increase or a decrease in stock price
    int columnColors[maxX]; // 0 = white, 1 = red, 2 = green
    for (i=0; i<maxX; i++) {
        columnColors[i] = 0; // Initialize by setting every element to 0
    }

    for (i=0; i < barYLen; i++){
        // printf("%f\n", barDataRev[i][4]);
        // map high/low parts of the candlestick
        mhigh = map(barDataRev[i][2], atl, ath, high, low);
        mlow = map(barDataRev[i][1], atl, ath, high, low);
        // graph[mlow][j] = 0x2588;
        for (vpos=mlow;vpos<=mhigh;vpos++) {
            graph[vpos][j] = 0x2502; // fill in the high/low part of the candlestick
        }
        // map open/close parts of the candlestick
        mhigh = map(barDataRev[i][0], atl, ath, high, low);
        mlow = map(barDataRev[i][3], atl, ath, high, low);
        if (mlow > mhigh){ // If "mlow" is greater than "mhigh", that means the stock went down in price
            tmp = mlow;
            mlow = mhigh;
            mhigh = tmp;
            columnColors[j] = 1;
        }
        else{ // Otherwise the stock increased in price
            columnColors[j] = 2;
        }
        // graph[mlow][j] = 0x2588;
        for (vpos=mlow;vpos<=mhigh;vpos++) {
            graph[vpos][j] = 0x2588; // fill in the open/close part of the candlestick
        }
        j++;
    }

    // Draw graph
    int margin = digits((int) (ath*100), 0) + 2;

    double price;
    for (i=0; i<maxY; i++) {
        printf("\x1b[0m");
        // Drawy y axis labels
        if (i % 5 == 0 && i >= low && i <= high) {
            price = map(i, low, high, ath, atl);
            for (j=0; j<margin-digits((int)(price*100), 0)-2; j++) {
                printf(" ");
            }
            printf("$%.2f",price);
        }
        else{
            for (j=0; j<margin; j++){
                printf(" ");
            }
        }
        for (j = 0; j < maxX; j++) {
            if (i != 0 && i != maxY-1){
                switch (columnColors[j]) { // ASCII Escape sequences for setting print color
                case 0:
                    printf("\x1b[0m"); // White
                    break;
                case 1:
                    printf("\x1b[31m"); // Red
                    break;
                case 2:
                    printf("\x1b[32m"); // Green
                    break;
                
                default:
                    printf("ERROR: Incorrect columncolor\n");
                    return(1);
                }
            }
            printf("%lc", graph[i][j]);
        }
        printf("\n");
    }
    // Draw x axis labels
    for (j=0; j<margin; j++){
        printf(" ");
    }
    printf("     "); // account for margin
    for (j=0; j <barYLen; j++) {
        if (j % 5 == 0) {
            printf("%i", (int) barDataRev[j][4]);
            if ((int) barDataRev[j][4] > 9) {
                printf("   ");
            }
            else {
                printf("    ");
            }
        }
    }

    printf("\n\n");
    return(0);
}
