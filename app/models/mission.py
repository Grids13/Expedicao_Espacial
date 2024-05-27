from sqlalchemy import and_,desc
from app import db


class Missao(db.Model):
    __tablename__ = 'mission'
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    data_lancamento = db.Column(db.Date)
    destino = db.Column(db.String(100))
    estado = db.Column(db.String(100))
    tripulacao = db.Column(db.String(200))
    carga_util = db.Column(db.String(200))
    duracao = db.Column(db.DateTime)
    custo = db.Column(db.Float)
    status = db.Column(db.Text)

    def __init__(self, nome, data_lancamento, destino, estado, tripulacao, carga_util, duracao, custo, status):
        self.nome = nome
        self.data_lancamento = data_lancamento
        self.destino = destino
        self.estado = estado
        self.tripulacao = tripulacao
        self.carga_util = carga_util
        self.duracao = duracao
        self.custo = custo
        self.status = status

    def save_mission(self,nome, data_lancamento, destino, estado, tripulacao, carga_util, duracao, custo, status):
        try:
            add_banco = Missao(nome, data_lancamento, destino, estado, tripulacao, carga_util, duracao, custo, status)
            print(add_banco)
            db.session.add(add_banco)
            db.session.commit()

        except Exception as e:
            print(e)
    
    


    def update_mission(self, id, nome, data_lancamento, destino, estado, tripulacao, carga_util, duracao, custo, status):
        try:
            db.session.query(Missao).filter(Missao.id==id).update({"nome":nome,
                                                                   "data_lancamento":data_lancamento,
                                                                   "destino":destino,
                                                                   "estado":estado,
                                                                   "tripulacao":tripulacao,
                                                                   "carga_util":carga_util,
                                                                   "duracao":duracao,
                                                                   "custo":custo,
                                                                   "status":status})
            db.session.commit()
        except Exception as e:
            print(e)
    
    def delete_mission(self,id):
        try:
            db.session.query(Missao).filter(Missao.id==id).delete()
            db.session.commit()
        
        except Exception as e:
            print(e)
    
    
    def get_by_id(self, mission_id):
        try:
          mission = db.session.query(Missao).filter(Missao.id == mission_id).all()
          mission_detail = [{'id': missions.id, 
                              'nome':missions.nome, 
                              'data_lancamento':missions.data_lancamento, 
                              'destino':missions.destino,
                              'estado':missions.estado, 
                              'tripulacao':missions.tripulacao, 
                              'carga_util':missions.carga_util, 
                              'duracao':missions.duracao,
                              'custo':missions.custo,
                              'status': missions.status}for missions in mission]
          return mission_detail
        
        except Exception as e:
            print(e)

    def get_by_date(self,data_inicial,data_final):
        try:
            mission = db.session.query(Missao).filter(and_(Missao.data_lancamento >= data_inicial , Missao.data_lancamento <= data_final)).all()
            mission_detail = [{'nome':missions.nome,
                               'data_lancamento':missions.data_lancamento,
                               'status':missions.status}for missions in mission]
            return mission_detail
            
        
        except Exception as e:
            print(e)

    def  all_missions(self,data_inicial,data_final):
         try:
             mission = db.session.query(Missao).filter((Missao.data_lancamento>=data_inicial) & (Missao.data_lancamento<=data_final)).order_by(Missao.data_lancamento.desc()).all()
             mission_detail = [{'nome':missions.nome,
                               'data_lancamento':missions.data_lancamento,
                               'status':missions.status,
                               'destino':missions.destino}for missions in mission]
             
             return mission_detail
         
         except Exception as e:
             return {"error": str(e)}
    