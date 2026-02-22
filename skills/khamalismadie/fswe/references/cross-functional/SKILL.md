# 跨职能协作

## 技术规范模板

```markdown
# Feature: Password Reset

## Overview
Brief description of the feature

## Goals
- Allow users to reset forgotten passwords
- Secure token-based verification

## Non-Goals
- Social login (out of scope)
- Password strength analytics (future)

## User Stories
- User requests password reset
- User receives email with link
- User sets new password

## Technical Design

### API Changes
- POST /api/password/reset-request
- POST /api/password/reset-confirm

### Database
- Add `password_reset_token` to users table
- Add `password_reset_expires` to users table

### Security
- Token expires in 1 hour
- Token is cryptographically random

## Timeline
- Development: 2 days
- Testing: 1 day

## Dependencies
- Email service (existing)
```

## 沟通技巧

| 情况 | 方法 |
|---------|----------|
| 遭到反对 | 提供数据及替代方案 |
| 解释技术细节 | 使用类比来帮助理解 |
| 意见不合 | 表达自己的担忧并保持倾听 |
| 请求帮助 | 明确说明你需要什么帮助 |

## 检查清单

- [ ] 编写技术规范
- [ ] 及时沟通遇到的阻碍
- [ ] 定期更新进展
- [ ] 记录决策内容
- [ ] 主动分享知识