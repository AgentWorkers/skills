# feishu-api-cache-fix

> 修复 Feishu API 的速率限制问题

**版本**: 1.0.1
**作者**: @bryan-chx
**标签**: feishu, api, fix, performance

## 问题

网关每分钟都会调用 Feishu API，导致速率限制被触发。

## 解决方案

在 probe.ts 文件中添加 2 小时的缓存机制。

## 使用方法

```bash
sudo bash fix_feishu_cache.sh
```