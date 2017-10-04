# @Time    : 2017/10/4 下午9:25
# @Author  : Obser


import socketserver
import json
import os
from core import protocol
from core import update

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            try:
                self.data = self.request.recv(1024).strip()
                if not self.data:
                    break
                print("{} 发送请求:".format(self.client_address[0]))

                cmd_dic = json.loads(self.data.decode())
                print(cmd_dic)
                action = cmd_dic["action"]
                if hasattr(self, action):
                    func = getattr(self, action)
                    func(cmd_dic)
            except Exception as e:
                pass

    def mkdir(self, *args):
        """
        创建目录
        :param args:
        :return:
        """
        cmd_dic = args[0]
        cmd = cmd_dic["cmd"]
        os.popen(cmd)

    def pwd(self, *args):
        """
        显示当前路径
        :param args:
        :return:
        """
        path = "root%s" % os.path.abspath(os.path.curdir).split(self.path)[1]
        self.request.send(path.encode())

    def rm(self, *args):
        """
        删除指定文件
        :param args:
        :return:
        """
        cmd_dic = args[0]
        filename = cmd_dic["filename"]
        if os.path.isfile(filename):
            filesize = os.path.getsize(filename)
            self.available += filesize
            update.update_available(self.user_file, self.available)
            os.remove(filename)
            self.request.send(protocol.Protocol.json_rm(status="200", total=self.total, available=self.available).encode())
        else:
            self.request.send(protocol.Protocol.json_rm(status="404").encode())

    def cd(self, *args):
        """
        进入指定目录
        :param args:
        :return:
        """
        cmd_dic = args[0]
        dir_name = cmd_dic["dirname"]
        if dir_name == "..":
            if os.path.abspath(os.path.curdir) == self.path:
                path = self.path
            else:
                path = os.path.pardir
        elif dir_name.find("/") != -1:
            path = "%s/%s" % (self.path, dir_name)
        else:
            path = "%s/%s" % (os.path.abspath(os.path.curdir), dir_name)

        if os.path.isdir(path):
            os.chdir(path)
            self.request.send(protocol.Protocol.json_cd(os.path.curdir, status="200").encode())
        else:
            self.request.send(protocol.Protocol.json_cd(os.path.curdir, status="404").encode())

    def auth(self, *args):
        """
        客户端认证
        :param args:
        :return:
        """
        cmd_dic = args[0]
        account = cmd_dic["account"]
        password = cmd_dic["password"]
        user_file = "%s/data/%s/user_info" % (BASE_DIR, account)
        if os.path.isfile(user_file):
            with open(user_file) as f:
                user_info = json.load(f)
                user_password = user_info["password"]
                if password == user_password:
                    self.request.send(protocol.Protocol.json_auth(total=user_info["total"],
                                                                  available=user_info["available"]).encode())
                    os.chdir("%s/data/%s/root" % (BASE_DIR, account))
                    self.path = "%s/data/%s/root" % (BASE_DIR, account)
                    self.total = user_info["total"]
                    self.available = user_info["available"]
                    self.user_file = user_file
                else:
                    self.request.send(protocol.Protocol.json_auth(status="404").encode())
        else:
            self.request.send(protocol.Protocol.json_auth(status="404").encode())

    def ls(self, *args):
        """
        显示当前目录文件
        :param args:
        :return:
        """
        cmd_dic = args[0]
        cmd = cmd_dic["action"]
        result = os.popen(cmd).read()
        self.request.send(protocol.Protocol.json_ls(resultsize=len(result)).encode())
        client_response = self.request.recv(1024)
        self.request.send(result.encode())

    def put(self, *args):
        """接收客户端上传的文件"""
        cmd_dic = args[0]
        filename = cmd_dic["filename"]
        filesize = cmd_dic["filesize"]
        if self.available - filesize < 0:
            self.request.send(protocol.Protocol.json_put(None, None, "300").encode())
        else:
            if os.path.isfile(filename):
                self.available = self.available + os.path.getsize(filename) - filesize
            else:
                self.available -= filesize

            f = open(filename, "wb")
            self.request.send(
                protocol.Protocol.json_put(None, None, "200", total=self.total, available=self.available).encode())
            received_size = 0
            while received_size < filesize:
                data = self.request.recv(1024)
                f.write(data)
                received_size += len(data)
            else:
                print("\033[32;1m文件 [%s] 上传完毕\033[0m" % filename)
                update.update_available(self.user_file, self.available)

    def get(self, *args):
        """向客户端发送文件"""
        cmd_dic = args[0]
        filename = cmd_dic["filename"]
        if os.path.isfile(filename):
            filesize = os.path.getsize(filename)
            json_msg_dic = protocol.Protocol.json_get(filename, filesize, status="200")
            self.request.send(json_msg_dic.encode())
            client_response = self.request.recv(1024)
            with open(filename, "rb") as f:
                for line in f:
                    self.request.send(line)
                else:
                    print("\033[32;1m文件 [%s] 发送完毕\033[0m" % filename)
        else:
            json_msg_dic = protocol.Protocol.json_get(None, None, status="404")
            self.request.send(json_msg_dic.encode())
