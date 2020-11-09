from django.shortcuts import render, redirect
from . import models, forms
from .models import *

import hashlib,json,requests,time, datetime

from collections import Counter
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

import logging
from django.views.generic import View

errcode = {
    '0':'请求成功',
    '-1':'系统错误',
    '-1000':'系统错误',
    '40014':'AccessToken不合法',
    '40097':'请求参数错误',
    '40101':'缺少必填参数',
    '41001':'缺少AccessToken',
    '42001':'AccessToken过期',
    '43002':'HTML Method错误',
    '44002':'POST Body为空',
    '47001':'POST Body格式错误',
    '85088':'该APP未开通云开发',
    '-401001':'SDK 通用错误：无权限使用 API',
    '-401002':'SDK 通用错误：API 传入参数错误',
    '-401003':'SDK 通用错误：API 传入参数类型错误',
    '-402001':'SDK 数据库错误：检测到循环引用',
    '-402002':'SDK 数据库错误：初始化监听失败',
    '-402003':'SDK 数据库错误：重连 WebSocket 失败',
    '-402004':'SDK 数据库错误：重建监听失败',
    '-402005':'SDK 数据库错误：关闭监听失败',
    '-402006':'SDK 数据库错误：收到服务器错误信息',
    '-402007':'SDK 数据库错误：从服务器收到非法数据',
    '-402008':'SDK 数据库错误：WebSocket 连接异常',
    '-402009':'SDK 数据库错误：WebSocket 连接断开',
    '-402010':'SDK 数据库错误：检查包序失败',
    '-402011':'SDK 数据库错误：未知异常',
    '-501001':'云资源通用错误：云端系统错误',
    '-403001':'SDK 文件存储错误：上传的文件超出大小上限',
    '-404001':'SDK 云函数错误：云函数调用内部失败：空回包',
    '-404002':'SDK 云函数错误：云函数调用内部失败：空 eventid',
    '-404003':'SDK 云函数错误：云函数调用内部失败：空 pollurl',
    '-404004':'SDK 云函数错误：云函数调用内部失败：空 poll 结果 json',
    '-404005':'SDK 云函数错误：云函数调用失败：超出最大正常结果轮询尝试次数',
    '-404006':'SDK 云函数错误：云函数调用内部失败：空 base resp',
    '-404007':'SDK 云函数错误：云函数调用失败：baseresponse.errcode 非 0',
    '-404008':'SDK 云函数错误：云函数调用失败：v1 轮询状态码异常',
    '-404009':'SDK 云函数错误：云函数调用内部失败：轮询处理异常',
    '-404010':'SDK 云函数错误：云函数调用失败：轮询结果已超时过期1',
    '-404011':'SDK 云函数错误：云函数调用失败：函数执行失败',
    '-404012':'SDK 云函数错误：云函数调用失败：超出最大轮询超时后尝试次数2',
    '-40400x':'SDK 云函数错误：云函数调用失败',
    '-404011':'SDK 云函数错误：云函数执行失败',
    '-501002':'云资源通用错误：云端响应超时',
    '-501003':'云资源通用错误：请求次数超出环境配额',
    '-501004':'云资源通用错误：请求并发数超出环境配额',
    '-501005':'云资源通用错误：环境信息异常',
    '-501007':'云资源通用错误：参数错误',
    '-501009':'云资源通用错误：操作的资源对象非法或不存在',
    '-501015':'云资源通用错误：读请求次数配额耗尽',
    '-501016':'云资源通用错误：写请求次数配额耗尽',
    '-501017':'云资源通用错误：磁盘耗尽',
    '-501018':'云资源通用错误：资源不可用',
    '-501019':'云资源通用错误：未授权操作',
    '-501020':'云资源通用错误：未知参数错误',
    '-501021':'云资源通用错误：操作不支持',
    '-502001':'云资源数据库错误：数据库请求失败',
    '-502002':'云资源数据库错误：非法的数据库指令',
    '-502003':'云资源数据库错误：无权限操作数据库',
    '-502005':'云资源数据库错误：集合不存在',
    '-502010':'云资源数据库错误：操作失败',
    '-502011':'云资源数据库错误：操作超时',
    '-502012':'云资源数据库错误：插入失败',
    '-502013':'云资源数据库错误：创建集合失败',
    '-502014':'云资源数据库错误：删除数据失败',
    '-502015':'云资源数据库错误：查询数据失败',
    '-503001':'云资源文件存储错误：云文件请求失败',
    '-503002':'云资源文件存储错误：无权限访问云文件',
    '-503003':'云资源文件存储错误：文件不存在',
    '-503003':'云资源文件存储错误：非法签名',
    '-504001':'云资源云函数错误：云函数调用失败',
    '-504002':'云资源云函数错误：云函数执行失败',
    '-601001':'微信后台通用错误：系统错误',
    '-601002':'微信后台通用错误：系统参数错误',
    '-601003':'微信后台通用错误：系统网络错误',
    '-601004':'微信后台通用错误：API 无权限',
    '-601005':'微信后台通用错误：非法 cloudID',
    '-601006':'微信后台通用错误：cloudID 已过期',
    '-601007':'微信后台通用错误：cloudID 和当前用户不匹配',
    '-601008':'微信后台通用错误：服务端内部请求超时',
    '-601009':'微信后台通用错误：账号缺少手机号',
    '-601010':'微信后台通用错误：缺少写权限',
    '-601011':'微信后台通用错误：无权限',
    '-601012':'微信后台通用错误：无权限访问该环境',
    '-601013':'微信后台通用错误：没有多端/跨账号权限',
    '-601015':'微信后台通用错误：拒绝访问（cloudbase_auth 函数返回空 errCode）',
    '-601016':'微信后台通用错误：拒绝访问（无环境 auth 信息）',
    '-601017':'微信后台通用错误：拒绝访问（cloudbase_auth 函数返回非 0 errCode）',
    '-601018':'微信后台通用错误：未授权的 API',
    '-604001':'微信后台云函数错误：回包大小超过 1M',
    '-604100':'微信后台云函数错误：API 不存在',
    '-604101':'微信后台云函数错误：无权限调用此 API',
    '-604102':'微信后台云函数错误：调用超时',
    '-604103':'微信后台云函数错误：云调用系统错误',
    '-604104':'微信后台云函数错误：非法调用来源',
    '-604101':'微信后台云函数错误：调用系统错误',
    '-605101':'微信后台 HTTP API 错误：查询语句解析失败'
}
appid = ''
secret = ''
env = ''

def getAccessToken(appid,secret):

    addr = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid='+appid+'&secret='+secret
    data = requests.session().get(addr).text#get/post

    #print(data)
    data = json.loads(data)
    access_token = data['access_token']
    return access_token

#查询数据库
def databaseQuery(access_token,env,query):

    data0={
        'env':env,
        'query':query
    }
    addr1 = 'https://api.weixin.qq.com/tcb/databasequery?access_token=' + access_token
    jsObject={}
    try:
        Object = requests.session().post(addr1,data=json.dumps(data0)).text
        jsObject = json.loads(Object)
    except Exception as e:
        print("e:", e)
        pass
    return jsObject


#更新数据库
def databaseUpdate(access_token,env,query):

    data0={
        'env':env,
        'query':query
    }
    addr1 = 'https://api.weixin.qq.com/tcb/databaseupdate?access_token=' + access_token
    try:
        Object = requests.session().post(addr1,data=json.dumps(data0)).text
        jsObject = json.loads(Object)
    except Exception as e:
        print("e:", e)
        pass


class deal(View):  # 核心! 处理url

    def __init__(self):
        pass

    def __del__(self):
        pass

    def get(self, request, **kwargs):
        first = kwargs.get('first')     # 类别(wechat)
        mid = kwargs.get('mid')         # 机器码
        fun = kwargs.get('function')    # 更新的项目
        value = kwargs.get('value')  # 数据值
        json = kwargs.get('json')     # 数据值

        print('get', first, mid, fun, value, json)

        if (first == 'DIODE'):  #http://106.12.142.179:8080/DIODE/2020/10/29/(json)
            
            if (json == 'json'):  #这三个判断返回数据json
                data = []
                if (mid == 'Week' or mid == 'lastWeek'):  #周榜
                    if (mid == 'Week'):
                        day = [datetime.date.today(), 0, 0, 0, 0, 0, 0]
                        one_day = datetime.timedelta(days=1)
                    else:
                        day = [datetime.date.today()-datetime.timedelta(days=7), 0, 0, 0, 0, 0, 0]
                        one_day = datetime.timedelta(days=1)

                    while day[0].weekday() != 0:
                        day[0] -= one_day
                    for num in range(1,7):
                        day[num] = day[0]+one_day*num

                    bigdata = []
                    bigtotal = {"标准时长":54000}
                    for num in range(0, 7):
                        t=day[num].strftime('%Y/%m/%d')
                        query_get = 'db.collection(\"check_in\").doc(\"' + str(t) + '\").get()'
                        access_token = getAccessToken(appid, secret)  #数据库操作前必做
                        jsondata = databaseQuery(access_token, env, query_get)
                        if (jsondata == {} or jsondata['data']==[]):
                            continue
                        jsondata = dict(jsondata)
                        jsondata = jsondata['data']
                        null=''
                        datadata = eval(jsondata[0])
                        counts = Counter(datadata['list'])
                        for i in counts:
                            if (counts[i][2] == null or counts[i][3] == null):
                                continue
                            

                            a1 = int(counts[i][2]) / 1000
                            timeArray = time.localtime(a1)
                            otherStyleTime1 = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                            
                            a2 = int(counts[i][3]) / 1000
                            timeArray = time.localtime(a2)
                            otherStyleTime2 = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                            
                            total = a2 - a1
                            if (i in bigtotal):
                                bigtotal[i] = bigtotal[i] + total
                            else:
                                bigtotal[i] = total
                    bigtotal = sorted(bigtotal.items(), key = lambda kv:(kv[1], kv[0]),reverse=True)
                    #print(bigtotal)
                    for i in bigtotal:
                    
                        total = i[1]
                        if (total >= 54000):
                            continue
                        m, s = divmod(total,60)
                        h, m = divmod(m, 60)
                        total=str(int(h))+'时'+str(int(m))+'分'+str(s)+'秒'
                        temp = {
                            'id': 0,
                            "name": i[0],
                            'start':'',
                            'end': '',
                            'total': total,
                        }
                        data.append(temp)

                    return JsonResponse(data, safe=False)
                        
                    
                elif (mid == 'All'):  #总榜
                    #TODO:理论上每周的结束，需要把旧一周的记录丢进database里，然后设定查询的周数在本地数据库找数据
                    return JsonResponse([{'id':0,'name':'太费劲了','start':"有空就做？",'end':"一定不咕！",'total':"time->∞"}], safe=False)
                else:  #日期
                    
                    t=mid+'/'+ fun+'/'+ value
                    query_get = 'db.collection(\"check_in\").doc(\"' + str(t) + '\").get()'
                    access_token = getAccessToken(appid, secret)  #数据库操作前必做
                    jsondata = databaseQuery(access_token, env, query_get)
                    jsondata = dict(jsondata)
                    jsondata = jsondata['data']
                    null=''
                    datadata = eval(jsondata[0])
                    counts = Counter(datadata['list'])
                    j=0
                    for i in counts:
                        if (counts[i][2] == null):
                            otherStyleTime1 = '-'
                            total = '-'
                        else:
                            a1 = int(counts[i][2]) / 1000
                            timeArray = time.localtime(a1)
                            otherStyleTime1 = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

                        if (counts[i][3] == null):
                            otherStyleTime2 = '-'
                            total = '-'
                        else:
                            a2 = int(counts[i][3]) / 1000
                            timeArray = time.localtime(a2)
                            otherStyleTime2 = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                        if (counts[i][2] != null and counts[i][3] != null):
                            total = a2 - a1
                            m, s = divmod(total,60)
                            h, m = divmod(m, 60)
                            total=str(int(h))+'时'+str(int(m))+'分'+str(s)+'秒'
                        temp = {
                            'id': j,
                            "name": i,
                            'start':otherStyleTime1,
                            'end': otherStyleTime2,
                            'total': total,
                        }
                        data.append(temp)
                        j = j + 1
                    data.sort(key=lambda x: x['start'])
                    return JsonResponse(data, safe=False)
            
            else:#这返回网页

                return render(request, 'login/base_diode_show.html', locals())
                #return HttpResponse(json.dumps({'status': 'success'}))

        else:
            return HttpResponse(json.dumps({'status': 'fail'}))
        

    def post(self, request, **kwargs):
        first = kwargs.get('first')     # 类别(wechat)
        mid = kwargs.get('mid')         # 机器码
        fun = kwargs.get('function')    # 更新的项目
        value = kwargs.get('value')  # 数据值
        dele = kwargs.get('json')     # 数据值

        print('post', first, mid, fun, value, dele)
        if (first == 'DIODE'):
            if(dele == 'delete'):
                json_receive = json.loads(request.body)
                json_receive = json_receive[0]
                d2 = datetime.datetime.strptime(json_receive['end'], '%Y-%m-%d %H:%M:%S')
                d1 = datetime.datetime.strptime(json_receive['start'], '%Y-%m-%d %H:%M:%S')
                
                if ((d2 - d1).total_seconds() < 300):
                    
                    
                    t = mid + '/' + fun + '/' + value
                    
                    query_get = 'db.collection(\"check_in\").doc(\"' + str(t) + '\").get()'
                    access_token = getAccessToken(appid, secret)  #数据库操作前必做
                    getpredata = databaseQuery(access_token, env, query_get)
                    getpredata = dict(getpredata)
                    getpredata = getpredata['data']
                    
                    null = None
                    getpredata = eval(getpredata[0])
                    
                    getpredata['list'][json_receive['name']][1] = null
                    getpredata['list'][json_receive['name']][3] = null

                    data = str(getpredata['list']).replace('None', 'null')
                    query_upd = 'db.collection(\"check_in\").doc(\"' + str(t) + '\").update({data:{list:' + data + '}})'
                    
                    databaseUpdate(access_token, env, query_upd)
                    return HttpResponse(json.dumps({'status': 'success'}))

                return HttpResponse(json.dumps({'status': 'authority_check0'}))