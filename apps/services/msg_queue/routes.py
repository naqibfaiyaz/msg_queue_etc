# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.services.msg_queue import blueprint
from flask import json, request, Response
# from flask_login import login_required
import etcd3, os.path
from csv import DictWriter, DictReader
import random, datetime

from apps import ETCD_HOST, ETCD_PORT, FILE_LOCATION

# @blueprint.route('/consumer/execute', methods=['GET', 'POST'])
# @login_required
def consumer(events):
    event=events.events[0]
    key = event.key.decode('utf-8')
    value = event.value.decode('utf-8')
    # print("You created the key " + key + " I was looking for with value " + value)
    # print(request.args.get('start'))
    # print(request.args.get('end'))
    # start=request.args.get('start') or RANGE_START
    # end=request.args.get('end') or RANGE_END
    # print(start)
    # print(end)
    # i=int(start)
    # chars = "".join( [random.choice(string.ascii_letters) for i in range(15)] )
    # values=[]
    fileName=FILE_LOCATION
    # # while i<=int(end):
    # key='test' + str(key)
    # print(value)
    # print(len(value))
    if len(value)>0:
        data={
            'key': key,
            'value': value
        }
        print("datetime" + str(datetime.datetime.now()) + "; consumer: " + json.dumps(data))
        # if(data['success']):
        #     # print(data)
        #     ##write to file
        appendToCSV(fileName, data)
    return deleteKey(key).data
    #     # if(deleteResponse['success']):
    #     #     values.append(data['data'])
    #     # else:
    #     #     values.append(data['data'])
    # i=i+1

    # print(values)

    # return Response(json.dumps({"total_consumed": len(values)}), content_type='application/json', status=200)

@blueprint.route('/producer/execute', methods=['GET', 'POST'])
# @login_required
def producer():
    # json_data=request.get_json()
    # if 'type' in json_data and json_data['type']=='msg_queue':
    #     if 'prefix' in json_data:
    #         prefix=json_data['prefix'] or '/msg/test_' 
    # else:
    #     prefix='/only_put/test_'

    prefix='/msg/test_' 
    
    # print(request.args.get('start'))
    # print(request.args.get('end'))
    # start=request.args.get('start') or RANGE_START
    # end=request.args.get('end') or RANGE_END
    # print(start)
    # print(end)
    # i=int(start)
    # # chars = "".join( [random.choice(string.ascii_letters) for i in range(15)] )
    # values=[]
    # # fileName='producer.csv'
    # # data = readCSV(fileName)
    
    # # if data['success']:
    # while i<=int(end):
    #     key='test' + str(i)
    #     value='Hello World ' + str(i)
    #     # key=row['key']
    #     # value=row['value']
        
    #     data=json.loads(putKey(key, value).data)
    #     print(data)
    #     if(data['success']):
    #         print(data)
    #         values.append(data['data'])

    #     i=i+1
    x=random.randint(0, 1000000)
    key=prefix + str(x)
    value='hello_' + str(x)
    data = {"key": key, "value": value}
    
    print("datetime" + str(datetime.datetime.now()) + "; producer: " + json.dumps(data))
    putKey(key, value)
    # print(values)
    # return "OK"
    return Response(json.dumps(data), content_type='application/json', status=200)

@blueprint.route('/producer/execute/batch', methods=['GET', 'POST'])
# @login_required
def batch_producer():
    batchSize=request.args.get('batch_size') or 1000
    print(batchSize)
    # json_data=request.get_json()
    # if 'type' in json_data and json_data['type']=='msg_queue':
    #     if 'prefix' in json_data:
    #         prefix=json_data['prefix'] or '/msg/test_' 
    # else:
    #     prefix='/only_put/test_'

    prefix='/msg/test_' 
    
    # print(request.args.get('start'))
    # print(request.args.get('end'))
    # start=request.args.get('start') or RANGE_START
    # end=request.args.get('end') or RANGE_END
    # print(start)
    # print(end)
    # i=int(start)
    # # chars = "".join( [random.choice(string.ascii_letters) for i in range(15)] )
    # values=[]
    # # fileName='producer.csv'
    # # data = readCSV(fileName)
    i=0
    dataArr=[]
    # # if data['success']:
    while i<=int(batchSize):
        x=random.randint(0, 1000000)
        key=prefix + str(x)
        value='hello_' + str(x)
        data = {"key": key, "value": value}
        # key=row['key']
        # value=row['value']
        
        print("producer: " + json.dumps(data))
        putKey(key, value)
        dataArr.append(data)
        i=i+1
    
    # print(values)
    # return "OK"
    return Response(json.dumps(data), content_type='application/json', status=200)

@blueprint.route('/watch/<key>', methods=['GET', 'POST'])
def watchKey(prefix):
    prefix=prefix or request.args.get('prefix')
    etcd=etcdClient()
    return etcd.watch_prefix(prefix)

@blueprint.route('/get/<key>', methods=['GET', 'POST'])
# @login_required
def getKey(key):
    etcd=etcdClient()
    
    response=etcd.get(key)
    
    if response[0]:
        data=response[0].decode("utf-8")
        status=200
        success=True
    else:
        data=None
        status=404
        success=False

    return Response(json.dumps({"success": success, "data": {"key":key, "value": data}}), content_type='application/json', status=status)

@blueprint.route('/delete/<key>', methods=['GET', 'POST'])
# @login_required
def deleteKey(key):
    etcd=etcdClient()
    
    response=etcd.delete(key)

    if response:
        data="Key has been Deleted"
        status=200
        success=True
    else:
        data="Key does not exist"
        status=404
        success=False

    return Response(json.dumps({'success': success, 'data': {"key": key, "value": data} }), content_type='application/json', status=status)


@blueprint.route('/put', methods=['POST'])
# @login_required
def putKey(key=None, value=None):
    key=key or request.form.get('key')
    value=value or request.form.get('value')
    etcd=etcdClient()

    response=etcd.put(key, value)
    return response
    # if response:
    #     data=value
    #     status=200
    #     success=True
    # else:
    #     data="Something went wrong"
    #     status=404
    #     success=False

    # return Response(json.dumps({'success': success, 'data': {"key": key, "value": data} }), content_type='application/json', status=status)

def etcdClient():
    hosts=ETCD_HOST
    
    for host in hosts:
        endpoint=host.split(':')
        host=endpoint[0]
        port=endpoint[1]
        print(endpoint)
        try:
            conn=etcd3.client(host=host, port=port)
            status=conn.status()
            
            return conn
        except Exception as e:
            if str(e)=='etcd connection failed':
                continue
            else:
                return {'success': False, 'msg': 'Connection Failed'}

def appendToCSV(fileName, data):
    field_names = ['key', 'value']
    file_size=0
    if os.path.exists(fileName):
        file_size = os.path.getsize(fileName)
        # print(file_size)
    # Open CSV file in append mode
    # Create a file object for this file
    try:
        f = open(fileName, 'a', newline='')
    except OSError as error:
        print("Could not open/read file:", fileName)
        print(error)
        return error
    
    with f as f_object:
        # print(f_object)
        # print(os.path.abspath(fileName))
        # Pass the file object and a list
        # of column names to DictWriter()
        # You will get a object of DictWriter
        dictwriter_object = DictWriter(f_object, fieldnames=field_names)
        if file_size==0:
            dictwriter_object.writeheader()  # file doesn't exist yet, write a header
        # Pass the dictionary as an argument to the Writerow()
        dictwriter_object.writerow(data)
        # print(write)
    
        # Close the file object
        f_object.close()


def readCSV(fileName):
    field_names = ['key', 'value']
    data=[]
    # Open CSV file in read mode
    with open(fileName, 'r') as f_object:
    
        # Pass the file object to DictReader()
        # You will get a object of DictReader
        input_file = DictReader(f_object, fieldnames=field_names)
        next(input_file)
        # Pass the dictionary as an argument to the Writerow()
        for row in input_file:
            data.append(row)
    
        # Close the file object
        f_object.close()

    if row:
        return {
            "success": True,
            "data": data
                }
    else:
        return {
            "success": False,
            "data": "No Data Available"
                }

@blueprint.route('/prefix_watch/', methods=['GET', 'POST'])
def define_watcher(prefixes=None):
    prefix=prefixes or request.form.get('prefix')
    etcd=etcdClient()
    print("datetime" + str(datetime.datetime.now()) + "; prefix:" + prefix)
    
    watch_data=etcd.add_watch_prefix_callback(prefix, consumer)
    # watch_data=etcd.watch_prefix("/msg/test_1")
    return  Response(json.dumps(watch_data), content_type='application/json', status=200)

@blueprint.route('/cancel_watch/', methods=['GET', 'POST'])
def define_cancel_watcher(id=None):
    watch_id=id or request.form.get('watch_id')
    etcd=etcdClient()
    # print(watch_id)
    watch_data=etcd.cancel_watch(watch_id)
    # watch_data=etcd.watch_prefix("/msg/test_1")
    return  Response(json.dumps(watch_data), content_type='application/json', status=200)

