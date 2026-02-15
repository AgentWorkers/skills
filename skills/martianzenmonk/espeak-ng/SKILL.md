---

**名称：espeak-ng**  
**描述：** 使用 `espeak-ng` 实现文本转语音（TTS）功能的工具。  

## espeak-ng 技能  
该技能允许您使用 `espeak-ng` 来生成语音输出。  

### 对于智能代理（Smart Agent）  
**命令：** `python espeak_skill.py <文本>`  
**示例：** `python espeak_skill.py "Hello world"`  

### 对于非智能代理（Non-Smart Agent）  
**命令：** `python ./skills/espeak-ng/espeak_skill.py <文本>`  
**示例：** `python ./skills/espeak-ng/espeak_skill.py "Hello world"`  

### 工具执行方式  
**命令：** `espeak-ng <文本>`  
**示例：** `espeak-ng "Hello world"`  

## 必备条件：**  
- 系统上必须已安装 `espeak-ng`。  
- 在 Linux/macOS 上，请确保已安装 `espeak-ng`：  
  - Ubuntu/Debian：`sudo apt-get install espeak-ng`  
  - CentOS/RHEL：`sudo yum install espeak-ng`  
  - macOS：`brew install espeak-ng`  
- Windows 11：从 [https://github.com/espeak-ng/espeak-ng/releases](https://github.com/espeak-ng/espeak-ng/releases) 下载 `espeak-ng.msi` 并安装。