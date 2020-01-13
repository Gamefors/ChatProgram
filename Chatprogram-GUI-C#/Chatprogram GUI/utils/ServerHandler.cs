using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Controls;
using System.Windows.Media;

namespace Chatprogram_GUI.utils
{
    public class ServerHandler
    {
        public objects.Client client;
        public TextBox output;
        public TreeView channelTreeView;

        public TreeViewItem welcomeChannelTreeView;

        public string[] easyRequestIds = new string[] { "001", "401", "411", "023", "031", "411", "711" };
        public ServerHandler(objects.Client client1, TextBox output1, TreeView channelTreeView1)
        {
            

            client = client1;
            output = output1;
            channelTreeView = channelTreeView1;

            channelTreeView.Dispatcher.Invoke(() => {
                welcomeChannelTreeView = new TreeViewItem();
                welcomeChannelTreeView.Header = "Welcome_Channel";
                welcomeChannelTreeView.Foreground = Brushes.White;
                channelTreeView.Items.Add(welcomeChannelTreeView);
            });
            
        }

        public void getChannel()
        {
            var DecEncHelper = new utils.DecodingEncodingHelper();
        }

        public void startPR()
        {
            bool connected = true;
            byte[] buffer = new byte[1024];
            var DecEncHelper = new DecodingEncodingHelper();
            while (connected)
            {
                try
                {
                    int bytesRec = client.SocketObject.Receive(buffer);
                    var s = Encoding.ASCII.GetString(buffer, 0, bytesRec);
                    handleRequest(s, client);
                }
                catch (Exception ex)
                {
                    connected = false;
                    Debug.WriteLine("disconnected");
                }
            }
        }
        public void handleRequest(string request, objects.Client client)
        {
            string requestId = request.Substring(0, 3);

            string requestdata = request.Remove(0, 3);

            if (easyRequestIds.Contains(requestId))
            {
                output.Dispatcher.Invoke(() => {
                    output.AppendText(requestdata + Environment.NewLine);
                });
            }
            else if (requestId == "611")
            {
                if (requestdata.Contains("exists"))
                {            
                    output.Dispatcher.Invoke(() => {
                        output.AppendText(requestdata + Environment.NewLine);
                    });
                }
                else
                {
                    string[] tempList;
                    tempList = requestdata.Split(new string[] { "," }, StringSplitOptions.None);
                    foreach (string obj in tempList)
                    {
                        string s = obj.Replace("'", "").Replace("[", "").Replace("]", "").Replace(" ", string.Empty);
                        if (s.Contains(client.Username))
                        {
                            output.Dispatcher.Invoke(() =>
                            {
                                TreeViewItem t = new TreeViewItem();
                                t.Header = s + "(you)";
                                t.Foreground = Brushes.White;
                                welcomeChannelTreeView.Items.Add(t);
                            });
                        }
                        else
                        {
                            output.Dispatcher.Invoke(() =>
                            {
                                TreeViewItem t = new TreeViewItem();
                                t.Header = s;
                                t.Foreground = Brushes.White;
                                welcomeChannelTreeView.Items.Add(t);
                            });
                        }
                    }
                }
            }
            else if (requestId == "811")
            {
                string[] test = requestdata.Split(new string[] { " " }, StringSplitOptions.None);
                if (requestdata.Contains("joined"))
                {
                    Debug.WriteLine(test[0] + "should be added");
                   // TreeViewItem t = new TreeViewItem();
                   // t.Header = test[0];
                   // t.Foreground = Brushes.White;
                   // welcomeChannelTreeView.Dispatcher.Invoke(() =>
                   // {
                    //    welcomeChannelTreeView.Items.Add(t);
                   // });
                    
                }
                else
                {
                    Debug.WriteLine(test[0] + "should be removed");
                  //  welcomeChannelTreeView.Dispatcher.Invoke(() =>
                   // {
                    //    foreach (TreeViewItem item in welcomeChannelTreeView.Items)
                     ///   {
                       //     if (item.Header.ToString() == test[0])
                        //    {
                         //       welcomeChannelTreeView.Items.Remove(item);
                          //  }
                     //   }
                      //  Debug.WriteLine("left");
                   // });
                }
            }
        }
    }

}
