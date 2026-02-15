# Feishu 提及助手

该工具可将 Feishu 用户/机器人的名称转换为 OpenID，从而支持在群聊中通过 @ 符号进行提及。

## 使用方法

```bash
node skills/feishu-mention-helper/lookup.js --name "Name To Find"
```

## 主要功能

- 搜索 Feishu 用户目录（需要相应的权限）  
- 将搜索结果缓存到 `skills/identity-manager/identities.json` 文件中（如果可用）  
- 返回格式化的提及字符串：`<at user_id="ou_...">名称</at>`