import os
try:
  import paramiko
  import requests
  import time
  from requests.auth import HTTPBasicAuth
  import sys, getopt
except Exception, e:
    os.system('pip install paramiko')
    import paramiko

def start_environment(cbnodes, prefix):
	cb_args = "couchbase_base={0}".format(cbnodes)
	args = ["docker-compose", "-p='{0}'".format(prefix), "scale", cb_args] #,  "spark_master=1",  spark_worker_args]
        print 'start environment args are', args
	run_command(args)

class docker(object):
     def __init__(self,host,username,password,num_container=4):
        self.client = paramiko.SSHClient()
        self.host = host
        self.username = username
        self.password = password
        self.num_container = num_container
        self.cbnodes =  None
        self.cbips =  []
        self.timeout =  20

     def connect(self):
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.client.connect(self.host, username=self.username, password=self.password)
        except Exception,e:
         raise e

     def start_docker(self):
         print 'Starting docker pull'
         self.client.exec_command('docker pull registry-couchbase.rhcloud.com/rhel7/couchbase')
         time.sleep(self.timeout)
         for i in range(self.num_container):
           print 'starting docker containers : ',i
           self.client.exec_command('docker run -d -P registry-couchbase.rhcloud.com/rhel7/couchbase')
           time.sleep(self.timeout)

     def get_pid_docker(self):
        cmd  = "docker ps | grep couchbase | awk '{print $1}'"
        (stdin, self.cbnodes, stderr) = self.client.exec_command(cmd)

     def kill_docker(self):
         self.get_pid_docker()
         for nodes in self.cbnodes:
             self.client.exec_command('docker kill {0}'.format(nodes))

     def get_ip_cb(self):
           for n in self.cbnodes:
                cmd = 'docker inspect --format "{{.NetworkSettings.IPAddress}}" ' + n
                (stdin, stdout, stderr) = self.client.exec_command(cmd)
                self.cbips.append(stdout.read().strip())
           print 'couchbase IPs : ' ,self.cbips

     def run(self):
        self.connect()
        self.kill_docker()
        self.start_docker()
        self.get_pid_docker()
        self.get_ip_cb()

class couchbase(docker):

        def __init__(self,host,username,password,num_container=4):
            super(couchbase,self).__init__(host,username,password,num_container)
            self.current_ip = None

        def setup_uname_pass(self):
           print 'setup username password for {0}'.format(self.current_ip)
           self.args =  "curl -v -X POST \
http://{0}:8091/settings/web -d 'password=password&username=Administrator&port=SAME'".format(self.current_ip)
           stdin,stdout,stderr= self.client.exec_command(self.args)

        def setup_service(self):
           print 'setup service for {0}'.format(self.current_ip)
           self.args="curl -u Administrator:password -v -X POST \
http://{0}:8091/node/controller/setupServices -d 'services=kv'".format(self.current_ip)
           stdin,stdout,stderr= self.client.exec_command(self.args)

        def add_node(self):
            print 'add node for {0}'.format(self.ip)
            self.args = 'curl -u Administrator:password {0}:8091/controller/addNode' \
                        ' -d "hostname={1}&user=Administrator&password=password"'.format(self.ip, self.current_ip)
            stdin,stdout,stderr= self.client.exec_command(self.args)
            time.sleep(self.timeout)

        def rebalance(self):
            print 'rebalance operation'
            known_nodes = ','.join([ 'ns_1@' + s for s in self.cbips])
            self.args = "curl -v -u Administrator:password -XPOST 'http://{0}:8091/controller/rebalance' \
  -d 'ejectedNodes=&knownNodes={1}'".format(self.current_ip,known_nodes)
            print self.args
            stdin,stdout,stderr= self.client.exec_command(self.args)
            print stdout.read()

        def init_couchbase_nodes(self):
               print self.cbips
               self.ip = self.cbips[0]
               for ip in self.cbips:
                   self.current_ip = ip
                   self.setup_service()
                   self.setup_uname_pass()
                   if ip != self.ip:
                       print 'adding node'
                       self.add_node()
               self.rebalance()

        def run(self):
            super(couchbase,self).run()
            self.init_couchbase_nodes()


def main(argv):
   ip = ''
   username = ''
   password = ''
   num_container = 0

   try:
      opts, args = getopt.getopt(argv,"hi:u:p:n:",["ip=","username=","password=","num_container="])
   except getopt.GetoptError:
      print 'docker.py -i ip -u username -p password -n num_containers'
      sys.exit(2)
   try:
       for opt, arg in opts:
          if opt == '-h':
             print 'docker.py -i ip -u username -p password -n num_containers'
             sys.exit()
          elif opt in ("-i", "--ip"):
             ip = arg
          elif opt in ("-u", "--username"):
             username = arg
          elif opt in ("-p", "--password"):
             password = arg
          elif opt in ("-n", "--num_container"):
             num_container= int(arg)
       cb = couchbase(ip,username,password,num_container)
       cb.run()
   except Exception, e:
       raise e

if __name__ == "__main__":
   main(sys.argv[1:])

