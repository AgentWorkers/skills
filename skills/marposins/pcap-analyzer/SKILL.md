**名称：pcap-analyzer**  
**描述：** 使用 `tshark` 分析 `.pcap` 或 `.pcapng` 文件，并生成结构化的网络取证报告（包括数据包来源、端口信息、DNS 请求、TLS 通信、HTTP 活动以及异常情况）。  
**官方网站：** https://www.wireshark.org/docs/man-pages/tshark.html  

**元数据：**  
```json
{
  "openclaw": {
    "emoji": "🦈",
    "requires": {
      "bins": ["tshark", "awk", "sed"],
      "files": ["/home/tom/openclaw-tools/pcap_summary.sh"]
    },
    "notes": [
      "该工具仅执行本地分析，不会导出 PCAP 文件数据。",
      "建议以只读权限运行；请勿修改用户文件。"
    ]
  }
}
```

---

# **PCAP 分析器（tshark）**  
该工具可将捕获的数据包转换为易于理解的报告，适用于实验室工作、事件排查及 CPENT 风格的练习。  

**报告内容：**  
- **捕获元数据**：文件类型、大小、首次/最后一次捕获时间（如有的话）  
- **主要数据包来源**：按数据包数量或字节数排序的终端节点（包括 IPv4 和 IPv6 地址）  
- **TCP/UDP 通信记录**：最活跃的 TCP/UDP 数据流  
- **服务/端口信息**：最常用的 TCP/UDP 目标端口  
- **DNS 请求**：最常见的域名及可疑的 DNS 请求模式  
- **TLS 通信**：SNI（Server Name Indicator）信息及常见的 JA3 类型签名（尽力获取）  
- **HTTP 活动**：主机头部信息及 URL（仅当数据包被解密或为明文时显示）  
- **异常情况**（基于启发式规则检测）：  
  - 仅发送 SYN 数据包的扫描行为  
  - 过高的 SYN 数据包发送频率  
  - 过多的 RST 数据包  
  - 罕见的目标准识符  
  - 单个主机与多个不同主机之间的通信（类似信标信号的行为）  

**输入参数：**  
- `pcap_path`：本地计算机上的 `.pcap` 或 `.pcapng` 文件的完整路径。  
（可选参数：）  
- `focus_host`：需要重点关注的 IP 地址（用于过滤报告内容）  
- `time_window`：用户指定的时间窗口（用于筛选数据包，仅供参考）  

**运行方式（终端命令）：**  
```bash
{baseDir}/scripts/analyze.sh "/full/path/to/capture.pcapng"
```