using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using System.Data.Odbc;
namespace FV_Teste.Classes
{
    class DadoBancoODBC
    {
        private bool conectado { get; set; }
        private string connString { get; set; }
        private OdbcConnection connection { get; set; }

        public DadoBancoODBC()
        {
            try
            {
                //this.connString = "server=localhost;uid=root;pwd=1234;Database=bancofv;port=3306";
                //JABIL FORMATO
                //this.connString = "Driver={SQL Server};Server=tcp:10.56.17.12;uid=P&D;pwd=@Jabil.2022;Database=bancofv;";
                //PADRÃO
                this.connString = "Driver={SQL Server};Server=192.168.0.19,3306;uid=P&D;pwd=@Jabil.2022;Database=bancofv;";
                //this.connString = "Driver={SQL Server};Server=localhost,3306;uid=P&D;pwd=@Jabil.2022;Database=bancofv;";
                this.connection = new OdbcConnection(this.connString);
                this.connection.Open();
                this.conectado = true;
            }

            catch
            {
                this.conectado = false;
            }
        }

        public bool conectaBanco()
        {
            try
            {
                this.connString = "Driver={SQL Server};Server=192.168.0.19,3306;uid=P&D;pwd=@Jabil.2022;Database=bancofv;";
                //this.connString = "server=localhost;uid=root;pwd=1234;Database=bancofv;port=3306";
                //JABIL FORMATO
                //this.connString = "Driver={SQL Server};Server=tcp:10.56.17.12;uid=P&D;pwd=@Jabil.2022;Database=bancofv;";
                //PADRÃO
                //this.connString = "Driver={SQL Server};Server=tcp:10.60.70.160,3306;uid=P&D;pwd=@Jabil.2022;Database=bancofv;";
                //this.connString = "Driver={SQL Server};Server=192.168.0.14,3306;uid=P&D;pwd=@Jabil.2022;Database=bancofv;";
                this.connection = new OdbcConnection(this.connString);
                this.connection.Open();
                this.conectado = true;
                return true;
            }

            catch
            {
                this.conectado = false;
                return false;
            }
        }

        public bool getStatus()
        {
            return this.conectado;
        }
        public List<DadoBanco> GetBanco()
        {

            OdbcDataReader reader = DB_Read("select * from dbo.Dados ORDER BY id DESC");
            List<DadoBanco> dados = new List<DadoBanco>();
            while (reader.Read())
            {
                DateTime time = reader.GetDateTime(1);
                dados.Add(new DadoBanco() { Teste = reader.GetString(2), Resultado = reader.GetString(3), Hora = time, Serial = reader.GetString(4), FaseStatus = reader.GetString(5), StatusFinal = reader.GetString(8), Log = reader.GetString(7), ValorFase = reader.GetString(6) });
                
            }

            reader.Close();
            return dados;
        }

        public OdbcDataReader DB_Read(string query)
        {

            OdbcCommand mySqlCommand = new OdbcCommand(query, this.connection);
            OdbcDataReader reader;

            mySqlCommand.ExecuteNonQuery();
            reader = mySqlCommand.ExecuteReader();
            //label1.Text = reader.HasRows.ToString();
            
            return reader;

        }

        public void DB_Write(string query)
        {
            OdbcCommand mySqlCommand = new OdbcCommand(query, this.connection);
            mySqlCommand.ExecuteNonQuery();
        }
    }
}
