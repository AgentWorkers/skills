---
name: opensysinfo-skill
version: 0.1.0
author: Privateer <85460639+pr1vateer@users.noreply.github.com>
description: 这是一个用于报告基本系统信息（操作系统、运行时间、CPU使用情况、内存使用情况以及磁盘信息的简单脚本。该脚本是用Bash语言实现的。）
entrypoint: scripts/sysinfo.sh
# metadata must be a single-line JSON object per OpenClaw parser requirements.
metadata: {"openclaw":{"emoji":"🧰","short":"Basic system info (bash)","requires":{"bins":["bash"]}}}
user-invocable: true
command-dispatch: tool
command-tool: sysinfo
commands:
  - name: sysinfo
    usage: sysinfo [--format text|json] [--disk PATH]
    description: |
      Emit basic system information.
      Options:
        --format json   -> produce machine-readable JSON
        --format text   -> (default) human readable text
        --disk PATH     -> report disk usage for PATH (default '/')
---
# sysinfo-skill

这是一个简单的 OpenClaw 技能，用于报告主机系统的信息。其实现完全基于 Bash 脚本，需要 `bash` 环境才能运行。

入口点：`{baseDir}/scripts/sysinfo.sh`