---
name: better-auth
description: |
  Self-hosted auth for TypeScript/Cloudflare Workers with social auth, 2FA, passkeys, organizations, RBAC, and 15+ plugins. Requires Drizzle ORM or Kysely for D1 (no direct adapter). Self-hosted alternative to Clerk/Auth.js.

  Use when: self-hosting auth on D1, building OAuth provider, multi-tenant SaaS, or troubleshooting D1 adapter errors, session caching, rate limits, Expo crashes, additionalFields bugs.
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# better-auth - D1适配器与错误预防指南

**版本**: better-auth@1.4.16（2026年1月21日）  
**重大变更**: 仅支持ESM（v1.4.0版本）；默认禁止管理员身份冒充（v1.4.6版本）；多团队表结构更新（v1.3版本）；D1版本需要Drizzle/Kysely（不支持直接适配器）