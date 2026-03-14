---
name: disk-analyzer
description: "Duf — 一款用于分析磁盘使用情况（包括剩余可用空间）的自动化工具。当您需要使用 Duf 的功能时，可以将其投入使用。"
runtime: python3
license: MIT
---
# Duf

**Duf** — 磁盘使用情况/剩余空间分析工具

## 为什么要使用这个工具？

- 受到热门开源项目的启发（在 GitHub 上获得了数千个星标）  
- 无需安装——可以直接使用系统自带的工具  
- 具有实际功能——会执行真实的命令并生成真实的输出结果  

## 命令说明  

运行 `scripts/duf.sh <command>` 来使用该工具：  

- `overview`：显示所有挂载磁盘的总体使用情况  
- `usage`：[path]：显示指定目录的文件使用情况  
- `top`：[n] [path]：显示指定目录中前 n 个占用空间最大的文件  
- `find-big`：[size]：查找大小超过指定值（例如 100MB）的文件  
- `duplicates`：[path]：查找重复文件  
- `clean`：[path]：建议需要清理的文件  
- `watch`：[path]：监控磁盘使用情况的变化  
- `export`：[format]：以 Markdown 或 JSON 格式导出报告  
- `info`：显示工具的版本信息  

## 快速入门  

```bash
duf.sh help
```  

---

> **免责声明**：  
此工具为独立开发的原创作品，与所引用的开源项目无关，也未获得其授权或基于该项目进行开发。未复制任何代码；引用该开源项目仅用于提供背景信息。  

技术支持：BytesAgain | bytesagain.com | hello@bytesagain.com