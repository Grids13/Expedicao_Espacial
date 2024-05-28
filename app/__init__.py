from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///crud3.db'
db = SQLAlchemy(app)

# Importa todos os modelos que você deseja criar no banco de dados
from app.models.mission import Missao
# Cria todas as tabelas no banco de dados
with app.app_context():
    db.create_all()

from app.view.reso_mission import  MissionCreate, MissionUpdate, MissionDelete,MissionById,MissionByDesc
api.add_resource(MissionCreate, '/create')
api.add_resource(MissionUpdate, '/update')
api.add_resource(MissionDelete, '/delete')
api.add_resource(MissionById,  '/id/<int:id>')
api.add_resource(MissionByDesc, '/all')

