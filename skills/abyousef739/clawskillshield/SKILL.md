# ClawSkillShield 🛡️  
**专为 OpenClaw/ClawHub 技能设计的本地安全扫描工具**  

## 功能概述  
- **静态安全分析**：检测潜在的安全风险和恶意代码模式  
- **识别以下问题**：  
  - 硬编码的敏感信息（API 密钥、凭据、私钥）  
  - 高风险的导入模块（`os`、`subprocess`、`socket`、`ctypes`）  
  - 危险的编程操作（`eval()`、`exec()`、`open()`）  
  - 混淆技术（如 Base64 编码、可疑的编码方式）  
  - 硬编码的 IP 地址  
- **风险评分**（0–10 分）+ 详细的威胁报告  
- **自动隔离高风险技能**  

## 双重使用设计  
- **命令行界面（CLI）**：用户可在安装技能前快速进行安全检查  
- **代理 API**：可供自动化代理或 Moltbot 使用，主动扫描并隔离高风险技能（在 ClawHavoc 事件后至关重要）  

## 快速入门  
### 命令行界面（CLI）  
```bash
pip install -e .
clawskillshield scan-local /path/to/skill
clawskillshield quarantine /path/to/skill
```  

### Python API（代理使用）  
```python
from clawskillshield import scan_local, quarantine

threats = scan_local("/path/to/skill")
if risk_score < 4:  # HIGH RISK
    quarantine("/path/to/skill")
```  

## 无依赖性  
完全基于 Python 开发，无需网络连接，完全在本地运行。  

## 重要性  
ClawHavoc 事件表明恶意技能可能轻易渗透到系统中。ClawSkillShield 提供了一层可信的开源防御机制——通过离线审计代码来保障系统安全。  

---

**GitHub**: https://github.com/AbYousef739/clawskillshield  
**许可证**: MIT  
**作者**: Ab Yousef  
**联系方式**: contact@clawskillshield.com