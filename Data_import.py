import pandas as pd
import mariadb as db
import math
import re 

#Book_ID
def book_clean(data):
    # preprocess and clean the data for the "book" column in the data frame (df)
    book = data['book']
    #book = pd.DataFrame([['Sacramento', 'California'], ['Miami', 'Florida']], columns=['City', 'State'])
    book.to_csv('Clean_Data/book.csv')

#Title
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
                idxToTitle[book_nos[i]] = "NULL"
                break

        #Title was clean
        if(validTitle):
            idxToTitle[book_nos[i]] = str(titles[i])

    #Prepare pandas to write out to csv
    titleExport = pd.DataFrame.from_dict(idxToTitle, orient="index")

    #Write out the book number, and the clean title to a csv so we can stitch it back together later 
    titleExport.to_csv(r'Clean_Data/titles1.csv')

#Binding_Type
def binding_clean(data):

    No_covers = list(['Unknown Binding', 'NaN', 'Na', 'NA', 'NULL',"None",'Reliure inconnue','Contacter le vendeur'])
    df = data[['book','binding']]
   
    df.loc[df['binding'].isin(No_covers), 'binding'] = ''
   
    #Parsing out numbers
    df['binding'] = df['binding'].str.replace(r'\d','')

    Paperback = list(['Broché', 'Taschenbuch', 'Encuadernaciï¿½n de tapa blanda', 'brochï¿½', 'Brochï¿½', 'Broché.',
                        'aschenbuch', 'Broschiert', 'brossura', 'Brosurra','Livre de poche',
                        'Encuadernación de tapa blanda','Rustica','Rústica','Couverture souple', 'Format Poche'])

    Hardback = list(['Gebundene Ausgabe','gebundene Ausgabe.', 'gebundene Ausgabe Leinen',
                     'Cartonné','Couverture rigide','Indbundet pænt halvlæder'])
    Hardcover = list(['hardcover','hard cover','HardCover','hardCover', 'Hard Cover', 'Hard cover'])
    df.loc[df['binding'].isin(Paperback), 'binding'] = 'Paperback'
    df.loc[df['binding'].isin(Hardback), 'binding'] = 'Hardback'
    df.loc[df['binding'].isin(Hardcover), 'binding'] = 'Hardcover'

    df.to_csv('Clean_Data/binding.csv')
    
#Pub_Date
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

#Condition
def condition_clean_1(data):
    #Read in "book" and the raw "condition" column.
    book_nos = data['book']
    conditions = data['condition']

    #Key = "book" from raw data, value = clean title  
    idxToCondition = dict()
    idxToCondition["book"] = "condition"    #Hardcode in the column names for the csv when rendered in Excel

    #Keep only conditions that match one of these (any case)
    validConditions = ["new", "very good", "good", "fair", "poor"]

    #Iterate over every title and store the dataframe indeces of titles with only alphabetic characters in it
    for i in range(len(conditions)):                    #Title Loop
        if(not isinstance(conditions[i], float)):       #Hardcoded error handler (NA is a float in a csv apparently...)
            if(conditions[i].lower() in validConditions):
                idxToCondition[book_nos[i]] = str(conditions[i].lower())
            else:
                idxToCondition[book_nos[i]] = "NULL"
        else:
            idxToCondition[book_nos[i]] = "NULL"

        print(i)

    #Prepare pandas to write out to csv
    conditionExport = pd.DataFrame.from_dict(idxToCondition, orient="index")

    #Write out the book number, and the clean title to a csv so we can stitch it back together later 
    conditionExport.to_csv(r'Clean_Data/conditions1.csv')

#Price
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

#Author_Note
def authornote_clean_1(data):
    #I just did a quick run through in Excel for the first level of cleaning.
    pass

#ISBN_10
def isbn10_clean_1(data):
    isbn10 = data['isbn10']
    bookNum = data['book']

    idxToIsbn10 = dict()
    idxToIsbn10['book'] = 'isbn10'


    for i in range(len(isbn10)):
        if(isinstance(isbn10[i], float)):
            idxToIsbn10[bookNum[i]] = "NULL"
        elif(len(isbn10[i]) == 10):
            idxToIsbn10[bookNum[i]] = str(isbn10[i])
        else:
            idxToIsbn10[bookNum[i]] = "NULL"


    PriceExport = pd.DataFrame.from_dict(idxToIsbn10, orient="index")
    PriceExport.to_csv('Clean_Data/isbn10.csv')

#Signed
def signed_clean(data):
    signed = data['signed']
    bookNum = data['book']

    idxToSigned = dict()
    idxToSigned['book'] = 'signed'

    for i in range(len(signed)):
        if type(signed[i]) == float:
             idxToSigned[bookNum[i]] = "NULL"
        elif (signed[i][:1] == 'n' or signed[i][:1] == 'N') and signed[i] != "NULL":
            idxToSigned[bookNum[i]] = "NULL"
        else:
            idxToSigned[bookNum[i]] = signed[i]

    SignedExport = pd.DataFrame.from_dict(idxToSigned, orient="index")
    SignedExport.to_csv('Clean_Data/signed.csv')

#Jacket_Condition
def jacket_clean_1(data):
    #Read in "book" and the raw "condition" column.
    book_nos = data['book']
    conditions = data['dustjacket']

    #Key = "book" from raw data, value = clean title
    idxToCondition = dict()
    # Hardcode in the column names for the csv when rendered in Excel
    idxToCondition["book"] = "JacketCondition"

    #Keep only conditions that match one of these (any case)
    validConditions = ["new", "very good", "good", "fair", "poor"]

    #Iterate over every title and store the dataframe indeces of titles with only alphabetic characters in it
    for i in range(len(conditions)):  # Title Loop
        # Hardcoded error handler (NA is a float in a csv apparently...)
        if(not isinstance(conditions[i], float)):
            if(conditions[i].lower() in validConditions):
                idxToCondition[book_nos[i]] = str(conditions[i].lower())
            else:
                idxToCondition[book_nos[i]] = "NULL"
        else:
            idxToCondition[book_nos[i]] = "NULL"

        print(i)

    #Prepare pandas to write out to csv
    conditionExport = pd.DataFrame.from_dict(idxToCondition, orient="index")

    #Write out the book number, and the clean title to a csv so we can stitch it back together later
    conditionExport.to_csv(r'Clean_Data/jacketConditions1.csv')

#Edition
def edition_clean(data):
    
    df = data[['book','edition']]
    df['edition'] = df['edition'].str.replace(r'1st','First')
    df['edition'] = df['edition'].str.replace(r'1','First')
    df['edition'] = df['edition'].str.replace(r'2nd','Second')
    df['edition'] = df['edition'].str.replace(r'Printing','Edition')
    df['edition'] = df['edition'].str.replace(r'.*Unknown.*','')
  
    df.to_csv('Clean_Data/edition.csv')

#Author Name (This keeps all the bad authors)
def author_clean_1(data):
    df = data[['book', 'author']]
    #df['b'] = df.author.str.match(r'[a-zA-Z]*[, ]+[a-zA-Z]*[ ]?[a-zA-Z]*').astype(str)

    df['author'] = df.author.str.replace(r'^[a-zA-Z]*[, ]+[a-zA-Z]*[ ]?[a-zA-Z]*$', "").astype(str)

    df.to_csv('Clean_Data/bad_authors1.csv')
    
def language_parse(data):
    
    German  = list(['aschenbuch', 'Broschiert', 'Gebundene Ausgabe', 'gebundene Ausgabe.', 
                    'gebundene Ausgabe Leinen',"None"])
    French  = list(['Contacter le vendeur', 'Broché', 'Broché.', 'brochï¿½', 'Brochï¿½', 'Cartonné','Couverture rigide',
                'Couverture souple','Format Poche','Livre de poche','Reliure inconnue'])
    Italian = list(['brossura','Brosurra','Rustica','Rústica'])
    Spanish = list(['Encuadernación de tapa blanda'])
    Danish  = list(['Indbundet pænt halvlæder'])
    bind_data = data[['book', 'binding']]

    df = data[['book']]
    df['language'] = 'English'
    df.loc[bind_data['binding'].isin(German), 'language'] = 'German'
    df.loc[bind_data['binding'].isin(French), 'language'] = 'French'
    df.loc[bind_data['binding'].isin(Italian), 'language'] = 'Italian'
    df.loc[bind_data['binding'].isin(Spanish), 'language'] = 'Spanish'
    df.loc[bind_data['binding'].isin(Danish), 'language'] = 'Danish'
    
    df.to_csv('Clean_Data/language.csv')


def synopsis_clean(data):
    synopsis = data['synopsis']
    bookNum = data['book']

    idxToSynopsis = dict()
    idxToSynopsis['book'] = 'synopsis'

    for i in range(len(synopsis)):
        if type(synopsis[i]) == float:
            idxToSynopsis[bookNum[i]] = "NULL"
        else:
            if 'ï¿½' in synopsis[i]:
                synopsis[i] = synopsis[i].replace('ï¿½', '')
            if '&&' in synopsis[i]:
                synopsis[i] = synopsis[i].replace('&&', '')
            if 'LDIV' in synopsis[i]:
                synopsis[i] = synopsis[i].replace('LDIV', '')
            idxToSynopsis[bookNum[i]] = synopsis[i]

    SynopsisExport = pd.DataFrame.from_dict(idxToSynopsis, orient="index")
    SynopsisExport.to_csv('Clean_Data/synopsis.csv')

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
    #title_clean_1(df)
    #binding_clean(df)
    #pubdate_clean(df)
    #condition_clean_1(df)
    #price_clean(df)
    #isbn10_clean_1(df)  # Code adapted from https://www.geeksforgeeks.org/program-check-isbn/isbn10_clean_1(df)
    #signed_clean(df)
    #jacket_clean_1(df)
    #edition_clean(df)
    #author_clean_1(df)
    #synopsis_clean(df)
    #language_parse(df)
