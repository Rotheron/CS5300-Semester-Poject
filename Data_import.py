import pandas as pd
import mariadb as db
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
    data = pd.read_csv('Cole_Processing_Data/inventory.csv', encoding = "ISO-8859-1")   
    df = pd.DataFrame(data, columns= ['book','title','author','binding','pubdate','publisher','isbn10','isbn13','condition','dustjacket','signed','edition','price','descr','synopsis','about_auth'])
    

    #book_clean(df)
    title_clean_1(df)

