---
name: openclaw-pii-anonymizer  
description: 一款用于 OpenClaw 的隐私保护工具：在将个人身份信息（PII，如姓名/电子邮件/路径/IP 地址）传递给外部模型（如 Grok/OpenRouter）之前，使用 Ollama 对这些信息进行匿名化处理。该工具兼容各种主机和虚拟机环境，可用于 memory_search 操作、工具调用以及 HEARTBEAT.md 文件的清洗工作。  

metadata:  
  openclaw:  
    requires: {  
      bins: [jq, curl],  
      env: [OLLAMA_URL]  
    }  
  install:  
    - {  
      id: jq, kind: apt, package: jq  
    }  
    - {  
      id: curl, kind: apt, package: curl  
    }  
  homepage: https://github.com/[ORG]/openclaw-pii-anonymizer  
  user-invocable: false  

# OpenClaw PII Anonymizer  

**功能**：  
- **保护 MEMORY.md 文件中的数据不被泄露**：通过 Ollama（phi3:mini）对文件中的个人信息进行匿名化处理，确保数据安全。  

## 使用方法  
```
./privacy-anonymize.sh "Seth at /home/derenger email@example.com"
→ "[PERSON] at [PATH] [EMAIL]"
```  

## 集成方式：  
- **HEARTBEAT.md 文件处理**：执行命令 `Task: ./privacy-anonymize.sh "$(memory_get MEMORY.md)"`  
- **定时任务**：在执行 web_search 或其他操作之前，自动对相关文件进行匿名化处理。  
- **OLLAMA 服务器地址**：默认为 `localhost:11434`（虚拟机环境）或 `10.0.2.2:11434`（主机环境）。  

## Ollama 模型的安装方法  
```
ollama pull phi3:mini
```  

## 相关文件：  
- `privacy-anonymize.sh`：核心处理脚本。