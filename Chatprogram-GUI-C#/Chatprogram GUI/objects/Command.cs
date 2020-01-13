using System.Net;

namespace Chatprogram_GUI.objects
{
    public class Command
    {
        public string Name { get; set; }
        public string Syntax { get; set; }
        public string Arguments { get; set; }
        public string Description { get; set; }
        public Command(string name, string syntax, string arguments, string description)
        {
            Name = name.ToLower();
            Syntax = syntax;
            Arguments = arguments;
            Description = description;
        }
    }
}
