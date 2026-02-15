---
name: domain-dns-ops
description: >
  Domain/DNS ops across Cloudflare, DNSimple, Namecheap for Peter. Use for onboarding zones to Cloudflare, flipping nameservers, setting redirects (Page Rules/Rulesets/Workers), updating redirect-worker mappings, and verifying DNS/HTTP. Source of truth: ~/Projects/manager.
---

# 域名/DNS 操作（Peter）

该技能涉及使用一个简单的路由器来管理域名和 DNS 设置：请以 `~/Projects/manager` 作为配置的基准，运行相应的仓库脚本，并遵循相应的检查清单。

## 配置基准（请先阅读）

- `~/Projects/manager/DOMAINS.md`：域名与目标服务器的映射关系；注册商相关的提示；需要排除的域名。
- `~/Projects/manager/DNS.md`：关于如何将域名配置到 Cloudflare 以及 DNS/重定向的详细步骤。
- `~/Projects/manager/redirect-worker.ts` 和 `~/Projects/manager/redirect-worker-mapping.md`：用于处理重定向逻辑的脚本和配置文件。

## 操作流程（新域名 → Cloudflare → 重定向）

1. **确定路由模式**：
   - 使用页面规则进行重定向（适用于小规模、按区域划分的情况）。
   - 使用规则集或批量重定向功能（需要具备相应的权限）。
   - 或者使用 `redirect-worker` 来处理重定向逻辑。

2. **配置 Cloudflare 区域**：
   - 通过界面创建 Cloudflare 区域，然后使用 `cli4` 命令进行确认：
     - `cli4 --get name=example.com /zones`

3. **设置名称服务器**：
   - 如果注册商是 Namecheap：执行 `cd ~/Projects/manager && source profile && bin/namecheap-set-ns example.com emma.ns.cloudflare.com scott.ns.cloudflare.com`。
   - 如果注册商是 DNSimple：请参考 `~/Projects/manager/DNS.md` 以获取相关的 API 说明。

4. **设置 DNS 配置（以便 Cloudflare 能够处理 HTTPS 请求）**：
   - 设置代理服务器（ apex A 记录）和通配符 A 记录，指向 `192.0.2.1`（具体操作请参见 `~/Projects/manager/DNS.md` 中的 `cli4` 命令）。

5. **执行重定向**：
   - 如果使用页面规则：请参考 `~/Projects/manager/DNS.md` 中提供的 `cli4 --post ... /pagerules` 模板。
   - 如果使用 `redirect-worker`：请更新 `~/Projects/manager/redirect-worker-mapping.md` 中的配置，并根据 `~/Projects/manager/DNS.md` 的说明部署相应的路由规则。

6. **验证配置**：
   - 检查 DNS 设置：`dig +short example.com @1.1.1.1`（确认 Cloudflare 是否正确响应）。
   - 测试 HTTPS 重定向：`curl -I https://example.com`（确认是否返回 301 状态码）。

## 常用操作

- **检查 Cloudflare API 令牌的有效性**：`source ~/.profile`（优先使用 `CLOUDFLARE_API_TOKEN`；如果不存在则使用 `CF_API_TOKEN`）。
- **禁用“阻止 AI 机器人”的功能**：`cd ~/Projects/manager && source profile && bin/cloudflare-ai-bots status` 或 `bin/cloudflare-ai-bots disable`。

## 修改后的操作（提交/推送）

如果你对 `~/Projects/manager` 目录中的任何内容（文档、脚本或配置文件）进行了修改，请确保也在该目录下提交更改：

1. 查看修改内容：`cd ~/Projects/manager && git status && git diff`
2. 将修改的文件添加到暂存区：`git add <paths>`
3. 提交更改：使用常规的提交信息（例如 `git commit -m "feat: …"`、`fix:` 或 `docs:` 等）。
4. 仅在被明确要求时才推送更改到远程仓库：`git push origin main`

## 注意事项：

- 除非被明确要求，否则不要修改 `.md` 文件或 `steipete.md` 文件；请先查看 `~/Projects/manager/DOMAINS.md` 以获取正确的配置信息。
- 在调试 Cloudflare 相关问题时，请先确认注册商信息是否正确（错误的信息服务器设置通常是导致问题的原因）。
- 尽量采用可逆的操作步骤；每次修改后都请进行验证（名称服务器 → DNS 设置 → 重定向逻辑）。