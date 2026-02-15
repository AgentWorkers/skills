---
name: omadeus
description: 通过 Omadeus REST API 管理 Omadeus 实体。
homepage: https://omadeus.com/
metadata: {"clawdbot":{"emoji":"📋"}}
---
# Omadeus Skill

直接通过Clawdbot管理Omadeus实体。

## 使用方法

所有命令均使用`curl`来调用Omadeus的REST API。

### 列出实体
```bash
curl -X LIST -s "https://milestone.xeba.ir/dolphin/apiv1/nuggetviews?take=25&zone=inbox&kind=!task"
```
## 注意事项

- 在API调用中应使用自定义的方法名称，例如`list`、`create`等。
- 实体信息可以通过Omadeus的URL或`list`命令来获取。
- API密钥和令牌可提供对您Trello账户的完整访问权限——请妥善保管！
- 请求速率限制：每10秒内最多300次请求。
- 每个API端点在900秒内的请求次数上限为100次。

## 示例
```bash
curl -X LIST -s "https://milestone.xeba.ir/dolphin/apiv1/nuggetviews?take=25&zone=inbox&kind=!task"
```