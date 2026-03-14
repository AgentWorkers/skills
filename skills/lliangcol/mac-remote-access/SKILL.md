---
name: mac-remote-access
description: 通过 Tailscale 对 macOS 机器进行故障诊断、配置以及恢复远程访问。适用于设置或排查 Mac 的 SSH、屏幕共享（Screen Sharing/VNC）、RealVNC、AnyDesk 等远程访问服务；同时也可用于处理 Tailscale 的访问控制列表（ACL）相关问题，尤其是针对 Windows 到 Mac 的远程访问场景。该工具特别适用于解决端口 22/5900 无法被访问的问题，以及那些在 Tailscale 网络中可见但无法成功连接的故障情况。此外，它还支持紧急情况下的远程恢复计划（break-glass remote recovery）。
---
# Mac远程访问

设置或排查通过Tailscale进行Mac远程访问的问题。

## 工作流程

1. 首先检查Mac端。
2. 验证远程客户端是否能够通过TCP连接到Mac。
3. 在调整VNC客户端设置之前，先检查Tailscale的访问控制列表（ACL）。
4. 确保至少保留一条命令行恢复路径（例如通过SSH）。
5. 建议采用分层化的访问方案：以SSH作为备用方案，AnyDesk作为主要的图形界面（GUI）访问方式，VNC作为次要方案。

## Mac端的检查

在能够直接访问Mac的情况下，首先执行以下操作：

```bash
tailscale status
tailscale ip -4
sudo systemsetup -getremotelogin
sudo /usr/sbin/netstat -anv -p tcp | grep '\.5900 .*LISTEN'
nc -vz <Mac-IP> 5900
```

如果屏幕共享功能出现故障，请重启该功能：

```bash
sudo launchctl kickstart -k system/com.apple.screensharing
```

## Windows端的检查

建议使用PowerShell进行测试，并优先使用TCP连接测试，而非ping命令：

```powershell
Test-NetConnection <Mac-IP> -Port 22
Test-NetConnection <Mac-IP> -Port 5900
```

解释：

- 如果`22=False`且`5900=False`，则首先检查Tailscale的访问控制列表（ACL）或相关策略。
- 如果`22=True`且`5900=False`，则检查Mac的屏幕共享功能或VNC服务。
- 如果`22=True`且`5900=True`，则需要进一步检查客户端的身份验证设置或兼容性问题。

## 访问控制列表（ACL）的使用建议

在排查问题时，建议使用明确的访问控制列表（ACL）设置。

请参考`references/acl-template.md`以获取一个基本的ACL模板示例。

## 参考资料

- `references/acl-template.md` — 基本的ACL模板
- `references/checklist.md` — 基本检查清单
- `references/sop.md` — 从开始到结束的操作流程指南
- `references/anydesk-rustdesk.md` — 关于AnyDesk和RustDesk的图形界面访问方案及故障排查指南