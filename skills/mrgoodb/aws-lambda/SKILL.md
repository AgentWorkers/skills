---
name: aws-lambda
description: 通过 AWS CLI/API 管理 AWS Lambda 函数。部署、调用并监控无服务器函数。
metadata: {"clawdbot":{"emoji":"λ","requires":{"env":["AWS_ACCESS_KEY_ID","AWS_SECRET_ACCESS_KEY","AWS_REGION"]}}}
---
# AWS Lambda  
无服务器计算服务。  

## 环境配置  
```bash
export AWS_ACCESS_KEY_ID="xxxxxxxxxx"
export AWS_SECRET_ACCESS_KEY="xxxxxxxxxx"
export AWS_REGION="us-east-1"
```  

## 列出所有函数  
```bash
aws lambda list-functions
```  

## 调用函数  
```bash
aws lambda invoke --function-name myFunction --payload '{"key": "value"}' output.json
```  

## 创建新函数  
```bash
aws lambda create-function --function-name myFunction \
  --runtime nodejs18.x --handler index.handler \
  --role arn:aws:iam::123456789:role/lambda-role \
  --zip-file fileb://function.zip
```  

## 更新函数代码  
```bash
aws lambda update-function-code --function-name myFunction --zip-file fileb://function.zip
```  

## 获取函数日志  
```bash
aws logs tail /aws/lambda/myFunction --follow
```  

## 链接  
- 控制台：https://console.aws.amazon.com/lambda  
- 文档：https://docs.aws.amazon.com/lambda