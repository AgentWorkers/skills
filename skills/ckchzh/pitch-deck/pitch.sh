#!/usr/bin/env bash
CMD="$1"; shift 2>/dev/null; INPUT="$*"
case "$CMD" in
  create) cat << 'PROMPT'
你是融资顾问。生成12页融资演示大纲(可直接做PPT)：1.封面 2.问题 3.解决方案 4.产品 5.市场规模 6.商业模式 7.竞争 8.团队 9.里程碑 10.财务 11.融资需求 12.愿景。每页要点+讲稿。用中文。
项目：
PROMPT
    echo "$INPUT" ;;
  slide) cat << 'PROMPT'
你是演示设计师。优化单页幻灯片：1.核心信息(1句话) 2.数据可视化建议 3.视觉布局 4.讲稿(30秒)。用中文。
幻灯片内容：
PROMPT
    echo "$INPUT" ;;
  story) cat << 'PROMPT'
你是故事教练。设计路演故事线：1.英雄之旅结构 2.情感曲线 3.数据锚点 4.高潮设计 5.结尾号召。用中文。
项目：
PROMPT
    echo "$INPUT" ;;
  investor) cat << 'PROMPT'
你是投资人。模拟投资人Q&A：10个尖锐问题+推荐回答框架：1.市场 2.竞争 3.团队 4.财务 5.退出。用中文。
项目：
PROMPT
    echo "$INPUT" ;;
  demo) cat << 'PROMPT'
你是Demo Day教练。准备清单：1.5分钟演讲结构 2.时间分配 3.演示技巧 4.常见错误 5.着装建议。用中文。
PROMPT
    echo "$INPUT" ;;
  feedback) cat << 'PROMPT'
你是路演评委。评审演示文稿：1.整体评分(1-100) 2.内容完整性 3.故事吸引力 4.数据说服力 5.TOP3改进建议。用中文。
演示内容：
PROMPT
    echo "$INPUT" ;;
  *) cat << 'EOF'
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🎯 Pitch Deck — 使用指南
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  create [项目]      12页融资演示大纲
  slide [内容]       单页优化
  story [项目]       故事线设计
  investor [项目]    投资人Q&A模拟
  demo              Demo Day准备
  feedback [内容]    演示评审+评分

  Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
EOF
    ;;
esac
