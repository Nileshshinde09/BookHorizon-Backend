from flask import Flask, jsonify, request
import joblib
import numpy as np
from bookinfo_converter import book_info_to_list,getISBN,getDETAILS
popular = joblib.load("popular_info.joblib")
books = joblib.load("books_info.joblib")
pt = joblib.load("pt.joblib")
similarity_score = joblib.load("similarity_score.joblib")



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


@app.route('/recommend_books',methods=['GET','POST'])
def recommend():
    nameofbook = request.args.get('bookname')
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
    

@app.route('/getISBN',methods=['GET','POST'])
def findISBN():
    nameofbook=request.args.get('isbn')
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
@app.route('/getDetialsOnISBN',methods=['GET','POST'])
def getDetialsOnISBN(nameofbook):
    nameofbook=request.args.get('ISBN')
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

