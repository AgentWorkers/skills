---
name: vigil
description: AI代理的安全防护机制，适用于以下场景：  
1. 在执行代理工具调用之前对其进行验证；  
2. 构建能够执行shell命令、文件操作或API调用的代理；  
3. 为任何MCP服务器或代理框架添加安全防护层；  
4. 审计代理的行为。  
该机制能够检测并阻止具有破坏性的命令、SSRF攻击、SQL注入、路径遍历、数据泄露、提示框注入以及凭证泄露等安全风险。  
需要安装`vigil-agent-safety` npm包（大小：12.3KB，延迟小于2毫秒）。  
来源：github.com/hexitlabs/vigil
---

# Vigil — 代理安全防护机制

该机制用于验证 AI 代理的实际操作行为（而非它们所发出的指令），适用于任何调用工具的代理程序。

## 先决条件

使用该功能需要 `vigil-agent-safety` npm 包（大小：12.3KB，许可证：Apache 2.0）：

```bash
npm install vigil-agent-safety
```

- **源代码：** https://github.com/hexitlabs/vigil  
- **npm：** https://www.npmjs.com/package/vigil-agent-safety  
- **该 npm 包没有运行时依赖项。** 该功能仅作为该包的封装层使用。

## 快速入门

```typescript
import { checkAction } from 'vigil-agent-safety';

const result = checkAction({
  agent: 'my-agent',
  tool: 'exec',
  params: { command: 'rm -rf /' },
});

// result.decision === "BLOCK"
// result.reason === "Destructive command pattern"
// result.latencyMs === 0.3
```

## 监控内容：

- 破坏性命令（如 `rm -rf`、`mkfs`、反向 shell） → 阻止执行  
- SSRF（跨站请求伪造，针对元数据端点、本地主机、内部 IP 地址的请求） → 阻止执行  
- 数据泄露（通过 `curl` 请求外部服务器或访问 `.ssh/id_rsa` 文件） → 阻止执行  
- SQL 注入（如 `DROP TABLE`、`UNION SELECT`） → 阻止执行  
- 路径遍历（如访问 `../../../etc/shadow` 文件夹） → 阻止执行  
- 提示框注入（用于绕过指令执行，例如使用 `[INST]` 标签） → 阻止执行  
- 编码攻击（如 Base64 解码、`eval(atob())`） → 阻止执行  
- 凭据泄露（API 密钥、AWS 密钥、访问令牌） → 触发警报  

共 22 条安全规则，无任何依赖项，每次检查耗时少于 2 毫秒。

## 使用模式

```typescript
import { configure } from 'vigil-agent-safety';

// warn = log violations but don't block (recommended to start)
configure({ mode: 'warn' });

// enforce = block dangerous calls
configure({ mode: 'enforce' });

// log = silent logging only
configure({ mode: 'log' });
```

## 与 Clawdbot 结合使用

将 Vigil 作为代理工具的安全防护层进行集成。`scripts/vigil-check.js` 脚本可帮助您通过命令行执行验证操作：

```bash
# Check a tool call
node scripts/vigil-check.js exec '{"command":"rm -rf /"}'
# → BLOCK: Destructive command pattern

# Check a safe call
node scripts/vigil-check.js read '{"path":"./README.md"}'
# → ALLOW
```

## 策略配置

可加载内置的策略模板：

```typescript
import { loadPolicy } from 'vigil-agent-safety';

loadPolicy('restrictive');  // Tightest rules
loadPolicy('moderate');     // Balanced (default)
loadPolicy('permissive');   // Minimal blocking
```

## 命令行接口（CLI）

```bash
npx vigil-agent-safety check --tool exec --params '{"command":"ls -la"}'
npx vigil-agent-safety policies
```

## 相关链接：

- GitHub：https://github.com/hexitlabs/vigil  
- npm：https://www.npmjs.com/package/vigil-agent-safety  
- 文档：https://hexitlabs.com/vigil