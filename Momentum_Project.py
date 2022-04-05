import datetime
import time
import pandas as pd
from pandas import DataFrame
import numpy as np
import matplotlib.pyplot as plt

class Momentum:
    def __init__(self, start_date, end_date, ticker):
        start_date= datetime.datetime.strptime(start_date, "%m/%d/%Y")
        end_date= datetime.datetime.strptime(end_date, "%m/%d/%Y")
        self.start_date= start_date
        self.end_date= end_date
        self.ticker= ticker

    def calculateMomentumIndicators(self, lookback, window):
        #assumes window is in number of days 
    
#*********************************************PULLING DATA FROM YAHOO FINANCE ********************************** https://query1.finance.yahoo.com/v7/finance/download/AAPL?period1=1617307273&period2=1648843273&interval=1d&events=history&includeAdjustedClose=true
        
        #First, I start off by defining what my ticker will be
        ticker= self.ticker

        #Then, I determine how much data I want using the start and end dates 
        period1= int(time.mktime(self.start_date.timetuple()))
        period2= int(time.mktime(self.end_date.timetuple()))

        #here, I made my interval for the data one day, it will show us data of the stock from each day 
        interval='1d'

        #now, I am pulling data from yahoo finance using the URL where you download the data from
        yahoo_finance_data= f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'

        #Here, I create a data frame of the YahooFinance data
        df=pd.read_csv(yahoo_finance_data)

        #because I want Adjusted Close in my final table, I am defining a variable showing all the adjusted closing dates 
        AdjustedClose=df['Adj Close']


#***************************CALCULATING LOWER AND UPPER BOUNDS OF BOLLINGER BANDS************************** 
        

        #calculating the moving average using the window provided by the user 

        Moving_Average= df['Close'].rolling(window=int(window)).mean()

        #calculating the Standard Deviation using the window provided by the user

        Standard_Devation = df['Close'].rolling(window=int(window)).std()
        #Now, I am calculating the Lower and Upper Bounds of the Bollinger Bands 
        Upper= Moving_Average + 2*Standard_Devation
        Lower = Standard_Devation - 2*Standard_Devation




 ##*******************************CALCULATING MACD***************************************************************

        #Calculating the 26 and 12 day periods for the MACD 
        daytwelve= df['Adj Close'].ewm(span=12, adjust=False).mean()
        twentysixday=df['Adj Close'].ewm(span=26, adjust=False).mean()
        #Calculating MACD 
        MACD=daytwelve-twentysixday

##*******************************CALCULATING RSI***************************************************************

        #first, calculating the difference so that I can determine if I am gaining or loosing 
        difference=df['Close'].diff()
        #a gain is defined as a positive difference 
        gain=difference.clip(lower=0)
        #a gain is defined as a negative difference 
        loss=-1*difference.clip(upper=0)
        #now, finding the estimated moving avg of gain and loss 
        ema_gain=gain.ewm(com=13, adjust=False).mean()
        ema_loss=loss.ewm(com=13, adjust=False).mean()
        #calculating RS vallue 
        rs=ema_gain/ema_loss
        #using RS to calculate RSI
        RSI=100-(100/(1+rs))


##*******************************PRESENTING THE DATA***************************************************************


        datatable=DataFrame({
                        'Date':df["Date"],
            
                        'Adjusted Close':AdjustedClose,
                        'MACD': MACD, 
                        'RSI':RSI,
                        'Upper Bound': Upper,
                        'Lower Bound': Lower
                        

                        })
        print(datatable)




    def strategy(self):
        #First, I start off by defining what my ticker will be
        ticker= self.ticker

        #Then, I determine how much data I want using the start and end dates 
        period1= int(time.mktime(self.start_date.timetuple()))
        period2= int(time.mktime(self.end_date.timetuple()))

        #here, I made my interval for the data one day, it will show us data of the stock from each day 
        interval='1d';

        #now, I am pulling data from yahoo finance using the URL where you download the data from
        yahoo_finance_data= f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'

        #Here, I create a data frame of the YahooFinance data
        df=pd.read_csv(yahoo_finance_data)
 
        #Calculating the 26 and 12 day periods for the MACD 
        daytwelve= df['Adj Close'].ewm(span=12, adjust=False).mean()
        twentysixday=df['Adj Close'].ewm(span=26, adjust=False).mean()

        #Calculating MACD 
        df['MACD']=MACD=daytwelve-twentysixday

        #Making my buy signal when MACD is greater than 1.
        #This means that the EMA in the past 12 days is greater than it has been in the past 26 days
        #This is a good indicator to buy because it shows that the price in the past 12 days is higher than it was in the past 26 days

        
        df['Signal']= np.where(df['MACD']>0, 1, 0)
        df['Signal']= np.where(df['MACD']<0, -1, df['Signal'])
        df['Transaction']= np.where(df['MACD']>0, "Buy", "Null")
        df['Transaction']= np.where(df['MACD']<0, "Sell", df['Transaction'])


        df['Signal2']= np.where(df['MACD']>0, 1, 0)
        df['Signal2']= np.where(df['MACD']<0, -1, df['Signal'])
        df['Buy'] =np.where(df['Signal']==1, df['Close'], np.NAN)
        df['Sell'] =np.where(df['Signal']==-1, df['Close'], np.NAN)
        #df['return'] = np.log(df['Close']).diff()
        #df['Date']= np.where(df['Signal']>=1, 1, 0)
        Buy_Sum= df["Buy"].sum()
        Sell_Sum= df["Sell"].sum()
        Profits=Buy_Sum-Sell_Sum
        
        new_df=df[df['Signal']==  -1]
        new_df=df[df['Signal2']==  1]

        datatable=DataFrame({
                        'Date':df["Date"],
            
                        'MACD': MACD, 
                        'Transaction':df['Transaction'],
                        'Share Price': df["Close"],
                        'Profits' : Profits
                        

                        })
        print(datatable)

    def comparePerformance(self):
        #First, I start off by defining what my ticker will be
        ticker= self.ticker

        #Then, I determine how much data I want using the start and end dates 
        period1= int(time.mktime(self.start_date.timetuple()))
        period2= int(time.mktime(self.end_date.timetuple()))

        #here, I made my interval for the data one day, it will show us data of the stock from each day 
        interval='1d';

        #now, I am pulling data from yahoo finance using the URL where you download the data from
        yahoo_finance_data= f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'

        #Here, I create a data frame of the YahooFinance data
        df=pd.read_csv(yahoo_finance_data)
        length= len(df)-1

        
        #Calculating the 26 and 12 day periods for the MACD 
        daytwelve= df['Adj Close'].ewm(span=12, adjust=False).mean()
        twentysixday=df['Adj Close'].ewm(span=26, adjust=False).mean()

        #Calculating MACD 
        df['MACD']=MACD=daytwelve-twentysixday

        #Making my buy signal when MACD is greater than 1.
        #This means that the EMA in the past 12 days is greater than it has been in the past 26 days
        #This is a good indicator to buy because it shows that the price in the past 12 days is higher than it was in the past 26 days
    
        df['Signal']= np.where(df['MACD']>0, 1, 0)
        df['Signal']= np.where(df['MACD']<0, -1, df['Signal'])
        df['Transaction']= np.where(df['MACD']>0, "Buy", "Null")
        df['Transaction']= np.where(df['MACD']<0, "Sell", df['Transaction'])
        df['Signal2']= np.where(df['MACD']>0, 1, 0)
        df['Signal2']= np.where(df['MACD']<0, -1, df['Signal'])
        df['Buy'] =np.where(df['Signal']==1, df['Close'], np.NAN)
        df['Sell'] =np.where(df['Signal']==-1, df['Close'], np.NAN)
        Buy_Sum= df["Buy"].sum()
        Sell_Sum= df["Sell"].sum()
        Profits=Buy_Sum-Sell_Sum
        diff = Profits - (df["Close"][length]- df["Close"][0])
        print("The Strategy preforms with a difference of " + str(diff))
    


#testing 
m = Momentum("01/01/2021", "07/01/2021", "MSFT")
m.calculateMomentumIndicators(0,'30')
m.strategy()
m.comparePerformance()

           

