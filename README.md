# tstock - Check stocks from the terminal!

Just type `tstock aapl` to get a 3 month candlestick chart of $AAPL in your terminal!

Example:

<img src="https://i.ibb.co/Pry8DWC/tstockex.png" alt="tstockex" border="0">

# Dependencies
- cURL. That's it. Just make sure it's installed on your system.

# Installation
- Download the binary, or compile it from source yourself with `make tstock` 
- Make a free MarketStack API account at https://marketstack.com/signup/free
- Login and find your API Access Key on the Dashboard page
- Run `export MARKETSTACK_API_KEY=<your access key>`. You can make this permanent by adding that command to your `.bashrc`.

# Notes
- The free tier of the API is limited to 100 API calls per month.
