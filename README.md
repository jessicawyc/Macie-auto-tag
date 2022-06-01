# Macie-auto-tag
after macie scan for sensitive information, using lambda to automatically tag S3 object based on customized label
可以在lambda环境变量中自定数据的保密级别
![snapshot](https://github.com/jessicawyc/Macie-auto-tag/blob/main/macie-define-level.png)
可以采用以下两种架构实现:
lambda代码请下载:
直接通过Eventbridge的方式: [macie-eb-auto-tag.py](https://github.com/jessicawyc/Macie-auto-tag/blob/main/macie-eb-auto-tag.py)
![diagram](https://github.com/jessicawyc/Macie-auto-tag/blob/main/maci-auto-tag-architect.png)

从Securityhub通过手动方式发送:macie-sh-auto-tag.py
## create eventbridge
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
