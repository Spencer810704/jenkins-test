properties([
  buildDiscarder(
      logRotator(
          numToKeepStr: '5'
      )
  )
])

pipeline {
    agent any
    environment {
        // UAT 環境配置
        ETCD_HOST = "etcd"
        ETCD_PORT = 2379
        ETCD_USERNAME = "root"
        ETCD_PASSWORD = credentials("etcd-password")
        VIRTAUL_IP = "192.168.68.12"
    }
    parameters {
        choice(name: 'env', choices: ['uat'], description: 'environment')
        string(name: 'wl_code', defaultValue: 'ae888', description: '白牌')
        string(name: 'mps_one_ip', defaultValue: '192.168.0.200', description: 'mps01 對應IP地址')
        string(name: 'mps_two_ip', defaultValue: '192.168.0.201', description: 'mps02 對應IP地址')
    }
    stages {
        stage('Upgrade pip and install requirements') {
            steps {
                withPythonEnv('/usr/bin/python3'){
                    // 查看python版本
                    sh 'python --version'
                    
                    // 升級pip版本
                    sh 'pip install --upgrade pip' 
                    
                    // 安裝依賴包
                    sh 'pip install -r requirements.txt'
                    
                    // 顯示安裝套件
                    sh 'pip list'
                }
            }
        }
        stage('add coredns and mothership record') {
            steps {
                withPythonEnv('/usr/bin/python3'){
                    sh "python3 add_record.py $ETCD_HOST $ETCD_PORT $ETCD_USERNAME $ETCD_PASSWORD ${params.env} ${params.wl_code} mps01 ${params.mps_one_ip}"
                    sh "python3 add_record.py $ETCD_HOST $ETCD_PORT $ETCD_USERNAME $ETCD_PASSWORD ${params.env} ${params.wl_code} mps02 ${params.mps_two_ip}"
                    sh "python3 add_virtual_ip.py $ETCD_HOST $ETCD_PORT $ETCD_USERNAME $ETCD_PASSWORD ${params.env} ${params.wl_code} $VIRTAUL_IP "
                    sh "python3 add_mothership_record.py $ETCD_HOST $ETCD_PORT $ETCD_USERNAME $ETCD_PASSWORD ${params.env} ${params.wl_code} "
                }
            }
        }

    }
    post {
        cleanup {
            /* clean up our workspace */
            // deleteDir()
            
            /* clean up tmp directory */
            dir("${workspace}@tmp") {
                deleteDir()
            }
            
            /* clean up script directory */
            dir("${workspace}@script") {
                deleteDir()
            }
        }
    }
}
