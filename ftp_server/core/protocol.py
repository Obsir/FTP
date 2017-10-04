# @Time    : 2017/10/4 下午1:58
# @Author  : user_info

import json


class Protocol(object):
    @staticmethod
    def json_put(filename, filesize, status="200", total=0, available=0):
        msg_dic = {
            "action": "put",
            "status": status,
            "filename": filename,
            "filesize": filesize,
            "total": total,
            "available": available
        }
        return json.dumps(msg_dic)

    @staticmethod
    def json_auth(account=None, password=None, status="200", total=0, available=0):
        msg_dic = {
            "action": "auth",
            "account": account,
            "password": password,
            "status": status,
            "total": total,
            "available": available
        }
        return json.dumps(msg_dic)

    @staticmethod
    def json_get(filename, filesize, status="200"):
        msg_dic = {
            "action": "get",
            "status": status,
            "filename": filename,
            "filesize": filesize
        }
        return json.dumps(msg_dic)

    @staticmethod
    def json_ls(resultsize=0, status="200"):
        msg_dic = {
            "action": "ls",
            "status": status,
            "resultsize": resultsize
        }
        return json.dumps(msg_dic)

    @staticmethod
    def json_pwd(status="200"):
        msg_dic = {
            "action": "pwd",
            "status": status
        }
        return json.dumps(msg_dic)

    @staticmethod
    def json_mkdir(cmd, status="200"):
        msg_dic = {
            "action": "mkdir",
            "status": status,
            "cmd": cmd
        }
        return json.dumps(msg_dic)

    @staticmethod
    def json_cd(dir_name, status="200"):
        msg_dic = {
            "action": "cd",
            "status": status,
            "dirname": dir_name
        }
        return json.dumps(msg_dic)

    @staticmethod
    def json_rm(filename=None, status="200", total=0, available=0):
        msg_dic = {
            "action": "rm",
            "status": status,
            "filename": filename,
            "total": total,
            "available": available
        }
        return json.dumps(msg_dic)