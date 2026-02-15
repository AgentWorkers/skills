---
name: glab-ci
description: **使用说明：**  
在处理 glab ci（GitHub Actions 的 CI/CD 工具）命令时，请参考以下说明。
---

# glab ci

## 概述

```

  Work with GitLab CI/CD pipelines and jobs.                                                                            
         
  USAGE  
         
    glab ci <command> [command] [--flags]  
            
  COMMANDS  
            
    artifact <refName> <jobName> [--flags]  Download all artifacts from the last pipeline.
    cancel <command> [command]              Cancel a running pipeline or job.
    config <command> [command] [--flags]    Work with GitLab CI/CD configuration.
    delete <id> [--flags]                   Delete CI/CD pipelines.
    get [--flags]                           Get JSON of a running CI/CD pipeline on the current or other specified branch.
    lint [--flags]                          Checks if your `.gitlab-ci.yml` file is valid.
    list [--flags]                          Get the list of CI/CD pipelines.
    retry <job-id> [--flags]                Retry a CI/CD job.
    run [--flags]                           Create or run a new CI/CD pipeline.
    run-trig [--flags]                      Run a CI/CD pipeline trigger.
    status [--flags]                        View a running CI/CD pipeline on current or other branch specified.
    trace [<job-id>] [--flags]              Trace a CI/CD job log in real time.
    trigger <job-id> [--flags]              Trigger a manual CI/CD job.
    view [branch/tag] [--flags]             View, run, trace, log, and cancel CI/CD job's current pipeline.
         
  FLAGS  
         
    -h --help                               Show help for this command.
    -R --repo                               Select another repository. Can use either `OWNER/REPO` or `GROUP/NAMESPACE/REPO` format. Also accepts full URL or Git URL.
```

## 快速入门

```bash
glab ci --help
```

## 子命令

有关完整的 `--help` 命令输出，请参阅 [references/commands.md](references/commands.md)。