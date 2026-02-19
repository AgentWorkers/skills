---
name: email-design
description: "电子邮件营销设计：包括布局模式、邮件主题行生成规则以及邮件发送效果优化策略。内容涵盖欢迎邮件、促销邮件、交易类邮件的模板设计，同时注重移动设备的适配性。适用于电子邮件营销、新闻通讯制作、持续邮件发送（drip campaign）等场景。相关术语包括：电子邮件设计（email design）、邮件模板（email template）、电子邮件营销（email marketing）、新闻通讯设计（newsletter design）、邮件布局（email layout）、邮件活动（email campaign）、欢迎邮件（welcome email）、促销邮件（promotional email）、交易类邮件（transactional email）、邮件主题行（email subject line）、邮件标题图片（email header image）以及邮件横幅（email banner）。"
allowed-tools: Bash(infsh *)
---
# 电子邮件设计

通过 [inference.sh](https://inference.sh) 命令行工具，利用 AI 生成的视觉元素来设计转化率高的营销邮件。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Generate email header banner
infsh app run infsh/html-to-image --input '{
  "html": "<div style=\"width:600px;height:250px;background:linear-gradient(135deg,#667eea,#764ba2);display:flex;align-items:center;justify-content:center;font-family:system-ui;color:white;text-align:center\"><div><h1 style=\"font-size:36px;margin:0\">Spring Sale — 30% Off</h1><p style=\"font-size:18px;opacity:0.9\">This weekend only</p></div></div>"
}'
```

> **安装说明：** [安装脚本](https://cli.inference.sh) 仅会检测您的操作系统和架构，然后从 `dist.inference.sh` 下载相应的二进制文件，并验证其 SHA-256 校验和。无需提升权限或后台进程。也可以选择 [手动安装与验证](https://dist.inference.sh/cli/checksums.txt)。

## 电子邮件宽度与布局

| 约束条件 | 值 | 原因 |
|-----------|-------|-----|
| **最大宽度** | 600px | Gmail 和 Outlook 的渲染标准 |
| **移动设备宽度** | 320-414px | 为移动设备提供响应式布局 |
| **单列布局** | 更推荐 | 适用于移动设备的显示 |
| **双列布局** | 尽量少用 | 在许多客户端上会导致布局混乱 |
| **图片宽度** | 最大 600px，双列布局时为 300px | 对于 Retina 显示屏，应提供 1200px 的高分辨率图片 |
| **字体大小（正文）** | 14-16px | 小于 14px 时在移动设备上难以阅读 |
| **字体大小（标题）** | 22-28px | 需要确保可扫描 |
| **行高** | 1.5 | 保证所有设备上的可读性 |

### 倒金字塔布局

这种最有效的电子邮件布局能将用户的注意力集中在一个主要的行动号召（CTA）上：

```
┌──────────────────────────────────┐
│           HEADER IMAGE           │  ← Brand/visual hook
│          (600 x 200-300)         │
├──────────────────────────────────┤
│                                  │
│     Headline (one line)          │  ← What's this about
│                                  │
│     2-3 sentences of body copy   │  ← Why should I care
│     explaining the value.        │
│                                  │
│        ┌──────────────┐          │
│        │   CTA BUTTON  │         │  ← One clear action
│        └──────────────┘          │
│                                  │
├──────────────────────────────────┤
│     Footer: Unsubscribe link     │
└──────────────────────────────────┘
```

## 主题行

### 有效的公式

| 公式 | 例子 | 开启率影响 |
|---------|---------|-----------------|
| 数字 + 好处 | “5 种方法将构建时间缩短一半” | 高 |
| 问题 | “您还在周五进行部署吗？” | 高 |
| 操作指南 | “三步自动完成报告” | 中等偏高 |
| 紧急性（真实的） | “最后一天：年度计划享受 70% 的折扣” | 高（如果是真实的） |
| 个性化 | “[姓名]，您的每周报告已准备好” | 非常高 |
| 好奇心触发 | “用户们热议的那一项功能” | 中等偏高 |

### 规则

| 规则 | 值 |
|------|-------|
| **长度** | 30-50 个字符（移动设备通常会截断到 35 个字符） |
| **预览文本** | 主题行后的前 40-100 个字符——请精心设计这部分内容 |
| **表情符号** | 最多使用 1 个，放在开头或结尾，根据受众测试 |
| **全部大写** | 绝对不要使用——会触发垃圾邮件过滤器 |
| **垃圾邮件触发词** | 避免在主题中使用 “免费”、“立即行动”、“限时优惠”、“点击这里” 等词汇 |
| **个性化** | 在主题中包含收件人的名字，可以提高开启率 20% 以上 |

### 预览文本

预览文本会显示在收件箱中的主题行之后。请不要忽视这部分内容。

```
❌ "View this email in your browser" (default, wasted space)
❌ "Having trouble viewing this?" (no one cares)

✅ Subject: "5 ways to cut build time"
   Preview: "Number 3 saved us 6 hours per week"

✅ Subject: "Your monthly report is ready"
   Preview: "Revenue up 23% — here's what drove it"
```

## 电子邮件类型

### 欢迎邮件（自动发送，注册当天）

| 元素 | 内容 |
|---------|---------|
| 主题 | “欢迎使用 [产品] — 接下来会发生什么” |
| 标题 | 品牌图片或产品截图 |
| 正文 | 3-4 句话：用户注册的目的、预期体验以及一个快速的操作指南 |
| 行动号召 | “完成设置” 或 “尝试您的第一个 [操作]” |
| 发送时间 | 注册后立即发送 |

### 促销/活动邮件

| 元素 | 内容 |
|---------|---------|
| 主题 | 强调好处，必要时加入紧迫感 |
| 标题 | 显示优惠或结果的图片 |
| 正文 | 问题 → 解决方案 → 优惠 → 截止时间 |
| 行动号召 | “享受 70% 的折扣” 或 “开始免费试用” |
| 紧急性 | 提供真实的截止时间，避免虚假的稀缺感 |

### 产品更新/变更日志

| 元素 | 内容 |
|---------|---------|
| 主题 | “新功能：[功能名称] 已上线” |
| 标题 | 新功能的截图或视觉展示 |
| 正文 | 新功能的内容、重要性以及使用方法 |
| 行动号召 | “尝试 [新功能]”

### 交易类邮件（收据、确认邮件）

| 规则 | 原因 |
|------|-----|
| 主题中明确说明目的 | “您的订单 #1234 已确认” |
| 设计简洁 | 避免与营销邮件混淆 |
| 重要信息放在页面上方 | 包含订单编号、金额和日期 |
| 减少促销内容 | CAN-SPAM 规则允许少量促销信息，但要保持简洁 |

## 标题图片设计

```bash
# Welcome email header
infsh app run infsh/html-to-image --input '{
  "html": "<div style=\"width:600px;height:250px;background:linear-gradient(135deg,#2d3436,#636e72);display:flex;align-items:center;padding:40px;font-family:system-ui;color:white\"><div><p style=\"font-size:14px;text-transform:uppercase;letter-spacing:2px;opacity:0.7;margin:0\">Welcome to</p><h1 style=\"font-size:42px;margin:8px 0 0;font-weight:800\">DataFlow</h1><p style=\"font-size:18px;opacity:0.8;margin-top:4px\">Your data, automated</p></div></div>"
}'

# Sale / promotional header
infsh app run infsh/html-to-image --input '{
  "html": "<div style=\"width:600px;height:300px;background:linear-gradient(135deg,#e74c3c,#c0392b);display:flex;align-items:center;justify-content:center;font-family:system-ui;color:white;text-align:center\"><div><p style=\"font-size:20px;opacity:0.9;margin:0\">This Weekend Only</p><h1 style=\"font-size:72px;margin:8px 0;font-weight:900\">30% OFF</h1><p style=\"font-size:18px;opacity:0.8\">All annual plans. Ends Sunday.</p></div></div>"
}'

# Feature announcement header with AI visual
infsh app run falai/flux-dev-lora --input '{
  "prompt": "clean modern email header banner, abstract flowing data visualization, dark blue gradient background, subtle glowing nodes and connections, tech aesthetic, minimal, no text, 600x250 equivalent",
  "width": 1200,
  "height": 500
}'
```

## 行动号召按钮

| 规则 | 值 |
|------|-------|
| **宽度** | 200-300px，不要占满整个屏幕 |
| **高度** | 最小 44-50px（确保可点击） |
| **颜色** | 与背景有高对比度 |
| **文本** | 行动动词 + 结果：例如 “开始免费试用” |
| **形状** | 圆角（边框半径 4-8px） |
| **位置** | 放在页面上方；长邮件时在底部重复显示 |
| **数量** | 每封邮件中只有一个主要的行动号召按钮 |

### 兼容性强的按钮

HTML 按钮在不同电子邮件客户端上的显示效果可能不同。请使用 “兼容性强的按钮” 技术（Outlook 使用 VML，其他客户端使用 HTML/CSS）：

```html
<!-- Bulletproof button (works everywhere including Outlook) -->
<table cellpadding="0" cellspacing="0" border="0">
  <tr>
    <td align="center" bgcolor="#22c55e" style="border-radius:6px;">
      <a href="https://yoursite.com/action" target="_blank"
         style="font-size:16px;font-family:sans-serif;color:#ffffff;
                text-decoration:none;padding:12px 24px;display:inline-block;
                font-weight:bold;">
        Start Free Trial
      </a>
    </td>
  </tr>
</table>
```

## 移动设备优化

| 规则 | 原因 |
|------|-----|
| 单列布局 | 双列布局在移动设备上会导致显示混乱 |
| 字体大小至少 14px | 过小的字体难以阅读 |
| 行动号召按钮高度至少 44px | 保证在苹果和安卓设备上可点击 |
| 图片宽度调整为 100% | 避免水平滚动 |
| 元素垂直排列 | 在窄屏幕上避免并排显示 |
| 在 Gmail 应用、Apple Mail 和 Outlook 上进行测试 | 这三个是最常用的电子邮件客户端 |

**超过 60% 的电子邮件是在移动设备上打开的。** 请优先考虑移动设备的显示效果。

## 邮件送达率检查清单

| 因素 | 规则 |
|--------|------|
| 图片与文本的比例 | 图片占比不超过 40%，文本占比 60%（垃圾邮件过滤器会标记图片过多的邮件） |
| 图片的替代文本 | 必须添加——许多客户端默认会屏蔽图片 |
| 取消订阅链接 | 根据 CAN-SPAM 和 GDPR 法规要求，必须提供方便的取消订阅链接 |
| 发件人名称 | 使用易于识别的个人或品牌名称 |
| 回复地址 | 使用真实的地址，不要使用 no-reply@（会影响邮件送达率） |
| 邮件列表管理 | 定期清除无效订阅者 |
| SPF/DKIM/DMARC | 技术认证——设置一次，对邮件送达率至关重要 |

## 常见错误

| 错误 | 问题 | 解决方法 |
|---------|---------|-----|
| 无预览文本 | 显示 “在浏览器中查看” 或随机代码 | 请设置明确的预览文本 |
| 仅包含图片的邮件 | 图片被屏蔽会导致邮件显示为空白，增加垃圾邮件风险 | 图片占比不超过 60%，并添加替代文本 |
| 多个行动号召 | 使用户困惑，降低点击率 | 每封邮件中只有一个主要的行动号召 |
| 文字过小 | 在移动设备上难以阅读 | 正文字体大小至少 14px，标题字体大小至少 22px |
| 使用 no-reply@ 作为发件人地址 | 会影响邮件送达率，显得不专业 | 使用真实的回复地址 |
| 未进行移动设备测试 | 60% 以上的用户会在移动设备上打开邮件，因此必须进行测试 | 在 Gmail 应用和 Apple Mail 上进行测试 |
| 未提供取消订阅链接 | 违反 CAN-SPAM 规则，容易引发投诉 | 在页脚提供明确的取消订阅链接 |
| 设计过于复杂 | 不同电子邮件客户端对 CSS 的解析方式不一致 | 保持布局简单，使用内联样式 |
| 虚假的紧迫感 | 会降低用户的信任度 | 只使用真实的截止时间信息 |

## 相关技能

```bash
npx skills add inference-sh/skills@landing-page-design
npx skills add inference-sh/skills@ai-image-generation
npx skills add inference-sh/skills@prompt-engineering
```

查看所有可用工具：`infsh app list`