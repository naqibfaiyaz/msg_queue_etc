# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.services.msg_queue import blueprint
from flask import render_template, json, request, jsonify, Response, redirect
# from flask_login import login_required
import etcd3, os.path
from csv import DictWriter, DictReader
import random
import string

from apps import ETCD_HOST, ETCD_PORT

@blueprint.route('/index')
# @login_required
def RedirectIndex():
    return index()

@blueprint.route('/')
# @login_required
def index():
    return render_template('home/index.html', segment='index')

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
    fileName='consumer' + '.csv'
    # # while i<=int(end):
    # key='test' + str(key)
    data={
        'key': key,
        'value': value
    }
    print(data)
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
    key='/list/test_' + str(x)
    value='hello_' + str(x)
    print(key, value)
    putKey(key, value)
    # print(values)
    # return "OK"
    return Response(json.dumps({"key": key, "value": value}), content_type='application/json', status=200)

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
    # Open CSV file in append mode
    # Create a file object for this file
    with open(fileName, 'a', newline='') as f_object:
    
        # Pass the file object and a list
        # of column names to DictWriter()
        # You will get a object of DictWriter
        dictwriter_object = DictWriter(f_object, fieldnames=field_names)
        if file_size==0:
            dictwriter_object.writeheader()  # file doesn't exist yet, write a header
        # Pass the dictionary as an argument to the Writerow()
        dictwriter_object.writerow(data)
    
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
    
etcd=etcdClient()
etcd.add_watch_prefix_callback("/list/test_", consumer)
# watch_data=etcd.watch_prefix("/list/test_1")
# print(watch_data)