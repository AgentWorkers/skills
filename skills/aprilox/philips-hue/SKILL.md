---
name: philips-hue
description: 通过 API v1 对 Philips Hue 灯具进行本地控制
homepage: https://developers.meethue.com/
metadata: {"clawdbot":{"emoji":"💡","requires":{"bins":["curl","jq","python3"]}}}
---
# Philips Hue Skill  
通过API v1实现Philips Hue灯具的本地控制。  

## 安装与配置  

### 1. 先决条件  
- 确保本地网络中有一台Philips Hue Bridge。  
- 确保您的系统上已安装`curl`、`jq`和`python3`。  

### 2. 配置`.env`文件  
在技能目录下创建一个`.env`文件：  
```bash
BRIDGE_IP=192.168.1.XX  # Your bridge IP
USERNAME=your_api_key   # Obtained after pairing
```  

### 3. 配对（获取API密钥）  
如果您还没有`USERNAME`，请按照以下步骤操作：  
1. 按下Philips Hue Bridge上的物理按钮。  
2. 运行测试命令；脚本会指导您完成配对过程，或者您也可以使用设置工具将“OpenClaw”注册为新的设备类型。  

## 使用方法  
`hue.sh`脚本设计得既快速又灵活，支持在单个命令中组合多种操作。  

### 基本命令  
```bash
# Turn On / Off
./hue.sh light 1 on
./hue.sh light 1 off

# See status of all lights
./hue.sh status
```  

### 高级控制（命令链）  
您可以结合使用颜色、十六进制代码和亮度来控制灯具：  
```bash
# Turn on in blue at 50% brightness
./hue.sh light 1 on color blue bri 50

# Use HTML Hex codes (e.g., #3399FF)
./hue.sh light 1 color "#3399FF"

# Change color only
./hue.sh light 1 color red

# Precise setting (Brightness 0-100, Hue 0-65535, Sat 0-254)
./hue.sh light 1 bri 80 sat 200 hue 15000
```  

### 支持的颜色  
- **命名颜色：** `red`（红色）、`blue`（蓝色）、`green`（绿色）、`yellow`（黄色）、`orange`（橙色）、`pink`（粉色）、`purple`（紫色）、`white`（白色）、`warm`（暖色调）、`cold`（冷色调）。  
- **十六进制颜色：** 任何以`#`开头的HTML颜色代码（例如`#FF5733`）。请确保颜色代码用引号括起来。  

## 技能结构  
- `hue.sh`：控制脚本（基于Shell语言编写）。  
- `.env`：存储您的敏感信息（IP地址和API密钥）。  
- `SKILL.md`：本文档。  

---  
💡 **提示：** 为了方便快速使用，可以在工作区的`TOOLS.md`文件中添加这些命令的快捷链接或说明。