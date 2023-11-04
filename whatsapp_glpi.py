from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import requests
import time

Base = declarative_base()

class Ticket(Base):
    __tablename__ = 'glpi_tickets'
    id = Column(Integer, primary_key=True)
    status = Column(Integer)
    processado = Column(Boolean, default=False)  
    name = Column(String) 
 

def monitorar_chamados():
    engine = create_engine('mysql+mysqlconnector://root:''@localhost/glpi10')
    Session = sessionmaker(bind=engine)

    while True:
        try:
            session = Session()
            novos_chamados = session.query(Ticket).filter_by(status=1, processado=False).all()

            for chamado in novos_chamados:

                #Irá fazer a chamada a API

                response = requests.get('https://api.callmebot.com/whatsapp.php', params={
                'phone': 'SEU NUMERO DE TELEFONE',
                'text': f'Novo Chamado Registrado | Título: {chamado.name} | Número: {chamado.id}',
                'data': 'qualquer_outro_dado_necessario',
                'apikey': 'SUA API CALL ME BOT'
                })

                if response.status_code == 200:
                    print(f'Chamado {chamado.id} processado com sucesso!')
                    chamado.processado = True
                else:
                    print(f'Erro ao processar chamado {chamado.id}')
                
            session.commit()

        finally:
            session.close()

        print("Verificação concluída. Aguardando 10 segundos.")
        time.sleep(10)

if __name__ == '__main__':
    monitorar_chamados()

