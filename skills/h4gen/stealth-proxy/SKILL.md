---
name: vpn
description: 这是一项元技能（meta-skill），用于通过协调使用 shell 脚本、curl-http、wireguard、tailscale、dns、ipinfo 和 moltguard 等工具来设置安全网络隧道、进行地理访问诊断以及检测网络异常后自动恢复任务执行。当用户需要控制 VPN 切换、验证地理位置、检查 DNS 安全性，或者自动重试之前被阻止的工作流程时，可以使用该技能。
homepage: https://clawhub.ai
user-invocable: true
disable-model-invocation: false
metadata: {"openclaw":{"emoji":"🔐","requires":{"bins":["bash","curl"],"anyBins":["nordvpn","mullvad","expressvpn","wg","tailscale"],"env":[],"config":[]},"note":"Requires at least one tunnel path (provider CLI, WireGuard, or Tailscale exit node). Optional security/geo enrichment: MoltGuard and IPinfo."}}
---

# 目的

当访问因地理/IP策略被阻止时，建立一条安全、经过验证的路径，然后安全且可审计地恢复被阻止的工作流程。

主要目标：
1. 检测并分类阻止行为；
2. 在用户明确同意的情况下，切换到有效的隧道路径；
3. 验证公共IP、地区和DNS的安全性；
4. 有限次数的重试后重新执行被阻止的任务；
5. 返回可审计的连接报告。

这是一项编排技能，它不能保证对受限服务的合法访问。

# 必需安装的技能

核心诊断/编排工具：
- `shell-scripting`（最新版本：`1.0.0`）
- `curl-http`（最新版本：`1.0.0`）

隧道路径选项（至少选择一个）：
- 通过shell编排使用的提供商CLI路径（NordVPN / Mullvad / ExpressVPN）
- `wireguard`（最新版本：`1.0.0`）
- `tailscale`（最新版本：`1.0.0`）

安全与验证扩展工具：
- `dns`（最新版本：`1.0.0`）
- `ipinfo`（最新版本：`1.0.0`）
- `moltguard`（最新版本：`6.0.2`，可选但推荐）

安装/更新：

```bash
npx -y clawhub@latest install shell-scripting
npx -y clawhub@latest install curl-http
npx -y clawhub@latest install wireguard
npx -y clawhub@latest install tailscale
npx -y clawhub@latest install dns
npx -y clawhub@latest install ipinfo
npx -y clawhub@latest install moltguard
npx -y clawhub@latest update --all
```

验证：

```bash
npx -y clawhub@latest list
```

# 所需的凭证和访问权限

所需访问权限：
- 选定的隧道路径的有效账户/会话
- 选定的路径对应的本地可执行文件（`nordvpn`/`mullvad`/`expressvpn` 或 `wg` 或 `tailscale`）

可选密钥：
- `MOLTGUARD_API_KEY`（如果启用了MoltGuard远程检测模式）
- `IPINFO_TOKEN`（可选，用于更精确的地理位置验证）

前置检查：

```bash
command -v nordvpn || command -v mullvad || command -v expressvpn || command -v wg || command -v tailscale
echo "$MOLTGUARD_API_KEY" | wc -c
echo "$IPINFO_TOKEN" | wc -c
```

强制要求：
- 如果缺少密钥或认证信息，切勿默默失败。
- 在遇到阻止情况时，始终返回 `MissingAPIKeys` 和/或 `MissingCredentials`。
- 继续进行非阻止性的诊断，并在需要时将输出标记为 `Partial`。

# 合规性检查（强制要求）

在切换隧道之前，确认并记录：
- 用户修改网络路由的授权；
- 用户对相关法律/条款的确认；
- 切换地理位置的明确目的（如测试、一致性检查、隐私加固）。

如果缺少确认信息：
- 不要执行切换命令；
- 仅返回诊断结果。

# 输入参数（LM必须首先收集）

- `blocked_url` 或 `blocked_endpoint`
- `blocked_task_name`（示例：`prediction-market-arbitrage`）
- `target_region`
- `tunnel_path`（`provider-cli`、`wireguard`、`tailscale-exit-node`）
- `provider_or_profile`（提供商名称、WG配置文件或出口节点名称）
- `risk_mode`（`diagnose-only`、`switch-and-verify`、`switch-and-resume`）
- `kill_switch_required`（`yes/no`）
- `max_retries`（默认值：2）

在明确隧道路径和目标地区之前，不要执行切换操作。

# 工具职责

## shell-scripting

用作控制平面：
- 执行检测；
- 负责连接/断开操作；
- 实现重试和清理逻辑；
- 保证日志记录的准确性。

## curl-http

用于协议级别的验证：
- 执行基线检查及切换后的HTTP检查；
- 捕获`403`/地理阻止的签名；
- 比较HTTP头部和状态码。

## wireguard

在需要基于配置文件的隧道时使用：
- 控制配置文件的激活；
- 检查路由和允许的IP地址；
- 确保隧道配置中的DNS处理正确。

## tailscale

用于tailnet和出口节点路径的配置：
- 使用 `tailscale up --exit-node=<node>` 命令；
- 通过 `tailscale ping`/status 命令验证连接性；
- 在可用出口节点之间快速切换。

## dns

用于检测DNS泄漏和验证：
- 检查DNS解析器的行为；
- 区分权威记录和缓存记录；
- 在DNS路径仍为本地时，明确判断泄漏风险。

## ipinfo

用于地理位置验证：
- 验证切换后的国家/地区/ASN信息；
- 与基线数据进行比较；
- 提供地理位置匹配的置信度。

## moltguard

用作提示/工具的安全防护机制：
- 清理敏感的提示/工具内容；
- 检测获取内容中的提示注入模式；
- 防止工作流程日志中意外泄露敏感信息。

重要限制：
- MoltGuard不是VPN管理工具，也不是完整的网络泄漏检测工具。

# 标准的因果信号链

1. **阻止检测**：
- 向被阻止的端点发送基线请求；
- 将阻止原因分类为 `geo_block`、`ip_block`、`auth_block` 或 `other_http_error`。

2. **基线快照**：
- 捕获切换前的公共IP、国家和解析器上下文信息。

3. **隧道路径选择**：
- 选择一个路径：
  - 提供商提供的CLI命令；
  - WireGuard配置文件；
  - Tailscale出口节点。
- 在连接前验证相应工具和配置文件的可用性。

4. **隧道激活**：
- 连接到选定的路径；
- 从工具输出中确认会话状态；
- 如果有需要，执行强制关闭隧道的操作。

5. **地理和IP验证**：
- 比较切换前后的公共IP；
- 使用 `ipinfo.io`（可选）和令牌验证目标国家；
- 记录国家信息是否匹配。

6. **DNS安全检查**：
- 检查DNS解析器的行为，检测明显的DNS绕过模式；
- 如果在完全使用隧道的情况下DNS仍然无法正常工作，标记为风险。

7. **访问重试**：
- 重试被阻止的端点；
- 将HTTP状态和内容与基线数据进行比较。

8. **任务恢复**：
- 如果重试成功，自动恢复被阻止的工作流程（`switch-and-resume`模式）；
- 否则，在重试次数范围内更换端点或配置文件，然后停止操作并记录原因。

建议使用的验证命令：

```bash
curl -s ifconfig.me
curl -s https://ipinfo.io/json
curl -I "${BLOCKED_URL}"
```

# 漏洞和安全检查

成功前的最低要求：
- 公共IP发生变化；
- 目标国家与预期一致（或提供明确的偏差解释）；
- 端点从被阻止状态变为可访问或预期的状态；
- DNS路径与隧道配置一致；
- 如果启用了MoltGuard，没有未解决的高风险警告。

如果需要执行强制关闭隧道操作，但该操作未被支持或未通过验证：
- 返回 `Needs Review`，并避免恢复高风险任务。

# 输出内容

必须返回的信息包括：
- `BlockDiagnosis`：阻止类型及基线HTTP证据
- `TunnelPath`：选定的路径及选择理由
- `TunnelStatus`：连接状态、切换前后的IP地址、目标地区是否匹配
- `DNSSafety`：DNS解析器的行为及泄漏风险评估（`low|medium|high`）
- `SecurityStatus`：MoltGuard的模式（`enabled`、`gateway-only`、`disabled`）及未解决的警告
- `AccessRetest`：切换后的结果及与基线的对比情况
- `TaskResumption`：任务是恢复还是继续被阻止，以及原因
- `NextActions`：对于未解决的阻止问题，提供具体的命令或账户操作步骤

# 质量控制

在最终输出之前，需要验证：
- 诊断结果是否有依据；
- 是否有切换前后的网络证据；
- 是否遵守了重试次数限制；
- 是否明确说明了缺失的凭证或密钥；
- 是否明确说明了提供商/路径的局限性。

如果任何检查失败，返回 `Needs Revision` 并指明具体的缺失内容。

# 故障处理

- 如果缺少隧道工具或配置文件，返回 `MissingCredentials` 并提供具体的安装/配置步骤；
- 如果缺少VPN账户或认证信息，返回 `MissingCredentials`，跳过切换步骤；
- 如果在检测模式下缺少 `MOLTGUARD_API_KEY`，返回 `MissingAPIKeys`，并继续使用仅限网关的模式；
- 如果隧道已连接但地理信息仍然不匹配，尝试使用不同的端点或配置文件重试一次；
- 如果重试后端点仍然被阻止，返回完整的证据并需要手动决定下一步操作。

# 安全防护措施

- 绝不要代表用户声明符合法律或条款要求；
- 在没有进行切换前后的验证之前，绝不要声称系统处于安全状态；
- 绝不要无限制地切换地区；
- 绝不要隐藏模糊或失败的访问状态。