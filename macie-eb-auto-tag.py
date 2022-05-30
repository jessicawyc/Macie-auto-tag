#针对从eventbridge过来的单条macie-finding 进行分析后对文件打自定义的tag
import json
import boto3
import os
s3 = boto3.client('s3')
typelist=[]
#把环境变量中设置的级别取出
tagkey=os.environ['tagkey']
dataclass=[]
for i in range(5):
    dataclass.append(os.environ[('level'+str(i))])
print(dataclass)
#判断现有标签的级别是否存在
def currenttag(filetag):
    oldlevel=0
    for each in filetag:
        if each['key']==tagkey:
            oldvalue=each['value']
            #为防止标签名称修改过找不到,就归0
            if oldvalue in dataclass:
                oldlevel=dataclass.index(oldvalue)
    return(oldlevel)

#标签定级分析,需要提前预置对应关系,并对原有标签进行比较,取较高者
datadic={"CREDIT_CARD_NUMBER":3,"USA_SOCIAL_SECURITY_NUMBER":1,"NAME":2,"ChineseID":3,"PHONE_NUMBER":4,"AWS_CREDENTIALS":2}
def taglevel(typelist,oldlevel):
    levels=[]
    for i in range(len(typelist)):
        if (typelist[i] in datadic.keys()):
            levels.append(datadic[typelist[i]])
            newlevel=max(oldlevel,max(levels))
            return(newlevel)
        else:
            return(0)
#给object打上标签
def tagobj(s3name,filename,tagkey,value):
    response = s3.put_object_tagging(
        Bucket=s3name,
        Key=filename,
        Tagging={
            'TagSet': [
                {
                    'Key': tagkey,
                    'Value': value
                }
            ]
        }
    )
    return response
    

def lambda_handler(event, context):
    #获得S3相关信息
    accountid = event["detail"]["accountId"]
    region = event["detail"]["region"]
    s3name = event["detail"]["resourcesAffected"]["s3Bucket"]["name"]
    s3tag = event["detail"]["resourcesAffected"]["s3Bucket"]["tags"] #need to check whether it is has classification tag already, list with dics
    filename = event["detail"]["resourcesAffected"]["s3Object"]["key"]
    filetag = event["detail"]["resourcesAffected"]["s3Object"]["tags"]
#获得敏感数据结果信息
    #自定义的扫描rule结果
    if event["detail"]["classificationDetails"]["result"]["customDataIdentifiers"]["totalCount"]>0:
        detectionlist=event["detail"]["classificationDetails"]["result"]["customDataIdentifiers"]["detections"] 
        for i in range(len(detectionlist)):
            if detectionlist[i]["name"] not in typelist:
                typelist.append(detectionlist[i]["name"])
    #managed rule结果获取
    findinglist=event["detail"]["classificationDetails"]["result"]["sensitiveData"]
    if len(findinglist)>0:
        for i in range(len(findinglist)):
            detectionlist=findinglist[i]["detections"]
            for j in range(len(detectionlist)):
                if detectionlist[j]["type"] not in typelist:
                    typelist.append(detectionlist[j]["type"])
    print(typelist)
#判断需要打上的标签的级别,原来的与新扫描出的结果,取最高
    oldlevel=currenttag(filetag)
    print('原有标签级别为:'+str(oldlevel))
    valuelevel=taglevel(typelist,oldlevel)
    value=dataclass[valuelevel]
#为S3中的obj打上对应的标签
    print('正在为S3:'+str(s3name)+'中的文件:'+str(filename)+'打上标签: '+str(valuelevel)+'级标签,'+str(value))
    result=tagobj(s3name,filename,tagkey,value)
    return (result)
