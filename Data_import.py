import pandas as pd
import mariadb as db
import math
import re 

#Book_ID
def book_clean(data):
    # preprocess and clean the data for the "book" column in the data frame (df)
    book = data['book']
    #book = pd.DataFrame([['Sacramento', 'California'], ['Miami', 'Florida']], columns=['City', 'State'])
    book.to_csv('Clean_Data/book.csv', index=False)

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

    df.to_csv('Clean_Data/binding.csv', index=False)
    
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
  
    df.to_csv('Clean_Data/edition.csv', index=False)

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
    Spanish = list(['Encuadernación de tapa blanda','Encuadernaci�n de tapa blanda','Encuadernaciï¿½n de tapa blanda'])
    Danish  = list(['Indbundet pænt halvlæder','Indbundet p�nt halvl�der','Indbundet pï¿½nt halvlï¿½der'])
    bind_data = data[['book', 'binding']]
    df = data[['book']]
    df['language'] = 'English'
    df.loc[bind_data['binding'].isin(German), 'language'] = 'German'
    df.loc[bind_data['binding'].isin(French), 'language'] = 'French'
    df.loc[bind_data['binding'].isin(Italian), 'language'] = 'Italian'
    df.loc[bind_data['binding'].isin(Spanish), 'language'] = 'Spanish'
    df.loc[bind_data['binding'].isin(Danish), 'language'] = 'Danish'
    
    df.to_csv('Clean_Data/language.csv', index=False)


def publisher_clean(data):
    df = data[['book','publisher']]
    df['publisher'] = df['publisher'].str.replace(r'.*[dD][oO][Vv][eE][Rr].*','Dover')
    df['publisher'] = df['publisher'].str.replace(r'.*[Aa][cC][eE].*','Ace')
    df['publisher'] = df['publisher'].str.replace(r'.*[bB][aA][lL][Ll][aA][nN][a]?[Tt][iI][nN][Ee].*','Ballantine')
    df.to_csv('Clean_Data/publisher.csv', index = False)

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


def book_merge(title_csv, condition_csv, price_csv, jacket_condition_csv):
    title_df = pd.read_csv(title_csv)
    condition_df = pd.read_csv(condition_csv)
    price_df = pd.read_csv(price_csv)
    jacket_condition_df = pd.read_csv(jacket_condition_csv)

    merge1 = title_df.merge(condition_df, on = 'book')
    merge2 = merge1.merge(price_df, on = 'book')
    merge3 = merge2.merge(jacket_condition_df, on = 'book')

    #Add Book_Info_ID to each book (1-1 match between Book entity and Book_Info entity. [0,12041])
    Book_Info_ID_List = list()
    for i in range(len(merge3)):
        Book_Info_ID_List.append(i)

    merge3["Book_Info_ID"] = Book_Info_ID_List
    merge3.to_csv('Table_Data/book_table.csv', index=False)

def book_info_merge(pubDate_csv, edition_csv, synopsis_csv, signed_csv, ISBN_csv):
    pubDate_df = pd.read_csv(pubDate_csv)
    edition_df = pd.read_csv(edition_csv)
    synopsis_df = pd.read_csv(synopsis_csv)
    signed_df = pd.read_csv(signed_csv)
    ISBN_df = pd.read_csv(ISBN_csv)

    merge1 = pubDate_df.merge(edition_df, on = 'book')
    merge2 = merge1.merge(synopsis_df, on = 'book')
    merge3 = merge2.merge(signed_df, on = 'book')
    merge4 = merge3.merge(ISBN_df, on = 'book')

    merge4 = merge4.drop(columns='book')
    merge4.to_csv('Table_Data/book_info_table.csv')

def linking_table_creator():
    linking_file = "Clean_Data/language.csv" #Set the file you want to grab values from
    table = 'Table_Data/language.csv'
    lookup_table = 'Table_Data/book_languages.csv'
    val_to_replace = 'language'
    data = pd.read_csv(linking_file, encoding = "ISO-8859-1")
    df = pd.DataFrame(data, columns= ['book',val_to_replace])

    Unique = df[val_to_replace].unique()
    Unique_df = pd.DataFrame(Unique, columns = [val_to_replace])
    Unique_df.to_csv(table)

    #Replace values in other csv with corresponding ID
    for index,value in enumerate(Unique):
        df[val_to_replace] = df[val_to_replace].str.replace(value,str(index))
    df.to_csv(lookup_table,index=False)

    

def linking_table_creator_author_book():
    linking_file = "Clean_Data/authors1.csv" #Set the file you want to grab values from
    table = 'Table_Data/authors.csv'
    lookup_table = 'Table_Data/author_book.csv'
    val_to_replace = 'author'
    data = pd.read_csv(linking_file, encoding = "ISO-8859-1")
    df = pd.DataFrame(data, columns= ['book',val_to_replace])

    Unique = df[val_to_replace].unique()
    Unique_df = pd.DataFrame(Unique, columns = [val_to_replace])
    Unique_df.to_csv(table)

    #Replace values in other csv with corresponding ID
    for index,value in enumerate(Unique):
        df[val_to_replace] = df[val_to_replace].str.replace(value,str(index))
    df[val_to_replace] = df[val_to_replace].str.extract(r'(\d+)', expand=False)
    df.to_csv(lookup_table,index=False)

def linking_table_creator_bind_book():
    linking_file = "Clean_Data/binding.csv" #Set the file you want to grab values from
    table = 'Table_Data/binding.csv'
    lookup_table = 'Table_Data/binding_info_book.csv'
    val_to_replace = 'binding'
    data = pd.read_csv(linking_file, encoding = "ISO-8859-1")
    df = pd.DataFrame(data, columns= ['book',val_to_replace])

    Unique = df[val_to_replace].unique()
    Unique_df = pd.DataFrame(Unique, columns = [val_to_replace])
    Unique_df.to_csv(table)
    #Replace values in other csv with corresponding ID
    for index,value in enumerate(Unique):
        df[val_to_replace] = df[val_to_replace].str.replace(str(value),str(index))
    df[val_to_replace] = df[val_to_replace].str.extract(r'(\d+)', expand=False)
    df.to_csv(lookup_table,index=False)

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
    #publisher_clean(df)
    #book_merge('Clean_Data/titles1.csv', 'Clean_Data/conditions1.csv', 'Clean_Data/price.csv', 'Clean_Data/jacketConditions1.csv')
    linking_table_creator_bind_book()
    #book_info_merge('Clean_Data/pubdate.csv', 'Clean_Data/edition.csv', 'Clean_Data/synopsis.csv', 'Clean_Data/signed.csv', 'Clean_Data/isbn10.csv')

