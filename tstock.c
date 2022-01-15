// Gabe Banks
// 1/3/22

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <wchar.h>
#include <locale.h>
#include <time.h>
#include <math.h>
#include <unistd.h>

#include <curl/curl.h>
#include <curl/urlapi.h>

// Size of the buffer used for curl requests
#define CURL_RAW_BUFF_SIZE 20000

// Function declarations
void printHelp();
double map(double x, double l1, double h1, double l2, double h2);
// Gets the raw data from the MarketStack API.
char *getMarketStackData(const char *apiKey, const struct tm *dateFrom, const struct tm *dateTo, const char *ticker);
// Simple CURL callback to append data to a buffer
static size_t appendToBufferWriter(char *data, size_t size, size_t nmemb, char *buffer);
int main(int argc, char *argv[]);

// Print the help message and exit
void printHelp()
{
    printf("Usage: tstock [OPTIONS]... TICKER\n"
           "Prints a candlestick chart of TICKER in the terminal.\n"
           "Options:\n"
           "    -d [days]       Number of days to go back in API call. Defaults to 90.\n"
           "    -h              print this message and exit\n"
           "    -v              enables verbosity\n"
           "    -y [lines]      Specify height of the chart. Defaults to 40.\n");
    return;
}

// Maps a number x from scale l1, h1 to relative scale in l2, h2
double map(double x, double l1, double h1, double l2, double h2)
{
    return (((x - l1) / (h1 - l1)) * (h2 - l2)) + l2;
}

static size_t appendToBufferWriter(char *data, size_t size, size_t nmemb, char *buffer)
{
    if (!buffer)
        return (0);
    // TODO: Does this work if there is a \0 in the data? Can there be a \0 in the data?
    if (strlen(buffer) + size * nmemb > CURL_RAW_BUFF_SIZE)
        exit(EXIT_FAILURE);
    strncat(buffer, data, size * nmemb);
    return size * nmemb;
}

char *getMarketStackData(const char *apiKey, const struct tm *dateFrom, const struct tm *dateTo, const char *ticker)
{
    // We allocate memory for the data returned by the request
    char *curlBuffer = malloc(CURL_RAW_BUFF_SIZE);
    memset(curlBuffer, 0, CURL_RAW_BUFF_SIZE);
    CURL *curl = curl_easy_init();

    if (!curl)
        return (0);

    // TODO: Handle errors from curl_easy_setopt

    // Set curl buffer
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, appendToBufferWriter);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, curlBuffer);

    // Generate the API url
    CURLU *url = curl_url();
    curl_url_set(url, CURLUPART_URL, "http://api.marketstack.com/v1/eod", 0);

    char tokenParam[11 + 32 + 1] = "access_key="; // strlen("access_key=") == 11 && strlen("<MARKETSTACK_API_KEY>") == 32
    strcat(tokenParam, apiKey);
    curl_url_set(url, CURLUPART_QUERY, tokenParam, CURLU_APPENDQUERY);

    // TODO: Maybe write a small string view struct for easier string manipulation? This is... not great...
    char dateFromParam[10 + 10 + 1] = "date_from="; // The dates will always be 10 characters long with the provided format, and "date_from=" is also 10 characters
    char dateFromRaw[10 + 1];
    strftime(dateFromRaw, sizeof(dateFromRaw), "%Y-%m-%d", dateFrom);
    strcat(dateFromParam, dateFromRaw);
    curl_url_set(url, CURLUPART_QUERY, dateFromParam, CURLU_APPENDQUERY);

    char dateToParam[10 + 8 + 1] = "date_to="; // The dates will always be 10 characters long with the provided format, and "date_to=" is 8 characters
    char dateToRaw[10 + 1];
    strftime(dateToRaw, sizeof(dateToRaw), "%Y-%m-%d", dateTo);
    strcat(dateToParam, dateToRaw);
    curl_url_set(url, CURLUPART_QUERY, dateToParam, CURLU_APPENDQUERY);

    char symbolsParam[32] = "symbols=";
    strcat(symbolsParam, ticker);
    curl_url_set(url, CURLUPART_QUERY, symbolsParam, CURLU_APPENDQUERY);

    char *finalUrl;
    curl_url_get(url, CURLUPART_URL, &finalUrl, 0);
    curl_url_cleanup(url);

    // TODO: Check if verbose flag is set to log
    fprintf(stdout, "Getting data from: %s\n", finalUrl);

    curl_easy_setopt(curl, CURLOPT_URL, finalUrl);

    CURLcode res = curl_easy_perform(curl);
    (void) res; // TODO: Check res for errors
    curl_easy_cleanup(curl);
    return (curlBuffer);
}

int main(int argc, char *argv[])
{
    // Set locale for unicode characters
    setlocale(LC_CTYPE, "");

    // maxX, maxY determine the dimensions, in characters, of the graph
    int maxX;      // This is set to the number of candles + 12
    int maxY = 40; // Can be set with -y

    // Variables that can be modified with flags
    int verbose = 0;   // Toggled with -v
    int daysBack = 90; // Set with -d
    char strDaysBack[10] = "90";

    // Index variables for loops
    int i = 0;
    int j = 0;

    // Parse options
    int opt; // TODO: setup args for different API backends
    while ((opt = getopt(argc, argv, ":d:y:vh")) != -1)
    {
        switch (opt)
        {
        case 'd':
            strcpy(strDaysBack, optarg);
            daysBack = atoi(optarg);
            break;
        case 'y':
            maxY = atoi(optarg);
            break;
        case 'h':
            printHelp();
            return 0;
            break;
        case 'v':
            verbose = 1;
            break;
        case ':':
            printf("Option -%c needs a value.\n", optopt);
            printHelp();
            return 0;
            break;
        case '?':
            printf("Unknown option `-%c'.\n", optopt);
            printHelp();
            return 0;
            break;
        }
    }
    // Check for right number of arguments
    if (optind != argc - 1)
    {
        printHelp();
        return 1;
    }

    // Stores the ticker provided as argument by user
    char ticker[50];
    strcpy(ticker, argv[optind]);

    // Check for API key stored in env variable $MARKETSTACK_API_KEY
    const char *apikey = getenv("MARKETSTACK_API_KEY");
    if (apikey == NULL)
    {
        printf("API key not detected! Follow these instructions to get your API Key working:\n");
        printf("- Make a free MarketStack API account at https://marketstack.com/signup/free\n");
        printf("- Login and find your API Access Key on the Dashboard page\n");
        printf("- Run \"export MARKETSTACK_API_KEY=<your access key>\".\n");
        printf("    You can make this permanent by adding a line like \"export MARKETSTACK_API_KEY=<your access key>\" to your .bashrc\n");
        return (1);
    }

    // Find date values
    time_t now = time(NULL);
    // Here we dereference the value from localtime() to copy it so that the second call to localtime() doesn't overwrite the data from the first
    struct tm tm_now = *localtime(&now);
    time_t start = time(NULL) - (86400 * daysBack); // defaults to 90 days * seconds in a day (86400)
    struct tm tm_start = *localtime(&start);

	// This will malloc some memory, we need to free `data` once we're done!
    char *data = getMarketStackData(apikey, &tm_start, &tm_now, ticker);

    // If the received data is under 100 characters, something probably went wrong
    if (strlen(data) < 100)
    {
        printf("Didn't receive enough data from API. Check your internet connection. Is this stock covered by the API?\n");
        if (verbose)
            printf("Received following data from API: %s\n", data);
        return (1);
    }

    if (verbose)
        printf("Raw JSON data received:\n%s\nParsing...\n", data);

    // Code for parsing JSON data:
    // looking for either 0=open, 1=high, 2=low, 3=close, 4=day
    int looking = 0;
    // Temporary location to store variables when parsing raw API data
    char tempPriceStr[500];
    double tempPrice;
    // Temporary location for date while parsing
    char tmpDay[4];
    // Final location for parsed bar data.
    // Right now just pray that the user doesn't try to pull over 1000 days worth of data...
    // Each row is of the shape: [Open, high, low, close, day]
    double barData[1000][5];
    // Index variable
    int bari = 0;
    // ath, atl, for keeping track of all-time-high and all-time-low prices, within the specified time window.
    double ath = 0;
    double atl = 99999999;

    // Start parsing API data
    i = 0;
    while (data[i] != ']')
    {
        if (data[i - 1] == '"' && data[i] == 'e' && data[i + 1] == 'r' && data[i + 2] == 'r' && data[i + 3] == 'o' && data[i + 4] == 'r')
        {
            printf("ERROR: The API returned an error: %s\n", data);
            return (1);
        }
        switch (looking)
        {
        case 0:
            if (data[i - 1] == '"' && data[i] == 'o' && data[i + 1] == 'p' && data[i + 2] == 'e' && data[i + 3] == 'n')
            {
                looking = 1;
                j = i + 6;
                while (data[j] != ',')
                {
                    tempPriceStr[j - i - 6] = data[j];
                    j++;
                }
                tempPriceStr[j - i - 5] = '\0';
                tempPrice = atof(tempPriceStr);
                barData[bari][0] = tempPrice;
            }
            break;
        case 1:
            if (data[i - 1] == '"' && data[i] == 'h' && data[i + 1] == 'i' && data[i + 2] == 'g' && data[i + 3] == 'h')
            {
                looking = 2;
                j = i + 6;
                while (data[j] != ',')
                {
                    tempPriceStr[j - i - 6] = data[j];
                    j++;
                }
                tempPriceStr[j - i - 5] = '\0';
                tempPrice = atof(tempPriceStr);
                barData[bari][1] = tempPrice;
                if (tempPrice > ath)
                {
                    ath = tempPrice;
                }
            }
            break;
        case 2:
            if (data[i - 1] == '"' && data[i] == 'l' && data[i + 1] == 'o' && data[i + 2] == 'w')
            {
                looking = 3;
                j = i + 5;
                while (data[j] != ',')
                {
                    tempPriceStr[j - i - 5] = data[j];
                    j++;
                }
                tempPriceStr[j - i - 4] = '\0';
                tempPrice = atof(tempPriceStr);
                barData[bari][2] = tempPrice;
                if (tempPrice < atl)
                {
                    atl = tempPrice;
                }
            }
            break;
        case 3:
            if (data[i - 1] == '"' && data[i] == 'c' && data[i + 1] == 'l' && data[i + 2] == 'o' && data[i + 3] == 's' && data[i + 4] == 'e')
            {
                looking = 4;
                j = i + 7;
                while (data[j] != ',')
                {
                    tempPriceStr[j - i - 7] = data[j];
                    j++;
                }
                tempPriceStr[j - i - 6] = '\0';
                tempPrice = atof(tempPriceStr);
                barData[bari][3] = tempPrice;
            }
            break;
        case 4:
            if (data[i - 1] == '"' && data[i] == 'd' && data[i + 1] == 'a' && data[i + 2] == 't' && data[i + 3] == 'e')
            {
                looking = 0;
                tmpDay[0] = data[i + 15];
                tmpDay[1] = data[i + 16];
                tmpDay[2] = '\0';
                barData[bari][4] = atof(tmpDay);
                bari++;
            }
            break;

        default:
            printf("ERROR: looking has an invalid value\n");
            return (1);
        }
        i++;
    }

    // We're no longer using the data, so we can free the memory back
    free(data);

    // The final value of bari will be the number of rows barData has. Store in barYLen
    int barYLen = bari;
    if (verbose)
        printf("Found %i days of OHLC data.\n", barYLen);
    // Reverse the barData, so that earliest is first
    double barDataRev[1000][5];
    for (i = 0; i < barYLen; i++)
    {
        for (j = 0; j < 5; j++)
        {
            barDataRev[i][j] = barData[barYLen - i - 1][j];
        }
    }
    // Set X dimension of graph to number of candles + 12
    maxX = barYLen + 12;

    // Create 2d array of unicode characters that will become the graph
    wchar_t graph[maxY][maxX];

    // Clear the array by setting every element to a blank space
    for (i = 0; i < maxY; i++)
    {
        for (j = 0; j < maxX; j++)
        {
            graph[i][j] = ' ';
        }
    }

    // Draw top and bottom borders
    for (i = 0; i < maxX; i++)
    {
        graph[0][i] = 0x2500;                              // 0x2500 = ─
        graph[maxY - 1][i] = i % 5 == 0 ? 0x253c : 0x2500; // every fifth character, draw a "┼"
    }
    // Draw left and right borders
    for (i = 0; i < maxY; i++)
    {
        graph[i][0] = i % 5 == 0 ? 0x253c : 0x2502; // every fifth character, draw a "┼"
        graph[i][maxX - 1] = 0x2502;
    }
    // Draw corners
    graph[0][0] = 0x250c;               // 0x250c = ┌
    graph[0][maxX - 1] = 0x2510;        // 0x2510 = ┐
    graph[maxY - 1][0] = 0x2514;        // 0x2514 = └
    graph[maxY - 1][maxX - 1] = 0x2518; // 0x2518 = ┘

    // Don't even bother with graph title if there's not 40 days worth of data
    if (daysBack >= 40)
    {
        // Draw graph title
        char upper[10];
        for (i = 0; i < strlen(ticker); i++)
        {
            upper[i] = toupper(ticker[i]);
        }
        upper[i] = '\0';
        char title[50] = "  ";
        strcat(title, strDaysBack);
        strcat(title, " Day Stock Price for $");
        strcat(title, upper);
        strcat(title, "  ");
        graph[0][1] = 0x2524; // ┤
        for (i = 0; i < strlen(title); i++)
        {
            graph[0][i + 2] = title[i];
        }
        graph[0][i + 2] = 0x251c; // ├
    }

    // Declare variables for drawing candlesticks
    // Lower and upper bounds of which rows to draw a candle stick
    int low = 4;
    int high = maxY - 4;
    // mlow, mhigh = mapped low and mapped high. Prices that have been mapped to the scale of the Y axis.
    int mlow;
    int mhigh;
    int vpos;
    // Temp variable for switching mlow and mhigh
    int tmp;
    // Set index to start at 5 for padding inside chart
    j = 5;
    // Declare array for keeping track of which columns saw an increase or a decrease in stock price
    int columnColors[maxX]; // 0 = white, 1 = red, 2 = green
    for (i = 0; i < maxX; i++)
    {
        columnColors[i] = 0; // Initialize by setting every element to 0
    }

    for (i = 0; i < barYLen; i++)
    {
        // map high/low parts of the candlestick
        mhigh = map(barDataRev[i][2], atl, ath, high, low);
        mlow = map(barDataRev[i][1], atl, ath, high, low);
        // fill in the high/low part of the candlestick
        for (vpos = mlow; vpos <= mhigh; vpos++)
        {
            graph[vpos][j] = 0x2502;
        }
        // map open/close parts of the candlestick
        mhigh = map(barDataRev[i][0], atl, ath, high, low);
        mlow = map(barDataRev[i][3], atl, ath, high, low);
        // If "mlow" is greater than "mhigh", that means the stock went down in price
        if (mlow > mhigh)
        {
            tmp = mlow;
            mlow = mhigh;
            mhigh = tmp;
            columnColors[j] = 1;
        }
        else
        { // Otherwise the stock increased in price
            columnColors[j] = 2;
        }
        // fill in the open/close part of the candlestick
        for (vpos = mlow; vpos <= mhigh; vpos++)
        {
            graph[vpos][j] = 0x2588;
        }
        j++;
    }

    // Print graph to terminal
    // String holding an axis label
    char label[15];
    sprintf(label, "$%.2f", ath);
    // Margin between the y-axis of the graph and the left edge of the screen
    int margin = strlen(label);
    // Variable for holding a numeric stock price
    double price;
    // Start looping through "graph" and printing character by character
    for (i = 0; i < maxY; i++)
    {
        // ANSI escape code for resetting font/color
        printf("\x1b[0m");
        // Print y axis labels and margin
        if (i % 5 == 0 && i >= low && i <= high)
        {
            price = map(i, low, high, ath, atl);
            sprintf(label, "$%.2f", price);
            for (j = 0; j < margin - strlen(label); j++)
            {
                printf(" ");
            }
            printf("$%.2f", price);
        }
        else
        {
            for (j = 0; j < margin; j++)
            {
                printf(" ");
            }
        }
        // Print graph contents
        for (j = 0; j < maxX; j++)
        {
            if (i != 0 && i != maxY - 1)
            {
                switch (columnColors[j])
                { // ANSI Escape sequences for setting print color
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
                    return (1);
                }
            }
            printf("%lc", graph[i][j]);
        }
        printf("\n");
    }
    for (j = 0; j < margin; j++)
    {
        printf(" ");
    }
    printf("     "); // account for margin
    // Print x axis labels
    for (j = 0; j < barYLen; j++)
    {
        if (j % 5 == 0)
        {
            printf("%i", (int)barDataRev[j][4]);
            if ((int)barDataRev[j][4] > 9)
            {
                printf("   ");
            }
            else
            {
                printf("    ");
            }
        }
    }

    printf("\n\n");
    return (0);
}
