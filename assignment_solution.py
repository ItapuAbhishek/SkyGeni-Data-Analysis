#importing the required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#reading the data

def load_data():
    try:
        #dict of dataframes
        data={
            'financial_df': pd.read_csv('finanical_information.csv'),
            'industry_client_df': pd.read_csv('industry_client_details.csv'),
            'payment_information_df': pd.read_csv('payment_information.csv'),
            'subscription_information_df' : pd.read_csv('subscription_information.csv') 
        }
        return data
    except:
        raise Exception('Error in reading the data')

       
#displaying the first 5 rows of data
def display_data(df):
    print('Displaying the first 5 rows of each dataframe')
    for key,value in df.items():
        print(f'{key} dataframe')
        print(value.head())
        print('----------------------')
   
#checking the data info
def check_data_info(df):
    print('Displaying the info of each dataframe')
    for key,value in df.items():
        print(f'{key} dataframe')
        print(value.info())
        print('----------------------')

#detecting null values
def detect_null_values(df):
    print('Displaying the null values of each dataframe')
    for key,value in df.items():
        print(f'{key} dataframe')
        print(value.isnull().sum())
        print('----------------------')

#checking unique values
def unique_values(df):
    for key,value in df.items():
        print(f'{key} dataframe')
        print(value.nunique())
        print('----------------------')
        

#Detecting the Number of financial and block chain clients organization has

def number_of_clients(df):
    industry_client_df=df['industry_client_df']

    financial_block_chain_client=industry_client_df[industry_client_df['industry'].isin(['Finance Lending','Block Chain'])]

    print(f'Number of financial lending and block chain clients organization has:{financial_block_chain_client.shape[0]}')

    #plotting the number of clients
    plt.title('Number of financial lending and block chain clients organization has')
    plt.xlabel('Industry')
    plt.ylabel('Number of clients')
    bars= plt.bar(financial_block_chain_client['industry'].value_counts().index,financial_block_chain_client['industry'].value_counts().values)
    plt.bar_label(bars,fmt= '%d')
    plt.show()


#Finding the industry that has the highest renewal rate
def industry_with_highest_renewal_rate(df):

    industry_client_df=df['industry_client_df']
    subscription_information_df=df['subscription_information_df']
    
    #merging the two dataframes industry_client_df and subscription_information_df
    joined_df= industry_client_df.merge(subscription_information_df,how='inner',on='client_id')

    #getting the renewal rate for each industry
    grouped_df= joined_df.groupby('industry')['renewed'].mean()

    print(f'{grouped_df.idxmax()} industry has highest renewal rate in the organization with {np.round(grouped_df.max(),2)*100}% renewal rate')
    
    #plotting the renewal rate for each industry

    plt.title('Renewal rate for each industry')
    plt.xlabel('Industry')
    plt.ylabel('Renewal rate')
    bars= plt.bar(grouped_df.index,grouped_df.values)
    plt.bar_label(bars,fmt= '%d')
    plt.show()


#average inflation rate when their subscriptions were renewed

def average_inflation_rate(df):

    subscription_information_df=df['subscription_information_df']
    financial_df=df['financial_df']
    
    #converting the date columns to datetime
    subscription_information_df['start_date']= pd.to_datetime(subscription_information_df['start_date'])
    subscription_information_df['end_date']= pd.to_datetime(subscription_information_df['end_date'])

    financial_df['start_date']= pd.to_datetime(financial_df['start_date'])
    financial_df['end_date']= pd.to_datetime(financial_df['end_date'])

    #Function to get the inflation rate
    def get_inflation_rate(end_date):
        
        """"
        finding the inflation rate for a given subscription end_date by checking in which financial period it falls into

        """
        subscribed_row= financial_df[(financial_df['start_date']<=end_date) & (financial_df['end_date']>=end_date)]
        return subscribed_row['inflation_rate'].values[0] if not subscribed_row.empty else np.nan
        
    subscription_renewed= subscription_information_df[subscription_information_df['renewed']==True].copy()
    subscription_renewed['inflation_rate']=subscription_renewed['end_date'].apply(get_inflation_rate)
    
    #average of inflation rate values for the renewal period
    average= subscription_renewed['inflation_rate'].mean()
    print(f"Average inflation rate when their subsciptions were renewed: {round(average,2)}")


# median amount paid per year
def median_amount_paid_per_year(df):

    payment_information_df=df['payment_information_df']
    
    #converting the date columns to datetime
    payment_information_df['payment_date'] = pd.to_datetime(payment_information_df['payment_date'])
    #retrieving the year from the payment date
    payment_information_df['year']= payment_information_df['payment_date'].dt.year
    
    #getting the median amount paid per year
    print("median amount paid per year")
    print(payment_information_df.groupby('year')['amount_paid'].median())
    
    #plotting the median amount paid per year
    plt.title('median amount paid per year')
    plt.xlabel('Year')
    plt.ylabel('Amount paid')
    bars= plt.bar(payment_information_df.groupby('year')['amount_paid'].median().index,payment_information_df.groupby('year')['amount_paid'].median().values)
    plt.bar_label(bars,fmt= '%d')
    plt.show()


if __name__=='__main__':
    
    #Function for loading the data
    data=load_data()

    #Function for displaying the data
    display_data(data)

    #Function for checking the data
    check_data_info(data)

    #Function for detecting null values
    detect_null_values(data)

    #Function for checking unique values
    unique_values(data)

    #1Q Function for finding the number of clients
    number_of_clients(data)

    #2Q Function for finding the industry with highest renewal rate
    industry_with_highest_renewal_rate(data)

    #3Q Function for finding the average inflation rate
    average_inflation_rate(data)

    #4Q Function for finding the median amount paid per year
    median_amount_paid_per_year(data)
