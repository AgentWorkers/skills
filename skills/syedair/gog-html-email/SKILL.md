---
name: gog-html-email
description: 通过 gog CLI，使用模板和样式发送格式精美的 HTML 邮件。
homepage: https://gogcli.sh
metadata:
  {
    "openclaw":
      {
        "emoji": "📧",
        "requires": { "bins": ["gog"] }
      }
  }
---
# gog-html-email

为 gog CLI 提供了增强型的 HTML 电子邮件格式化功能，附带了现成的模板可供使用。

## 如何发送 HTML 电子邮件

**请始终遵循以下工作流程：**

1. 从 `workspace/skills/gog-html-email/templates/` 目录中读取相应的模板文件。
2. 使用 `sed` 命令替换模板中的占位符。
3. 通过 `gog gmail send --body-html` 命令发送电子邮件。

**示例：**
```bash
TEMPLATE=$(cat workspace/skills/gog-html-email/templates/basic.html)
HTML=$(echo "$TEMPLATE" | sed 's/\[NAME\]/John/g' | sed 's/\[MESSAGE\]/Your message here/g' | sed 's/\[SIGNATURE\]/Your Name/g')
gog gmail send --to recipient@example.com --subject "Subject" --body-html "$HTML"
```

**多段文本邮件的示例：**
```bash
TEMPLATE=$(cat workspace/skills/gog-html-email/templates/basic.html)
# Replace [MESSAGE] with multiple <p> tags for proper spacing
MESSAGE='<p style="margin: 0 0 16px 0;">First paragraph.</p><p style="margin: 0 0 16px 0;">Second paragraph.</p><p style="margin: 0 0 16px 0;">Third paragraph.</p>'
HTML=$(echo "$TEMPLATE" | sed "s|\[MESSAGE\]|$MESSAGE|g" | sed 's/\[NAME\]/John/g' | sed 's/\[SIGNATURE\]/Your Name/g')
gog gmail send --to recipient@example.com --subject "Subject" --body-html "$HTML"
```

**请避免以下操作：**
- 手动构建 HTML 字符串。
- 使用 heredocs 或多行字符串。
- 在 HTML 中直接插入 `\n` 字符。
- 将多段文本放在一个 `<p>` 标签内。

## 模板选择指南

根据邮件用途选择合适的模板：

**商务/专业用途：**
- `basic.html` - 简单的专业电子邮件
- `meeting.html` - 会议邀请（需要填写：姓名、主题、日期、时间、时长、地点、签名）
- `follow-up.html` - 回访邮件
- `status-update.html` - 项目更新邮件
- `invoice.html` - 发票和付款通知
- `button.html` - 包含行动号召按钮的电子邮件
- `newsletter.html` - 通讯邮件

**伊斯兰/宗教用途：**
- `jummah.html` - 主麻日祝福邮件（Jummah Mubarak）
- `eid.html` - 开斋节祝福邮件（Eid Mubarak）
- `ramadan.html` - 斋月祝福邮件（Ramadan Mubarak）

**庆祝用途：**
- `birthday.html` - 生日祝福邮件
- `anniversary.html` - 周年纪念邮件
- `congratulations.html` - 祝贺邮件
- `new-year.html` - 新年祝福邮件（需要填写：姓名、祝福语、年份、签名）

**其他用途：**
- `welcome.html` - 欢迎新用户邮件
- `thank-you.html` - 感谢邮件
- `highlight.html` - 重要公告邮件
- `multi-paragraph.html` - 多段文本邮件

## HTML 模板文件

所有模板都位于 `templates/` 目录中。每个模板都使用了 `[BRACKETS]` 中的占位符，您可以将这些占位符替换为实际内容。

### 可用的模板

1. **basic.html** - 简单的专业电子邮件
   - 占位符：`[NAME]`, `[MESSAGE]`, `[SIGNATURE]`

2. **highlight.html** - 包含高亮区域的电子邮件
   - 占位符：`[NAME]`, `[HIGHLIGHT_MESSAGE]`, `[MESSAGE]`, `[SIGNATURE]`

3. **button.html** - 包含行动号召按钮的电子邮件
   - 占位符：`[NAME]`, `[MESSAGE]`, `[BUTTON_URL]`, `[BUTTON_TEXT]`, `[SIGNATURE]`

4. **multi-paragraph.html** - 多段文本电子邮件
   - 占位符：`[NAME]`, `[PARAGRAPH_1]`, `[PARAGRAPH_2]`, `[PARAGRAPH_3]`, `[SIGNATURE]`

5. **meeting.html** - 会议邀请邮件
   - 占位符：`[NAME]`, `[TOPIC]`, `[DATE]`, `[TIME]`, `[DURATION]`, `[LOCATION]`, `[SIGNATURE]`

6. **follow-up.html** - 回访邮件
   - 占位符：`[NAME]`, `[TOPIC]`, `[MESSAGE]`, `[SIGNATURE]`

7. **newsletter.html** - 通讯邮件格式
   - 占位符：`[NEWSLETTER_TITLE]`, `[DATE]`, `[SECTION_1_TITLE]`, `[SECTION_1_CONTENT]`, `[SECTION_2_TITLE]`, `[SECTION_2_CONTENT]`

8. **invoice.html** - 发票通知邮件
   - 占位符：`[NAME]`, `[INVOICE_NUMBER]`, `[DATE]`, `[AMOUNT]`, `[DUE_DATE]`, `[DESCRIPTION]`, `[PAYMENT_URL]`, `[SIGNATURE]`

9. **welcome.html** - 带有行动号召的欢迎邮件
   - 占位符：`[NAME]`, `[MESSAGE]`, `[GETstarted_URL]`, `[SIGNATURE]`

10. **status-update.html** - 项目状态更新邮件
    - 占位符：`[NAME]`, `[PROJECT_NAME]`, `[COMPLETED_ITEMS]`, `[IN_PROGRESS_ITEMS]`, `[BLOCKED_ITEMS]`, `[NEXT_STEPS]`, `[SIGNATURE]`

### 特殊场合模板

11. **jummah.html** - 主麻日祝福邮件
    - 占位符：`[NAME]`, `[MESSAGE]`, `[SIGNATURE]`
    - 特点：蓝色渐变背景的伊斯兰祝福语

12. **eid.html** - 开斋节祝福邮件
    - 占位符：`[NAME]`, `[MESSAGE]`, `[SIGNATURE]`
    - 特点：绿色渐变背景和伊斯兰祝福语

13. **ramadan.html** - 斋月祝福邮件
    - 占位符：`[NAME]`, `[MESSAGE]`, `[SIGNATURE]`
    - 特点：紫色渐变背景和斋月祝福语

14. **birthday.html** - 生日祝福邮件
    - 占位符：`[NAME]`, `[MESSAGE]`, `[SIGNATURE]`
    - 特点：粉色渐变背景和庆祝表情符号

15. **anniversary.html** - 周年纪念邮件
    - 占位符：`[NAME]`, `[MESSAGE]`, `[SIGNATURE]`
    - 特点：粉黄色渐变背景和浪漫主题

16. **congratulations.html** - 祝贺邮件
    - 占位符：`[NAME]`, `[MESSAGE]`, `[SIGNATURE]`
    - 特点：金蓝色渐变背景和成功主题

17. **thank-you.html** - 感谢邮件
    - 占位符：`[NAME]`, `[MESSAGE]`, `[SIGNATURE]`
    - 特点：柔和的淡色调渐变背景和感激之情

18. **new-year.html** - 新年祝福邮件
    - 占位符：`[NAME]`, `[MESSAGE]`, `[YEAR]`, `[SIGNATURE]`
    - 特点：紫色渐变背景和庆祝主题

### 直接使用模板

```bash
# Read template, replace placeholders, and send
TEMPLATE=$(cat workspace/skills/gog-html-email/templates/basic.html)
HTML=$(echo "$TEMPLATE" | sed 's/\[NAME\]/John/g' | sed 's/\[MESSAGE\]/Your message here/g' | sed 's/\[SIGNATURE\]/Your Name/g')
gog gmail send --to recipient@example.com --subject "Subject" --body-html "$HTML"
```

### 快速示例

**基本电子邮件：**
```bash
TEMPLATE=$(cat workspace/skills/gog-html-email/templates/basic.html)
HTML=$(echo "$TEMPLATE" | sed 's/\[NAME\]/John/g' | sed 's/\[MESSAGE\]/Just wanted to check in on the project status./g' | sed 's/\[SIGNATURE\]/Sarah/g')
gog gmail send --to john@example.com --subject "Project Check-in" --body-html "$HTML"
```

**会议邀请邮件：**
```bash
TEMPLATE=$(cat workspace/skills/gog-html-email/templates/meeting.html)
HTML=$(echo "$TEMPLATE" | sed 's/\[NAME\]/Team/g' | sed 's/\[TOPIC\]/Q1 Planning/g' | sed 's/\[DATE\]/March 15, 2026/g' | sed 's/\[TIME\]/2:00 PM/g' | sed 's/\[DURATION\]/1 hour/g' | sed 's/\[LOCATION\]/Conference Room A/g' | sed 's/\[SIGNATURE\]/Alex/g')
gog gmail send --to team@example.com --subject "Q1 Planning Meeting" --body-html "$HTML"
```

**带按钮的电子邮件：**
```bash
TEMPLATE=$(cat workspace/skills/gog-html-email/templates/button.html)
HTML=$(echo "$TEMPLATE" | sed 's/\[NAME\]/Sarah/g' | sed 's/\[MESSAGE\]/Please review the latest document./g' | sed 's|\[BUTTON_URL\]|https://docs.example.com/report|g' | sed 's/\[BUTTON_TEXT\]/View Document/g' | sed 's/\[SIGNATURE\]/Mike/g')
gog gmail send --to sarah@example.com --subject "Document Review" --body-html "$HTML"
```

**主麻日祝福邮件：**
```bash
TEMPLATE=$(cat workspace/skills/gog-html-email/templates/jummah.html)
HTML=$(echo "$TEMPLATE" | sed 's/\[NAME\]/Ahmed/g' | sed 's/\[MESSAGE\]/Wishing you a blessed Friday filled with peace and blessings./g' | sed 's/\[SIGNATURE\]/Your Name/g')
gog gmail send --to ahmed@example.com --subject "Jummah Mubarak" --body-html "$HTML"
```

**开斋节祝福邮件：**
```bash
TEMPLATE=$(cat workspace/skills/gog-html-email/templates/eid.html)
HTML=$(echo "$TEMPLATE" | sed 's/\[NAME\]/Family/g' | sed 's/\[MESSAGE\]/May this Eid bring joy, happiness, and prosperity to you and your loved ones./g' | sed 's/\[SIGNATURE\]/Your Name/g')
gog gmail send --to family@example.com --subject "Eid Mubarak" --body-html "$HTML"
```

**生日祝福邮件：**
```bash
TEMPLATE=$(cat workspace/skills/gog-html-email/templates/birthday.html)
HTML=$(echo "$TEMPLATE" | sed 's/\[NAME\]/Sarah/g' | sed 's/\[MESSAGE\]/Hope your special day is filled with joy, laughter, and wonderful memories!/g' | sed 's/\[SIGNATURE\]/Your Name/g')
gog gmail send --to sarah@example.com --subject "Happy Birthday!" --body-html "$HTML"
```

## 最佳实践

1. **使用模板文件** - 所有模板都已预先格式化并经过测试。
2. **单行 HTML** - 模板设计为单行格式，以避免格式问题。
3. **内联 CSS** - 所有模板都使用内联样式以确保在各种邮件客户端中显示正常。
4. **最大宽度** - 模板宽度设置为 600px，以获得最佳显示效果。
5. **系统字体** - 模板使用 `-apple-system, BlinkMacSystemFont, Segoe UI, Roboto` 字体以实现最佳显示效果。
6. **先进行测试** - 在发送给收件人之前，先给自己发送测试邮件。
7. **替换所有占位符** - 确保将所有 `[PLACEHOLDER]` 的值替换为实际内容。

## 自定义模板

您可以通过添加额外的 `sed` 命令来更改模板的颜色、字体和样式。

### 常见自定义操作

**更改渐变颜色：**
```bash
TEMPLATE=$(cat workspace/skills/gog-html-email/templates/birthday.html)
# Replace pink gradient with blue gradient
HTML=$(echo "$TEMPLATE" | sed 's/#f093fb/#4facfe/g' | sed 's/#f5576c/#00f2fe/g')
# Then replace placeholders and send
HTML=$(echo "$HTML" | sed 's/\[NAME\]/John/g' | sed 's/\[MESSAGE\]/Your message/g' | sed 's/\[SIGNATURE\]/Your Name/g')
gog gmail send --to recipient@example.com --subject "Subject" --body-html "$HTML"
```

**更改主体颜色：**
```bash
TEMPLATE=$(cat workspace/skills/gog-html-email/templates/basic.html)
# Change all blue (#007bff) to purple (#667eea)
HTML=$(echo "$TEMPLATE" | sed 's/#007bff/#667eea/g')
HTML=$(echo "$HTML" | sed 's/\[NAME\]/John/g' | sed 's/\[MESSAGE\]/Your message/g' | sed 's/\[SIGNATURE\]/Your Name/g')
gog gmail send --to recipient@example.com --subject "Subject" --body-html "$HTML"
```

**更改背景颜色：**
```bash
TEMPLATE=$(cat workspace/skills/gog-html-email/templates/highlight.html)
# Change highlight box from light gray to light blue
HTML=$(echo "$TEMPLATE" | sed 's/#f8f9fa/#e3f2fd/g')
HTML=$(echo "$HTML" | sed 's/\[NAME\]/John/g' | sed 's/\[MESSAGE\]/Your message/g' | sed 's/\[SIGNATURE\]/Your Name/g')
gog gmail send --to recipient@example.com --subject "Subject" --body-html "$HTML"
```

**更改字体大小：**
```bash
TEMPLATE=$(cat workspace/skills/gog-html-email/templates/basic.html)
# Make heading larger (36px to 48px)
HTML=$(echo "$TEMPLATE" | sed 's/font-size: 36px/font-size: 48px/g')
HTML=$(echo "$HTML" | sed 's/\[NAME\]/John/g' | sed 's/\[MESSAGE\]/Your message/g' | sed 's/\[SIGNATURE\]/Your Name/g')
gog gmail send --to recipient@example.com --subject "Subject" --body-html "$HTML"
```

**更改布局对齐方式（从居中改为左对齐）：**
```bash
TEMPLATE=$(cat workspace/skills/gog-html-email/templates/basic.html)
# Remove centering: change "margin: 0 auto" to "margin: 0"
HTML=$(echo "$TEMPLATE" | sed 's/margin: 0 auto/margin: 0/g')
HTML=$(echo "$HTML" | sed 's/\[NAME\]/John/g' | sed 's/\[MESSAGE\]/Your message/g' | sed 's/\[SIGNATURE\]/Your Name/g')
gog gmail send --to recipient@example.com --subject "Subject" --body-html "$HTML"
```

### 颜色调色板参考

**当前模板的颜色设置：**

**生日（粉色）：**
- 渐变：`#f093fb` → `#f5576c`
- 标题颜色：`#f5576c`

**开斋节（绿色）：**
- 渐变：`#11998e` → `#38ef7d`
- 标题颜色：`#11998e`

**主麻日（蓝色）：**
- 渐变：`#4facfe` → `#00f2fe`
- 标题颜色：`#4facfe`

**斋月（紫色）：**
- 渐变：`#667eea` → `#764ba2`
- 标题颜色：`#667eea`

**周年纪念（粉黄色）：**
- 渐变：`#fa709a` → `#fee140`
- 标题颜色：`#fa709a`

**祝贺（金蓝色）：**
- 渐变：`#ffd89b` → `#19547b`
- 标题颜色：`#19547b`

**感谢（淡色调）：**
- 渐变：`#a8edea` → `#fed6e3`
- 标题颜色：`#a8edea` → `#fed6e3`

**新年（紫色）：**
- 渐变：`#667eea` → `#764ba2`
- 标题颜色：`#667eea`

**推荐的替代调色板：**
- 海洋（Ocean）：`#2E3192` → `#1BFFFF`
- 日落（Sunset）：`#FF512F` → `#F09819`
- 森林（Forest）：`#134E5E` → `#71B280`
- 皇家（Royal）：`#8E2DE2` → `#4A00E0`
- 温暖（Warm）：`#FF6B6B` → `#FFE66D`
- 凉爽（Cool）：`#4ECDC4` → `#556270`

### 高级自定义

**多色调整：**
```bash
TEMPLATE=$(cat workspace/skills/gog-html-email/templates/birthday.html)
# Change to ocean theme
HTML=$(echo "$TEMPLATE" | \
  sed 's/#f093fb/#2E3192/g' | \
  sed 's/#f5576c/#1BFFFF/g' | \
  sed 's/\[NAME\]/John/g' | \
  sed 's/\[MESSAGE\]/Your message/g' | \
  sed 's/\[SIGNATURE\]/Your Name/g')
gog gmail send --to recipient@example.com --subject "Subject" --body-html "$HTML"
```

**创建自定义模板变体：**
```bash
# Save customized version as new template
TEMPLATE=$(cat workspace/skills/gog-html-email/templates/birthday.html)
echo "$TEMPLATE" | sed 's/#f093fb/#2E3192/g' | sed 's/#f5576c/#1BFFFF/g' > workspace/skills/gog-html-email/templates/birthday-ocean.html
# Now use the custom template
TEMPLATE=$(cat workspace/skills/gog-html-email/templates/birthday-ocean.html)
HTML=$(echo "$TEMPLATE" | sed 's/\[NAME\]/John/g' | sed 's/\[MESSAGE\]/Your message/g' | sed 's/\[SIGNATURE\]/Your Name/g')
gog gmail send --to recipient@example.com --subject "Subject" --body-html "$HTML"
```

## 注意事项：

- 模板采用单行 HTML 格式，以避免格式问题。
- 对于复杂的布局（如表格或多段文本），请创建自定义模板文件。
- 在多个邮件客户端（Gmail、Outlook、Apple Mail）中测试 HTML 邮件。
- 对于不需要格式化的简单邮件，可以使用纯文本格式（`--body` 参数）。