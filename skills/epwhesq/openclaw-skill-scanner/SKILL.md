# 技能扫描器 (Skill Scanner)

**名称:** skill-scanner  
**版本:** 1.0.0  
**作者:** vrtlly.us  
**类别:** 安全 (Security)  

## 描述  
该工具会在安装前后扫描 ClawHub 中的技能（skills），检测是否存在恶意行为。能够识别 Base64 编码的 payload、反向 shell、数据泄露、加密矿工程序、混淆过的 URL 等恶意内容。  

## 使用方法  

### 扫描所有已安装的技能  
```bash
python3 scanner.py
```  

### 扫描特定的技能  
```bash
python3 scanner.py --skill <skill-name>
```  

### 扫描特定的文件  
```bash
python3 scanner.py --file <path-to-file>
```  

### 安装前的扫描流程（下载 → 扫描 → 生成报告 → 清理）  
```bash
python3 scanner.py --pre-install <clawhub-slug>
```  

### JSON 格式输出  
```bash
python3 scanner.py --json
python3 scanner.py --skill <name> --json
```  

### 安全安装钩子（Safe Installation Hook）  
```bash
bash install-hook.sh <clawhub-slug>
bash install-hook.sh <clawhub-slug> --force
```  

## 检测模式  
| 类别 | 检测内容 |  
|---|---|  
| Base64 编码的 payload | 位于 `exec/bash/eval` 附近的较长 Base64 字符串  
| 通过管道连接到 shell | `curl ... \| bash`, `wget ... \| sh`  
| 原始 IP 连接 | 类似 `http://1.2.3.4` 的 URL  
| 危险的函数 | `eval()`, `exec()`, `os.system()`, `subprocess(shell=True)`  
| 隐藏文件 | 在非预期位置创建的点文件（dotfiles）  
| 环境变量泄露 | 读取 `.env` 文件或发送 API 密钥  
| 混淆过的 URL | 如 `rentry.co`, `pastebin`, `hastebin` 等重定向链接  
| 假冒的依赖项 | 引用不存在的包  
| 数据泄露端点 | 如 `webhook.site`, `requestbin` 等  
| 加密矿工程序 | 如 `xmrig`, `stratum` 等矿工软件的引用  
| 密码保护文件 | 通过密码保护的 zip/tar 文件下载  

## 风险等级  
- **0-29（绿色）：** 无可疑行为  
- **30-69（黄色）：** 可疑——使用前请查看警告信息  
- **70-100（红色）：** 危险——很可能是恶意软件，切勿安装  

## 相关文件  
- `scanner.py`： 主扫描引擎  
- `install-hook.sh`： 安全安装脚本  
- `whitelist.json`： 已知安全的技能列表  
- `report-template.md`： Markdown 格式的报告模板