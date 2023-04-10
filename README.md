# Msg queue with python etcd-client

## ✨ Setup ETCD cluster

Use digital ocean for testing, they provide 200 credits and sufficient to test this.

> **Step 1** - Spin up 3 droplets; choose docker image from marketplace

<br />

> **Step 2** - Setup ETCD cLuster

<br />

```txt
In each server run the follwing commands
```

<br />

```bash
$ mkdir etcd
$ cd etcd
$ mkdir log
$ vi start.sh
```
Paste the following in node 1 and press :q! to save the files:
```txt
#!/bin/bash
REGISTRY=quay.io/coreos/etcd
REGISTRY=gcr.io/etcd-development/etcd
ETCD_VERSION=v3.4.23
TOKEN=my-etcd-token
CLUSTER_STATE=new
NAME_1=etcd-node-0
NAME_2=etcd-node-1
NAME_3=etcd-node-2
HOST_1=67.205.137.130 # use your droplet 1's public IP
HOST_2=143.198.161.94 # use your droplet 2's public IP
HOST_3=143.198.162.212 # use your droplet 3's public IP
CLUSTER=${NAME_1}=http://${HOST_1}:2380,${NAME_2}=http://${HOST_2}:2380,${NAME_3}=http://${HOST_3}:2380
DATA_DIR=/var/lib/etcd

THIS_NAME=${NAME_1}
THIS_IP=${HOST_1}
docker run \
  -p 2379:2379 \
  -p 2380:2380 \
  --volume=${DATA_DIR}:/etcd-data \
  --name etcd ${REGISTRY}:${ETCD_VERSION} \
  /usr/local/bin/etcd \
  --data-dir=/etcd-data --name ${THIS_NAME} \
  --initial-advertise-peer-urls http://${THIS_IP}:2380 --listen-peer-urls http://0.0.0.0:2380 \
  --advertise-client-urls http://${THIS_IP}:2379 --listen-client-urls http://0.0.0.0:2379 \
  --initial-cluster ${CLUSTER} \
  --initial-cluster-state ${CLUSTER_STATE} --initial-cluster-token ${TOKEN} >> log/${NAME_1}.log 2>&1 &
```

Paste the following in node 2 and press :q! to save the files:
```txt
#!/bin/bash
REGISTRY=quay.io/coreos/etcd
REGISTRY=gcr.io/etcd-development/etcd
ETCD_VERSION=v3.4.23
TOKEN=my-etcd-token
CLUSTER_STATE=new
NAME_1=etcd-node-0
NAME_2=etcd-node-1
NAME_3=etcd-node-2
HOST_1=67.205.137.130 # use your droplet 1's public IP
HOST_2=143.198.161.94 # use your droplet 2's public IP
HOST_3=143.198.162.212 # use your droplet 3's public IP
CLUSTER=${NAME_1}=http://${HOST_1}:2380,${NAME_2}=http://${HOST_2}:2380,${NAME_3}=http://${HOST_3}:2380
DATA_DIR=/var/lib/etcd

THIS_NAME=${NAME_2}
THIS_IP=${HOST_2}
docker run \
  -p 2379:2379 \
  -p 2380:2380 \
  --volume=${DATA_DIR}:/etcd-data \
  --name etcd ${REGISTRY}:${ETCD_VERSION} \
  /usr/local/bin/etcd \
  --data-dir=/etcd-data --name ${THIS_NAME} \
  --initial-advertise-peer-urls http://${THIS_IP}:2380 --listen-peer-urls http://0.0.0.0:2380 \
  --advertise-client-urls http://${THIS_IP}:2379 --listen-client-urls http://0.0.0.0:2379 \
  --initial-cluster ${CLUSTER} \
  --initial-cluster-state ${CLUSTER_STATE} --initial-cluster-token ${TOKEN} >> log/${NAME_2}.log 2>&1 &
```

Paste the following in node 3 and press :q! to save the files:
```txt
#!/bin/bash
REGISTRY=quay.io/coreos/etcd
REGISTRY=gcr.io/etcd-development/etcd
ETCD_VERSION=v3.4.23
TOKEN=my-etcd-token
CLUSTER_STATE=new
NAME_1=etcd-node-0
NAME_2=etcd-node-1
NAME_3=etcd-node-2
HOST_1=67.205.137.130 # use your droplet 1's public IP
HOST_2=143.198.161.94 # use your droplet 2's public IP
HOST_3=143.198.162.212 # use your droplet 3's public IP
CLUSTER=${NAME_1}=http://${HOST_1}:2380,${NAME_2}=http://${HOST_2}:2380,${NAME_3}=http://${HOST_3}:2380
DATA_DIR=/var/lib/etcd

THIS_NAME=${NAME_3}
THIS_IP=${HOST_3}
docker run \
  -p 2379:2379 \
  -p 2380:2380 \
  --volume=${DATA_DIR}:/etcd-data \
  --name etcd ${REGISTRY}:${ETCD_VERSION} \
  /usr/local/bin/etcd \
  --data-dir=/etcd-data --name ${THIS_NAME} \
  --initial-advertise-peer-urls http://${THIS_IP}:2380 --listen-peer-urls http://0.0.0.0:2380 \
  --advertise-client-urls http://${THIS_IP}:2379 --listen-client-urls http://0.0.0.0:2379 \
  --initial-cluster ${CLUSTER} \
  --initial-cluster-state ${CLUSTER_STATE} --initial-cluster-token ${TOKEN} >> log/${NAME_3}.log 2>&1 &
```

```bash
$ chmod +x start.sh
$ ./start.sh
```

```txt
Your cluster is ready, run the following to test the cluster status
```

<br />

> **Step 3** - Setup etcdctl in local
```bash
$ sudo apt update
$ ETCD_VERSION=${ETCD_VERSION:-v3.4.23}

$ curl -L https://github.com/coreos/etcd/releases/download/$ETCD_VERSION/etcd-$ETCD_VERSION-linux-amd64.tar.gz -o etcd-$ETCD_VERSION-linux-amd64.tar.gz

$ tar xzvf etcd-$ETCD_VERSION-linux-amd64.tar.gz
$ rm etcd-$ETCD_VERSION-linux-amd64.tar.gz

$ cd etcd-$ETCD_VERSION-linux-amd64
$ sudo cp etcd /usr/local/bin/
$ sudo cp etcdctl /usr/local/bin/

$ rm -rf etcd-$ETCD_VERSION-linux-amd64

$ etcdctl --version
```

<br />

> **Step 4** - Check cluster health and member list

```bash
$ etcdctl --write-out=table --endpoints=$ENDPOINTS endpoint status
$ etcdctl --write-out=table --endpoints=$ENDPOINTS member list
```

<br />

## ✨ Setup msg_queue application


> **Step 1** - Setup the application
```bash
$ git clone https://github.com/naqibfaiyaz/msg_queue_etcd
$ sudo pip3 install virtualenv
$ virtualenv venv
$ source ./venv/bin/activate
$ sudo apt install libmysqlclient-dev
$ pip3 install -r requirements.txt
$ vi .env
```

```txt
paste the following environment variables and :q! to save:

FLASK_APP=run.py
FLASK_ENV=development
RANGE_START=0
RANGE_END=11
ETCD_HOST='67.205.137.130:2379,143.198.162.212:2379,143.198.161.94:2379,142.93.148.224:2379,142.93.151.80:2379' # use your droplet IPs
FILE_LOCATION='tmp/consumer.csv'
```

```bash
$ vi start.sh
```

```txt
paste the following and press :q! to save:

#!/bin/bash
docker-compose up --build > log.txt 2>&1 &
```

<br />

> **Step 2** - start the application
```bash
$ chmod +x start.sh
$ ./start.sh
```

```txt
APIs are up on the following endpoints

Producer: 
curl --location 'http://{{application_endpoint}}:2379/api/producer/execute'
Batch Producer: 
curl --location --request GET 'http://{{application_endpoint}}:2379/api/producer/execute/batch?batch_size=1000'
Watcher (need for consumer): 
curl --location --request GET 'http://{{application_endpoint}}:2379/api/prefix_watch' \
--form 'prefix="/msg/test_"'
```

<br />

## ✨ Setup benchmark tools

> **Step 1** - Install ab benchmark tool
```bash
$ apt-get install apache2-utils 
```
Visit `http://localhost:5085` in your browser. The app should be up & running.

<br />

> **Step 2** - ETCD benchmarking
```txt
Please follow ETCD documentation: https://etcd.io/docs/v3.4/op-guide/performance/#benchmarks
```

<br />

## ✨ Setup monitoring

> **Step 1** - ETCD Prometheus and Grafana
```txt
Please follow the documentation: https://etcd.io/docs/v3.1/op-guide/monitoring/
```

<br />

## ✨ Addtional commands, comes handy while running the benchmarkings

> Add new nodes:
```txt
While adding new nodes change the CLUSTER_STATE environment variable to 'existing' from 'new'

CLUSTER_STATE=existing

also run  rm -rf /var/lib/etcd if the node ran etcd previously
```

<br />

> Add and remove nodes from cluster

```bash
$ etcdctl --endpoints=$ENDPOINTS member add ${NAME_4} --peer-urls=http://${HOST_4}:2380
$ etcdctl --endpoints=$ENDPOINTS member remove 8e9f539e948d6de8
```

<br />

> compaction and defragmation
```bash
$ rev=$(ETCDCTL_API=3 etcdctl --endpoints=http://$HOST_1:2379 endpoint status --write-out="json" | egrep -o '"revision":[0-9]*' | egrep -o '[0-9].*')
$ ETCDCTL_API=3 etcdctl --endpoints=$ENDPOINTS compact $rev
$ ETCDCTL_API=3 etcdctl --endpoints=$ENDPOINTS defrag
$ etcdctl --write-out=table --endpoints=$ENDPOINTS endpoint status
```

<br />

## ✨ Code-base structure

The project is coded using blueprints and an intuitive structure presented bellow:

```bash
< PROJECT ROOT >
   |
   |-- apps/
   |    |
   |    |-- msg_queue/                      # A simple app that serves the routes
   |    |    |-- routes.py                  # Define app routes and functions
   |    |
   |    |-- static/
   |    |    |-- consumer.csv               # Used by the consumer if default location is used
   |    |
   |    __init__.py                         # Initialize the app
   |
   |-- requirements.txt                     # App Dependencies
   |
   |-- .env                                 # Inject Configuration via Environment
   |-- run.py                               # Start the app - WSGI gateway
   |
   |-- ************************************************************************
```

<br />
