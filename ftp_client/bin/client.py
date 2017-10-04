# @Time    : 2017/10/4 下午2:21
# @Author  : user_info


import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


from core import main


if __name__ == '__main__':
    main.run()