import pandas as pd
import networkx as nx
import ipywidgets as wd
from IPython.display import display
import sqlalchemy as sa
from tqdm.notebook import tqdm

class socios():
    G = nx.Graph()

    def __init__(self,db,test=True):
        engine = sa.create_engine(db)
        #engine = sa.create_engine('sqlite:///grapho20230315.db')
    
        print("Lendo database...")
        with engine.connect() as db:
            query ='''SELECT COUNT() FROM grapho;'''
            total = db.execute(sa.text(query)).fetchall()[0][0]
            if test:
                query ='''SELECT A,B FROM grapho limit 10;'''
            else:
                query ='''SELECT A,B FROM grapho;'''
            cursor = db.execute(sa.text(query))
            for i in tqdm(cursor,total=total):
                socios.G.add_edge(*i)
        print("Número de registros carregados: {:,}".format(socios.G.number_of_nodes()).replace(",","."))

        lb_alvo = wd.Label("ALVO:")
        tx_alvo = wd.Text(value='TELEFONICA')
        box_alvo=wd.HBox([lb_alvo,tx_alvo])
        lb_pesquisa = wd.Label("ORIGEM:")
        tx_pesquisa = wd.Text(value='NESTLE')
        bt_pesquisa = wd.Button(description="PESQUISAR", icon='search')
        out = wd.Output(layout={'border': '1px solid black'})
        box_origem=wd.HBox([lb_pesquisa,tx_pesquisa,bt_pesquisa])
        box=wd.VBox([box_alvo,box_origem,out])

        def executa(self):
            with out:
                out.clear_output()
                socios.localizar(tx_alvo.value,tx_pesquisa.value)

        bt_pesquisa.on_click(executa)

        print("Sugestoes de pesquisa: Nestle, Telefonica,Odebrecht,Wassef...\n")
        display(box)

    def validar(pesquisa:str)->str:
        pesquisa = pesquisa.upper()
        for node in tqdm(socios.G.nodes()):
            if node.startswith(pesquisa):
                return node
        return ""

    def localizar(inicio, fim):
        inicio, fim = socios.validar(inicio), socios.validar(fim)
        print(f" Inicio validado: {inicio} \n Fim validado {fim}\n")
        if inicio !="" and fim !="":
            if not nx.has_path(socios.G,inicio ,fim):
                print("Caminho não encontrado")
            else:
                print("Caminho localizado \n"+"*"*64)
                print(*nx.shortest_path(socios.G,source=fim,target=inicio),sep = "\n")
            print("\n")



