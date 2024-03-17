#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session, request, render_template_string
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    # session['page_views'] = 0
    session.pop('page_views', default=None)
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():


    articles = [article.to_dict() for article in Article.query.all()]
    
    response = make_response(
        jsonify(articles),
        200
    )

    return response

@app.route('/articles/<int:id>', methods=['GET'])
def show_article(id):

    

    
    if request.method == 'GET':

        # count = int(request.cookies.get('visited_article count', 0))
        # session['page_views'] = 0
        
        
        # count = count+1
        if 'page_views' in session:
            session['page_views'] = session.get('page_views') + 1

        else: 
            session['page_views'] = 1

        if 'page_views' in session and session['page_views'] > 3:
            return make_response(
            jsonify({'message': 'Maximum pageview limit reached'}),
            401
        )




    
        article = Article.query.filter_by(id=id).first()



        article_dict = article.to_dict()

        response = make_response(
            jsonify(article_dict),
            200
        )


        # response.set_cookie('visited_article count', str(count))



        return response
    
# @app.route('/get_session')
# def get_session():
    
#         return render_template_string("""
#             {% if session['page_views'] %}
#                 <h1> {{ session['page_views'] }}!</h1>
#             {% else %}
#                 <h1>Nothing</h1>
#             {% endif %}
#         """)
     

if __name__ == '__main__':
    app.run(port=5555)
