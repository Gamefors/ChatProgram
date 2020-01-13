using System.Net;

namespace Chatprogram_GUI.objects
{
    public class Config
    {
        public IPAddress Ip { get; set; }
        public int Port { get; set; }
        public Config(IPAddress ip, int port)
        {
            Ip = ip;
            Port = port;
        }
    }
}
