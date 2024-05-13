using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data.SqlClient;
namespace FV_Teste.Classes
{
    class DadoBancoSQLServer
    {

        private string connString { get; set; }
        private SqlConnection connection { get; set; }

        public DadoBancoSQLServer()
        {
            //this.connString = "server=localhost;uid=root;pwd=1234;Database=bancofv;port=3306";
            //this.connString = "server=tcp:10.56.17.12,3306;uid=P&D;pwd=@Jabil.2022;Database=bancofv;Integrated Security=True";
            this.connString = "server=tcp:10.60.70.160,3306;uid=P&D;pwd=@Jabil.2022;Database=bancofv;Integrated Security=True";
            this.connection = new SqlConnection(connString);
            this.connection.Open();
        }

        public List<DadoBanco> GetBanco()
        {
            
            SqlDataReader reader = DB_Read("select * from dbo.Dados ORDER BY id DESC");
            List<DadoBanco> dados = new List<DadoBanco>();
            while (reader.Read())
            {
                dados.Add(new DadoBanco() { Teste = reader.GetString(2), Resultado = reader.GetString(3), Hora = reader.GetDateTime(1), Serial = reader.GetString(4), FaseStatus = reader.GetString(5), StatusFinal = reader.GetString(8), Log = reader.GetString(7), ValorFase = reader.GetString(6) });
            }

            reader.Close();
            return dados;
        }

        public SqlDataReader DB_Read(string query)
        {

            SqlCommand mySqlCommand = new SqlCommand(query, this.connection);
            SqlDataReader reader;

            mySqlCommand.ExecuteNonQuery();
            reader = mySqlCommand.ExecuteReader();
            //label1.Text = reader.HasRows.ToString();
            
            return reader;

        }

        public void DB_Write(string query)
        {
            SqlCommand mySqlCommand = new SqlCommand(query, this.connection);
            mySqlCommand.ExecuteNonQuery();
        }

    }

}

