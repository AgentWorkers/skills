---
name: resolving-domains
description: ENS（Ethereum Name Service）和Web3身份解析功能，适用于XMTP代理。这些功能可用于解析域名、提取相关提及信息或获取Farcaster用户的个人资料。当发生ENS解析、Farcaster查询或提及信息提取时，这些功能会被触发执行。
license: MIT
metadata:
  author: xmtp
  version: "1.0.0"
---

# XMTP 域名解析器

用于解析 Web3 身份信息，包括 ENS（Ethereum Name Service）、Farcaster、Basenames 和 Lens Protocol。

## 适用场景

在以下情况下请参考这些指南：
- 将 ENS 名称解析为地址
- 从消息中提取 @提及（mention）信息
- 获取 Farcaster 用户的个人信息
- 处理群组中的缩短地址

## 规则分类（按优先级排序）

| 优先级 | 分类 | 影响程度 | 前缀 |
|----------|----------|--------|--------|
| 1 | 解析 | 高 | `resolve-` |
| 2 | 提取 | 高 | `extract-` |
| 3 | 用户信息 | 中等 | `profiles-` |

## 快速参考

### 解析（高优先级）
- `resolve-address` - 将域名解析为地址
- `resolve-mentions` - 解析消息中的所有 @提及信息

### 提取（高优先级）
- `extract-mentions` - 从文本中提取 @提及信息

### 用户信息（中等优先级）
- `profiles-farcaster` - 获取 Farcaster 用户的个人信息

## 支持的平台

- **ENS** - `vitalik.eth`
- **Farcaster** - `dwr.eth`, `username.farcaster.eth`
- **Basenames** - `tony.base.eth`
- **Lens Protocol** - `stani.lens`

## 快速入门

```typescript
import { createNameResolver } from "@xmtp/agent-sdk/user";

// Resolve a single name using the SDK resolver
const resolver = createNameResolver(process.env.WEB3_BIO_API_KEY || "");
const address = await resolver("vitalik.eth");

// Resolve all mentions in a message
const resolved = await resolveMentionsInMessage(
  ctx.message.content,
  await ctx.conversation.members()
);
// Returns: { "bankr.eth": "0x...", "@fabri": "0x..." }

// Get Farcaster profile via web3.bio API
const profile = await fetchFarcasterProfile("dwr.eth");
console.log(profile.username, profile.fid);
```

## 实现示例

**从文本中提取 @提及信息：**

```typescript
const extractMentions = (message: string): string[] => {
  const mentions: string[] = [];
  
  // Full addresses
  const addresses = message.match(/(0x[a-fA-F0-9]{40})\b/g);
  if (addresses) mentions.push(...addresses);
  
  // @mentions and domains
  const atMentions = message.match(/@(?!0x)([\w.-]+\.eth|[\w.-]+)/g);
  if (atMentions) mentions.push(...atMentions.map(m => m.slice(1)));
  
  // Standalone domains
  const domains = message.match(/\b([\w-]+(?:\.[\w-]+)*\.eth)\b/g);
  if (domains) mentions.push(...domains);
  
  return [...new Set(mentions)];
};
```

**解析消息中的 @提及信息：**

```typescript
import { createNameResolver } from "@xmtp/agent-sdk/user";

const resolveMentionsInMessage = async (
  message: string, members?: GroupMember[]
): Promise<Record<string, string | null>> => {
  const resolver = createNameResolver(process.env.WEB3_BIO_API_KEY || "");
  const mentions = extractMentions(message);
  const results: Record<string, string | null> = {};
  
  await Promise.all(mentions.map(async (mention) => {
    if (mention.match(/^0x[a-fA-F0-9]{40}$/)) {
      results[mention] = mention;
    } else {
      const name = mention.includes(".") ? mention : `${mention}.farcaster.eth`;
      results[mention] = await resolver(name).catch(() => null);
    }
  }));
  return results;
};
```

**获取 Farcaster 用户的个人信息：**

```typescript
const fetchFarcasterProfile = async (name: string) => {
  const response = await fetch(`https://api.web3.bio/profile/${encodeURIComponent(name)}`);
  if (!response.ok) return { address: null, username: null, fid: null };
  const data = await response.json();
  const profile = data?.find((p: any) => p.platform === "farcaster");
  return {
    address: profile?.address,
    username: profile?.displayName,
    fid: profile?.social?.uid?.toString(),
  };
};
```

## 使用方法

如需详细说明，请阅读相应的规则文件：

```
rules/resolve-address.md
rules/extract-mentions.md
rules/profiles-farcaster.md
```