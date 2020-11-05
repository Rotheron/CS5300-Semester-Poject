import pandas as pd
import mariadb as db
import math
import re 


def book_clean(data):
    # preprocess and clean the data for the "book" column in the data frame (df)
    book = data['book']
    #book = pd.DataFrame([['Sacramento', 'California'], ['Miami', 'Florida']], columns=['City', 'State'])
    book.to_csv('Clean_Data/book.csv')


def title_clean_1(data):
    #Read in "book" and the raw "title" column.
    book_nos = data['book']
    titles = data['title']
    
    #Key = "book" from raw data, value = clean title  
    idxToTitle = dict()
    idxToTitle["book"] = "title"    #Hardcode in the column names for the csv when rendered in Excel

    #Keep only titles consisting of just these characters
    validChars = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ")
    
    #Does this entire title consist of just validChars?
    validTitle = True

    #Iterate over every title and store the dataframe indeces of titles with only alphabetic characters in it
    for i in range(len(titles)):                    #Title Loop
        validTitle = True
        for q in range(len(titles[i])):             #Character Loop
            if(titles[i][q] not in validChars):
                validTitle = False
                break

        #Title was clean
        if(validTitle):
            idxToTitle[book_nos[i]] = str(titles[i])

    #Prepare pandas to write out to csv
    titleExport = pd.DataFrame.from_dict(idxToTitle, orient="index")

    #Write out the book number, and the clean title to a csv so we can stitch it back together later 
    titleExport.to_csv(r'Clean_Data/titles1.csv')

def pubdate_clean(data):
    pubdate = data['pubdate']
    bookNum = data['book']

    idxToPubDate = dict()
    idxToPubDate["book"] = "PubDate"

    for i in range(len(pubdate)):
        #check if the publishing date is NaN and put in NULL if it is
        if math.isnan(pubdate[i]):
            idxToPubDate[bookNum[i]] = "NULL" #Hopefully DBeaver will read in "NULL" as actually NULL and not just a string
        else:
            idxToPubDate[bookNum[i]] = str(pubdate[i])

    PubDateExport = pd.DataFrame.from_dict(idxToPubDate, orient="index")
    PubDateExport.to_csv('Clean_Data/pubdate.csv')

def price_clean(data):
    price = data['price']
    bookNum = data['book']

    idxToPrice = dict()
    idxToPrice['book'] = 'price'

    for i in range(len(price)):
        #The only values in this column that are floats are the NA values. Everything else is a valid price string
        if type(price[i]) == float:
            idxToPrice[bookNum[i]] = "NULL"
        else:
            idxToPrice[bookNum[i]] = str(price[i])[2:]

    PriceExport = pd.DataFrame.from_dict(idxToPrice, orient="index")
    PriceExport.to_csv('Clean_Data/price.csv')


# def db_connection():
#     try:
#         conn = db.connect(
#             user="db_user",
#             password="db_user_passwd",
#             host="192.0.2.1",
#             port=3306,
#             database="employees"
#     )
#     except db.Error as e:
#         print(f"Error connecting to MariaDB Platform: {e}")
#         sys.exit(1)

if __name__ == "__main__":
    #Read in raw data, inventory.csv
    data = pd.read_csv('inventory_copy.csv', encoding = "ISO-8859-1")   
    df = pd.DataFrame(data, columns= ['book','title','author','binding','pubdate','publisher','isbn10','isbn13','condition','dustjacket','signed','edition','price','descr','synopsis','about_auth'])
    

    #book_clean(df)
    #title_clean_1(df)
    #pubdate_clean(df)
    price_clean(df)

