# Cmd Executor

## 概述
Cmd Executor 是 OpenClaw 的一个技能，允许用户在运行 OpenClaw 网关的机器上执行本地 Windows 命令。

该技能主要用于个人自动化操作、调试以及通过 OpenClaw 进行本地系统管理。

## 功能说明
- 执行用户提供的 Windows 命令
- 捕获标准输出（standard output）和标准错误（standard error）
- 将执行结果返回到聊天界面

## 支持的平台
- Windows（PowerShell / CMD）

## 使用方法
发送以 “Run command: <your command>” 开头的消息来使用该技能。

示例：
Run command: dir "C:\Users\Md Sadik Laskar\Documents"

## 安全提示
该技能可以执行任意本地命令。请仅在可信环境中安装和使用该技能，切勿将其提供给不可信的用户。

## 常见使用场景
- 列出文件和文件夹
- 运行本地脚本
- 检查系统工具和实用程序