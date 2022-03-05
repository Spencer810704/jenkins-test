#!/usr/bin/python3

import sys
import json
import etcd3

class EtcdTools:
    def __init__(self, password) -> None:
        self.etcd = etcd3.client(host="etcd", port=2379, user="root", password=password)

    def load_config_from_django_settings(self):
        pass

    def load_config_from_file(self):
        pass

    def add_host_dns_record(self, env: str, wl_code: str, hostname: str, ip_address: str):
        """增加主機記錄到etcd(內部dns server是coredns+etcd)

        Args:
            env (str): 操作環境
            wl_code (str): whitelavel code
            hostname (str): 主機名稱(同nutanix vm名)
                舉例:
                - Prod環境格式為 mps01.ae888
                - 非Pord環境格式為 mps01.ae888.uat(以uat為例)
            ip_address (str): 該主機對應IP地址
        """
        hostname = hostname.split(".")[0]
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
        result = self.etcd.put(key=etcd_key, value=etcd_value)
        print(result)
        return result
        
    def delete_host_dns_record(self, env: str, wl_code: str, hostname: str):
        """刪除etcd主機記錄

        Args:
            env (str): 操作環境
            wl_code (str): whitelavel code
            hostname (str): 主機名稱(同nutanix vm名)
                舉例:
                - Prod環境格式為 mps01.ae888
                - 非Pord環境格式為 mps01.ae888.uat(以uat為例)
            ip_address (str): 該主機對應IP地址
        """

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
    password = sys.argv[2]
    
    print(f"password: {password}")

    etcd_tool = EtcdTools(password=password)

    env = "UAT".lower()
    wl_code = "abcd123".lower()
    game_type = "mps".lower()

    # # 增加解析
    hostname_one = "mps01.abcd123.uat".lower()
    ip_one = "127.0.0.1".lower()
    etcd_tool.add_host_dns_record(env=env, wl_code=wl_code, hostname=hostname_one, ip_address=ip_one)

    # # 增加解析
    hostname_two = "mps02.abcd123.uat".lower()
    ip_two = "127.0.0.1".lower()
    etcd_tool.add_host_dns_record(env=env, wl_code=wl_code, hostname=hostname_two, ip_address=ip_two)
