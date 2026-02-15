---
name: security-scanner
description: 针对Web应用程序、API和基础设施的自动化安全扫描及漏洞检测工具。适用于需要扫描目标系统以发现漏洞、检查SSL证书、查找开放端口、检测配置错误或执行安全审计的场景。该工具可与nmap、nuclei等安全工具集成使用。
---

# 安全扫描器

这是一个用于渗透测试和漏洞评估的自动化安全扫描工具包。

## 快速入门

### 端口扫描
```bash
nmap -sV -sC -oN scan.txt TARGET
```

### 漏洞扫描
```bash
nuclei -u TARGET -o results.txt
```

### SSL 检查
```bash
sslscan TARGET
```

## 扫描类型

### 1. 快速侦察
对活跃的主机和开放端口进行快速初步扫描：
```bash
nmap -sn -T4 SUBNET  # Host discovery
nmap -F TARGET       # Fast port scan (top 100)
```

### 2. 全面端口扫描
对所有端口和服务进行详细检测：
```bash
nmap -p- -sV -sC -A TARGET -oN full_scan.txt
```

### 3. Web 应用程序扫描
```bash
nuclei -u https://TARGET -t cves/ -t vulnerabilities/ -o web_vulns.txt
nikto -h TARGET -o nikto_report.txt
```

### 4. SSL/TLS 分析
```bash
sslscan TARGET
testssl.sh TARGET
```

## 输出结果

将报告保存到 `reports/security-scan-YYYY-MM-DD.md` 文件中，其中包含：
- 目标信息
- 开放的端口和服务
- 发现的漏洞（按严重程度分类）
- 建议措施

## 道德规范

- 仅扫描授权的目标
- 在进行测试前获得书面许可
- 负责任地报告漏洞
- 严禁未经授权擅自利用漏洞