import serial
import pyvisa as visa


class leituraHipot(object):

    def __init__(self):
        self.status=False
        self.serial=None
        self.visa=visa.ResourceManager(r'C:\Windows\system32\visa64.dll')
        self.conexao=[False,False]

    def getlista(self):

        return self.visa.list_resources()

    def conectaVisa(self, equipamento):
        try:
            self.equipamentoVisa = self.visa.open_resource(equipamento)


            a=self.getVisa()
            if a==None:
                self.conexao[1]=False
                return False
            else:
                self.conexao[1]=True
                return True
            # comando
            # self.equipamento.query("comando")

        except Exception as e:
            self.conexao[1]=False
            print("Erro Visa:", e)

            return False

    def conectaSerial(self, porta):

        try:
            self.closeSerial()
            self.equipamento = serial.Serial(port=porta, baudrate=9600)

            print(self.conexao)
            self.conexao[0]=True

            print("Foi Serial")

            return True
        except Exception as e:

            self.conexao[0] = False
            print("Erro Serial:", e)


            return False

    def getSerial(self):
        try:
            if self.equipamento.in_waiting > 0:
                txt = self.equipamento.readline()
                txt=txt.decode("utf8")

                return txt.replace("\n","")
            else:
                return None
        except Exception as e:
            print("Erro Leitura:",e)
            self.conexao[0]=False
            return None

    def getVisa(self):
        try:
            #val=self.equipamento.query("MEAS:VOLT? CH1")
            val=self.equipamentoVisa.query("C2:PAVA? MAX\n")
            val=str(val).replace("C2:PAVA MAX,","").replace("V\n","")
            print("Float",float(val))
            #self.equipamento.write("SYST:REM\n")
            #time.sleep(1)
            #comando para multímetro
            #self.equipamento.query("MEAS:VOLT? CH1\n")
            #print(self.equipamento.read())
            #self.equipamento.write('CURV?')
            #val=self.equipamento.read_bytes(1)
            return val

        except Exception as e:
            self.closeVisa()
            print("Erro Visa:",e)
            self.conexao[1]=False
            return None

    def getConexao(self):
        return self.conexao

    def closeSerial(self):
        try:
            self.equipamento.close()
            self.conexao[0]=False
        except:
            self.conexao[0]=False
            print("Fechado Serial")

    def closeVisa(self):
        try:
            self.equipamentoVisa.close()
            self.conexao[1]=False
        except:
            print("Fechado Visa")
            self.conexao[1]=False

if __name__ =="__main__":
    v=leituraHipot()
    print(v.getlista())