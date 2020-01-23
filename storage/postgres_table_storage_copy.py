from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from reader_storage import Storage

db = create_engine('postgresql://postgres:pass@localhost/all_books')
db.connect()
base = declarative_base()

class MyBook(base):
    __tablename__ = 'mybooks'

    ids = Column(String, primary_key=True)
    title = Column(String)
    author = Column(String)

#creating a session/connection with engine
Session = sessionmaker(db)  
session = Session()

base.metadata.create_all(db)

class Postgres(Storage):


    book_counter = 0

    def __init__(self):
        self.book_record = []
        self.book = {}


    
    def create(self,**kwargs):

        ids=kwargs['id']
        t=kwargs['title']
        a=kwargs['author']
        abook= MyBook(ids=ids, title = t, author = a)  
        session.add(abook)  
        session.commit()        
    
    def fetch(self, **kwargs):

        if  'id' in kwargs and len(kwargs) == 1 :
            idn = kwargs['id']
            result = session.query(MyBook).filter_by(ids = idn)
            if result:
                for book in result:
                    self.book['id'] = book.ids
                    self.book['title'] = book.title
                    self.book['author'] = book.author
                    self.book_record.append(self.book)
                return self.book_record
            return 'No Record Found'

        if  'title' in kwargs and len(kwargs) == 1 :
            title = kwargs['title']
            result = session.query(MyBook).filter_by(title = title)
            if result:
                for book in result:
                    self.book['id'] = book.ids
                    self.book['title'] = book.title
                    self.book['author'] = book.author
                    self.book_record.append(self.book)
                return self.book_record
            return 'No Record Found'            


        if  'author' in kwargs and len(kwargs) == 1:
            author = kwargs['author']
            result = session.query(MyBook).filter_by(author = author)
            if result:
                for book in result:
                    self.book['id'] = book.ids
                    self.book['title'] = book.title
                    self.book['author'] = book.author
                    self.book_record.append(self.book)
                return self.book_record
            return 'No Record Found' 


    def delete(self, **kwargs):

        if  'id' in kwargs and len(kwargs) == 1:
            idn = kwargs['id']
            for book in session.query(MyBook).filter_by(ids = idn):
                session.delete(book)
                session.commit()
                return 'delete successful'                
            return 'no record found'


        if  'author' in kwargs and len(kwargs) == 1:
            author = kwargs['author']
            for book in session.query(MyBook).filter_by(author = author):
                session.delete(book)
                session.commit()
                return 'delete successful'                
            return 'no record found'

        if  'title' and  'author' in kwargs  and len(kwargs) == 2:
            title = kwargs['title']
            author = kwargs['author']
            for book in session.query(MyBook).filter_by(author = author).filter_by(title = title):
                session.delete(book)
                session.commit()
                return 'delete successful'                
            return 'no record found'


    def fetch_all(self):
        books = session.query(MyBook).all()
        if books :
            return [book for book in books]             


# print(add_up(1,2))
a=Postgres()
# b=InMemory()
# print(a.create(id=8,author='Aka', title='Python Introduction'))
# print(a.create(id=9,author='sola',title='kemi'))
# print(a.fetch(id='1'))
# print(a.delete(id='1'))
print(a.delete(author='Aka',title ='Python Introduction'))
