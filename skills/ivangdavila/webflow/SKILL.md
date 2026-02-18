---
name: Webflow
slug: webflow
version: 1.0.0
description: 构建、发布并优化采用响应式设计、内容管理系统（CMS）架构的 Webflow 网站，同时确保项目交付的流程清晰、高效。
metadata: {"clawdbot":{"emoji":"🌐","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 快速参考

| 主题 | 文件 |
|-------|------|
| 响应式设计、断点设置 | `design.md` |
| 内容管理系统（CMS）集合、无头API | `cms.md` |
| 表单、数据分析、第三方集成 | `integrations.md` |
| 搜索引擎优化（SEO）、性能优化、可访问性 | `optimization.md` |

## 内存存储

用户偏好设置存储在 `~/webflow/memory.md` 文件中。系统激活后会自动读取这些设置。

**格式：**
```markdown
# Webflow Memory

## Profile
- role: freelancer | agency | founder | developer | marketer
- design-source: figma | sketch | from-scratch | template
- cms-needs: none | blog | multi-collection | headless

## Preferences
- class-naming: bem | utility | semantic
- breakpoints: mobile-first | desktop-first
```

首次使用时，请创建以下文件夹：`mkdir -p ~/webflow`

## 重要规则

1. **务必检查所有断点设置** — 桌面版的显示效果可能很好，但移动端的显示可能出问题。在向客户展示之前，务必测试平板设备、横屏模式和竖屏模式下的显示效果。
2. **为类名赋予有意义的名称** — 例如使用 `hero-heading` 而不是 `heading-23`。这样在项目交接时你会感到更加方便。
3. **在添加内容之前先设置好CMS** — 先定义内容集合、字段以及它们之间的关系。之后再迁移内容会非常麻烦。
4. **准确计算实际托管成本** — 基础托管服务、CMS托管服务以及业务级托管服务的费用是不同的。表单、CMS内容以及测试环境的搭建都会额外产生费用。
5. **使用真实数据测试表单功能** — Webflow的表单通知功能可能存在问题（例如无法正常发送通知），因此在发布前务必验证表单的提交功能是否正常。
6. **切勿依赖自动生成的响应式布局** — Webflow的自动调整可能不准确，必须手动调整断点设置。
7. **发布前进行全面审核** — 检查是否有缺失的alt文本、404错误页面、失效的链接、错误的favicon图标、OG图片、未启用的SSL证书以及错误的重定向设置。每次发布前都使用预发布检查清单。
8. **导出代码后需要进行清理** — Webflow导出的HTML和CSS文件通常会比较冗余。如果需要将项目迁移到其他平台，务必预留时间进行代码清理。

## 范围

本技能涵盖了Webflow的设计、开发及项目管理方面。关于通用网页设计原则，请参阅 `ui-design`；关于 landing page 的转换策略，请参阅 `landing-pages`。