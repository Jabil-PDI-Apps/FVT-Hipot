
import pyodbc
from sys import platform
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class BancoDeDados(object):

    def __init__(self,host,banco,usuario,senha):
        self.banco=banco
        self.usuario=usuario
        self.senha=senha
        self.host=host
        self.conectaBanco()
    

    def conectaBanco(self):
        #self.bancoDados=pymssql.connect(user=self.usuario,password=self.senha,database=self.banco,host=self.host,port=1433)
        #self.bancoDados=pymssql.connect(user=self.usuario,password=self.senha,database=self.banco,server=self.host,port=3306,charset="CP936")
        try:
            if platform=="linux" or platform=="linux2":
                txt='DRIVER={FreeTDS}; TDS_VERSION=7.4;' +'SERVER='+self.host+', 3306; DATABASE='+self.banco+"; UID="+self.usuario+'; PWD='+self.senha+';'
            else:
                #VERSAO JABIL
                #txt='DRIVER={SQL Server};'+'SERVER='+self.host+'; DATABASE='+self.banco+"; UID="+self.usuario+'; PWD='+self.senha+';'
                #VERSAO LOCAL
                txt = 'DRIVER={SQL Server};' + 'SERVER=' + self.host + ', 3306; DATABASE=' + self.banco + "; UID=" + self.usuario + '; PWD=' + self.senha + ';'
            print(txt)
            self.bancoDados=pyodbc.connect(txt)
            self.cursor=self.bancoDados.cursor()
            return True
        except Exception as e:
            print("Erro:",e)
            return False

    def readQuery(self,query):
        self.cursor.execute(query)
        result=self.cursor.fetchall()
        self.bancoDados.commit()

        #self.bancoDados.close()
        return  result

    def writeQuery(self,query):
        try:
            self.cursor.execute(query)
            self.bancoDados.commit()
            print("insert ok")
            return True
        except Exception as e:
            print("Erro bdo:", e)
            return False
    
    def writeQueryMult(self,sql,val):
        try:
            self.cursor.execute(sql,val)
            self.bancoDados.commit()
            print("insert ok")
            return True
        except Exception as e:
            print("Erro bdo:", e)
            return False
    
    

if __name__ == "__main__":
    banco=BancoDeDados("localhost","bancofv","P&D","@Jabil.2022")
    q=banco.readQuery("SELECT TOP 1 * FROM dbo.Dados ORDER BY id DESC ;")
    banco.writeQuery("INSERT INTO dbo.configuracoes (modelo) VALUES ('Modelo G');")
    #banco.writeQuery("DELETE FROM dbo.configuracoes WHERE id in (8,9, 10);")
    print(q)