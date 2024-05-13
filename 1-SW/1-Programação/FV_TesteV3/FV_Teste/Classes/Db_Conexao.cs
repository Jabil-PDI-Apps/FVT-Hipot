using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using MySqlConnector;

namespace FV_Teste.Classes
{
    class Db_Conexao
    {
        private string connString { get; set; }
        private MySqlConnection connection { get; set; }
        
        public Db_Conexao()
        {
            //this.connString = "server=localhost;uid=root;pwd=1234;Database=bancofv;port=3306";
            this.connString = "server=localhost;uid=P&D;pwd=@Jabil.2022;Database=bancofv;port=3306";
            this.connection = new MySqlConnection(connString);
            this.connection.Open();
        }

        public List<DadoBanco> GetBanco()
        {
            MySqlDataReader reader = DB_Read("select * from dbo.Dados");
            List<DadoBanco> dados=new List<DadoBanco>();
            while (reader.Read())
            {
                dados.Add(new DadoBanco() { Teste = reader.GetString(2), Resultado = reader.GetString(3),  Serial = reader.GetString(4), FaseStatus=reader.GetString(5),StatusFinal=reader.GetString(8),Log= reader.GetString(7),ValorFase=reader.GetString(6) });
            }

            reader.Close();
            return dados;
        }

        public MySqlDataReader DB_Read(string query)
        {
            
            MySqlCommand mySqlCommand = new MySqlCommand(query, this.connection);
            MySqlDataReader reader;

            //mySqlCommand.ExecuteNonQuery();
            reader = mySqlCommand.ExecuteReader();
            //label1.Text = reader.HasRows.ToString();
            return reader;
            
        }

        public void DB_Write(string query)
        {
            MySqlCommand mySqlCommand = new MySqlCommand(query, this.connection);
            mySqlCommand.ExecuteNonQuery();
        }
        
    }
}
