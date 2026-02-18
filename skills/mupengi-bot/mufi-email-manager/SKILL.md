---
name: mufi-email-manager
description: 韩国风格的电子邮件集成管理工具。支持通过 IMAP/SMTP 协议统一管理 Gmail、Naver、Daum 和 Kakao Mail 等邮箱服务。具备未读邮件汇总功能、关键词过滤、自动回复以及每日邮件摘要生成等功能。
---
# mufi-email-manager

这是一个基于 IMAP/SMTP 的工具，用于统一管理韩国主要的电子邮件服务（Gmail、Naver、Daum、Kakao）。

## 主要功能

- 📬 **多账户管理**：同时管理 Gmail、Naver、Daum 和 Kakao 的邮件账户
- 📊 **智能摘要**：自动汇总并分类未读邮件
- 🔍 **关键词过滤**：自动检测重要邮件（如工作、支付、安全相关）
- 🤖 **自动回复**：使用模板快速回复邮件
- 📰 **每日摘要**：生成每日邮件汇总报告

## 设置

### 环境变量设置

在 `skills` 文件夹中创建 `.env` 文件，或通过环境变量进行配置：

```bash
# 기본 계정 (필수)
DEFAULT_ACCOUNT=gmail  # gmail, naver, daum, kakao 중 선택

# Gmail 계정
GMAIL_USER=your@gmail.com
GMAIL_PASS=your_app_password
GMAIL_IMAP_HOST=imap.gmail.com
GMAIL_IMAP_PORT=993
GMAIL_SMTP_HOST=smtp.gmail.com
GMAIL_SMTP_PORT=587

# 네이버 메일
NAVER_USER=your@naver.com
NAVER_PASS=your_password
NAVER_IMAP_HOST=imap.naver.com
NAVER_IMAP_PORT=993
NAVER_SMTP_HOST=smtp.naver.com
NAVER_SMTP_PORT=587

# 다음(Daum) 메일
DAUM_USER=your@daum.net
DAUM_PASS=your_password
DAUM_IMAP_HOST=imap.daum.net
DAUM_IMAP_PORT=993
DAUM_SMTP_HOST=smtp.daum.net
DAUM_SMTP_PORT=465

# 카카오(Kakao) 메일
KAKAO_USER=your@kakao.com
KAKAO_PASS=your_password
KAKAO_IMAP_HOST=imap.kakao.com
KAKAO_IMAP_PORT=993
KAKAO_SMTP_HOST=smtp.kakao.com
KAKAO_SMTP_PORT=465

# 필터 키워드 (쉼표로 구분)
IMPORTANT_KEYWORDS=결제,청구,납부,계약,승인,보안,비밀번호,urgent,invoice
SPAM_KEYWORDS=광고,홍보,이벤트,쿠폰,할인

# 다이제스트 설정
DIGEST_ENABLED=true
DIGEST_TIME=09:00
DIGEST_RECIPIENTS=your@gmail.com
```

## 韩国电子邮件服务器信息

| 服务 | IMAP 服务器 | IMAP 端口 | SMTP 服务器 | SMTP 端口 | 备注 |
|--------|-----------|-----------|-----------|-----------|------|
| Gmail | imap.gmail.com | 993 | smtp.gmail.com | 587 | 使用两步验证时需要应用密码 |
| Naver | imap.naver.com | 993 | smtp.naver.com | 587 | 需要启用 IMAP/SMTP 设置 |
| Daum | imap.daum.net | 993 | smtp.daum.net | 465 | 使用 SSL |
| Kakao | imap.kakao.com | 993 | smtp.kakao.com | 465 | 使用 SSL |
| Hanmail | imap.daum.net | 993 | smtp.daum.net | 465 | 与 Daum 设置相同 |

**注意：**
- **Gmail**：使用两步验证时必须使用应用密码。
- **Naver**：需要在邮件设置中启用 IMAP/SMTP 功能。
- **Daum/Kakao**：SMTP 端口为 465（直接使用 SSL 连接）。

## 命令

### 1. 查看统一邮件

查看所有账户的未读邮件：

```bash
node scripts/check-all.js [--limit 20]
```

仅查看特定账户的邮件：

```bash
node scripts/check.js --account gmail [--limit 10]
node scripts/check.js --account naver [--limit 10]
```

### 2. 智能摘要

根据关键词对未读邮件进行分类和汇总：

```bash
node scripts/summary.js [--account gmail] [--recent 24h]
```

**输出示例：**
```
📬 읽지 않은 메일 요약 (Gmail)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 중요 (3건)
  - [결제] 카드 승인 내역 안내 (신한카드)
  - [보안] 새로운 기기에서 로그인 시도 (Google)
  - [업무] 프로젝트 마감 알림 (팀장님)

🟡 일반 (12건)
  - 주간 뉴스레터 (Tech News)
  - 배송 완료 알림 (쿠팡)
  ...

🔵 읽을만한 (5건)
  - 친구 초대장 (Facebook)
  ...
```

### 3. 重要邮件过滤

仅提取关键词标记的重要邮件：

```bash
node scripts/filter.js --keywords "결제,청구,승인" [--account all] [--recent 7d]
```

### 4. 自动回复

使用模板快速回复邮件：

```bash
# 템플릿 목록
node scripts/reply.js --list

# 템플릿 사용
node scripts/reply.js --uid 12345 --template thanks --account gmail

# 커스텀 답장
node scripts/reply.js --uid 12345 --body "감사합니다." --account gmail
```

**默认模板：**
- `thanks`：表示感谢
- `confirm`：表示确认收到
- `meeting`：表示安排会议
- `ooo`：表示不在办公时间

### 5. 每日摘要

生成每日邮件汇总报告：

```bash
node scripts/digest.js [--date 2026-02-16] [--accounts gmail,naver]
```

**输出格式：**
- 文本报告
- 可选择通过 HTML 邮件发送
- 支持 JSON 格式

### 6. 发送邮件

提供统一的邮件发送接口：

```bash
node scripts/send.js \
  --account gmail \
  --to recipient@example.com \
  --subject "안녕하세요" \
  --body "메일 본문입니다." \
  [--attach file.pdf]
```

### 7. 搜索

在所有账户中统一搜索邮件：

```bash
node scripts/search.js \
  --query "프로젝트" \
  [--accounts gmail,naver] \
  [--recent 30d] \
  [--limit 50]
```

## 模板定制

可以在 `scripts/templates.json` 文件中修改回复模板：

```json
{
  "thanks": {
    "subject": "Re: {original_subject}",
    "body": "안녕하세요,\n\n메일 감사합니다.\n확인 후 회신 드리겠습니다.\n\n감사합니다."
  },
  "confirm": {
    "subject": "Re: {original_subject}",
    "body": "확인 완료했습니다.\n추가 문의 사항 있으시면 연락 주세요."
  }
}
```

## 定时任务示例

- 每天早上 9 点发送每日摘要：
```bash
0 9 * * * cd /path/to/mufi-email-manager && node scripts/digest.js --send
```

- 每 30 分钟检查一次重要邮件：
```bash
*/30 * * * * cd /path/to/mufi-email-manager && node scripts/filter.js --keywords "긴급,urgent" --notify
```

## 安装

```bash
cd skills/mufi-email-manager
npm install
```

## 安全注意事项

- 将 `.env` 文件添加到 `.gitignore` 文件中
- 建议使用 Gmail 的应用密码
- 不要将密码硬编码在代码中
- 注意不要自动删除重要邮件

## 故障排除

**连接失败：**
- 检查服务器地址和端口
- 检查防火墙设置

**认证失败：**
- 重新确认电子邮件地址和密码
- 对于 Gmail，确认是否使用了应用密码
- 对于 Naver，确认是否启用了 IMAP/SMTP 设置

**TLS/SSL 错误：**
- Daum/Kakao 使用 SMTP 端口 465（直接使用 SSL 连接）
- Gmail/Naver 使用 SMTP 端口 587（启用 STARTTLS）

## 许可证

MIT 许可证