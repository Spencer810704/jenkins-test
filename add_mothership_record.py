#!/usr/bin/python3

import sys
from utils.etcd_helper import EtcdTools

if __name__ == "__main__":
    etcd_hostname = sys.argv[1]
    etcd_port = sys.argv[2]
    etcd_username = sys.argv[3]
    etcd_password = sys.argv[4]
    
    env = sys.argv[5].lower()
    wl_code = sys.argv[6].lower()   
    
    etcd_tool = EtcdTools(hostname=etcd_hostname, port=etcd_port, username=etcd_username, password=etcd_password)

    # 增加總後台K/V紀錄
    etcd_tool.add_whitelabel_info_to_etcd(env=env, wl_code=wl_code)
