# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 13:14:11 2022

@author: juran
"""

# %% Imports
import pandas as pd
from os.path import dirname, realpath
from tqdm import tqdm
# glob é um utilitario pra lidar dom diretorios
from glob import glob

# %% Pegando diretorio atual
workingDir = dirname(realpath(__file__))

# %% Lendo CSV
def readzip(fzip:str):
    col= ['cnpj','tip_socio','nome','cpf_cnpj','cd_qualif','dt_entrada','pais','cpf_rep','representante','cd_qualif_rep','faixa_etaria']
    dt=pd.read_csv(fzip,compression='zip', header=None, sep=';', quotechar='"', encoding='latin1')
    dt.columns=col
    print(f"Registros lidos {len(dt):,}")
    return dt

# %% Criando Dataframe de saida
def converte(dt :pd.DataFrame):
    col1, col2 =[],[]
    for index,registro in tqdm(dt.iterrows(), total=len(dt)):
        try:
            col1.append(registro.cnpj)
            if(registro.tip_socio==1):
                col2.append(registro.cpf_cnpj)
            else:
                col2.append(str(registro.nome) + str(registro.cpf_cnpj))
            if(not pd.isna(registro.representante)):
                col1.append(registro.cpf_cnpj)
                col2.append(str(registro.representante) + str(registro.cpf_rep))
        except:
            print(f"Erro no registro {index}")
    return pd.DataFrame({'col1':col1,'col2':col2})
# %% Utilitario pra retornar os arquivos


# %% Converte e Concatena
files=[]
for i in range(10):
    files.append('K3241.K03200Y'+str(i)+'.D20212.SOCIOCSV.zip')
 
path = workingDir+"\JAN2021SOCIO\\"

for file in files:
    print(f"Lendo arquivo: {file}")
    dt = readzip(path+file)
    print("Convertendo em DataFrame para Grapho")
    out = converte(dt)
    print("Salvando arquivo como:" + file[:-3]+"csv")
    out.to_csv(path+file[:-3]+"csv", sep=";",encoding='latin1',header=False, index=False)
    

# %% Concatenar em um unico arquivo
print("Concatenando tudo em um CSV")

df = pd.concat(map(lambda x: pd.read_csv(x, header=None, sep=';', encoding='latin1'),
    glob(path+'*.csv')))
print(f"{len(df):,}")
df.to_csv("socios.csv",sep=";",index=False, header=False)

print("Tudo terminadoooooo!!!!!!!!!!!!!")

# %%

print(df.head())