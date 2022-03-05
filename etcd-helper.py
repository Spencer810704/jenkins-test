#!/usr/bin/python3

import sys
import json
import etcd3

class EtcdTools:
    def __init__(self, hostname, port, username, password) -> None:
        self.etcd = etcd3.client(host=hostname, port=port, user=username, password=password)

    def add_host_dns_record(self, env: str, wl_code: str, hostname: str, ip_address: str):

        dns_record_ttl = 60

        # 因prod環境與其他環境命名方式不是統一 , 由傳入的env參數進行判斷
        if env == "prod":
            etcd_key = f"/coredns/nexiosoft/{wl_code}/{hostname}"

        elif env == "uat" or env == "stg" or env == "sit":
            etcd_key = f"/coredns/nexiosoft/{env}/{wl_code}/{hostname}"

        # 序列化
        etcd_value = json.dumps({"host": f"{ip_address}", "ttl": dns_record_ttl})

        print(f"etcd key: {etcd_key}")
        print(f"etcd value: {etcd_value}")

        # 寫入etcd
        print("寫入etcd")
        self.etcd.put(key=etcd_key, value=etcd_value)
        
    def delete_host_dns_record(self, env: str, wl_code: str, hostname: str):
        
        hostname = hostname.split(".")[0]

        # 因prod環境與其他環境命名方式不是統一 , 由傳入的env參數進行判斷
        if env == "prod":
            etcd_key = f"/coredns/nexiosoft/{wl_code}/{hostname}"

        elif env == "uat" or env == "stg" or env == "sit":
            etcd_key = f"/coredns/nexiosoft/{env}/{wl_code}/{hostname}"

        # 寫入etcd
        print("刪除etcd")
        print(f"etcd key: {etcd_key}")
        self.etcd.delete(key=etcd_key)
        
        

if __name__ == "__main__":
    hostname = sys.argv[1]
    port = sys.argv[2]
    username = sys.argv[3]
    password = sys.argv[4]
    
    env = sys.argv[5].lower()
    wl_code = sys.argv[6].lower()    
    host = sys.argv[7].lower()
    ip_address = sys.argv[8].lower()
    
    etcd_tool = EtcdTools(hostname=hostname, port=port, username=username, password=password)

    # 增加解析
    etcd_tool.add_host_dns_record(env=env, wl_code=wl_code, hostname=host, ip_address=ip_address)

