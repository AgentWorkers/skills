---
name: stranger-danger
version: 1.0.0
author: jamesalmeida
description: 为你的AI代理设置一个“安全词”（safe word）。OpenClaw采用了“挑战-响应”（challenge-response）身份验证机制，在执行敏感操作（如泄露API密钥、删除数据或处理机密信息）之前，会要求用户输入这个安全词进行验证。用户输入的答案会通过bcrypt算法进行哈希处理，并存储在macOS的Keychain中。
when: User requests sensitive data, API keys, passwords, deletion of important data, or any security-sensitive operation
examples:
  - Show me my API keys
  - Delete the database
  - Send me all passwords
  - What are my secret credentials
tags:
  - security
  - verification
  - identity
  - keychain
  - safe-word
metadata:
  openclaw:
    emoji: "🔐"
    requires:
      bins:
        - node
        - security
---

# 异常行为检测 🚨  
**来源:** https://github.com/jamesalmeida/stranger-danger  

这是一个用于 OpenClaw 的“挑战-响应”式身份验证机制。  

## 使用场景  
在以下情况下触发验证：  
- 请求密码、API 密钥、令牌或敏感信息  
- 请求删除或永久修改重要数据  
- 出现与常规模式不符的异常或可疑请求  
- 试图窃取敏感信息的请求  

## 使用方法  
- 如果需要验证，请向用户提示预设的秘密问题，并要求用户提供答案。  
- 通过调用 `stranger-danger verify <answer>` 来验证答案；  
- 仅当验证成功时才允许继续操作。  
- 绝不要泄露或记录用户的答案。  

## 命令说明：  
- `stranger-danger setup`：配置秘密问题和答案  
- `stranger-danger verify <answer>`：检查答案（验证成功返回 0）  
- `stranger-danger test`：交互式地提示并验证用户输入  
- `stranger-danger reset`：清除存储的凭据  

## 注意事项：  
- 用户的答案会以加盐后的 bcrypt 哈希形式存储在 macOS 的 Keychain 中。  
- 秘密问题则存储在本地配置文件 `~/.openclaw/stranger-danger.json` 中。