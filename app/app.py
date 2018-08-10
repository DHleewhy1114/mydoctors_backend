from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_graphql import GraphQLView
from schema import schema
from models import db_session,User
from flask_login import LoginManager
from flask_login import login_user, logout_user, current_user, login_required
import json
from flask_jwt_extended import (
    JWTManager, jwt_optional, create_access_token,
    get_jwt_identity, jwt_required
)
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'#바꿀것
#index login 설정할것
login_manager=LoginManager()
login_manager.init_app(app)
jwt = JWTManager(app)

@app.route('/')
def index():
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
    access_token = create_access_token(identity=username)
    print (access_token)
    return jsonify(access_token=access_token), 200

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
    #return view
    return jwt_required(view)

app.add_url_rule('/graphql', view_func=graphql_view())

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.run(threaded=True, debug=True)