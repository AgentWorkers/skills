---
name: bitbucket
description: 通过 API 管理 Bitbucket 仓库、拉取请求（pull requests）以及持续集成/持续部署（pipelines）流程。
metadata: {"clawdbot":{"emoji":"🪣","requires":{"env":["BITBUCKET_USERNAME","BITBUCKET_APP_PASSWORD"]}}}
---
# Bitbucket  
用于托管 Git 仓库的工具。  

## 环境配置  
```bash
export BITBUCKET_USERNAME="xxxxxxxxxx"
export BITBUCKET_APP_PASSWORD="xxxxxxxxxx"
```  

## 列出仓库  
```bash
curl -u "$BITBUCKET_USERNAME:$BITBUCKET_APP_PASSWORD" "https://api.bitbucket.org/2.0/repositories/$BITBUCKET_USERNAME"
```  

## 创建拉取请求（Pull Request）  
```bash
curl -X POST -u "$BITBUCKET_USERNAME:$BITBUCKET_APP_PASSWORD" \
  "https://api.bitbucket.org/2.0/repositories/{workspace}/{repo}/pullrequests" \
  -H "Content-Type: application/json" \
  -d '{"title": "Feature PR", "source": {"branch": {"name": "feature"}}, "destination": {"branch": {"name": "main"}}}'
```  

## 链接  
- 文档：https://developer.atlassian.com/cloud/bitbucket/rest