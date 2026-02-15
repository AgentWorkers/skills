---
name: freemobile-sms
description: 通过 Free Mobile 向你的“人类伙伴”发送短信
license: FPC (Fais pas chier), https://clauzel.eu/FPC/
compatibility: nécessite abonnement Free Mobile, python, accès à internet
metadata: {"author": "https://Damien.Clauzel.eu", "version": "0.1", "openclaw": {"emoji": "💬", "homepage": "https://github.com/dClauzel/freemobile-sms", "requires": {"bins": ["python3"], "env": ["FREEMOBILE_SMS_USER", "FREEMOBILE_SMS_API_KEY"], "install": [{"id": "brew", "kind": "brew", "formula": "python3", "bins": ["python3"], "label": "Installe python3 CLI (brew)"}]}, "primaryEnv": "FREEMOBILE_SMS_API_KEY"}}
allowed-tools: Bash(python3:*)
---

# 向你的联系人发送短信

## 何时使用此技能

当你需要向你的联系人发送短信时，请使用此技能。

## 使用示例

- `scripts/FreeMobile_sms.py --message "你的牙医预约在1小时后" --timeout 15`

## 配置

发送短信的脚本会使用以下环境变量。你无需进行任何额外的配置：
- `FREEMOBILE_SMS_USER`：Free Mobile的用户名
- `FREEMOBILE_SMS_API_KEY`：Free Mobile的API密钥

## 限制

- 每天最多可发送200-250条短信（Free Mobile的限制）
- 每条短信最多160个字符
- 发送间隔至少为10秒
- 仅能发送到Free Mobile用户的手机号码

## 文档

有关详细信息，请参阅[文档](references/REFERENCE.md)。