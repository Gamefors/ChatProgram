using System.Text;
namespace Chatprogram_GUI.utils
{
    public class DecodingEncodingHelper
    {
        public byte[] StringToBytes(string str)
        {
            byte[] buffer = new byte[1024];
            return Encoding.ASCII.GetBytes(str);
        }
        public string bytesToString(int bytes)
        {
            byte[] buffer = new byte[1024];
            return Encoding.ASCII.GetString(buffer, 0, bytes);
        }
    }
}
