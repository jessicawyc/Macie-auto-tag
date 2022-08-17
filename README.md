# 2 Ways to tag S3 Object automatically with customized sensitive label based on Macie Finding
There are two architecture to acheive the automatically tagging action:
可以采用以下两种架构实现:
lambda代码请下载:index.zip
直接通过Eventbridge的方式: [macie-eb-auto-tag.py](https://github.com/jessicawyc/Macie-auto-tag/blob/main/macie-eb-auto-tag.py)
![diagram](https://github.com/jessicawyc/Macie-auto-tag/blob/main/maci-auto-tag-architect.png)
##  Variables Instructions
### Step 1 Define custom labels
可以在lambda环境变量中自定数据的保密级别 Define custome label in lambda's enviroment variables
![snapshot](https://github.com/jessicawyc/Macie-auto-tag/blob/main/macie-define-level.png)

### Step 2 Define identifier mapping with label level 
Download the file [mapping.json](/mapping.json), change the numbers for each identifier you use, for custome identifier,just add Key Value pair in the file.
Then upload the json file into a S3 bucket, input the s3 name and file name in lambda's enviroment variables
## Deployment
## 方案1 Architecture 1 
Deploy Template either in console or with below CLI command for mutiple regions
Set Parameter
```
stackname=macieautotag2ways
regions=($(aws ec2 describe-regions --query 'Regions[*].RegionName' --output text))
```
Run Cloudformation template in all regions
```
for region in $regions; do
aws cloudformation create-stack --stack-name $stackname --template-body file://Arch1-template.yaml \
--parameters  \
ParameterKey=level0,ParameterValue=public  \
ParameterKey=level1,ParameterValue=internal  \
ParameterKey=level2,ParameterValue=sensitive  \
ParameterKey=level3,ParameterValue=topsecret  \
ParameterKey=tagkey,ParameterValue=datalevel  \
ParameterKey=s3bucketname,ParameterValue=maciemappingbucket  \
ParameterKey=s3filepath,ParameterValue=mapping.json \
--capabilities CAPABILITY_IAM \
--region=$region
echo $region
done
```

## 方案2 Architecture 2 
Create Securityhub custom action to manually trigger tagging 从Securityhub通过手动方式发送
Only need to deploy one lambda and eventbridge rule in the aggregated region.
Need to create a custom action to send macie finding to eventbridge
### Step 1 Create Custom Action in Security Hub
Set Paramter
```
name='autotags3'
region=eu-west-3
description='trigger lambda to tag s3 object based on self-defined label'
id='tag'
```
Run CLI Command to create resources
```
caarn=$(aws securityhub create-action-target \
    --name $name\
    --description $description \
    --id $id --region=$region --query 'ActionTargetArn' --output text)
echo $caarn
```
The output will be the custom action's arn,like below:

```
arn:aws:securityhub:<region>:<accountid>:action/custom/tag
```
### Step 2 Create Eventbridge Rule and Lambda

Run Cloudformation template in only the aggregated region of security hub.
### CLI command
The command is quite similiar, make sure you use the right yaml file.
Set Parameter
```
stackname=sechub-macie-autotag
region=eu-west-2
```
Run CLI command to create a cloudformation stack
```
aws cloudformation create-stack --stack-name $stackname --template-body file://Arch2-sechub-template.yaml \
--parameters  \
ParameterKey=customactionarn,ParameterValue=$caarn  \
ParameterKey=level0,ParameterValue=public  \
ParameterKey=level1,ParameterValue=internal  \
ParameterKey=level2,ParameterValue=sensitive  \
ParameterKey=level3,ParameterValue=topsecret  \
ParameterKey=tagkey,ParameterValue=datalevel  \
ParameterKey=s3bucketname,ParameterValue=maciemappingbucket  \
ParameterKey=s3filepath,ParameterValue=mapping.json \
--capabilities CAPABILITY_IAM \
--region=$region
```
If the Output looks like this, you successully create the stack and wait until it finish running.
```
{
    "StackId": "arn:aws:cloudformation:<region>:<accountid>:stack/sechub-macie-autotag/1cc659a0-1de9-11ed-a006-069cbc938d24"
}
```
#### Console way
If you choose to create cloudformation stack in aws console. The output from CLI in last step of the custom action, is the first paramter you will input into the stack.
