---
name: heroku
description: 通过 CLI（命令行界面）和 API（应用程序编程接口）来管理 Heroku 应用程序、动态服务器（dynos）以及插件。实现应用程序的部署和扩展（即调整应用程序的运行规模）。
metadata: {"clawdbot":{"emoji":"🟣","requires":{"env":["HEROKU_API_KEY"]}}}
---
# Heroku  
一种平台即服务（Platform as a Service）的解决方案。  

## 环境配置  
```bash
export HEROKU_API_KEY="xxxxxxxxxx"
```  

## 命令行界面（CLI）命令  
```bash
heroku apps
heroku create app-name
heroku logs --tail -a app-name
heroku ps -a app-name
heroku ps:scale web=1 -a app-name
heroku config -a app-name
heroku config:set KEY=value -a app-name
```  

## API  
- **列出应用程序（List Apps）**：  
```bash
curl "https://api.heroku.com/apps" \
  -H "Authorization: Bearer $HEROKU_API_KEY" \
  -H "Accept: application/vnd.heroku+json; version=3"
```  
- **重启 Dyno 服务器（Restart Dynos）**：  
```bash
curl -X DELETE "https://api.heroku.com/apps/{app}/dynos" \
  -H "Authorization: Bearer $HEROKU_API_KEY" \
  -H "Accept: application/vnd.heroku+json; version=3"
```  

## 链接  
- **控制面板（Dashboard）**：https://dashboard.heroku.com  
- **文档（Documentation）**：https://devcenter.heroku.com/articles/platform-api-reference