# @Time    : 2017/10/2 下午5:10
# @Author  : Obser


import socketserver

from core import ftp_server


def run():
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    server = socketserver.ThreadingTCPServer((HOST, PORT), ftp_server.MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
