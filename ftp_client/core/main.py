# @Time    : 2017/10/4 下午12:32
# @Author  : user_info


from core import ftp_client

def run():
    client = ftp_client.FTPClient("localhost", 9999)
    client.start()