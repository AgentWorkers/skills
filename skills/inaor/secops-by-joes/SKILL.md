---
name: Security Joes AI Analyst
description: **SecOps检查内容：**  
- 端点监控（EDR、Sysmon）  
- 定期更新系统组件（EVTX）  
- 实施最小权限策略  
- 网络可见性管理  
- 凭据保护（Kerberos/NTLM/Pass-the-Hash）  
- 设备清单及已知漏洞的监控  
- 每周安全评估  
- 技能完整性验证（如设备启动时的身份验证、版本信息检测等）  

**适用场景：**  
- 在实施或审查主机安全配置时  
- 在处理EDR/Sysmon/EVTX系统时  
- 在调整权限设置时  
- 在评估网络安全风险时  
- 在加强凭证安全时  
- 在进行定期安全审查时  
- 在检测潜在的安全威胁或技能滥用行为时
version: 1.0.0
author: Security Joes
authorUrl: https://www.securityjoes.com
homepage: https://www.securityjoes.com
license: MIT
metadata:
  openclaw:
    emoji: "🔒"
    category: "security"
tags:
  - security
  - secops
  - clawhub
  - edr
  - sysmon
  - evtx
---

# Security Joes AI Analyst

您负责指导和实施针对终端的安全操作检查（SecOps），重点关注以下方面：**端点检测与响应（EDR）**、**系统监控（Sysmon）**、**系统更新**、**心跳信号（Heartbeat）上的事件传输（EVTX）**、**最小权限原则**、**网络可见性**、**凭证保护**（Kerberos/NTLM/密码传递攻击防护**、**设备清单及已知漏洞**，以及**每周安全评估**。操作目标主要为Windows系统；在适用的情况下，将使用PowerShell/WMI/注册表以及EVTX技术。

## 职责范围

1. **端点检测与响应（EDR）**：
   - 确保至少安装并启用一个端点检测与响应工具（如Microsoft Defender或CrowdStrike），并报告其是否存在及运行状态。

2. **系统监控（Sysmon）**：
   - 确认Sysmon已安装并正在记录日志；识别日志存储的位置（通常为EVTX格式）。

3. **系统更新**：
   - 检查操作系统版本及补丁状态；如果系统版本超过规定期限（例如30天以上未打补丁），则报告异常情况。

4. **心跳信号与EVTX**：
   - 通过心跳信号查询Security/Sysmon/Defender的事件传输日志，获取最近的安全警报信息，并生成相应的汇总报告或触发警报。

5. **最小权限原则**：
   - 确认设备或用户是否以最小权限运行（非管理员权限），并检查是否存在未经授权的权限提升行为。

6. **网络可见性**：
   - 了解设备能够访问的网络及接口信息（包括ARP协议、WiFi连接、域信任关系等）。

7. **凭证保护（网络层面）**：
   - 实施Kerberos/NTLM安全策略，并加强密码传递攻击的防护机制（如SMB签名、LDAP签名、NTLM限制等）。

8. **设备详情与已知漏洞**：
   - 统计设备上的操作系统版本、已安装的补丁信息及软件列表，并将其与已知的安全漏洞信息进行对比分析。

9. **每周安全评估**：
   - 每周执行全面的安全操作检查，生成评估报告，并可选择性地通过事件形式进行通知。

10. **技能完整性检查**：
    - 在系统首次启动时，对当前技能及其它已知技能进行哈希处理并存储哈希值；在每次系统启动时重新计算哈希值并进行比较。通过版本信息判断系统是否经历了升级或被入侵。

## 适用场景

- 当用户需要了解主机安全状态、终端健康状况或请求进行定期安全评估时。
- 在部署或扩展安全数据收集工具/心跳信号检测逻辑时。
- 当涉及到端点检测与响应（EDR）、系统监控（Sysmon）、事件传输（EVTX）、最小权限原则、网络可见性、凭证保护、漏洞防护等相关内容时。
- 在评估“健康终端”的标准或规则时。

---

## 1. 端点检测与响应（EDR）检查

### Microsoft Defender
- 服务名称：`WinDefend`（使用`Get-Service WinDefend`查询）。
- 可选：使用`Get-MpComputerStatus`（或`MpCmdRun.exe -GetStatus`）获取签名版本及实时防护状态。
- 注册表相关键：`HKLM\SOFTWARE\Microsoft\Windows Defender`及相关的产品状态信息。

### CrowdStrike Falcon
- 服务名称：`CsAgent`（使用`Get-Service CsAgent -ErrorAction SilentlyContinue`查询）。
- 注册表相关键：`HKLM\SYSTEM\CurrentControlSet\Services\CsAgent`或`HKLM\SOFTWARE\CrowdStrike`下的Falcon特定配置项。

### 其他工具（如SentinelOne、Carbon Black等）
- 建议使用相应的服务名称，并根据需要检查注册表或进程状态。明确指定环境中主要的端点检测与响应工具。

**输出示例**：
- 至少包含以下信息：`edr_present: true|false`、`edr_name: "Defender"|"CrowdStrike"`等；可选`edr_healthy: true|false`（表示服务是否正在运行）。

---

## 2. 系统监控（Sysmon）检查
- 服务名称：`Sysmon64`或`Sysmon`（使用`Get-Service Sysmon64`或`Sysmon -ErrorAction SilentlyContinue`查询）。
- 日志文件通常存储在`C:\Windows\System32\winevt\Logs\`目录下，文件名为`Microsoft-Windows-Sysmon%4Operational.evtx`。
- 可选：使用`Sysmon64 -s`或已知配置路径来确认日志记录的详细范围。

**输出示例**：
- `sysmonInstalled: true|false`、`sysmon_log_path: "..."`（如果存在日志文件）；可选`sysmon_service_running: true|false`。

---

## 3. 系统更新检查
- **快速检查**：
  - 使用`Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 1`获取最新的补丁安装时间。
  - 或使用`Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion".CurrentBuild`获取操作系统版本信息。

- **详细检查**：
  - 可以通过WMI `Win32_QuickFixEngineering`或COM `Microsoft.Update.Session`获取更详细的系统更新状态，包括是否需要重启等信息。

---

## 4. 心跳信号与EVTX警报
- 在心跳信号触发时（或按照预定时间间隔进行检查）：
  - 安全相关的EVTX日志文件位于`C:\Windows\System32\winevt\Logs\Security.evtx`。
  - Sysmon的EVTX日志文件位于`Microsoft-Windows-Sysmon%4Operational.evtx`。
  - Microsoft-Windows-Windows Defender的EVTX日志文件位于`Microsoft-Windows-Windows Defender/Operational`。
  - 可根据需要查看应用程序或系统的其他相关日志文件。

**检查内容**：
- 安全相关事件（如登录失败、敏感权限使用、账户锁定等）。
- 系统监控相关的事件（如临时文件的创建、可疑的父进程/子进程关系等）。
- 安全防御工具相关的事件（如检测到的威胁、警告等）。

**实施建议**：
- 使用PowerShell命令`Get-WinEvent -FilterHashtable @{ LogName='Security'; StartTime=$since }`来查询指定时间的日志。
- 或者编写小型脚本/工具，读取EVTX日志并生成简洁的JSON格式数据，供数据收集工具进一步处理或生成警报。

## 5. 最小权限原则检查
- 确认设备或用户是否以最小权限运行（非管理员权限）。
- 使用`whoami /groups`命令查看用户所属组；通过`Get-Process -Id $PID).StartInfo.Verb`或WMI/CIM检查进程的权限提升情况。
- 使用`net localgroup Administrators`命令查看当前用户或系统服务账户是否属于管理员组。
- 注册表设置`HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\EnableLUA`判断UAC是否启用；`ConsentPromptBehaviorAdmin`和`PromptOnSecureDesktop`设置用于控制UAC提示行为。

**输出示例**：
- `least_privilege: true|false`、`current_user_elevated: true|false`、`in_local_admins: true|false`。

---

## 6. 网络可见性检查
- 了解设备能够访问的网络及邻居设备：
  - 使用`Get-NetAdapter`和`Get-NetIPAddress`命令列出所有网络适配器和IP地址。
  - 使用`Get-NetNeighbor`或`arp -a`命令查看设备最近通信的邻居设备信息。
  - 使用`netsh wlan show networks`或`Get-NetAdapter | Where-Object {$_.InterfaceDescription -match 'Wi-Fi'}`查看WiFi连接信息及WLAN配置。
  - 使用`systeminfo`和`nltest /domain_trusts`命令查看设备所属域及信任关系。
  - 使用`net view`和`net session`命令查看设备的网络连接情况。

**输出示例**：
- `interfaces[]`（包含适配器名称、IP地址、网关信息）、`arp_count`或`neighbors_count`、`wifi_ssids[]`、`domain_member: true|false`、`domain_name`、`trusts[]`、`net_view_count`或`net_session_count`。

## 7. 凭证保护（网络层面）
- 检查网络层面的凭证保护机制，以防止Kerberos/NTLM攻击和密码传递攻击：
  - 使用`Get-SmbClientConfiguration`和`Get-SmbServerConfiguration`配置SMB签名要求。
  - 对于域控制器，检查`HKLM\SYSTEM\CurrentControlSet\Services\NTDS\Parameters\LDAPServerIntegrity`设置以强制使用LDAP签名。
  - 检查NTLM限制设置（如`RestrictNTLMInDomain`/`RestrictNTLMOutbound`）。
  - 使用`Get-CimInstance -ClassName Win32_DeviceGuard`或注册表设置`HKLM\SYSTEM\CurrentControlSet\Control\Lsa\LsaCfgFlags`来启用Credential Guard保护机制。

**输出示例**：
- `smb_signing_required_client: true|false`、`smb_signing_required_server: true|false`、`ldap_signing`、`lm_compat_level`、`credential_guard: true|false`、`lsa_protected: true|false`。

## 8. 设备详情与已知漏洞检查
- 统计设备信息，并将其与已知漏洞信息进行对比分析：
  - 使用`Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion`获取操作系统版本及补丁信息。
  - 使用`Get-HotFix`或WMI `Win32_QuickFixEngineering`获取最新的热修复程序信息。
  - 使用`Get-ItemProperty HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*`和`HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*`获取已安装软件的详细信息。
  - 检查操作系统版本及软件版本是否与已知漏洞相关联。

**输出示例**：
- `os_name`、`os_build`、`last_patch_date`、`hotfix_count`、`installed_products[]`（包含软件名称和版本信息）、`known_vuln_count`（包含已知漏洞的CVE ID和严重性）。

## 9. 每周安全评估
- 每周执行全面的安全操作检查，生成评估报告（并可选择性地通过事件形式进行通知）。

**检查内容**：
- [ ] 是否安装了端点检测与响应工具且运行正常（第1节）。
- [ ] 是否配置并启用了系统监控日志记录（第2节）。
- [ ] 系统是否保持最新状态（第3节）。
- [ ] 最近的安全警报汇总（第4节）。
- [ ] 是否遵循最小权限原则（第5节）。
- [ ] 设备的网络可见性及邻居设备信息（第6节）。
- [ ] 凭证保护措施是否有效（第7节）。
- [ ] 设备清单及已知漏洞情况（第8节）。
- [ ] 技能完整性是否通过哈希验证（第10节）。

**工作流程**：
1. 执行所有检查任务（或调用汇总这些检查结果的脚本）。
2. 使用预设的“主机安全状态报告模板”生成每周评估报告，并添加网络、凭证保护和漏洞相关的详细信息。
3. 可选择性地触发一个专门的事件：`type: 'weekly_assessment'`（或`config_change`，其中`assessment = true`），报告中包含汇总结果（计数、布尔值等）。

**调度安排**：
- 每周自动执行检查（例如使用cron/Task Scheduler或定时任务），并记录上次执行时间以避免在同一周内重复执行。

## 10. 技能完整性检查
- 在系统首次启动时（或没有存储的哈希值时），对当前技能及其它已知技能进行哈希处理并存储哈希值。
- 在每次系统启动时重新计算哈希值并与存储的哈希值进行比较。通过技能文件中的版本信息判断系统是否经历了升级或被入侵。

**具体要求**：
- **哈希对象**：项目范围内的所有技能文件（位于`.cursor/skills/`目录下），个人范围内的文件位于`~/.cursor/skills/`目录下。每个技能文件应包含`SKILL.md`文件；如有参考文档或示例文件（`reference.md`、`examples.md`），也应一并哈希处理。除非特别说明，否则不要哈希`scripts/`目录下的文件。
- **哈希算法**：使用SHA-256对文件内容进行哈希处理（统一使用UTF-8编码或原始字节格式）。如果技能文件可能在不同操作系统上被编辑，需在哈希前统一处理行尾格式。

**存储方式**：
- 项目范围内的哈希文件存储路径：`.cursor/skills/.skill-integrity.json`。
- 个人范围内的哈希文件存储路径：`~/.cursor/skills/.skill-integrity.json`（或包含项目和个人文件路径的单一文件）。
- 注意：如果哈希文件包含特定于设备的敏感信息，请不要将其提交到版本控制系统中；可以将这些文件添加到`.gitignore`文件中或仅保留本地副本。
- **文件格式**：按技能名称或相对路径进行分类存储。

### 首次启动时的处理流程
1. 列出所有技能文件目录（项目范围内的`.cursor/skills/*`，个人范围内的`~/.cursor/skills/*`）。
2. 读取每个技能文件中的`version`字段（如果存在），并对`SKILL.md`及其参考文档/示例文件进行哈希处理。
3. 生成`.skill-integrity.json`文件，其中包含技能名称、首次执行时间（`firstRun`）和最后一次检查时间（`lastChecked`）。

### 每次启动时的处理流程
1. 加载`.skill-integrity.json`文件（如果文件不存在，则视为首次启动，执行首次启动时的处理流程）。
2. 重新列出所有技能文件目录；对于每个技能文件，读取当前的`version`字段并计算哈希值。
3. **比较结果**：
  - 如果哈希值未变化，则更新`lastChecked`字段。
  - 如果哈希值发生变化且文件版本未更新，则视为系统升级，更新存储的`version`和`fileHashes`字段；无需触发警报。
  - 如果哈希值发生变化但文件版本未更新或缺失，则视为系统可能被入侵，触发警报（例如：“技能完整性：[技能名称]文件内容被篡改”）。
  - 如果发现新的技能文件（存在于磁盘上但未在存储的哈希值中），则将其添加到存储列表中，并更新相应的哈希值。

**版本信息的要求**：
- 技能文件的YAML格式前端应包含`version: "x.y"`字段。在有意升级技能时，需要更新版本号（例如从`1.0`升级到`1.1`），以便下次启动时将哈希变化视为正常升级操作。
- 如果技能文件中没有`version`字段，则任何哈希变化都可能表明系统被入侵。

**输出示例**：
- 每次启动时，输出`skill_integrity`字段的值，表示技能状态为`ok`、`compromised`或`upgraded`。如果系统被入侵，会列出受影响的技能文件。

**集成说明**：
- 在代理程序启动时（例如会话开始时或首次应用该技能时）执行此检查。可选择将技能完整性检查结果包含在每周安全评估报告中。
- 在系统被入侵时，触发MoltSOC警报（类型：`alert`，严重性：高，摘要中包含技能名称及哈希变化详情）。

---

## 主机安全状态报告模板
在生成主机安全状态报告、心跳信号摘要或每周安全评估报告时，使用以下结构：

---

## 与MoltSOC的集成
- 已有的心跳信号事件（类型：`heartbeat`）应包含EDR/Sysmon/更新/事件传输、最小权限原则、网络可见性、凭证保护及漏洞摘要信息，以便在仪表板或规则中显示终端的安全状态或具体故障情况。
- 新的警报（例如“端点检测与响应工具未安装”、“系统监控停止”、“事件传输日志缺失”、“权限过高”、“凭证保护措施薄弱”、“已知漏洞”等）应遵循相同的事件格式。
- 在系统被入侵时（哈希值发生变化但版本未更新），触发警报，报告中包含技能名称及哈希变化详情。
- 在每周安全评估报告中，输出汇总结果；仪表板可以显示上一次的安全评估结果及未通过的检查项。

## 隐私与安全注意事项
- 报告中不应包含原始日志内容或个人身份信息（PII）；仅使用计数结果、事件ID和简要摘要。
- EVTX查询应限制在安全相关的通道和时间范围内；避免将完整日志数据传输到数据收集工具中。
- 对于网络可见性和漏洞相关内容，仅报告统计数据和摘要信息（如邻居设备数量、漏洞数量等）；除非有特殊需求，否则不要输出完整的ARP表或CVE/漏洞详情。

## 关于Security Joes
[Security Joes](https://www.securityjoes.com)提供安全操作指导、终端安全监控工具及自动化工作流程。该技能（Security Joes AI Analyst）由Security Joes维护，适用于ClawHub及兼容的代理平台。

- **官方网站**：[https://www.securityjoes.com](https://www.securityjoes.com)
- **关于我们**：[https://www.securityjoes.com/about](https://www.securityjoes.com/about)