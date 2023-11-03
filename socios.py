from networkx import Graph, has_path,shortest_path
from ipywidgets import Label, Text, HBox, Button, Output, VBox
from IPython.display import display
from sqlalchemy import create_engine,text
from tqdm.notebook import tqdm

class socios():
    G = Graph()
    __full = False
    __db = None

    def __init__(self,db,test=True):
        socios.__db = db
        engine = create_engine(socios.__db)
    
        print("Lendo database...")
        with engine.connect() as db:
            query="SELECT name FROM sqlite_schema WHERE type ='table' AND name='EMPRESA' limit 1;"
            try:
                socios.__full = True if db.execute(text(query)).fetchone() else False    
            except:
                query="SELECT name FROM sqlite_master WHERE type ='table' AND name='EMPRESA' limit 1;"
                socios.__full = True if db.execute(text(query)).fetchone() else False
            query ='''SELECT COUNT() FROM grapho;'''
            total = db.execute(text(query)).fetchall()[0][0]
            if test:
                query ='''SELECT A,B FROM grapho limit 10;'''
            else:
                query ='''SELECT A,B FROM grapho;'''
            cursor = db.execute(text(query))
            for i in tqdm(cursor,total=total):
                socios.G.add_edge(*i)
        print("Número de registros carregados: {:,}".format(socios.G.number_of_nodes()).replace(",","."))

        lb_alvo = Label("DESTINO:")
        tx_alvo = Text(value='00000000')
        box_alvo= HBox([lb_alvo,tx_alvo])
        lb_pesquisa = Label("ORIGEM:")
        tx_pesquisa = Text(value='43073394')
        bt_pesquisa = Button(description="PESQUISAR", icon='search')
        out = Output(layout={'border': '1px solid black'})
        box_origem=HBox([lb_pesquisa,tx_pesquisa,bt_pesquisa])
        box=VBox([box_alvo,box_origem,out])

        def executa(self):
            with out:
                out.clear_output()
                socios.localizar(tx_alvo.value,tx_pesquisa.value)

        bt_pesquisa.on_click(executa)
        print("Sugestoes de pesquisa: Entre com Radical do CNPJ com 8 digitos ou Nome completo \n")
        display(box)

    def validar(pesquisa:str)->str:
        pesquisa = pesquisa.upper()
        for node in tqdm(socios.G.nodes()):
            if node.startswith(pesquisa):
                return node
        return ""

    def razao(lista:list)->list:
        if socios.__full:
            engine = create_engine(socios.__db)
            res=[]
            with engine.connect() as db:
                for i in lista:
                    c=""
                    if len(i)==8:
                        c = db.execute(text(f"SELECT RAZAO_SOCIAL FROM EMPRESA WHERE CNPJ_BASICO={i} LIMIT 1;")).fetchone()[0]
                    res.append(i+" "+c)
        else:
            return lista
        return res

    def localizar(inicio:str, fim:str)-> None:
        inicio, fim = socios.validar(inicio), socios.validar(fim)
        print(f" Destino validado: {inicio} \n Origem validado {fim}\n")
        if inicio !="" and fim !="":
            if not has_path(socios.G,inicio ,fim):
                print("Caminho não encontrado")
            else:
                print("Caminho localizado \n"+"*"*64)
                path=shortest_path(socios.G,source=fim,target=inicio)
                print(*socios.razao(path),sep = "\n")
            print("\n")
