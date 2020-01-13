using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.Net;
using System.Net.Sockets;
using System.Diagnostics;
using System.Threading;
using System.Windows.Threading;

namespace Chatprogram_GUI
{
    /// <summary>
    /// Interaktionslogik für MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public bool connected = false;
        public objects.Client client;
        public objects.Config config;
        public objects.Client connectedClient;

        public utils.InputHandler inputHandler;
        public MainWindow()
        {
            inputHandler = new utils.InputHandler();
            InitializeComponent();
            config = new objects.Config(IPAddress.Parse("127.0.0.1"), 5000);
        }
        private void MenuItem_Click(object sender, RoutedEventArgs e)
        {
            var option = sender as MenuItem;
            if (option.Name == "Disconnect")
            {
                client.SocketObject.Close();
                UsernameEntry.Text = "";
                Status.Header = "_Offline";
                ConnectionStatus.Visibility = Visibility.Hidden;
                Status.Background = Brushes.Red;
                ChattingGrid.Visibility = Visibility.Hidden;
                Disconnect.IsEnabled = false;
                Login.IsEnabled = true;
                connected = false;
                
            }
            else if (option.Name == "Login")
            {
                LoginGrid.Visibility = Visibility.Visible;
                Login.IsEnabled = false;
            }
            else if (option.Name == "Quit")
            {
                try
                {
                    client.SocketObject.Close();
                }
                catch (System.NullReferenceException)
                {
                    Debug.Print("[Client/Error] No Socket to shutdown.(Cause: Quitting before even connected.)");
                }
                Application.Current.Shutdown();
            }
            
        }
        public void TryConnect(object s)
        {
            string username = s.ToString();
            int trys = 0;
            byte[] buffer = new byte[1024];

            var DecEncHelper = new utils.DecodingEncodingHelper();
            ConnectionStatus.Dispatcher.Invoke(() => {
                ConnectionStatus.Text = "Connecting...";
            });
            while (!connected)
            {
                Socket socketObject = new Socket(config.Ip.AddressFamily, SocketType.Stream, ProtocolType.Tcp);
                var Client = new objects.Client(username, socketObject, config.Ip, config.Port, "first_channel_is_managed_by_server");
                IPEndPoint serverIp = new IPEndPoint(Client.Ip, Client.Port);
                
                IAsyncResult result = Client.SocketObject.BeginConnect(Client.Ip, Client.Port, null, null);

                bool success = result.AsyncWaitHandle.WaitOne(5000, true);

                if (Client.SocketObject.Connected)
                {
                    ConnectionStatus.Dispatcher.Invoke(() => {

                        ConnectionStatus.Text = "Connected";
                    });
                    ClientOutput.Dispatcher.Invoke(() => {
                        ClientOutput.Text = "" + Environment.NewLine;
                    });
                    client = new objects.Client(username, socketObject, config.Ip, config.Port, "first_channel_is_managed_by_server");
                    Client.SocketObject.EndConnect(result);
                    connectedClient = Client;
                    client.SocketObject.Send(DecEncHelper.StringToBytes($"011{client.Username}"));
                    Thread.Sleep(10);
                    client.SocketObject.Send(DecEncHelper.StringToBytes($"611Welcome_Channel"));
                    Status.Dispatcher.Invoke(() => {
                        Status.Header = $"_Online as : {client.Username}";
                        Status.Background = Brushes.Green;
                    });
                    connected = true;
                    Disconnect.Dispatcher.Invoke(() => {
                        Disconnect.IsEnabled = true;
                    });
                    utils.ServerHandler _serverHandler = new utils.ServerHandler(client, ClientOutput, ChannelTreeView);
                    Thread t = new Thread(new ThreadStart(_serverHandler.startPR));
                    t.Start();
                    _serverHandler.getChannel();
                }
                else
                {
                    Client.SocketObject.Close();
                    ConnectionStatus.Dispatcher.Invoke(() => {
                        ConnectionStatus.Text = $"Trying to connect ip: {Client.Ip} Attempts: {trys}";
                    });
                    Debug.Print($"[Client/Info] Attempting to connect to server with ip: {Client.Ip} Attempts: {trys}");
                }
                trys++;
                Thread.Sleep(2000);
            }
        }
        private void ConfirmButton_Click(object sender, RoutedEventArgs e)
        {
            string username = UsernameEntry.Text;
            LoginGrid.Visibility = Visibility.Hidden;
            ChattingGrid.Visibility = Visibility.Visible;
            ConnectionStatus.Visibility = Visibility.Visible;
            ConnectionStatus.Text = $"[Client/Info] Trying to connect...";
            Thread tryconnect = new Thread(new ParameterizedThreadStart(TryConnect));
            object test = username;
            tryconnect.Start(test);
        }
        
        public void OnKeyDownHandler(object sender, KeyEventArgs e)
        {
            var DecEncHelper = new utils.DecodingEncodingHelper();
            if (connected)
            {
                if (e.Key == Key.Enter)
                {
                    string msg = ClientInput.Text;
                    if (msg.StartsWith("/"))
                    {
                        inputHandler.handleInput(msg.Remove(0, 1), connectedClient, ClientOutput);
                    }
                    else
                    {
                        ClientOutput.AppendText("Du: " + msg + Environment.NewLine);
                        client.SocketObject.Send(DecEncHelper.StringToBytes($"001{msg}"));
                    }
                    ClientInput.Text = "";
                }
            }
           
        }

    }
}
