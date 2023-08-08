from flask import Flask,render_template,request
import pandas as pd
import numpy as np

popular_books = pd.read_pickle('popular.pkl')
pt = pd.read_pickle('pt.pkl')
books = pd.read_pickle('books.pkl')
similarity_scores = pd.read_pickle('similarity_scores.pkl')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popular_books['Book-Title'].values),
                           author =list(popular_books['Book-Author'].values),
                           image=list(popular_books['Image-URL-M'].values),
                           votes=list(popular_books['num_rating'].values),
                           rating=list(popular_books['avg_rating'].values)
                           )
@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route("/recommend_books", methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]

    data = []
    for i in similar_items:
        item = []
        temp = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('recommend.html',data=data)

if __name__ == '__main__':
    app.run(debug=True)