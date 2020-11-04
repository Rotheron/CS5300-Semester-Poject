import pandas as pd
import mariadb as db
import re 
import sys
# cd into this directory to run the code \\minerfiles.mst.edu\dfs\users\ztbmwf\CS5300\Semester Project


def book_clean(data):
    # preprocess and clean the data for the "book" column in the data frame (df)
    book = data['book']
    #book = pd.DataFrame([['Sacramento', 'California'], ['Miami', 'Florida']], columns=['City', 'State'])
    book.to_csv('book.csv')


def title_clean(data):
    pass

def author_clean(data):
    author = data['author']
    print(author)
    pass
def binding_clean(data):
    pass
def db_connection():
    try:
        conn = db.connect(
            user="db_user",
            password="db_user_passwd",
            host="192.0.2.1",
            port=3306,
            database="employees"
    )
    except db.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

if __name__ == "__main__":
    data = pd.read_csv(r'\\minerfiles.mst.edu\dfs\users\ztbmwf\CS5300\Semester Project\inventory.csv', encoding = "ISO-8859-1")   
    df = pd.DataFrame(data, columns= ['book','title','author','binding','pubdate','publisher','isbn10','isbn13','condition','dustjacket','signed','edition','price','descr','synopsis','about_auth'])
    book_clean(df)
    author_clean(df)
    pass