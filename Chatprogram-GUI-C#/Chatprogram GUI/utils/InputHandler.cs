using Chatprogram_GUI.objects;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Controls;

namespace Chatprogram_GUI.utils
{
    public class InputHandler
    {
        List<Command> commandList = new List<Command>();
        public TextBox output;
        public objects.Client client;
        public Command cmdClear;
        
        void initializeCommands()
        {
            cmdClear = createCommand("Clear", "/clear", "NONE", "Clears your interpreter console.");
        }

        Command createCommand(string name, string syntax, string arguments, string description)
        {
            Command command = new objects.Command(name, syntax, arguments, description);
            commandList.Add(command);
            return command;
        }

        public InputHandler()
        {
            initializeCommands();
        }

        public void handleInput(string command1, objects.Client client1, TextBox output)
        {
            bool isCommand = true;
            client = client1;
            string[] command = command1.Split(new string[] { " " }, StringSplitOptions.None);
            try
            {
                var s = command[0];
            }
            catch (Exception ex)
            {
                isCommand = false;
                output.Dispatcher.Invoke(() =>
                {
                    output.AppendText("[Client/Error] type /help for a list of commands" + Environment.NewLine);
                });
            }
            if (isCommand)
            {
                if (command[0].ToLower() == cmdClear.Name)
                {
                    output.Dispatcher.Invoke(() =>
                    {
                        output.Text = "";
                    });
                }
                else
                {
                    output.Dispatcher.Invoke(() =>
                    {
                        output.AppendText("[Client/Error] Unknown command: " + command[0] + Environment.NewLine);
                        output.AppendText("[Client/Error] type /help for a list of commands" + Environment.NewLine);
                    });
                }
            }
        }
    }
}

