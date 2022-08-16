# 2 Ways to tag S3 Object with customized sensitive label based on Macie Finding


可以在lambda环境变量中自定数据的保密级别 Define custome label in lambda's enviroment variables
![snapshot](https://github.com/jessicawyc/Macie-auto-tag/blob/main/macie-define-level.png)
There are two architecture to acheive the automatically tagging action:
可以采用以下两种架构实现:
lambda代码请下载:index.zip
直接通过Eventbridge的方式: [macie-eb-auto-tag.py](https://github.com/jessicawyc/Macie-auto-tag/blob/main/macie-eb-auto-tag.py)
![diagram](https://github.com/jessicawyc/Macie-auto-tag/blob/main/maci-auto-tag-architect.png)


## 方案1 Architecture 1 Create eventbridge rule to automatically trigger tagging after Macie generates sensitive data finding
## Cloudformation
Run the template in each region to deploy
##CLI
### 参数设置
```
regions=($(aws ec2 describe-regions --query 'Regions[*].RegionName' --region=us-east-1 --output text))
rulename='macierule'
```
### 运行CLI命令
```
for region in $regions; do
rulearn=$(aws events put-rule  --name $rulename  --event-pattern "{\"source\": [\"aws.macie\"],\"detail-type\": [\"Macie Finding\"]}" --region=$region --query 'RuleArn' --output text)
echo $rulearn
echo $region
done
```
## 方案2 Architecture 2 Create Securityhub custom action to manually trigger tagging 从Securityhub通过手动方式发送
To be continued
