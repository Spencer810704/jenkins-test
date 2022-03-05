import sys
from utils.etcd_helper import EtcdTools

if __name__ == "__main__":
    etcd_hostname = sys.argv[1]
    etcd_port = sys.argv[2]
    etcd_username = sys.argv[3]
    etcd_password = sys.argv[4]
    
    env = sys.argv[5].lower()
    wl_code = sys.argv[6].lower()    
    host = sys.argv[7].lower()
    
    etcd_tool = EtcdTools(hostname=etcd_hostname, port=etcd_port, username=etcd_username, password=etcd_password)

    # 刪除解析
    etcd_tool.delete_host_dns_record(env=env, wl_code=wl_code, host=host)
