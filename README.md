# Macie-auto-tag
after macie scan for sensitive information, using lambda to automatically tag S3 object based on customized label
可以采用以下两种架构实现:
lambda代码请下载:
直接通过Eventbridge的方式: [macie-eb-auto-tag.py] (https://github.com/jessicawyc/Macie-auto-tag/blob/main/macie-eb-auto-tag.py)
![diagram](https://github.com/jessicawyc/Macie-auto-tag/blob/main/maci-auto-tag-architect.png)

从Securityhub通过手动方式发送:macie-sh-auto-tag.py
