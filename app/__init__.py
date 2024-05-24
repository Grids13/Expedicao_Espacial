from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api


app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///crud3.db'
db = SQLAlchemy(app)

# Importa todos os modelos que você deseja criar no banco de dados
from app.models.mission import Missao
# Cria todas as tabelas no banco de dados
with app.app_context():
    db.create_all()

from app.view.reso_mission import  MissionCreate, MissionUpdate, MissionDelete,MissionById, MissionByDate
api.add_resource(MissionCreate, '/create')
api.add_resource(MissionUpdate, '/update')
api.add_resource(MissionDelete, '/delete')
api.add_resource(MissionById,  '/by_id')
api.add_resource(MissionByDate, '/by_date')
