from flask import jsonify
from flask_restful import Resource, reqparse
from app.models.mission import Missao
from datetime import datetime

# Para add
argumentos = reqparse.RequestParser() # Definir os argumentos
argumentos.add_argument('nome', type=str)
argumentos.add_argument('data_lancamento', type=str)
argumentos.add_argument('destino', type=str)
argumentos.add_argument('estado', type=str)
argumentos.add_argument('tripulacao', type=str)
argumentos.add_argument('carga_util', type=str)
argumentos.add_argument('duracao', type=str)
argumentos.add_argument('custo', type=float)
argumentos.add_argument('status', type=str)

# Para att
argumentos_update = reqparse.RequestParser()
argumentos_update.add_argument('id', type=int)
argumentos_update.add_argument('nome', type=str)
argumentos_update.add_argument('data_lancamento', type=str)
argumentos_update.add_argument('destino', type=str)
argumentos_update.add_argument('estado', type=str)
argumentos_update.add_argument('tripulacao', type=str)
argumentos_update.add_argument('carga_util', type=str)
argumentos_update.add_argument('duracao', type=str)
argumentos_update.add_argument('custo', type=float)
argumentos_update.add_argument('status', type=str)

#Para Deletar
argumentos_delete = reqparse.RequestParser()
argumentos_delete.add_argument('id', type=int)

#por id
argumentos_search_id = reqparse.RequestParser()
argumentos_search_id.add_argument('id', type=int)

#Para pesquisar por data
argumentos_search_data = reqparse.RequestParser()
argumentos_search_data.add_argument('data_inicial', type=str)
argumentos_search_data.add_argument('data_final', type=str)




#Pesquisar por Id
class MissionById(Resource):
    def get(self):
        try:
           data = argumentos_search_id.parse_args()
           if 'id' not in data or not data['id']:
                return {"message": "O parametro Id  e necessario"}

           missao=Missao.get_by_id(self,data['id'])
           
           if missao:
                return jsonify(missao)
           else:
                return {"message": "Missao nao encontrada"}
        
        except Exception as e:
            return jsonify({"error": str(e)})

class MissionByDate(Resource):
    def get(self):
        try:
           data = argumentos_search_data.parse_args()
           data_inicial = datetime.strptime(data['data_inicial'],'%Y-%m-%d')
           data_final = datetime.strptime(data['data_final'],'%Y-%m-%d')

           missao=Missao.get_by_date(self,data_inicial, data_final)
           
           if missao:
               return jsonify(missao)
           
           else:
               return {"Message":"Missao nao encontrada"},404

        except Exception as e:
            return jsonify({"error": str(e)})   
#Criar Missao
class MissionCreate(Resource):
    def post(self):
        try:
            data = argumentos.parse_args()
            
            data_lancamento = datetime.strptime(data['data_lancamento'],'%Y-%m-%d')
            duracao = datetime.strptime(data['duracao'], '%Y-%m-%d %H:%M:%S')
            
            Missao.save_mission(self, data['nome'], 
                                data_lancamento,
                                data['destino'], 
                                data['estado'],
                                data['tripulacao'], 
                                data['carga_util'], 
                                duracao, 
                                data['custo'], 
                                data['status'])

            return jsonify( {"message": 'Missão criada com sucesso!'})

        except Exception as e:
            return jsonify({"error": str(e)})




#Editar missao 
class MissionUpdate(Resource):
    def put(self):
        try:
            data = argumentos_update.parse_args()
           
            data_lancamento = datetime.strptime(data['data_lancamento'], '%Y-%m-%d')
            duracao = datetime.strptime(data['duracao'], '%Y-%m-%d %H:%M:%S')
            
            Missao.update_mission(self, data['id'],
                                    data['nome'],
                                    data_lancamento,
                                    data['destino'],
                                    data['estado'],
                                    data['tripulacao'],
                                    data['carga_util'],
                                    duracao,
                                    data['custo'],
                                    data['status']
                                    )

            return {"message": 'Missão atualizada com sucesso!'}
        
        except Exception as e:
            return jsonify({"error": str(e)})

 #Deletar Missao    
class MissionDelete(Resource):
    def delete(self):
        try:
           data = argumentos_delete.parse_args()
           Missao.delete_mission(self,data['id'])
           
           return {"message": 'Missão deletada com sucesso!'}
           
        
        except Exception as e:
            return jsonify({"error": str(e)})



