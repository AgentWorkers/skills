---
name: qa-check
description: 所有开发工作在发布前都必须经过强制性的质量保证流程。在将任何项目部署到生产环境之前，必须执行以下步骤：验证构建过程、测试浏览器功能、检查移动设备的响应性，并确保没有损坏的链接或图片。
author: gizmolab
version: 1.0.0
tags: [qa, quality, testing, validation, deployment]
---
# 质量保证（QA）检查

这是部署前的强制性质量检查步骤。在任何项目上线之前都必须执行此检查。

## 使用场景

- 在执行 `vercel --prod` 或任何生产环境部署之前
- 在公开/分享项目网址之前
- 在将技能发布到 ClawHub 之前
- 在进行重大代码更改之后

## 质量保证检查清单

### 1. 构建验证
```bash
# Ensure build succeeds without errors
cd <project-dir>
npm run build
```

**失败标准：** 构建过程中出现错误，或提示缺少依赖项。

### 2. 浏览器功能测试

使用浏览器工具验证以下内容：
- [ ] 页面加载时没有控制台错误
- [ ] 所有交互元素（按钮、链接、表单）都能正常使用
- [ ] 图片没有损坏（在“网络”标签页中检查是否有 404 错误）
- [ ] 控制台中没有 JavaScript 错误

```
browser snapshot → check for errors
browser console → verify no red errors
```

### 3. 移动设备响应性测试

```
browser screenshot --mobile
```

检查以下内容：
- [ ] 内容在移动设备上可正常显示
- [ ] 没有需要水平滚动的部分
- [ ] 按钮/链接可点击（尺寸适中）
- [ ] 导航功能正常工作

### 4. 链接验证

```bash
# Check all external links resolve
grep -r "href=" src/ | grep -o 'https://[^"]*' | sort -u | while read url; do
  curl -s -o /dev/null -w "%{http_code} $url\n" "$url"
done
```

### 5. 性能快速检查

- 页面加载时间小于 3 秒
- 代码包大小不超过 500KB
- 图片已优化（不是原始截图）

### 6. SEO/元数据基础检查

在 `index.html` 中验证以下内容：
- [ ] 设置了 `<title>` 标签（非通用标题）
- [ ] 存在 `<meta name="description">` 标签
- [ ] 存在用于社交分享的 `<meta property="og:*">` 标签
- [ ] 有自定义的图标（favicon）

## 部署前命令

```bash
# Run full QA suite
scripts/qa-check.sh <project-dir>
```

## 如果任何检查失败，则禁止部署

如果任何一项检查失败，请：
1. 记录问题
2. 修复问题
3. 重新运行质量保证检查
4. 确认问题解决后再进行部署

## 快速参考

| 检查项目 | 使用工具 | 合格标准 |
|--------|--------|-----------|
| 构建    | `npm run build` | 命令执行成功且无错误 |
| 浏览器    | `browser snapshot` | 控制台无错误 |
| 移动设备 | `browser screenshot` | 页面内容可读且无滚动需求 |
| 链接    | `curl` | 所有请求返回 200 或 301 状态码 |
| 性能    | 浏览器测试 | 页面加载时间小于 3 秒 |
| SEO     | 查看 `index.html` | 所有元数据均存在 |

## 部署后的验证

部署完成后，务必执行以下操作：
1. 在浏览器中访问项目的生产环境网址
2. 测试主要功能
3. 检查移动设备上的显示效果
4. 确认分析数据（如果已启用）是否正常加载

只有在完成以上步骤后，才能公开/分享该项目。