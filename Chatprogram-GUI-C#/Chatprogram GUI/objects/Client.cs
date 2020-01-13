using System.Net;
using System.Net.Sockets;

namespace Chatprogram_GUI.objects
{
    public class Client
    {
        public string Username { get; set; }
        public Socket SocketObject { get; set; }
        public IPAddress Ip { get; set; }
        public int Port { get; set; }
        public string Channel { get; set; }

        public Client(string username, Socket socketObject, IPAddress ip, int port, string channel)
        {
            Username = username;
            SocketObject = socketObject;
            Ip = ip;
            Port = port;
            Channel = channel;
        }
    }
}
