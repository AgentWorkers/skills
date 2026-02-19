---
name: dangerous-manifest-skill
description: **具有危险性要求的技能**
metadata:
  clawdbot:
    emoji: "💀"
    requires:
      bins:
        - node
        - sudo
        - rm
        - curl
      env:
        - AWS_SECRET_ACCESS_KEY
    files: ["**/*"]
---
# 危险的Manifest技能

该技能需要使用危险的二进制文件，并且具有过度的文件访问权限。