import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()

def conectarSoltronicBD():
    try:
        conexao = mysql.connector.connect(
            host = os.getenv("HOST"), 
            user  = os.getenv("USER"),
            password = os.getenv("PASSWORD"),
            database = os.getenv("DATABASE")
        )

        if(conexao):
            print("✅ Conexão realizada com sucesso!")
            return conexao
        else:
            print("❌ Não foi possível conectar com PORTAIS_SOLTRONIC.")
            return None
        
    except Exception as connectFail:
        print("erro: ", connectFail)
        return None

def executarConsulta(script):
    conexao = conectarSoltronicBD()
    cursor = conexao.cursor()
    if(conexao):
        cursor.execute(script)
        resultado = cursor.fetchall()

        for i in resultado:
            print(i)

        cursor.close()
        conexao.close()

        return resultado
    else:
        print("❌ Não foi possível realizar a Consulta: Conexão não foi estabelecida.")

def selecionarCodST(script):
    conexao = conectarSoltronicBD()
    cursor = conexao.cursor()
    if(conexao):
        cursor.execute(script)
        resultado = cursor.fetchone()

        if(resultado):
            return resultado[0]
        else:
            return None
    else:
        print("❌ Não foi possível pegar o Codigo Soltronic: Conexão não estabelecida.")

def selecionarRanking(script):
    conexao = conectarSoltronicBD()
    cursor = conexao.cursor()
    if(conexao):
        cursor.execute(script)
        resultado = cursor.fetchone()
        if(resultado):
            return str(resultado)
        else:
            return None
    else:
        print("❌ Não foi possível pegar o Ranking do Código Soltronic: Conexão não estabelecida.")