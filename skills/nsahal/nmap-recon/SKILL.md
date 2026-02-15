# Nmap 侦察

使用 Nmap 进行网络侦察和端口扫描。当需要扫描目标、查找开放端口、检测服务、检查漏洞或执行网络侦察时，请使用该工具。

## 触发命令
- `scan [目标]`  
- `port scan`  
- `nmap`  
- `what ports are open`  
- `recon [目标]`  
- `service detection`  
- `vulnerability scan`  

## 必备条件
- 必须安装 `nmap`（在 Kali 中为默认安装软件，可通过包管理器获取）  
- 执行 SYN 扫描和操作系统检测时需要 root 权限或 `sudo`  

## 使用方法

### 快速扫描（前 1000 个端口）  
```bash
nmap -sC -sV -oA scan_$(date +%Y%m%d_%H%M%S) TARGET
```  

### 全部端口扫描  
```bash
nmap -p- -sC -sV -oA fullscan_$(date +%Y%m%d_%H%M%S) TARGET
```  

### 快速检查（快速扫描）  
```bash
nmap -F -T4 TARGET
```  

### 隐秘 SYN 扫描（需要 root 权限）  
```bash
sudo nmap -sS -sV -O -oA stealth_$(date +%Y%m%d_%H%M%S) TARGET
```  

### UDP 扫描（前 100 个端口）  
```bash
sudo nmap -sU --top-ports 100 -oA udp_$(date +%Y%m%d_%H%M%S) TARGET
```  

### 漏洞扫描  
```bash
nmap --script vuln -oA vulnscan_$(date +%Y%m%d_%H%M%S) TARGET
```  

### 强制扫描（包括操作系统、版本信息及路由追踪）  
```bash
nmap -A -T4 -oA aggressive_$(date +%Y%m%d_%H%M%S) TARGET
```  

## 输出解析  
Nmap 支持多种输出格式（使用 `-oA` 参数）：  
- `.nmap`：人类可读格式  
- `.xml`：机器可解析格式  
- `.gnmap`：适用于搜索引擎的格式  

### 从 `.gnmap` 输出中提取开放端口信息：  
```bash
grep "open" scan.gnmap | awk -F'[/]' '{print $1}' | tr ',' '\n' | sort -u
```  

### 提取服务版本信息：  
```bash
grep -E "^[0-9]+/" scan.nmap | awk '{print $1, $3, $4}'
```  

### 从 XML 输出中快速获取扫描结果摘要：  
```bash
xmllint --xpath "//port[@state='open']" scan.xml 2>/dev/null
```  

## 常见扫描配置文件  
| 配置文件 | 命令 | 适用场景 |  
|---------|---------|----------|  
| Quick | `nmap -F -T4` | 快速初步侦察  
| Standard | `nmap -sC -sV` | 检测服务及使用默认脚本  
| Full | `nmap -p- -sC -sV` | 扫描所有 65535 个端口  
| Stealth | `sudo nmap -sS -T2` | 隐秘扫描  
| Vuln | `nmap --script vuln` | 漏洞检测  
| Aggressive | `nmap -A -T4` | 全面扫描（包括详细信息）  

## 脚本分类  
```bash
# List available scripts
ls /usr/share/nmap/scripts/

# Run specific category
nmap --script=default,safe TARGET
nmap --script=vuln TARGET
nmap --script=exploit TARGET
nmap --script=auth TARGET

# Run specific script
nmap --script=http-title TARGET
nmap --script=smb-vuln* TARGET
```  

## 目标指定方法  
```bash
# Single host
nmap 192.168.1.1

# CIDR range
nmap 192.168.1.0/24

# Range
nmap 192.168.1.1-254

# From file
nmap -iL targets.txt

# Exclude hosts
nmap 192.168.1.0/24 --exclude 192.168.1.1
```  

## 扫描时间设置选项  
- `-T0`：极度谨慎（用于规避入侵检测系统）  
- `-T1`：较为隐蔽（用于规避入侵检测系统）  
- `-T2`：常规速度  
- `-T3`：默认速度  
- `-T4`：快速扫描  
- `-T5`：极快速度（可能遗漏部分端口）  

## 权限要求  
⚠️ **仅允许扫描您拥有权限的目标，或获得明确书面授权的目标。**  
**严禁扫描以下内容：**  
- 未经许可的公共基础设施  
- 您无法控制的网络  
- 未经批准的生产系统  

## 示例工作流程  
```bash
# 1. Quick scan to find live hosts
nmap -sn 192.168.1.0/24 -oA live_hosts

# 2. Fast port scan on discovered hosts
nmap -F -T4 -iL live_hosts.gnmap -oA quick_ports

# 3. Deep scan interesting hosts
nmap -p- -sC -sV -oA deep_scan TARGET

# 4. Vulnerability scan
nmap --script vuln -oA vuln_scan TARGET
```