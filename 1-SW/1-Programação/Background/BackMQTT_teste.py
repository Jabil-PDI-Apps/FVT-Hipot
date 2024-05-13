from http import client
import re
import os
import paho.mqtt.client as mqtt
from Classes.Banco import BancoDeDados
import serial
import threading
import time




class Serial_Barcode():
    def __init__(self):
        #self.port = "/dev/ttyUSB0"
        self.port = 'COM4'

        self.baudrate = 9600
        self.ser = ''
       
        print ("Serial:" + str(self.port) +", " + str(self.baudrate))
        self.conectaSerial()

    def conectaSerial(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate)
            print("portUart: " + str(self.ser.is_open))
            return True
        
        except:
            print("erro ao conectar " + self.port + ": ")
            return False
		
    def read(self):
        try:
            if (self.ser.is_open):
                line = self.ser.readline().decode('utf-8').rstrip()
                #line = self.ser.read_until(b'\r').decode('utf-8').rstrip()
                #self.ser.close()            
                return line
            else:
                print("portUart: " + str(self.ser.is_open))
                self.conectaSerial()
            
        except:
            print("erro ao comunicar ")

            return False
    
    def close(self):
        self.ser.close() 


class FVT_IOT_engine():
    def __init__(self):
        
        self.Broker  = "192.168.0.19"
        #self.Broker = "192.168.7.222"
        self.PortaBroker = 1883
        self.KeepAliveBroker = 60

        self.ser = Serial_Barcode()
        self.client = mqtt.Client()
        #self.bc = BancoFVT_Tester()

        #self.bc.novoRegistro("OK", "RCI60F3P210913") #RCI60F3P210913

        #self.topico = 'status/teste'
        self.topico = 'status/fase'

        self.dadoMQTT = ""
        self.dadoser = ""
        self.SN = ""
        self.dado=""
        self.conectaMQTT()

        self.currentSN = ""
        self.modoInsertBcoDados = "TESTANDO"#"INSERIR" #"ATUALIZAR"
    
    def readedSN(self):
        while True:

            try:
                self.dadoser = self.ser.read()
                if (self.dadoser == None):
                    print("Restabelencendo Serial")
                    self.ser.conectaSerial()
                    time.sleep(0.5)

                if (self.dadoser == False):
                    self.ser.close()
                    time.sleep(1)
                    print("clsoseSN")
                time.sleep(0.1)
            except:
                print("Restabelencendo Serial")
                self.ser.conectaSerial()
                time.sleep(0.5)

    
    def on_connect(self, client, userdata, flags, rc):

        print("[STATUS] Conectado ao Broker. Resultado de conexao: "+str(rc))  
        #faz subscribe automatico no topico
        client.subscribe(self.topico)
        
    def on_message(self, client, userdata, message):
        print("mensagem nova")
        self.dadoMQTT = str(message.payload.decode("utf-8"))
  
    def conectaMQTT(self):
        try:
            print("[STATUS] Inicializando MQTT...")
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message
            self.client.connect(self.Broker, self.PortaBroker, self.KeepAliveBroker)
            #self.client.connect(Broker)
            self.client.publish(self.topico,'teste')

        except Exception as e:

            print("erro ao conectar broker" + self.Broker + ": ", e)
            return False

    def startMQTT(self):
        self.client.subscribe(self.topico)
        self.client.loop_forever()
    
    def run(self):        
        threading._start_new_thread(self.readedSN,())
        threading._start_new_thread(self.startMQTT,())
        print ("Threads started")
        print ("engine started")
        while True:
            self.engine()
        
    def engine(self):
        

        if self.dadoMQTT!="" and self.dadoser!="":
            topico = 'status/teste'
            print(self.currentSN)
            send = "{sn:'" + self.dadoser + "',resultado:'"+self.dadoMQTT+"'}"
            self.client.publish(topico, send)
            self.dadoMQTT=""
            self.dadoser=""







if __name__ == "__main__":
    
    #bc = BancoFVT_Tester()
    #dado=bc.ultimoRegistro()
    #back.atualizarRegistro("OK",50)
    #back.novoRegistro("OK","RPC48F3P21100055")
    #print(dado)

    #ser = Serial_Barcode()
    #SERIAL = ser.read()
    #print(SERIAL)
    
    print ("start")
    device = FVT_IOT_engine()
    device.run()





'''
teste = ("select "
+ "id, "
+ "serial, "
+ "resultadolog, "
+ "resultadofase, "
+ "statusfinal" 
+ " from " + TABELA)

ultimaLinha = ("select "
+ "id, "
+ "serial, "
+ "resultadolog, "
+ "resultadofase, "
+ "statusfinal" 
+ " from " + TABELA
+ " where id=(SELECT max(id) FROM " + TABELA + ")")

#dado=banco.readQuery("select id,serial,resultadolog,resultadofase,statusfinal" + " from dbo.Dados")
#dado=banco.readQuery(teste)
#print(dado)

os.system('cls')
print("verificando banco")
dado2 = banco.readQuery(ultimaLinha)

print(type(dado2))

print(dado2)
print(dado2[0])

for i in range(len(dado2[0])):
    print("pos:" + str(i) + " " + str(dado2[0][i]) +
        ", type: "  + str(type(dado2[0][i])))
    
pos = dado2[0][0]
sn = dado2[0][1]
r_log  = dado2[0][2]


#insert
#banco.writeQuery("INSERT INTO dbo.configuracoes (modelo) VALUES ('Modelo H');")

#mult inserts
#query = "INSERT INTO dbo.configuracoes (modelo,data) VALUES('Modelo J','29-01-2022')"
#banco.writeQuery(query)

#DELETE
#banco.writeQuery("DELETE FROM dbo.configuracoes WHERE id in (8,9, 10);")

#Update
query = "update dbo.usuarios set nome='Nelson Seixas', matricula=54321" \
                            + ",status='ATIVO', email='1@1.com'" \
                            + " where id=1"

print(query)

try:
    banco.writeQuery(query)
except Exception as e:
    print("Erro bdo:", e)






INSERT INTO `configuracoes` (`id`, `modelo`, `teste1min`, `teste1max`, `teste2min`, `teste2max`, `teste3min`, `teste3max`, `dataAlteracao`, `ultimo_usuario`) VALUES
	(1, 'Modelo A', 35, 56, 0.7, 15, 8, 13, '2021-11-18 10:21:57', 'Francisco'),
	(2, 'Modelo B', -1, -1, 0, 5, 0, 5, '2021-11-18 10:21:57', 'Francisco'),
	(3, 'Modelo C', -1, -1, 2, 5, 2, 7, '2021-11-18 10:21:57', 'Francisco'),
	(4, 'Teste D', 1, 2, 3, 4, 4, 6, '2021-12-06 15:47:46', 'Francisco'),
	(7, 'Modelo AH', 0, 25, 0, 1, 0, 1, '2021-12-06 20:26:18', 'Francisco'),
	(17, 'MODELO H', 1, 2, 3, 4, 4, 6, '2021-12-10 10:39:53', 'Francisco'),
	(20, 'Modelo JABIL', 0, 1, 0, 1, 0, 1, '2021-12-10 10:57:59', 'Francisco');
banco.writeQuery("INSERT INTO "
 + TABELA + " (id, serial, resultadofase)"
 "VALUES"
                (5,'Chair',120),
                (6,'Tablet',300)
                "")
                '''


'''
dado2 = str(banco.readQuery(ultimaLinha))
print(dado2)

#dado2 = re.split('\[\(|, \'|\'|\)\]',dado2)
dado2 = re.split('\[\(|, |\)\]',dado2)
#dado2=banco.readQuery("SELECT * FROM dbo.Dados WHERE id=(SELECT max(id) FROM dbo.Dados)")
print(type(dado2))
print(dado2)

for i in range(30):
    print("pos:" + str(i) + " " + dado2[i])
print(dado2)
'''



'''

    msg = ""
    #Callback - conexao ao broker realizada
    def on_connect(client, userdata, flags, rc):
        print("[STATUS] Conectado ao Broker. Resultado de conexao: "+str(rc))
    
        #faz subscribe automatico no topico
        client.subscribe(TopicoSubscribe)
    
    #Callback - mensagem recebida do broker
    def on_message(client, userdata, message):
        msg = str(message.payload.decode("utf-8"))
        print("message received " + msg)
        #print("message topic=",message.topic)
        #print("message qos=",message.qos)
        #print("message retain flag=",message.retain)

        
    
    #print("[MSG RECEBIDA] Topico: "+msg.topic+" / Mensagem: "+MensagemRecebida)


    print("[STATUS] Inicializando MQTT...")
    #inicializa MQTT:
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(Broker, PortaBroker, KeepAliveBroker)
    #client.connect(Broker)#client.connect('localhost')
    client.publish('status/fase','PC')#client.publish('status/fase','OK')
    client.subscribe('status/fase')
    print("1")
    client.loop_forever()
    
def newResult(msg):
    print ("gravar dados:" + msg)

def engineTester(status):




 
#programa principal:
try:
        print("[STATUS] Inicializando MQTT...")
        #inicializa MQTT:
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
 
        #client.connect(Broker, PortaBroker, KeepAliveBroker)
        client.connect(Broker)
        client.publish('status/fase','PC')
        client.loop_forever()
except KeyboardInterrupt:
        print ("\nCtrl+C pressionado, encerrando aplicacao e saindo...")
        sys.exit(0)
        #'''


