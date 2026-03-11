#!/usr/bin/env bash
CMD="$1"; shift 2>/dev/null; INPUT="$*"
case "$CMD" in
  integrate) cat << 'PROMPT'
You are an expert. Help with: 支付集成流程. Provide detailed, practical output. Use Chinese.
User request:
PROMPT
    echo "$INPUT" ;;
  wechat-pay) cat << 'PROMPT'
You are an expert. Help with: 微信支付接入. Provide detailed, practical output. Use Chinese.
User request:
PROMPT
    echo "$INPUT" ;;
  alipay) cat << 'PROMPT'
You are an expert. Help with: 支付宝接入. Provide detailed, practical output. Use Chinese.
User request:
PROMPT
    echo "$INPUT" ;;
  refund) cat << 'PROMPT'
You are an expert. Help with: 退款流程. Provide detailed, practical output. Use Chinese.
User request:
PROMPT
    echo "$INPUT" ;;
  webhook) cat << 'PROMPT'
You are an expert. Help with: 回调配置. Provide detailed, practical output. Use Chinese.
User request:
PROMPT
    echo "$INPUT" ;;
  test) cat << 'PROMPT'
You are an expert. Help with: 沙箱测试. Provide detailed, practical output. Use Chinese.
User request:
PROMPT
    echo "$INPUT" ;;
  *) cat << 'EOF'
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Payment Integration — 使用指南
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  integrate       支付集成流程
  wechat-pay      微信支付接入
  alipay          支付宝接入
  refund          退款流程
  webhook         回调配置
  test            沙箱测试

  Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
EOF
    ;;
esac
