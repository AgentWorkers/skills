---
name: cs-autoresponder
description: 多渠道客户服务自动回复系统，具备常见问题解答（FAQ）匹配功能、问题升级机制以及每日工作汇总功能。
homepage: https://github.com/openclaw/skills
metadata:
  {
    "openclaw":
      {
        "emoji": "🎧",
        "requires": { "bins": ["node"] },
        "install":
          [
            {
              "id": "node-brew",
              "kind": "brew",
              "formula": "node",
              "bins": ["node"],
              "label": "Install Node.js (brew)",
            },
          ],
      },
  }
---
# 🎧 CS自动回复系统

这是一个专为客服设计的自动回复工具，能够接收来自多渠道的客户咨询，并提供基于FAQ的自动回复、问题升级以及每日咨询汇总服务。

## 主要功能

1. **多渠道接收**：支持检测来自Kakao Talk通知、Instagram私信、电子邮件等渠道的客户咨询。
2. **FAQ匹配**：根据客户公司的FAQ数据库（JSON格式），通过语义匹配提供自动回复。
3. **问题升级**：当检测到复杂或棘手的咨询时，会通过Discord或Kakao Talk向相关负责人发送通知。
4. **回复语气定制**：能够根据客户公司的品牌形象生成符合其风格的语气回复。
5. **日志记录**：保存所有客服对话的日志（按日分类）。
6. **每日报表**：提供每日客服工作汇总（包括总咨询量、自动处理率、升级次数等）。

## 初始设置

### 1. 创建客户公司配置文件

```bash
cd {baseDir}
cp config/template.json config/고객사명.json
```

编辑 `config/客户公司名称.json` 文件：
- `clientId`：唯一标识符
- `name`：客户公司名称
- `channels`：需要关联的渠道（Kakao、Instagram、电子邮件）
- `tone`：回复语气（正式、友好、随意）
- `escalationTarget`：Discord频道ID或Kakao Talk联系人号码
- `faqPath`：FAQ数据库文件路径

### 2. 创建FAQ数据库

```bash
cp config/faq-template.json config/고객사명-faq.json
```

添加FAQ条目（JSON数组格式）：
```json
[
  {
    "id": "faq001",
    "question": "영업시간이 어떻게 되나요?",
    "keywords": ["영업시간", "몇시", "언제", "운영"],
    "answer": "저희는 평일 10:00-22:00, 주말 12:00-20:00 영업합니다.",
    "category": "운영정보"
  }
]
```

## 使用方法

### 启动渠道监控

```bash
node {baseDir}/scripts/monitor.js --config config/고객사명.json
```

建议使用`pm2`在后台运行该脚本：
```bash
pm2 start {baseDir}/scripts/monitor.js --name cs-mufi -- --config config/고객사명.json
pm2 logs cs-mufi
```

### 手动测试回复功能

```bash
node {baseDir}/scripts/respond.js \
  --config config/고객사명.json \
  --channel instagram \
  --user "iam.dawn.kim" \
  --message "영업시간 알려주세요"
```

### 查看每日报表

```bash
node {baseDir}/scripts/dashboard.js --config config/고객사명.json --date 2026-02-18
```

### 手动触发问题升级

```bash
node {baseDir}/scripts/escalate.js \
  --config config/고객사명.json \
  --channel instagram \
  --user "angry_customer" \
  --message "환불 요청합니다" \
  --reason "환불 요청"
```

## 目录结构

```
cs-autoresponder/
├── SKILL.md
├── scripts/
│   ├── monitor.js       # 채널 모니터링 메인 루프
│   ├── respond.js       # FAQ 매칭 & 자동 응답
│   ├── escalate.js      # 에스컬레이션 알림
│   └── dashboard.js     # 일일 요약 대시보드
├── lib/
│   ├── channels.js      # 채널 어댑터 (mock API)
│   ├── matcher.js       # 의미 기반 FAQ 매칭
│   └── logger.js        # 대화 로그 기록
├── config/
│   ├── template.json    # 고객사 설정 템플릿
│   └── faq-template.json # FAQ DB 템플릿
└── logs/
    └── YYYY-MM-DD/      # 일별 대화 로그 (clientId별)
```

## 渠道适配器（模拟接口）

目前使用模拟API进行测试。在生产环境中，需要修改 `lib/channels.js` 文件：
- **Kakao Talk**：使用Kakao Alimtalk API
- **Instagram**：利用 `tools/insta-cli/v2.js` 模块
- **电子邮件**：使用himalaya或Gmail API

## 基于语义的匹配逻辑

`lib/matcher.js` 使用简单的关键词匹配机制：
1. 将客户咨询内容转换为小写。
2. 与FAQ中的关键词进行比较（部分匹配也算有效）。
3. 计算匹配得分（多个关键词匹配时得分增加）。
4. 如果得分高于0.6，则自动回复；否则将问题升级。

在生产环境中，建议使用OpenAI Embeddings或Claude等更强大的自然语言处理工具。

## 问题升级条件

满足以下任一条件时，系统会自动升级问题：
- FAQ匹配得分低于0.6
- 检测到负面关键词（如“退款”、“投诉”、“非常失望”等）
- 客户请求联系“负责人”、“经理”或“总经理”
- 同一客户连续发送3次相同咨询

## 日志格式

日志文件格式为：`logs/YYYY-MM-DD/{clientId}.jsonl`
```jsonl
{"timestamp":"2026-02-18T12:34:56.789Z","channel":"instagram","user":"iam.dawn.kim","message":"영업시간?","response":"평일 10-22시 영업합니다","faqId":"faq001","score":0.85,"escalated":false}
{"timestamp":"2026-02-18T12:40:11.123Z","channel":"kakao","user":"010-1234-5678","message":"환불하고 싶어요","response":null,"faqId":null,"score":0.0,"escalated":true,"reason":"환불 키워드"}
```

## 注意事项

- **保持语气一致性**：请严格按照客户公司的设定使用相应的语气。
- **保护个人信息**：禁止在日志中存储敏感信息（如居民身份证号、银行卡号）。
- **优化回复速度**：目标是在3秒内完成基于FAQ的自动回复。
- **避免过度升级**：频繁升级问题可能会引起客户不满，因此需持续优化FAQ内容。

## 可扩展性

- [ ] 基于OpenAI Embeddings的更精确语义匹配
- [ ] 保持对话上下文（实现会话管理）
- [ ] A/B测试（测试不同回复语气的效果）
- [ ] 支持多轮对话处理
- [ ] 自动学习FAQ内容（识别高频问题）
- [ ] 收集客户满意度反馈（通过回复后的评分系统）

---

**说明**：此工具目前使用模拟API运行。在生产环境中，需要将脚本与实际渠道的API进行集成。