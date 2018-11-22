from flask import Flask, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_graphql import GraphQLView
from schema import schema
from models import db_session,User
from flask_login import LoginManager
from flask_login import login_user, logout_user, current_user, login_required
import json
import os
from werkzeug.utils import secure_filename
import hashlib
import base64
#from flask.ext.uploads import UploadSet, configure_uploads,IMAGES
from flask_jwt_extended import (
    JWTManager, jwt_optional, create_access_token,
    get_jwt_identity, jwt_required
)
IMAGE_FOLDER='./static/img/'
WEB_FRONTEND_FOLDER='../webfrontend/build/'
ALLOWED_EXTENSIONS= set(['jpg','png','jpeg'])
app = Flask(__name__,static_url_path='')
app.config['JWT_SECRET_KEY'] = 'super-secret'#바꿀것
app.config['UPLOAD_FOLDER']=IMAGE_FOLDER
#index login 설정할것
login_manager=LoginManager()
login_manager.init_app(app)
jwt = JWTManager(app)

@app.route('/')
def index():
    print (os.path.abspath(os.path.dirname(__file__)))
    #return app.send_static_file('index.html')
    return "hello"
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

"""
fetch('http://localhost:5000/login',{method:'post',body:JSON.stringify({id:'admin',pw:'dsdsds'})}).then((response)=>response.json()).then(json=>{console.log(json.access_token)})
"""

@app.route('/login',methods=['POST'])
def login():
    print(request)
    print (request.data)
    #loginreq = json.loads(request.data)
    username = "d" #loginreq['id']
    pw = "d" #loginreq['pw']
    user = User.query.filter_by(username=username).first()
    #user_id = ("".join(["USER:",str(user.id)]))
    access_token = create_access_token(identity=user.id)
    print (access_token)
    return jsonify(access_token=access_token), 200

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/user_profile',methods=['GET','POST'])
#추후에 graphql에 합칠 것 
#https://github.com/lmcgartland/graphene-file-upload
#https://github.com/graphql-python/graphene-django/issues/101#issuecomment-331079482
def user_profile():
    if request.method == 'POST':
        print (request)
        print (request.content_type)
        print (request.files)
        if not 'file' in request.files:
            print ("file")
            return None
        else:
            file = request.files['file']
        if file.filename =='':
            print ("file2")
            return None
        if file and allowed_file(file.filename):
            print ("file3")
            #b64decoded_filename = base64.b64decode(user_id)
            #query로 user_id 로 user get 한 후 photo_profile에 'base64encode(User:{id})/file이름' 저장
            #doctor,question 도 같은 방식으로
            filename = secure_filename(file.filename)#위로 바꿀것
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            return None
"""
mutation{
  createUser(input:{
    username:"d"
    passwordHash:"d"
  }){
    user{
      id
      username
      passwordHash
    }
  }
}
"""
def graphql_view():
    view = GraphQLView.as_view('graphql', schema=schema, graphiql=True)
    return view
    #return jwt_required(view)

app.add_url_rule('/graphql', view_func=graphql_view())

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.run(threaded=True, debug=True)