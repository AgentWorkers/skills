---
name: jenkins
description: 通过 API 管理 Jenkins 作业、构建过程以及流水线（pipelines）。触发构建并监控其状态。
metadata: {"clawdbot":{"emoji":"🔧","requires":{"env":["JENKINS_URL","JENKINS_USER","JENKINS_TOKEN"]}}}
---
# Jenkins  
CI/CD自动化服务器。  

## 环境配置  
```bash
export JENKINS_URL="https://jenkins.example.com"
export JENKINS_USER="admin"
export JENKINS_TOKEN="xxxxxxxxxx"
```  

## 作业列表  
```bash
curl -u "$JENKINS_USER:$JENKINS_TOKEN" "$JENKINS_URL/api/json?tree=jobs[name,color]"
```  

## 触发构建  
```bash
curl -X POST -u "$JENKINS_USER:$JENKINS_TOKEN" "$JENKINS_URL/job/{jobName}/build"
```  

## 获取构建状态  
```bash
curl -u "$JENKINS_USER:$JENKINS_TOKEN" "$JENKINS_URL/job/{jobName}/lastBuild/api/json"
```  

## 链接  
- 文档：https://www.jenkins.io/doc/book/using/remote-access-api/