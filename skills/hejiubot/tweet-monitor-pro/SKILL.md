---
name: Tweet Monitor Pro
description: 无需登录或使用 API 密钥即可获取 X/Twitter 的推文、回复以及时间线信息。同时支持中文平台（微博、哔哩哔哩、CSDN、微信）。
---
# Tweet Monitor Pro

这是一个专为 OpenClaw 设计的商业 X/Twitter 抓取工具。无需登录，也无需 API 密钥。

## 特点

✅ **基础功能（完全独立）**：无需使用 Camofox 即可获取单条推文  
✅ **高级功能**：回复推文、查看用户时间线、使用 Google 搜索（需使用 Camofox）  
✅ **支持中文平台**：Weibo、Bilibili、CSDN、微信文章（部分平台无需 Camofox）  
✅ **配额管理**：基于订阅的使用限制  
✅ **支持 SkillPay**：可选的自动计费集成  

---

## 订阅计划

| 计划 | 月费 | 配额 | 功能 |
|------|-------------|-------|----------|
| 免费 | $0 | 10 次调用 | 获取单条推文 |
| Pro | $1.9 | 1,000 次调用 | 所有基础功能 + 查看时间线 + 回复推文 + 搜索 |
| Business | $9.9 | 无限次调用 | 所有功能 + API 访问 + 优先支持 |

---

## 快速入门

### 1. 安装

```bash
# From ClawHub
openclaw skills install tweet-monitor-pro

# Or manual
cp -r tweet-monitor-pro ~/.openclaw/skills/
```

### 2. （可选）启用 Camofox 以使用高级功能

```bash
openclaw plugins install @askjo/camofox-browser
# or manually: git clone https://github.com/jo-inc/camofox-browser && npm install && npm start
```

### 3. 使用

```javascript
// Fetch single tweet
const result = await agent.execute('tweet-monitor-pro.fetchTweet', {
  url: 'https://x.com/user/status/123456'
});
console.log(result.data.tweet.text);

// Fetch thread (replies)
const thread = await agent.execute('tweet-monitor-pro.fetchThread', {
  url: 'https://x.com/user/status/123456'
});
console.log(thread.data.replies);

// Fetch user timeline
const timeline = await agent.execute('tweet-monitor-pro.fetchTimeline', {
  username: 'elonmusk',
  limit: 50
});

// Check quota
const quota = await agent.execute('tweet-monitor-pro.getQuota', {});
console.log(`${quota.data.used}/${quota.data.limit} calls used`);

// Upgrade plan
await agent.execute('tweet-monitor-pro.upgradePlan', { plan: 'pro' });
```

---

## 工具

| 工具 | 描述 | 配额消耗 | 所需计划 |
|------|-------------|------------|---------------|
| `fetchTweet` | 获取单条推文（包含内容及统计数据） | 1 次调用 | 免费+ |
| `fetchThread` | 获取推文及所有回复（嵌套结构） | 3 次调用 | Pro+ |
| `fetchTimeline` | 获取用户时间线（最多 300 条推文） | 每 50 条推文消耗 1 次调用 | Pro+ |
| `monitorUser` | 实时监控新提及的推文 | 每次检查消耗 1 次调用 | Pro+ |
| `getQuota` | 查看剩余配额 | 0 次调用 | 所有计划均可使用 |
| `upgradePlan` | 升级订阅计划 | 0 次调用 | 所有计划均可使用 |

---

## 商业集成

### SkillPay.me 集成（可选）

1. 在 [SkillPay.me](https://skillpay.me) 上创建您的技能  
2. 获取 API 密钥和技能 ID  
3. 设置环境变量：  

```bash
export SKILLPAY_API_KEY="your_key"
export SKILLPAY_SKILL_ID="your_skill_id"
```

该工具会自动报告使用情况并触发计费。  

---

## 技术细节

- **基本数据获取**：使用 FxTwitter 的公共接口（无需身份验证）  
- **高级数据获取**：结合使用 Camofox 和 Nitter（可绕过 Cloudflare）  
- **中文平台支持**：Camofox 负责解析 JavaScript 内容  
- **输出格式**：标准 JSON 格式（包含文本、统计数据及媒体链接）  

---

## 常见问题

**问：为什么无法获取某些推文？**  
答：可能是账户受保护或 Twitter 有相关限制。公开账户通常可以正常获取。  

**问：Camofox 是什么？**  
答：Camofox 是一个运行在本地主机（localhost:9377）上的反检测浏览器工具，用于绕过 Cloudflare 和 JavaScript 防护机制，以使用高级功能。  

**问：配额用完怎么办？**  
答：可以升级到 Pro 或 Business 计划，或等待每月的配额重置（免费计划）。  

**问：支持批量获取推文吗？**  
答：Business 计划支持通过 API 进行批量操作；Pro 计划则可在配额范围内多次调用相关函数。  

---

## 许可证

MIT 许可证——允许商业用途。  

---

## 技术支持

如遇问题或需要功能请求，请在 GitHub 上提交 issue。