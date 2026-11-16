import numpy as np 
import pandas as pd 
import yfinance as yf
import matplotlib.pyplot as plt
from pathlib import Path
file_path = Path(__file__).parent / "protifilio.csv"                      #Used to locate File
balance_path = Path(__file__).parent/"Balance.csv"




print("Welcome to the protifilio tracker")


stock_buy = np.array([])
profit = np.array([])
buying_price = np.array([])
total_stocks = np.array([])
stock_tickers = np.array([])

try:
    balance_df = pd.read_csv(balance_path)
    Balance = balance_df.loc[0, "Balance"]

except FileNotFoundError:
    Balance = 200000


try:
    df = pd.read_csv(file_path)                    #To check weather the file already exists or n                                                                                ot

except FileNotFoundError:
    df = pd.DataFrame(columns=["Name", "Buying Price", "Quantity","Ticker"])
    df.to_csv(file_path, index=False)





def Company(company_name,registered_name):                                       # Main structure of the code 
     global stock_buy
     global profit
     global buying_price
     global total_stocks
     global stock_name
     global stock_tickers
     global df
     global Balance
     
     

     stock = yf.Ticker(registered_name)                                 # Used to access the stock chart
     stock_name = company_name
     data = stock.history(period="5d", interval="1m")
     daily = stock.history(period="5d", interval="1d")           #x=open,y=close,z=corrent
     
     open = daily["Open"].dropna().iloc[-1]                            # Used to access the prices of stocks 
     close = daily["Close"].dropna().iloc[-1]
     current = data["Close"].dropna().iloc[-1]
     data_rel = {
         "Closing_Price": close,
         "Opening_Price": open,
         "Current_Price": current
     }
     Table = pd.DataFrame(data_rel, index=[0])             # Used to show the details and price of stock in proper tabular format
     print(Table)
     
     plt.figure(figsize=(10, 5))                                                     # Used to display the stock chart
     plt.plot(data.index, data["Close"], label=f"{company_name} Stock Price")
     plt.title(f"{company_name} Stock Chart")
     plt.xlabel("Time")
     plt.ylabel("Price (₹)")
     plt.legend()
     plt.grid(True)
     plt.xticks(rotation=45)
     plt.tight_layout()
     plt.show()
     print('''Press 1 to invest in stocks 
      or Press 2 to exit''' )
     buy_or_not=int(input("Please Enter Your Choice:-"))

     if buy_or_not==1:                                                         # Condition to buy a stock or not
         no_of_stocks=int(input("Please Enter the no. of stocks:-"))
         if no_of_stocks<=0:                                                   
              print("Enter a valid number of stocks:-")
         else:
              print("Processing...")
              purchase_price=float(current)                                   # Puchasing price of the stock
              bill=(no_of_stocks*purchase_price)
              if bill<=Balance:                                               # Condition to check whether balance is sufficient or not
                print("Total Bill=",bill)
                print("------------------------------------")
                stock_buy = np.append(stock_buy, stock_name)                  # Used top store the names of the stocks bought
                total_stocks = np.append(total_stocks, no_of_stocks)          # To store quantity of stocks bought
                buying_price = np.append(buying_price, purchase_price)        # To store buying price of the stock bought
                stock_tickers = np.append(stock_tickers, registered_name)
                Balance -= bill                                               #Used to update the Balance 
                balance_df = pd.DataFrame({"Balance": [Balance]})
                balance_df.to_csv(balance_path, index=False)
              
         
                new_protifilio=pd.DataFrame({                                 # Used to store the details of the stock bought
                   "Name":[stock_name],
                   "Buying Price":[purchase_price],
                   "Quantity":[no_of_stocks],
                   "Ticker":[registered_name]
                })
                df=pd.concat([df,new_protifilio],ignore_index=True)           # Used to add the details of the stock to csv file in orser to store it
                df.to_csv(file_path,index=False)                              # Used to convert dataframe to csv file

                return Balance

              
              else:
                print("Insufficient Balance")
     else:
          print("Visit Again")

     
              
while True:                                                                # Starting Menu
          
    print('''  Press 1 to to check balance
  Press 2 to view companies
  Press 3 to check your Protifilio
  Press 4 to Sell Stocks
  Press 5 to exit''')
    choice=int(input("Please Enter Your Choice: "))
    
    
    if choice==1:
        print(Balance)
    
    
    elif choice==2:                                                  # Company List
          print('''  Press 1 to view Reliance Industries
    Press 2 to view HDFC Bank
    Press 3 to view ICICI Bank
    Press 4 to view Tata Consultancy Services (TCS)
    Press 5 to view Bharti Airtel''')
          
          
          company_choice=int(input("Please Enter your Choice:-"))
          if company_choice==1:
               Company("Reliance Industries","RELIANCE.NS")
          elif company_choice==2:
               Company("HDFC BANK","HDFCBANK.NS")
          elif company_choice==3:
               Company("ICICI BANK","ICICIBANK.NS")
          elif company_choice==4:
               Company("Tata Consultancy Services (TCS)","TCS.NS")
          elif company_choice==5:
               Company("Bharti Airtel","BHARTIARTL.NS")
          else:
               print("Thank You, Visit Again")
   
   
    elif choice == 3:
        print(df)                                    # Used tpo display Protifilio(the data stored into csv file related to the purchases)
    elif choice==4:
       print(df)
       index_no=int(input("Please Enter the Transaction number which you want to remove"))
       current_price = yf.Ticker(df.loc[index_no, "Ticker"]).history(period="1d", interval="1m")["Close"].dropna().iloc[-1]
       selling_price = df.loc[index_no, "Quantity"] * current_price
       print('''Press 1 to confirm Transation
       Press 2 to Cancle Transation''')
       final=int(input("Please Enter Your Choice"))
       if final==1:
        df=df.drop(index_no)
        df=df.reset_index(drop=True)
        df.to_csv(file_path,index=False)
        Balance += selling_price
        balance_df = pd.DataFrame({"Balance": [Balance]})
        balance_df.to_csv(balance_path, index=False)
        print(("Your Balance="),Balance)
        print(df)
       elif final==2:
           print("Transaction Canceled")
       else:
           print("Sorry, You made an ERROR")
