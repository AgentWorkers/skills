# OpenClaw Web Gateway

这是一个基于 Flask 的简易 Web 界面，用于与 OpenClaw 代理进行交互。

## 类型  
interface  

## 运行时语言  
python  

## 功能  
- 多用户聊天界面  
- 与 OpenClaw 的 HTTP 集成  
- 持久化的用户界面状态  
- 简单的内存管理辅助工具  
- 可选的 Google Maps 集成  

## 系统要求  
- Python 3.10 或更高版本  
- 本地或远程运行的 OpenClaw 实例  

## 安装方法  
```bash
python3 -m venv .venv  
source .venv/bin/activate  
pip install -r requirements.txt  
```

## 本地配置  
在项目根目录下创建一个名为 `.env` 的文件，并填写以下内容：  
```
APP_TITLE=OpenClaw Web Gateway  
APP_SUBTITLE=OpenClaw 的本地聊天界面  
HOST=0.0.0.0  
PORT=5002  
OPENCLAW_BASE_URL=http://127.0.0.1:18789  
OPENCLAW_TOKEN=  
OPENCLAW_MODEL=default  
OPENCLAW_CHANNEL=web-gateway  
GOOGLE_MAPS_EMBED_API_KEY=  
STATE_FILE=./gateway_state.json  
MEMORY_ROOT=~/.openclaw/memory  
PARTICIPANTS_FILE=./config/participants.json  
DEFAULT_USER=alex  
```  

接下来，根据以下示例创建 `config/participants.json` 文件：  
```json
[
  {
    "key": "alex",
    "display_name": "Alex",
    "aliases": ["alex", "a"]
  },
  {
    "key": "sam",
    "display_name": "Sam",
    "aliases": ["sam", "s"]
  }
]  
```  

最后，运行以下命令：  
```bash
./run.sh  
http://127.0.0.1:5002  
```  

**注意事项：**  
- 请勿将实际的 `.env` 文件和 `config/participants.json` 文件提交到代码仓库中。  
- 如果您的网关不需要身份验证，可以将其 `OPENCLAW_TOKEN` 设置为空。  

**作者：**  
Romain Jeanneret