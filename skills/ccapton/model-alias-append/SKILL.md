---
name: model-alias-append
version: "1.0.2"
description: |
  Automatically appends the model alias to the end of every response with integrated hook functionality and configuration change detection.
  Use when transparency about which model generated each response is needed.

  Use when: providing model transparency, tracking which model generated responses, 
  monitoring configuration changes, or ensuring response attribution.
license: MIT
---

# 模型别名追加功能

> 在配置发生变化时，自动为响应内容添加模型别名

![模型别名示例](https://github.com/Ccapton/FileRepertory/blob/master/files/model_alias_snapshot.png?raw=true)

## 主要特性
- 🔍 **自动检测** - 识别每个响应所使用的模型
- 🏷️ **别名追加** - 从 openclaw 的配置文件 `agentsdefaults.models.{yourModelDict}.alias` 中添加模型别名（格式如下）
```
"agents": {
  "defaults": {
    "model": {
      "primary": "gemma3:27b-local",
      "fallbacks": [ "qwen" ]
    },
    "models": {
      "ollama-local/gemma3:27b": {
        "alias": "gemma3:27b-local"
      },
      "qwen-portal/coder-model": {
        "alias": "qwen"
      }
    }
  }
}
```
- 🔄 **实时监控** - 监控配置变化
- 📢 **更新通知** - 在配置发生变化时进行提示
- 🛡️ **格式保留** - 保持回复标签和格式的完整性

## 安装
```
npx clawhub@latest install model-alias-append
```

## 工作原理
1. 在响应内容发送之前进行拦截
2. 确定生成响应的模型
3. 为响应内容添加相应的模型别名
4. 在配置发生变化时显示更新提示

## 设置
> 无需额外配置 - 从现有的 `openclaw.json` 文件中读取配置信息

## 输出示例
```
Your response content...

[Model alias configuration updated] // This line will not appear until openclaw.json modified

gemma3:27b-local
```