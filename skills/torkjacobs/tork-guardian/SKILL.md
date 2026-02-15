# OpenClaw 的 Tork Guardian

> OpenClaw 是一款功能强大的工具，而 Tork 则为其提供了安全保障。

Tork 是专为 OpenClaw 代理设计的、企业级安全与治理解决方案。它能够检测个人身份信息（PII），执行政策规定，生成合规性报告，控制工具访问权限，并在安装技能之前扫描其中可能存在的漏洞。

## 安装

```bash
npm install @torknetwork/guardian
```

## 快速入门

```typescript
import { TorkGuardian } from '@torknetwork/guardian';

const guardian = new TorkGuardian({
  apiKey: process.env.TORK_API_KEY!,
});

// Govern an LLM request before sending
const result = await guardian.governLLM({
  messages: [
    { role: 'user', content: 'Email john@example.com about the project' },
  ],
});
// PII is redacted: "Email [EMAIL_REDACTED] about the project"

// Check if a tool call is allowed
const decision = guardian.governTool({
  name: 'shell_execute',
  args: { command: 'rm -rf /' },
});
// { allowed: false, reason: 'Blocked shell command pattern: "rm -rf"' }
```

## 网络安全

Tork Guardian 可以监控所有网络活动——包括端口绑定、出站连接以及 DNS 查询——并通过 SSRF 防御、反向 shell 检测以及针对每种技能的速率限制来保障网络安全。

### 使用网络处理功能

```typescript
const guardian = new TorkGuardian({
  apiKey: process.env.TORK_API_KEY!,
  networkPolicy: 'default',
});

const network = guardian.getNetworkHandler();

// Validate a port bind
const bind = network.validatePortBind('my-skill', 3000, 'tcp');
// { allowed: true, reason: 'Port 3000/tcp bound' }

// Validate an outbound connection
const egress = network.validateEgress('my-skill', 'api.openai.com', 443);
// { allowed: true, reason: 'Egress to api.openai.com:443 allowed' }

// Validate a DNS lookup (flags raw IPs)
const dns = network.validateDNS('my-skill', 'api.openai.com');
// { allowed: true, reason: 'DNS lookup for api.openai.com allowed' }

// Get the full activity log for compliance
const log = network.getActivityLog();

// Get a network report with anomaly detection
const report = network.getMonitor().getNetworkReport();
```

### 独立功能

```typescript
import { validatePortBind, validateEgress, validateDNS } from '@torknetwork/guardian';

const config = { apiKey: 'tork_...', networkPolicy: 'strict' as const };

validatePortBind(config, 'my-skill', 3000, 'tcp');
validateEgress(config, 'my-skill', 'api.openai.com', 443);
validateDNS(config, 'my-skill', 'api.openai.com');
```

### 更改策略设置

```typescript
// Default — balanced for dev & production
const guardian = new TorkGuardian({
  apiKey: 'tork_...',
  networkPolicy: 'default',
});

// Strict — enterprise lockdown (443 only, explicit domain allowlist)
const guardian = new TorkGuardian({
  apiKey: 'tork_...',
  networkPolicy: 'strict',
});

// Custom — override any setting
const guardian = new TorkGuardian({
  apiKey: 'tork_...',
  networkPolicy: 'custom',
  allowedOutboundPorts: [443, 8443],
  allowedDomains: ['api.myservice.com'],
  maxConnectionsPerMinute: 30,
});
```

有关威胁覆盖范围、策略比较及合规性报告的详细信息，请参阅 [docs/NETWORK-SECURITY.md](docs/NETWORK-SECURITY.md)。

## 示例配置

以下是针对常见环境的预构建配置：

```typescript
import {
  MINIMAL_CONFIG,
  DEVELOPMENT_CONFIG,
  PRODUCTION_CONFIG,
  ENTERPRISE_CONFIG,
} from '@torknetwork/guardian';
```

| 配置 | 策略 | 网络设置 | 说明 |
|--------|--------|---------|-------------|
| `MINIMAL_CONFIG` | 标准配置 | 默认设置 | 仅需要 API 密钥，所有设置均使用默认值 |
| `DEVELOPMENT_CONFIG` | 最简配置 | 默认设置 | 放松的策略设置，详细日志记录 |
| `PRODUCTION_CONFIG` | 标准配置 | 默认设置 | 禁止某些数据泄露相关域名（如 pastebin、ngrok、burp） |
| `ENTERPRISE_CONFIG` | 严格配置 | 严格策略设置 | 明确允许的域名列表，每分钟最多 20 次连接，仅支持 TLS 协议 |

```typescript
import { TorkGuardian, PRODUCTION_CONFIG } from '@torknetwork/guardian';

const guardian = new TorkGuardian({
  ...PRODUCTION_CONFIG,
  apiKey: process.env.TORK_API_KEY!,
});
```

## 配置设置

```typescript
const guardian = new TorkGuardian({
  // Required
  apiKey: 'tork_...',

  // Optional
  baseUrl: 'https://www.tork.network',   // API endpoint
  policy: 'standard',                     // 'strict' | 'standard' | 'minimal'
  redactPII: true,                        // Enable PII redaction

  // Shell command governance
  blockShellCommands: [
    'rm -rf', 'mkfs', 'dd if=', 'chmod 777',
    'shutdown', 'reboot',
  ],

  // File access control
  allowedPaths: [],                        // Empty = allow all (except blocked)
  blockedPaths: [
    '.env', '.env.local', '~/.ssh',
    '~/.aws', 'credentials.json',
  ],

  // Network governance
  networkPolicy: 'default',               // 'default' | 'strict' | 'custom'
  allowedInboundPorts: [3000, 8080],       // Ports skills may bind to
  allowedOutboundPorts: [443],             // Ports for outbound connections
  allowedDomains: ['api.openai.com'],      // If non-empty, only these domains are allowed
  blockedDomains: ['evil.com'],            // Domains always blocked
  maxConnectionsPerMinute: 60,             // Per-skill egress rate limit
});
```

## 策略规则

| 策略类型 | 对个人身份信息（PII）的处理方式 | 对 shell 命令的处理方式 | 对文件的处理方式 | 对网络活动的处理方式 |
|--------|------------------|------------------|------------------|-------------------------|
| **严格** | 检测到 PII 时立即拒绝访问 | 完全阻止所有相关操作 | 仅允许白名单中的文件访问 | 完全阻止所有网络连接 |
| **标准** | 对 PII 进行模糊处理 | 阻止危险操作 | 阻止敏感文件访问 | 允许所有网络连接 |
| **最简** | 对 PII 进行模糊处理 | 允许所有操作 | 允许所有文件访问 | 允许所有网络连接 |

## 独立功能

```typescript
import { redactPII, generateReceipt, governToolCall } from '@torknetwork/guardian';

// Redact PII from text
const result = await redactPII('tork_...', 'Call 555-123-4567');

// Generate a compliance receipt
const receipt = await generateReceipt('tork_...', 'Processed user data');

// Check a tool call against policy
const decision = governToolCall(
  { name: 'file_write', args: { path: '.env' } },
  { policy: 'standard', blockedPaths: ['.env'] }
);
```

## 安全扫描器

在安装任何 OpenClaw 技能之前，可以使用该扫描器检查其中是否存在安全漏洞。扫描器会针对代码和网络层面检测 14 种常见的安全风险。

### 命令行界面（CLI）

```bash
# Scan a skill directory
npx tork-scan ./my-skill

# Full details for every finding
npx tork-scan ./my-skill --verbose

# JSON output for CI/CD
npx tork-scan ./my-skill --json

# Fail on any high or critical finding
npx tork-scan ./my-skill --strict
```

### 程序化接口

```typescript
import { SkillScanner, generateBadge } from '@torknetwork/guardian';

const scanner = new SkillScanner();
const report = await scanner.scanSkill('./my-skill');

console.log(`Risk: ${report.riskScore}/100`);
console.log(`Verdict: ${report.verdict}`); // 'verified' | 'reviewed' | 'flagged'
```

有关完整规则参考、风险等级说明以及示例输出，请参阅 [docs/SCANNER.md](docs/SCANNER.md)。

## Tork 验证的徽章

通过安全扫描的技能会获得 Tork 验证的徽章：

| 徽章类型 | 得分 | 含义 |
|---------|-------|---------|
| **Tork 验证**（绿色） | 0 - 29 分 | 安全可靠，可放心安装 |
| **Tork 审查中**（黄色） | 30 - 49 分 | 建议进行人工审核 |
| **Tork 警告**（红色） | 50 - 100 分 | 发现安全风险 |

```typescript
import { SkillScanner, generateBadge, generateBadgeMarkdown } from '@torknetwork/guardian';

const scanner = new SkillScanner();
const report = await scanner.scanSkill('./my-skill');
const badge = generateBadge(report);

// Add to your README
console.log(generateBadgeMarkdown(badge));
```

## 获取您的 API 密钥

请访问 [tork.network](https://tork.network) 注册以获取您的 API 密钥。