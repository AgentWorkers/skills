---
name: espeak-ng
description: 使用 espeak-ng 实现文本转语音（TTS）功能
---
# Espeak-ng

该技能允许您使用 espeak-ng 生成语音。

## 适用于智能代理（Smart Agent）
**命令：** `python espeak_skill.py <文本>`
**示例：** `python espeak_skill.py "Hello world"`

## 适用于非智能代理（Not Smart Agent）
**命令：** `python ./skills/espeak-ng/espeak_skill.py <文本>`
**示例：** `python ./skills/espeak-ng/espeak_skill.py "Hello world"`

## 工具执行（Tool Execution）
**命令：** `espeak-ng <文本>`
**示例：** `espeak-ng "Hello world"`

## 系统要求
- 系统上必须已安装 espeak-ng。
- 在 Linux/macOS 上，请确保已安装 espeak-ng：
  - Ubuntu/Debian：`sudo apt-get install espeak-ng`
  - CentOS/RHEL：`sudo yum install espeak-ng`
  - macOS：`brew install espeak-ng`
- Windows 11：从 [https://github.com/espeak-ng/espeak-ng/releases](https://github.com/espeak-ng/espeak-ng/releases) 下载 espeak-ng.msi 并安装。

注意：在 Windows 11 上，您需要手动从 GitHub 下载并安装 espeak-ng。