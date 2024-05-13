using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Drawing.Drawing2D;
using System.Threading;
using FV_Teste.Classes;
using System.Data.Odbc;
using System.IO;
using System.Windows;
using uPLibrary.Networking.M2Mqtt;
using uPLibrary.Networking.M2Mqtt.Messages;
using Newtonsoft.Json;
//using MySqlConnector;
//using System.Data.SqlClient;
namespace FV_Teste
{
    public partial class Form1 : Form
    {
        List<DadoBanco> dados = new List<DadoBanco>();
        //Db_Conexao db = new Db_Conexao();
        MqttClient mqttClient;
        DadoBancoODBC db = new DadoBancoODBC();
        Thread thread, threadFTP;
        bool erro = false, erroServer = false, erroMqtt=false,conectado = false;
        string serial = "";
        Log log = new Log();
        int c = 0;
        string server = "", local = "";
        string caminhoArquivo = "";
        System.Windows.Forms.Timer timer = new System.Windows.Forms.Timer();
        System.Windows.Forms.Timer timerFTP = new System.Windows.Forms.Timer();
        public Form1()
        {

            try
            {

                InitializeComponent();

                thread = new Thread(() => ReconectaBanco());
                threadFTP = new Thread(() => checkDirectory("c:"));
                Conexao();
                Estilos();
                setFiles();

                this.FormBorderStyle = FormBorderStyle.None;
                timer.Tick += Timer_Tick;
                timer.Interval = 2000;
                timer.Start();
            }
            catch (Exception ex)
            {
                erro = true;
                MessageBox.Show("Erro Form1:" + ex.Message);
            }

            mqttConect();
        }

        private void mqttConect()
        {
            try {
                //mqttClient = new MqttClient("10.58.8.29");
                mqttClient = new MqttClient("192.168.0.19");
                mqttClient.MqttMsgPublishReceived += MqttClient_MqttMsgPublishReceived;
                mqttClient.Subscribe(new string[] { "status/teste" }, new byte[] { MqttMsgBase.QOS_LEVEL_AT_LEAST_ONCE });
                mqttClient.Connect("FVT Application");
                

            }

            catch (Exception ex)
            {
                

                MessageBox.Show("Erro MQTT:" + ex.Message);
            }
        }

        private void MqttClient_MqttMsgPublishReceived(object sender, MqttMsgPublishEventArgs e)
        {
            try
            {
                var message = Encoding.UTF8.GetString(e.Message);
                dynamic js = JsonConvert.DeserializeObject(message);
                string query = "";
                string sn = js.sn, resultado = js.resultado;

                if (serialMQTTConsulta(sn) > 0)
                {
                    query = "update dbo.Dados set SERIAL='" + sn + "',resultadoFase='" + resultado + "' where SERIAL='"+sn+ "' and  statusFinal='ABERTO'";
                }

                else
                {
                    query = "INSERT INTO dbo.Dados(SERIAL,resultadoFase ) VALUES('" + sn + "','" + resultado + "')";
                }
                Console.WriteLine("MENSAGEM" + js.sn);
                db.DB_Write(query);
            }
            catch(Exception ex)
            {
                MessageBox.Show("Erro Mensagem Mqtt");
            }
        }

        private void ReconectaBanco()
        {
            dbStatus.BackColor = System.Drawing.ColorTranslator.FromHtml("#E8061D");
            conectado = db.conectaBanco();
            Console.WriteLine("Conectado:" + conectado);

            if (conectado == true)
            {
                erro = false;
            }


        }

        private void Timer_Tick(object sender, EventArgs e)
        {
            timer.Stop();
            try {
                if (!erro)
                {
                    Chamada();
                    //Console.WriteLine("Thread:"+thread.ThreadState);
                    dbStatus.BackColor = System.Drawing.ColorTranslator.FromHtml("#20c33b");
                }

                else
                {

                    //Console.WriteLine("Thread:" + thread.ThreadState);
                    if (thread.ThreadState == ThreadState.Unstarted)
                        thread.Start();
                    else if (thread.ThreadState == ThreadState.Stopped) {
                        thread = new Thread(() => ReconectaBanco());
                    }

                }
            }
            catch (Exception ex)
            {
                erro = true;
                MessageBox.Show("Erro Timer DB:" + ex.Message);
            }

            try
            {
                if (!erroServer)
                {
                    ftpStatus.BackColor = System.Drawing.ColorTranslator.FromHtml("#20c33b");
                }

                else
                {

                    //Console.WriteLine("Thread:" + threadFTP.ThreadState);
                    if (threadFTP.ThreadState == ThreadState.Unstarted)
                        threadFTP.Start();
                    else if (threadFTP.ThreadState == ThreadState.Stopped)
                    {
                        if (!erro)
                        {
                            OdbcDataReader r = db.DB_Read("select * from dbo.caminho");

                            string pt = "";
                            while (r.Read())
                            {

                                pt = r.GetString(2);

                            }
                            r.Close();

                            threadFTP = new Thread(() => checkDirectory(pt));
                        }
                        else
                        {
                            ftpStatus.BackColor = System.Drawing.ColorTranslator.FromHtml("#54c0e8");
                        }
                    }

                }
            }
            catch (Exception ex)
            {
                erroServer = true;
                MessageBox.Show("Erro Timer FTP:" + ex.Message);
            }

            timer.Start();
        }

        public void Estilos()
        {
            Color tabelaBackCor = System.Drawing.ColorTranslator.FromHtml("#54c0e8");
            //tabela.Columns[2].HeaderCell.Style.BackColor = Color.Red;
            //tabela.Columns[2].HeaderCell.Style.
            tabela.RowTemplate.Height = 40;

            tabela.EnableHeadersVisualStyles = false;
        }

        public async void Conexao()
        {
            try
            {
                Pen pen = new Pen(System.Drawing.ColorTranslator.FromHtml("#54c0e8"));
                Rectangle rectangle = new Rectangle(300, 300, 168, 90);
                Graphics g = this.CreateGraphics();
                g.DrawRectangle(pen, rectangle);
                g.DrawLine(pen, new Point(250, 0), new Point(400, 400));
                dbconnect();
                addStatus();
            }
            catch (Exception ex)
            {
                erro = true;
                MessageBox.Show("Erro Conexao:" + ex.Message);
            }
        }

        private void dbconnect()
        {
            try
            {

                dados = db.GetBanco();
            }
            catch (Exception ex)
            {
                erro = true;
                MessageBox.Show("Erro dbconnect:" + ex.Message);
            }

        }

        private void addStatus()
        {
            try {


                Button botao = new Button();
                //Image image = Image.FromFile(@"C:\Users\lumarques.MZNOLNPE079\Documents\1-Projetos\1-FVTeste\1-Programação\FV_Teste\FV_Teste\Resources\pata.png");
                dados = db.GetBanco();
                tabela.Rows.Clear();
                foreach (DadoBanco a in dados)
                {

                    DataGridViewRow row = (DataGridViewRow)tabela.Rows[0].Clone();
                    if (a.StatusFinal != "ABERTO")
                    {
                        row.Cells[0].Value = a.Hora;
                        row.Cells[1].Value = a.Serial;
                        row.Cells[2].Value = a.Teste;
                        row.Cells[3].Value = a.StatusFinal;
                        if (a.FaseStatus != "OK" || a.Teste != "OK")
                        {
                            if (a.FaseStatus != "OK")
                            {
                                row.Cells[2].Value = "Fase";
                            }

                            row.Cells[2].Style.BackColor = System.Drawing.ColorTranslator.FromHtml("#E8061D");
                            row.Cells[2].Style.ForeColor = System.Drawing.ColorTranslator.FromHtml("#ffffff");

                        }
                        else
                        {

                            row.Cells[2].Style.BackColor = System.Drawing.ColorTranslator.FromHtml("#20c33b");
                            row.Cells[2].Style.ForeColor = System.Drawing.ColorTranslator.FromHtml("#ffffff");

                        }

                        if (a.StatusFinal == "OK")
                        {

                            row.Cells[3].Style.BackColor = System.Drawing.ColorTranslator.FromHtml("#20c33b");
                            row.Cells[3].Style.ForeColor = System.Drawing.ColorTranslator.FromHtml("#ffffff");

                        }

                        else if (a.StatusFinal == "NG")
                        {

                            row.Cells[3].Style.BackColor = System.Drawing.ColorTranslator.FromHtml("#E8061D");
                            row.Cells[3].Style.ForeColor = System.Drawing.ColorTranslator.FromHtml("#ffffff");

                        }
                        //Para escrever imagem 
                        //row.Cells[3].Value = image;
                        tabela.Rows.Add(row);
                        foreach (DataGridViewColumn col in tabela.Columns)
                        {
                            col.HeaderCell.Style.Alignment = DataGridViewContentAlignment.MiddleCenter;

                        }
                        tabela.ColumnHeadersDefaultCellStyle.Alignment = DataGridViewContentAlignment.TopRight;

                    }
                }

            }

            catch (Exception ex) {
                erro = true;
                MessageBox.Show("Erro addStatus:" + ex.Message);
            }
        }

        private void setFiles()
        {
            try {
                OdbcDataReader rd = db.DB_Read("select * from dbo.caminho");

                string log = "";
                while (rd.Read())
                {
                    log = rd.GetString(1);
                    server = rd.GetString(2);
                    local = rd.GetString(3);
                }
                rd.Close();

                fileSystemWatcher1.Filter = "*.csv";
                fileSystemWatcher1.EnableRaisingEvents = true;
                //fileSystemWatcher1.Path = "C:\\Users\\lumarques.MZNOLNPE079\\Documents\\2-Repositório\\Jabil_FVT\\1-SW\\2-Simulacao\\";
                fileSystemWatcher1.Path = log;

            }
            catch (Exception ex) {
                erro = true;
                MessageBox.Show("Erro setFiles:" + ex);
            }
        }

        private void dataGridView1_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {
            if (e.ColumnIndex == 3)

                MessageBox.Show(e.RowIndex.ToString());
        }

        private void Form1_Load(object sender, EventArgs e)
        {


        }

        private void pictureBox3_Click(object sender, EventArgs e)
        {
            if (this.FormBorderStyle == FormBorderStyle.None)
            {
                this.FormBorderStyle = FormBorderStyle.Sizable;
            }
            else
            {
                this.FormBorderStyle = FormBorderStyle.None;
            }
        }

        private void fileSystemWatcher1_Changed(object sender, System.IO.FileSystemEventArgs e)
        {
            try
            {

                List<string> lista = new List<string>();
                //c += 1;
                Thread.Sleep(4000);
                lista = log.ReadLog(e.FullPath);
                //Aqui verifica se faz dois seguidos ou não
                if (serial != lista[0])
                {
                    //MessageBox.Show("Caminho Arquivo:" + local+"" + lista[0] + ".txt");
                    string cam = local + "\\" + lista[0] + ".txt";
                    //System.IO.File.WriteAllText(cam, lista[2]);
                    serial = lista[0];
                    string query = "";
                    if (quantidadeConsulta(lista[0]) > 0)
                        query = "update dbo.Dados set SERIAL='" + lista[0] + "',resultadoLog='" + lista[1] + "',textoLog='" + lista[2] + "' where resultadoLog='ABERTO' and serial='" + lista[0] + "'";
                    else
                        query = "INSERT INTO dbo.Dados(SERIAL, resultadoLog, textoLog) VALUES('" + lista[0] + "','" + lista[1] + "','" + lista[2] + "')";

                    db.DB_Write(query);

                }
                //MessageBox.Show(query);


            }
            catch (Exception ex)
            {
                erro = true;
                MessageBox.Show("Erro File Watcher:" + ex.Message);
            }

        }

        private void Chamada()
        {
            if (erro == false)
            {
                try
                {

                    bool atualiza = false;

                    dados = db.GetBanco();

                    foreach (DadoBanco a in dados)
                    {
                        if (a.StatusFinal != "OK")
                        {

                            if (a.Teste != "ABERTO" && a.FaseStatus != "ABERTO")
                            {
                                atualiza = true;

                                try
                                {
                                    OdbcDataReader rd = db.DB_Read("select * from dbo.caminho");

                                    while (rd.Read())
                                    {
                                        server = rd.GetString(2);
                                        local = rd.GetString(3);
                                        if (rd.GetString(4) == "Log")
                                        {

                                            caminhoArquivo = server + "\\" + a.Serial + ".txt";
                                        }
                                        else
                                        {
                                            caminhoArquivo = local + "\\" + a.Serial + ".txt";
                                        }
                                    }
                                }

                                catch
                                {
                                    MessageBox.Show("Sem caminho");
                                    erro = true;
                                }
                                //string caminhoArquivo = @"C:\Users\lumarques.MZNOLNPE079\Documents\2-Repositório\Jabil_FVT\1-SW\4-SaidaFase\" + a.Serial + ".txt";

                                if (a.FaseStatus == "OK")
                                {
                                    a.Log = a.Log + "MTeste Fase\nqPASS";
                                    try
                                    {
                                        erroServer = false;
                                        System.IO.File.WriteAllText(caminhoArquivo, a.Log);

                                    }
                                    catch (Exception ex)
                                    {
                                        erroServer = true;
                                        MessageBox.Show("erro server");
                                        db.DB_Write("update dados set statusfinal='NG', textoLog='" + a.Log + "' where serial='" + a.Serial + "' and statusfinal='ABERTO'");
                                    }
                                }
                                else
                                {
                                    if (a.Log.Contains("TP"))
                                    {
                                        a.Log = a.Log.Replace("TP", "TF\nFTeste Fase") + "MTeste Fase\nqFAIL";
                                        try
                                        {
                                            erroServer = false;
                                            System.IO.File.WriteAllText(caminhoArquivo, a.Log);

                                        }
                                        catch (Exception ex)
                                        {
                                            erroServer = true;
                                            db.DB_Write("update dados set statusfinal='NG', textoLog='" + a.Log + "' where serial='" + a.Serial + "' and statusfinal='ABERTO'");
                                        }

                                    }
                                    else
                                    {
                                        a.Log = a.Log + "MTeste Fase\nqFAIL";
                                        try
                                        {
                                            erroServer = false;
                                            System.IO.File.WriteAllText(caminhoArquivo, a.Log + "Log de saída de fase -> Fail");
                                        }

                                        catch (Exception ex)
                                        {
                                            erroServer = true;
                                            db.DB_Write("update dados set statusfinal='NG', textoLog='" + a.Log + "' where serial='" + a.Serial + "' and statusfinal='ABERTO'");
                                        }
                                    }
                                }

                                if (erroServer == false)
                                {
                                    try
                                    {
                                        db.DB_Write("update dados set statusfinal='OK', textoLog='" + a.Log + "' where serial='" + a.Serial + "' and statusfinal='ABERTO'");
                                    }
                                    catch (Exception ex)
                                    {
                                        erro = true;
                                    }

                                }
                                //MessageBox.Show("Enviado para:" + caminhoArquivo);

                            }

                        }

                    }
                    if (atualiza)
                    {
                        addStatus();
                    }
                    c += 1;
                    //Console.WriteLine(c);

                    timer.Start();
                    //Thread.Sleep(100);
                }

                catch (Exception ex)
                {
                    erro = true;
                    MessageBox.Show("Erro Chamada:" + ex.Message);
                }
                ultimoDadoCheck();
            }
            else
            {
                dbconnect();
            }

            
        }


        private void ultimoDadoCheck(){

            string query = "SELECT TOP 1 * FROM dbo.Dados WHERE statusFinal='OK' OR statusFinal='NG' ORDER BY id DESC ";
            try
            {
                OdbcDataReader rx = db.DB_Read(query);
                string f = "", l = "", final = "";
                while (rx.Read())
                {
                    f = rx.GetString(5);
                    l = rx.GetString(2);
                    final = rx.GetString(8);
                }
                if (f != "OK" || l != "OK" || final != "OK")
                {
                    BarraStatusGeral.Text = "REPROVADO";
                    BarraStatusGeral.BackColor = Color.FromArgb(((int)(((byte)(232)))), ((int)(((byte)(6)))), ((int)(((byte)(29)))));

                }
                else
                {
                    BarraStatusGeral.Text = "APROVADO";
                    BarraStatusGeral.BackColor = Color.FromArgb(((int)(((byte)(32)))), ((int)(((byte)(195)))), ((int)(((byte)(59)))));
                }
            }
            catch(Exception ex)
            {
                Console.WriteLine("erro");
            }
        }

        private void checkDirectory(string path) 
        {
            if (Directory.Exists(path))
            {
                erroServer = false;
                ftpStatus.BackColor = System.Drawing.ColorTranslator.FromHtml("#20c33b");
            }
            else
            {
                ftpStatus.BackColor = System.Drawing.ColorTranslator.FromHtml("#E8061D");
                erroServer = true;
            }
        }

        private int quantidadeConsulta(string codigo)
        {
            OdbcDataReader r = db.DB_Read("select * from dbo.Dados where resultadoLog='ABERTO' and serial='"+codigo+"'");
            int c = 0;
            while (r.Read()){
                c++;
            }
            r.Close();
            return c;
        }

        private int serialMQTTConsulta(string codigo)
        {
            OdbcDataReader r = db.DB_Read("select * from dbo.Dados where statusFinal='ABERTO' and serial='" + codigo + "'");
            int c = 0;
            while (r.Read())
            {
                c++;
            }
            r.Close();
            return c;
        }



    }
}
