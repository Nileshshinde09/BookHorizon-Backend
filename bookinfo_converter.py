import joblib
import ast,json
import numpy as np
def book_info_to_list():
    popular = joblib.load("popular_info.joblib")
    books = joblib.load("books_info.joblib")
    pt = joblib.load("pt.joblib")
    similarity_score = joblib.load("similarity_score.joblib")


    book_name = list(popular['Book-Title'].values),
    author = list(popular['Book-Author'].values),
    image = list(popular['Image-URL-M'].values),
    votes = list(popular['num_rating'].values),
    rating = list(popular['avg_rating'].values)

            

    bkn =[]
    aut = []
    img =[]
    rt =[]
    vt =[]
    for i,val in enumerate(book_name[0]):
        bkn.append(val)
    for i,val in enumerate(author[0]):
        aut.append(val)
    for i,val in enumerate(image[0]):
        img.append(val)
    for i,val in enumerate(votes[0]):
        vt.append(str(val))
    for i,val in enumerate(rating):
        val = str(round(val, 2))
        rt.append(val)
    
    res =[]

    for i,val in enumerate(bkn):
        temp ={
        "id":i+1,
        "book_name":bkn[i],
        "author":aut[i],
        "image":img[i],
        "votes":vt[i],
        "rating":rt[i],
        }
        res.append(temp)
    result = tuple(res)
    return result
def getISBN(name):
    books = joblib.load("books_info.joblib")
    if name:
        bookrow = books[books['Book-Title']==name]
        return str(int(bookrow['ISBN'].iloc[0]))
    return -1

def getDETAILS(nameorisbn):
    books = joblib.load("books_info.joblib")

    if nameorisbn:
        bookrow = books[books['Book-Title']==nameorisbn]
        sr = bookrow.iloc[:1,:6]
        return {
              'ISBN':str(int(sr.iloc[0][0])),
              'BookTitle':sr.iloc[0][1],
              'BookAuthor':sr.iloc[0][2],
              'YearOfPublication':sr.iloc[0][3],
              'Publisher':sr.iloc[0][4],
              'Image':sr.iloc[0][5]
        }
    return -1
            