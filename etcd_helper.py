#!/usr/bin/python3

import sys
import json
import etcd3

class EtcdTools:
    def __init__(self, hostname, port, username, password) -> None:
        self.etcd = etcd3.client(host=hostname, port=port, user=username, password=password)


    def add_host_dns_record(self, env: str, wl_code: str, host: str, ip_address: str):

        dns_record_ttl = 60

        # 因prod環境與其他環境命名方式不是統一 , 由傳入的env參數進行判斷
        if env == "prod":
            etcd_key = f"/coredns/nexiosoft/{wl_code}/{host}"

        elif env == "uat" or env == "stg" or env == "sit":
            etcd_key = f"/coredns/nexiosoft/{env}/{wl_code}/{host}"

        # 序列化
        etcd_value = json.dumps({"host": f"{ip_address}", "ttl": dns_record_ttl})

        print(f"etcd key: {etcd_key}")
        print(f"etcd value: {etcd_value}")

        # 寫入etcd
        print("寫入etcd")
        self.etcd.put(key=etcd_key, value=etcd_value)
        
    def delete_host_dns_record(self, env: str, wl_code: str, host: str):
       
        # 因prod環境與其他環境命名方式不是統一 , 由傳入的env參數進行判斷
        if env == "prod":
            etcd_key = f"/coredns/nexiosoft/{wl_code}/{host}"

        elif env == "uat" or env == "stg" or env == "sit":
            etcd_key = f"/coredns/nexiosoft/{env}/{wl_code}/{host}"

        # 寫入etcd
        print("刪除etcd")
        print(f"etcd key: {etcd_key}")
        self.etcd.delete(key=etcd_key)
        

    # ======================================== 白牌Virtual IP的dns紀錄 ====================================================

    def add_vip_host_dns_record(self, env: str, wl_code: str):

        dns_record_ttl = 60
        mps_virtual_ip = "192.168.27.11"

        # 因prod環境與其他環境命名方式不是統一 , 由傳入的env參數進行判斷
        if env == "prod":
            etcd_key = f"/coredns/nexiosoft/{wl_code}/mps"

        elif env == "uat" or env == "stg" or env == "sit":
            etcd_key = f"/coredns/nexiosoft/{env}/{wl_code}/mps"

        # 序列化
        etcd_value = json.dumps({"host": f"{mps_virtual_ip}", "ttl": dns_record_ttl})
        print(f"etcd key: {etcd_key}, etcd value: {etcd_value} 寫入etcd")
        
        # 寫入
        self.etcd.put(key=etcd_key, value=etcd_value)

    def delete_vip_host_dns_record(self, env:str, wl_code: str):
        
        # 因prod環境與其他環境命名方式不是統一 , 由傳入的env參數進行判斷
        if env == "prod":
            etcd_key = f"/coredns/nexiosoft/{wl_code}/mps"

        elif env == "uat" or env == "stg" or env == "sit":
            etcd_key = f"/coredns/nexiosoft/{env}/{wl_code}/mps"

        print(f"刪除 VIP domain: {etcd_key}")
        self.etcd.delete(key=etcd_key)

    # =========================================== 提供總後台調用 ====================================================
    def add_whitelabel_info_to_etcd(self, env:str, wl_code: str):
        
        # key
        etcd_key = f'/whitelabel/{env}/mps/{wl_code}'

        # 因prod環境與其他環境命名方式不是統一 , 由傳入的env參數進行判斷
        if env == "prod":
            etcd_value = f'mps.{wl_code}'

        elif env == "uat" or env == "stg" or env == "sit":
            etcd_value = f'mps.{wl_code}.{env}'

        print(f"新增白牌資訊: key={etcd_key}, value={etcd_value}")
        self.etcd.put(key=etcd_key, value=etcd_value)

    def delete_whitelabel_info_from_etcd(self, env:str, wl_code: str):

        # key
        etcd_key = f'/whitelabel/{env}/mps/{wl_code}'
         
        print(f"刪除白牌資訊: {etcd_key}")
        self.etcd.delete(key=etcd_key)
        
        
