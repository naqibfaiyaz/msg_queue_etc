# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.services.etcd_cluster_mgnt import blueprint
from flask import render_template, json, request, jsonify, Response, redirect
# from flask_login import login_required
import etcd3, os.path
from csv import DictWriter, DictReader

from apps import RANGE_START, RANGE_END, ETCD_HOST, ETCD_PORT

@blueprint.route('/members', methods=['GET', 'POST'])
# @login_required
def getMembers():
    etcd=etcdClient()
    members = etcd.members
    memList=[]

    for member in members:
        # print(member.id)
        memList.append({
            "id": member.id,
            "name": member.name,
            "peer_url": member.peer_urls[0],
            "client_url": member.client_urls[0]
        })

    print(memList)

    return Response(json.dumps({"Current Members": memList}), content_type='application/json', status=200)

@blueprint.route('/remove', methods=['POST'])
def removeMembers(member_id=None):
    member_id=member_id or request.form.get('id')
    etcd=etcdClient()

    try:
        response = etcd.remove_member(int(member_id))
        print(response)
        # print(memList)

        return Response(json.dumps({"msg": "member removed"}), content_type='application/json', status=200)
    except Exception as e:
        print(e)
        return Response(json.dumps({"msg": "Member not found"}), content_type='application/json', status=404)

@blueprint.route('/add', methods=['POST'])
def addMembers(url=None):
    url=url or request.form.get('url')
    etcd=etcdClient()
    
    url=[url]
    try:
        members = etcd.add_member('http://10.0.0.87:2380')
        print(members)
        memList=[]

        # memList.append({
        #     "id": member.id,
        #     "name": member.name,
        #     "peer_url": member.peer_urls[0],
        #     "client_url": member.client_urls[0]
        # })
        # print(memList)

        return Response(json.dumps({"msg": "Member Added"}), content_type='application/json', status=200)
    except Exception as e:
        print(e)
        return Response(json.dumps({"msg": "Member not found"}), content_type='application/json', status=404)

@blueprint.route('/leader', methods=['GET', 'POST'])
def getLeader():
    etcd=etcdClient()

    return Response(json.dumps({
            "id": etcd.status().leader.id,
            "name": etcd.status().leader.name,
            "peer_url": etcd.status().leader.peer_urls[0],
            "client_url": etcd.status().leader.client_urls[0]
        }), content_type='application/json', status=200)

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
            print(status)
            return conn
        except Exception as e:
            if str(e)=='etcd connection failed':
                continue
            else:
                return {'success': False, 'msg': 'Connection Failed'}
