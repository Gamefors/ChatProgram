import socketserver

class ServerThread(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass