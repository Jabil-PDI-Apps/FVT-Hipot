using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data.Odbc;

namespace FV_Teste.Classes
{
    class Log
    {
        public static string datePatt = @"MM/dd/yyyy HH:mm:ss";

        public string SN { get; set; }

        public List<string> ReadLog(string path)
        {
            
            List<string> lista = new List<string>();
            try
            {
                string linha = "";
                string SN = "";

                string failDescription = "";

                string testStep1 = "";
                string testStep2 = "";
                string testStep3 = "";
                string testStep4 = "";
                string testStep5 = "";
                string testStep6 = "";

                string testStatus1 = "";
                string testStatus2 = "";
                string testStatus3 = "";
                string testStatus4 = "";
                string testStatus5 = "";
                string testStatus6 = "";

                string volt1 = "";
                string volt2 = "";
                string volt3 = "";
                string volt4 = "";
                string volt5 = "";
                string volt6 = "";

                string current1 = "";
                string current2 = "";
                string current3 = "";
                string current4 = "";
                string current5 = "";
                string current6 = "";

                string power1 = "";
                string power2 = "";
                string power3 = "";
                string power4 = "";
                string power5 = "";
                string power6 = "";

                string LC = "";

                //Lendo arquivo .csv
                System.IO.StreamReader csvfile = new System.IO.StreamReader(path);
                linha = csvfile.ReadToEnd();

                //Criando vetores para separar o ultimo SN testado
                string[] linhasArray = linha.Split(new[] { Environment.NewLine }, StringSplitOptions.None);
                if (linhasArray[linhasArray.Length - 1] != "")
                {
                    try
                    {
                        //testStep = close
                        string[] dadosArray1 = linhasArray[linhasArray.Length - 1].Split(',');
                        testStatus1 = dadosArray1[6];
                        testStep1 = dadosArray1[5];
                        volt1 = dadosArray1[7].Split('/')[2];
                        current1 = dadosArray1[8].Split('/')[2];
                        power1 = dadosArray1[9].Split('/')[2];

                        //testStep = middle-Fan
                        string[] dadosArray2 = linhasArray[linhasArray.Length - 2].Split(',');
                        testStatus2 = dadosArray2[6];
                        testStep2 = dadosArray2[5];
                        volt2 = dadosArray2[7].Split('/')[2];
                        current2 = dadosArray2[8].Split('/')[2];
                        power2 = dadosArray2[9].Split('/')[2];

                        //testStep = low-Fan
                        string[] dadosArray3 = linhasArray[linhasArray.Length - 3].Split(',');
                        testStatus3 = dadosArray3[6];
                        testStep3 = dadosArray3[5];
                        volt3 = dadosArray3[7].Split('/')[2];
                        current3 = dadosArray3[8].Split('/')[2];
                        power3 = dadosArray3[9].Split('/')[2];

                        //testStep = water pump
                        string[] dadosArray4 = linhasArray[linhasArray.Length - 4].Split(',');
                        testStatus4 = dadosArray4[6];
                        testStep4 = dadosArray4[5];
                        volt4 = dadosArray4[7].Split('/')[2];
                        current4 = dadosArray4[8].Split('/')[2];
                        power4 = dadosArray4[9].Split('/')[2];

                        //testStep = Cool High-Fan
                        string[] dadosArray5 = linhasArray[linhasArray.Length - 5].Split(',');
                        testStatus5 = dadosArray5[6];
                        testStep5 = dadosArray5[5];
                        volt5 = dadosArray5[7].Split('/')[2];
                        current5 = dadosArray5[8].Split('/')[2];
                        power5 = dadosArray5[9].Split('/')[2];

                        //testStep = Security data
                        if (linhasArray[linhasArray.Length - 6] == "")
                        {
                            testStatus6 = "OK";
                            testStep6 = "Security Data";
                            volt6 = "null";
                            current6 = "null";
                            power6 = "null";
                            LC = "null";
                        }
                        else
                        {
                            string[] dadosArray6 = linhasArray[linhasArray.Length - 6].Split(',');
                            testStatus6 = dadosArray6[6];
                            testStep6 = dadosArray6[5];
                            volt6 = dadosArray6[7].Split('/')[1];
                            current6 = dadosArray6[8].Split('/')[1];
                            power6 = dadosArray6[9].Split('/')[1];
                            LC = dadosArray6[10].Split('/')[1];
                        }

                        //SN
                        SN = dadosArray1[1].Substring(1, 16);
                    }
                    catch
                    {
                        //testStep = close
                        string[] dadosArray1 = linhasArray[linhasArray.Length - 1].Split(',');
                        testStatus1 = dadosArray1[6];
                        testStep1 = dadosArray1[5];
                        volt1 = dadosArray1[7].Split('/')[2];
                        current2 = dadosArray1[8].Split('/')[2];
                        power3 = dadosArray1[9].Split('/')[2];

                        //testStep = middle-Fan
                        string[] dadosArray2 = linhasArray[linhasArray.Length - 2].Split(',');
                        testStatus2 = dadosArray2[6];
                        testStep2 = dadosArray2[5];
                        volt2 = dadosArray2[7].Split('/')[2];
                        current2 = dadosArray2[8].Split('/')[2];
                        power2 = dadosArray2[9].Split('/')[2];

                        //testStep = low-Fan
                        string[] dadosArray3 = linhasArray[linhasArray.Length - 3].Split(',');
                        testStatus3 = dadosArray3[6];
                        testStep3 = dadosArray3[5];
                        volt3 = dadosArray3[7].Split('/')[2];
                        current3 = dadosArray3[8].Split('/')[2];
                        power3 = dadosArray3[9].Split('/')[2];

                        //testStep = Cool High-Fan
                        string[] dadosArray4 = linhasArray[linhasArray.Length - 4].Split(',');
                        testStatus4 = dadosArray4[6];
                        testStep4 = dadosArray4[5];
                        volt4 = dadosArray4[7].Split('/')[2];
                        current4 = dadosArray4[8].Split('/')[2];
                        power4 = dadosArray4[9].Split('/')[2];

                        //testStep = Security data
                        if (linhasArray[linhasArray.Length - 5] == "")
                        {
                            testStatus5 = "OK";
                            testStep5 = "Security Data";
                            volt5 = "null";
                            current5 = "null";
                            power5 = "null";
                            LC = "null";
                        }
                        else
                        {
                            string[] dadosArray5 = linhasArray[linhasArray.Length - 5].Split(',');
                            testStatus5 = dadosArray5[6];
                            testStep5 = dadosArray5[5];
                            volt5 = dadosArray5[7].Split('/')[1];
                            current5 = dadosArray5[8].Split('/')[1];
                            power5 = dadosArray5[9].Split('/')[1];
                            LC = dadosArray5[10].Split('/')[1];
                        }

                        //SN
                        SN = dadosArray1[1].Substring(1, 16);
                    }

                    //Fail Description
                    if (SN.Substring(0, 3) == "RCI")
                    {
                        if (testStatus1 == "NG")
                        {
                            failDescription = "Close";
                            if (testStatus2 == "NG")
                            {
                                failDescription = "middle-Fan";
                                if (testStatus3 == "NG")
                                {
                                    failDescription = "low-Fan";
                                    if (testStatus4 == "NG")
                                    {
                                        failDescription = "water pump";
                                        if (testStatus5 == "NG")
                                        {
                                            failDescription = "Cool High-Fan";
                                            if (testStatus6 == "NG")
                                            {
                                                failDescription = "Security data";
                                            }
                                        }
                                    }
                                }
                            }
                        }
                        else
                        {
                            failDescription = "OK";
                        }
                    }
                    else if (SN.Substring(0, 3) == "RPC")
                    {
                        if (testStatus1 == "NG")
                        {
                            failDescription = "Close";
                            if (testStatus2 == "NG")
                            {
                                failDescription = "middle-Fan";
                                if (testStatus3 == "NG")
                                {
                                    failDescription = "low-Fan";
                                    if (testStatus4 == "NG")
                                    {
                                        failDescription = "Cool High-Fan";
                                        if (testStatus5 == "NG")
                                        {
                                            failDescription = "Security data";
                                        }
                                    }
                                }
                            }
                        }
                        else
                        {
                            failDescription = "OK";
                        }
                    }
                }
                else
                {
                    try
                    {
                        //testStep = close
                        string[] dadosArray1 = linhasArray[linhasArray.Length - 2].Split(',');
                        testStatus1 = dadosArray1[6];
                        testStep1 = dadosArray1[5];
                        volt1 = dadosArray1[7].Split('/')[2];
                        current1 = dadosArray1[8].Split('/')[2];
                        power1 = dadosArray1[9].Split('/')[2];

                        //testStep = middle-Fan
                        string[] dadosArray2 = linhasArray[linhasArray.Length - 3].Split(',');
                        testStatus2 = dadosArray2[6];
                        testStep2 = dadosArray2[5];
                        volt2 = dadosArray2[7].Split('/')[2];
                        current2 = dadosArray2[8].Split('/')[2];
                        power2 = dadosArray2[9].Split('/')[2];

                        //testStep = low-Fan
                        string[] dadosArray3 = linhasArray[linhasArray.Length - 4].Split(',');
                        testStatus3 = dadosArray3[6];
                        testStep3 = dadosArray3[5];
                        volt3 = dadosArray3[7].Split('/')[2];
                        current3 = dadosArray3[8].Split('/')[2];
                        power3 = dadosArray3[9].Split('/')[2];

                        //testStep = water pump
                        string[] dadosArray4 = linhasArray[linhasArray.Length - 5].Split(',');
                        testStatus4 = dadosArray4[6];
                        testStep4 = dadosArray4[5];
                        volt4 = dadosArray4[7].Split('/')[2];
                        current4 = dadosArray4[8].Split('/')[2];
                        power4 = dadosArray4[9].Split('/')[2];

                        //testStep = Cool High-Fan
                        string[] dadosArray5 = linhasArray[linhasArray.Length - 6].Split(',');
                        testStatus5 = dadosArray5[6];
                        testStep5 = dadosArray5[5];
                        volt5 = dadosArray5[7].Split('/')[2];
                        current5 = dadosArray5[8].Split('/')[2];
                        power5 = dadosArray5[9].Split('/')[2];

                        //testStep = Security data
                        if (linhasArray[linhasArray.Length - 7] == "")
                        {
                            testStatus6 = "OK";
                            testStep6 = "Security Data";
                            volt6 = "null";
                            current6 = "null";
                            power6 = "null";
                            LC = "null";
                        }
                        else
                        {
                            string[] dadosArray6 = linhasArray[linhasArray.Length - 7].Split(',');
                            testStatus6 = dadosArray6[6];
                            testStep6 = dadosArray6[5];
                            volt6 = dadosArray6[7].Split('/')[1];
                            current6 = dadosArray6[8].Split('/')[1];
                            power6 = dadosArray6[9].Split('/')[1];
                            LC = dadosArray6[10].Split('/')[1];
                        }

                        //SN
                        SN = dadosArray1[1].Substring(1, 16);
                        this.SN= dadosArray1[1].Substring(1, 16);
                    }
                    catch
                    {
                        //testStep = close
                        string[] dadosArray1 = linhasArray[linhasArray.Length - 2].Split(',');
                        testStatus1 = dadosArray1[6];
                        testStep1 = dadosArray1[5];
                        volt1 = dadosArray1[7].Split('/')[2];
                        current2 = dadosArray1[8].Split('/')[2];
                        power3 = dadosArray1[9].Split('/')[2];

                        //testStep = middle-Fan
                        string[] dadosArray2 = linhasArray[linhasArray.Length - 3].Split(',');
                        testStatus2 = dadosArray2[6];
                        testStep2 = dadosArray2[5];
                        volt2 = dadosArray2[7].Split('/')[2];
                        current2 = dadosArray2[8].Split('/')[2];
                        power2 = dadosArray2[9].Split('/')[2];

                        //testStep = low-Fan
                        string[] dadosArray3 = linhasArray[linhasArray.Length - 4].Split(',');
                        testStatus3 = dadosArray3[6];
                        testStep3 = dadosArray3[5];
                        volt3 = dadosArray3[7].Split('/')[2];
                        current3 = dadosArray3[8].Split('/')[2];
                        power3 = dadosArray3[9].Split('/')[2];

                        //testStep = Cool High-Fan
                        string[] dadosArray4 = linhasArray[linhasArray.Length - 5].Split(',');
                        testStatus4 = dadosArray4[6];
                        testStep4 = dadosArray4[5];
                        volt4 = dadosArray4[7].Split('/')[2];
                        current4 = dadosArray4[8].Split('/')[2];
                        power4 = dadosArray4[9].Split('/')[2];

                        //testStep = Security data
                        if (linhasArray[linhasArray.Length - 6] == "")
                        {
                            testStatus5 = "OK";
                            testStep5 = "Security Data";
                            volt5 = "null";
                            current5 = "null";
                            power5 = "null";
                            LC = "null";
                        }
                        else
                        {
                            string[] dadosArray5 = linhasArray[linhasArray.Length - 6].Split(',');
                            testStatus5 = dadosArray5[6];
                            testStep5 = dadosArray5[5];
                            volt5 = dadosArray5[7].Split('/')[1];
                            current5 = dadosArray5[8].Split('/')[1];
                            power5 = dadosArray5[9].Split('/')[1];
                            LC = dadosArray5[10].Split('/')[1];
                        }

                        //SN
                        SN = dadosArray1[1].Substring(1, 16);
                    }

                    //Fail Description
                    if (SN.Substring(0, 3) == "RCI")
                    {
                        if (testStatus1 == "NG")
                        {
                            failDescription = "Close";
                            if (testStatus2 == "NG")
                            {
                                failDescription = "middle-Fan";
                                if (testStatus3 == "NG")
                                {
                                    failDescription = "low-Fan";
                                    if (testStatus4 == "NG")
                                    {
                                        failDescription = "water pump";
                                        if (testStatus5 == "NG")
                                        {
                                            failDescription = "Cool High-Fan";
                                            if (testStatus6 == "NG")
                                            {
                                                failDescription = "Security data";
                                            }
                                        }
                                    }
                                }
                            }
                        }
                        else
                        {
                            failDescription = "OK";
                        }
                    }
                    else if (SN.Substring(0, 3) == "RPC")
                    {
                        if (testStatus1 == "NG")
                        {
                            failDescription = "Close";
                            if (testStatus2 == "NG")
                            {
                                failDescription = "middle-Fan";
                                if (testStatus3 == "NG")
                                {
                                    failDescription = "low-Fan";
                                    if (testStatus4 == "NG")
                                    {
                                        failDescription = "Cool High-Fan";
                                        if (testStatus5 == "NG")
                                        {
                                            failDescription = "Security data";
                                        }
                                    }
                                }
                            }
                        }
                        else
                        {
                            failDescription = "OK";
                        }
                    }
                }
                
                //Imprimindo resultado
                //updateUI(SN + ", " + failDescription); Se funcionar é OK

                //updateUI();
                //Enviando resultado ao Parser
                StringBuilder st = new StringBuilder();
                st=log2MES(SN, failDescription, LC, volt1, volt2, volt3, volt4, volt5, volt6, current1, current2, current3, current4, current5, current6, power1, power2, power3, power4, power5, power6, testStep1, testStep2, testStep3, testStep4, testStep5, testStep6);
                StringBuilder sta = new StringBuilder();
                sta.Append("SN: " + SN);
                sta.Append("Status: " + failDescription);
                sta.Append("LC: " + LC);
                //System.IO.File.WriteAllText(@"C:\Users\lumarques.MZNOLNPE079\Documents\1-Projetos\1-FVTeste\3-Saida\teste.txt", sta.ToString());
                
                lista.AddRange(new List<string>
                {
                    SN,failDescription,st.ToString()
                }) ;
                csvfile.Close();
                csvfile.Dispose();
                return lista;
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
                lista.Add("erro");
                return lista ;
                // Let the user know what went wrong.
                //MessageBox.Show(ex.Message);
            }
        }

        public StringBuilder log2MES(string SN, string failDescription, string LC, string volt1, string volt2, string volt3, string volt4, string volt5, string volt6, string current1, string current2, string current3, string current4, string current5, string current6, string power1, string power2, string power3, string power4, string power5, string power6, string testStep1, string testStep2, string testStep3, string testStep4, string testStep5, string testStep6)
        {
            DadoBancoODBC db = new DadoBancoODBC();
            OdbcDataReader reader = db.DB_Read("select * from dbo.caminho");
            string server = "", log = "", local = "";
            while (reader.Read())
            {
                
                server = reader.GetString(2);
                local = reader.GetString(3);
            }
            reader.Close();
            //Console.WriteLine("LOCAAAAAAAAAAL");
            //string caminhoArquivo = @"C:\Users\lumarques.MZNOLNPE079\Documents\2-Repositório\Jabil_FVT\1-SW\3-Saida\" + SN + ".txt"; //caminho completo

            string caminhoArquivo = local+"\\"+SN+".txt"; //caminho completo
            //caminhoArquivo=local + SN + ".txt";
            //MessageBox.Show(SN);
            //string caminhoArquivo = @"C:\Parser\" + SN + ".txt"; //caminho completo
            StringBuilder sConteudo = new StringBuilder();
            sConteudo.AppendLine("S" + SN);
            sConteudo.AppendLine("CJC-HITACHI");
            sConteudo.AppendLine("IJC-HITACHI");
            sConteudo.AppendLine("NJCH-FVT01"); // TEST STATION
            //sConteudo.AppendLine("NFVT1"); // TEST STATION
            sConteudo.AppendLine("PFVT1");
            if (failDescription.Length < 4)
            {
                sConteudo.AppendLine("TP");
            }
            else
            {
                sConteudo.AppendLine("TF");
                sConteudo.AppendLine("F" + failDescription);
            }

            if (SN.Substring(0, 3) == "RCI")
            {
                //
                sConteudo.AppendLine("M" + testStep6 + " - GB(mO)");
                sConteudo.AppendLine("d" + volt6);
                sConteudo.AppendLine("UO");
                //
                sConteudo.AppendLine("M" + testStep6 + " - IR(mO)");
                sConteudo.AppendLine("d" + current6);
                sConteudo.AppendLine("UO");
                //
                sConteudo.AppendLine("M" + testStep6 + " - ACW(mA)");
                sConteudo.AppendLine("d" + power6);
                sConteudo.AppendLine("UA");
                //
                sConteudo.AppendLine("M" + testStep6 + " - LC(mA)");
                sConteudo.AppendLine("d" + LC);
                sConteudo.AppendLine("UA");
                //
                sConteudo.AppendLine("M" + testStep5 + " - Volt(V)");
                sConteudo.AppendLine("d" + volt5);
                sConteudo.AppendLine("UV");
                //
                sConteudo.AppendLine("M" + testStep5 + " - Curr(A)");
                sConteudo.AppendLine("d" + current5);
                sConteudo.AppendLine("UA");
                //
                sConteudo.AppendLine("M" + testStep5 + " - Power(W)");
                sConteudo.AppendLine("d" + power5);
                sConteudo.AppendLine("UW");
                //
                sConteudo.AppendLine("M" + testStep4 + " - Volt(V)");
                sConteudo.AppendLine("d" + volt4);
                sConteudo.AppendLine("UV");
                //
                sConteudo.AppendLine("M" + testStep4 + " - Curr(A)");
                sConteudo.AppendLine("d" + current4);
                sConteudo.AppendLine("UA");
                //
                sConteudo.AppendLine("M" + testStep4 + " - Power(W)");
                sConteudo.AppendLine("d" + power4);
                sConteudo.AppendLine("UW");
                //
                sConteudo.AppendLine("M" + testStep3 + " - Volt(V)");
                sConteudo.AppendLine("d" + volt3);
                sConteudo.AppendLine("UV");
                //
                sConteudo.AppendLine("M" + testStep3 + " - Curr(A)");
                sConteudo.AppendLine("d" + current3);
                sConteudo.AppendLine("UA");
                //
                sConteudo.AppendLine("M" + testStep3 + " - Power(W)");
                sConteudo.AppendLine("d" + power3);
                sConteudo.AppendLine("UW");
                //
                sConteudo.AppendLine("M" + testStep2 + " - Volt(V)");
                sConteudo.AppendLine("d" + volt2);
                sConteudo.AppendLine("UV");
                //
                sConteudo.AppendLine("M" + testStep2 + " - Curr(A)");
                sConteudo.AppendLine("d" + current2);
                sConteudo.AppendLine("UA");
                //
                sConteudo.AppendLine("M" + testStep2 + " - Power(W)");
                sConteudo.AppendLine("d" + power2);
                sConteudo.AppendLine("UW");
                //
                sConteudo.AppendLine("M" + testStep1 + " - Volt(V)");
                sConteudo.AppendLine("d" + volt1);
                sConteudo.AppendLine("UV");
                //
                sConteudo.AppendLine("M" + testStep1 + " - Curr(A)");
                sConteudo.AppendLine("d" + current1);
                sConteudo.AppendLine("UA");
                //
                sConteudo.AppendLine("M" + testStep1 + " - Power(W)");
                sConteudo.AppendLine("d" + power1);
                sConteudo.AppendLine("UW");
            }
            if (SN.Substring(0, 3) == "RPC")
            {
                sConteudo.AppendLine("M" + testStep5 + " - GB(mO)");
                sConteudo.AppendLine("d" + volt5);
                sConteudo.AppendLine("UV");
                //
                sConteudo.AppendLine("M" + testStep5 + " - IR(mO)");
                sConteudo.AppendLine("d" + current5);
                sConteudo.AppendLine("UA");
                //
                sConteudo.AppendLine("M" + testStep5 + " - ACW(mA)");
                sConteudo.AppendLine("d" + power5);
                sConteudo.AppendLine("UW");
                //
                sConteudo.AppendLine("M" + testStep5 + " - LC(mA)");
                sConteudo.AppendLine("d" + LC);
                sConteudo.AppendLine("UA");
                //
                sConteudo.AppendLine("M" + testStep4 + " - Volt(V)");
                sConteudo.AppendLine("d" + volt4);
                sConteudo.AppendLine("UV");
                //
                sConteudo.AppendLine("M" + testStep4 + " - Curr(A)");
                sConteudo.AppendLine("d" + current4);
                sConteudo.AppendLine("UA");
                //
                sConteudo.AppendLine("M" + testStep4 + " - Power(W)");
                sConteudo.AppendLine("d" + power4);
                sConteudo.AppendLine("UW");
                //
                sConteudo.AppendLine("M" + testStep3 + " - Volt(V)");
                sConteudo.AppendLine("d" + volt3);
                sConteudo.AppendLine("UV");
                //
                sConteudo.AppendLine("M" + testStep3 + " - Curr(A)");
                sConteudo.AppendLine("d" + current3);
                sConteudo.AppendLine("UA");
                //
                sConteudo.AppendLine("M" + testStep3 + " - Power(W)");
                sConteudo.AppendLine("d" + power3);
                sConteudo.AppendLine("UW");
                //
                sConteudo.AppendLine("M" + testStep2 + " - Volt(V)");
                sConteudo.AppendLine("d" + volt2);
                sConteudo.AppendLine("UV");
                //
                sConteudo.AppendLine("M" + testStep2 + " - Curr(A)");
                sConteudo.AppendLine("d" + current2);
                sConteudo.AppendLine("UA");
                //
                sConteudo.AppendLine("M" + testStep2 + " - Power(W)");
                sConteudo.AppendLine("d" + power2);
                sConteudo.AppendLine("UW");
                //
                sConteudo.AppendLine("M" + testStep1 + " - Volt(V)");
                sConteudo.AppendLine("d" + volt1);
                sConteudo.AppendLine("UV");
                //
                sConteudo.AppendLine("M" + testStep1 + " - Curr(A)");
                sConteudo.AppendLine("d" + current1);
                sConteudo.AppendLine("UA");
                //
                sConteudo.AppendLine("M" + testStep1 + " - Power(W)");
                sConteudo.AppendLine("d" + power1);
                sConteudo.AppendLine("UW");
            }

            try
            {
                //invocando o método WriteAllText, informando o caminho e o conteúdo
                //Console.Write("CAMINHOOOO:"+caminhoArquivo);
                //System.IO.File.WriteAllText(caminhoArquivo, sConteudo.ToString());
                return sConteudo;
                //condição arquivo gerado
                //updateUI("Log File Generated!");
                //label3.BackColor = Color.GreenYellow;
            }
            catch (Exception ex)
            {
                return null;
                //Log não gerado
                //MessageBox.Show(ex.Message);
                //updateUI("Error Generating Log!");
                //label3.BackColor = Color.Red;
            }
        }

        public void SN_CLear()
        {
            this.SN = "";
        }

        public string GetSN()
        {
            return this.SN;
        }
    }
}
