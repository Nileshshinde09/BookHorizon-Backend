from flask import Flask, jsonify, request
import joblib
import numpy as np
# from bookinfo_converter import book_info_to_list,getISBN,getDETAILS
popular = joblib.load("popular_info.joblib")
books = joblib.load("books_info.joblib")
pt = joblib.load("pt.joblib")
similarity_score = joblib.load("similarity_score.joblib")

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

app = Flask(__name__)
@app.route('/')
def index():
    response =  jsonify({"Home":"Home"})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response
@app.route('/home',methods=['GET'])
def Home():
    if request.method == 'GET':
        response = jsonify( book_info_to_list())
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response


@app.route('/recommend_books/<string:nameofbook>',methods=['GET','POST'])
def recommend(nameofbook):
    if nameofbook:
        book_name_input = nameofbook
        index = np.where(pt.index == book_name_input)[0][0]
        similar_items = sorted(list(enumerate(similarity_score[index])),key = lambda x:x[1],reverse = True)[1:41]
        recommend_data = []
        for i in similar_items:
            item = []
            temp = books[books['Book-Title']== pt.index[i[0]]]
            item.extend(list(temp.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp.drop_duplicates('Book-Title')['Image-URL-M'].values))
            item.extend(list(temp.drop_duplicates('Book-Title')['ISBN'].values))


            recommend_data.append(item)
        response = jsonify(recommend_data)
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
    

@app.route('/getISBN/<string:nameofbook>',methods=['GET','POST'])
def findISBN(nameofbook):
    
    if nameofbook:
        try:
            
            response = jsonify(getISBN(name=nameofbook))
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            response.headers.add('Access-Control-Allow-Credentials', 'true')

            return response
        
        except Exception as e:
            return jsonify({"error":e})    
@app.route('/getDetialsOnISBN/<string:nameofbook>',methods=['GET','POST'])
def getDetialsOnISBN(nameofbook):
    
    if nameofbook:
        try:
            response = jsonify(getDETAILS(nameofbook))
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            response.headers.add('Access-Control-Allow-Credentials', 'true')

            return response
        
        except Exception as e:
            return jsonify({"error":e})    
if __name__=="__main__":
    app.run(debug=True)

