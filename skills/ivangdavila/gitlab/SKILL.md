---
name: GitLab
description: 避免常见的 GitLab CI/CD 错误：规则陷阱、隐性故障以及 YAML 合并问题。
metadata: {"clawdbot":{"emoji":"🦊","os":["linux","darwin","win32"]}}
---

## 规则使用中的常见陷阱  
- `rules:` 和 `only:/except:` 不能同时使用——每个任务中只能选择其中一个  
- 首个匹配到的规则会生效——请将特定规则放在通用规则之前  
- 如果缺少 `when:` 参数，规则默认会在任务成功时执行（`on_success`）——例如：`rules: - if: $CI_COMMIT_TAG` 表示仅在指定标签触发时执行该规则  
- 空的规则数组 `rules: []` 表示该规则永远不会被执行——这与完全没有规则的情况不同  
- 为规则添加 `- when: never` 可以防止某些条件被意外触发  

## 隐性失败情况  
- 在非受保护的分支上，如果缺少受保护的变量，任务仍会运行，但相关变量会为空  
- 如果运行器的标签与配置不匹配，任务会永远处于待处理状态（而不会报错）  
- 在非特权运行的环境中使用 `docker:dind` 时，可能会遇到难以理解的 Docker 错误  
- 如果变量格式不正确，即使被屏蔽了，这些变量仍会显示在日志中  

## YAML 合并时的问题  
- `extends:` 不会深度合并数组内容——脚本和变量数组会被替换，而不是被追加  
- 使用 `!reference [.job, script]` 可以重用代码片段——例如：`script: [!reference [.base, script], "my command"]`  
- `include:` 文件中的规则可能会覆盖其他文件中的规则——相同键的规则以最后一个文件中的为准  
- 跨文件的引用符号 `&`/`*` 无效——需要使用 `extends:` 来实现代码的跨文件重用  

## 工件与缓存  
- 缓存内容在多次运行之间不保证一致——将其视为一种优化手段，而非强制要求  
- 工件会自动按阶段下载——如果不需要，可以添加 `dependencies: []` 来跳过下载  
- `needs:` 会默认下载工件——如果需要跳过下载，可以使用 `needs: [{job: x, artifacts: false}]`  

## Docker-in-Docker 的注意事项  
- 共享的运行器通常不支持特权执行——需要自行部署运行器或进行特殊配置  
- 必须设置 `DOCKER_HOST: tcp://docker:2375`——否则任务会使用错误的 Docker 服务  
- 如果 `DOCKER_TLS_CERTDIR: ""`，则需要正确配置 TLS——否则会导致构建失败  

## 管道触发器  
- `CI_pipeline_SOURCE` 的值取决于触发器的类型（`push`、`merge_request_event`、`schedule`、`api`、`trigger` 等）  
- 合并请求（MR）相关的管道需要额外的规则（例如：`rules: - if: $CI_MERGE_REQUEST_IID`）  
- 分离的测试管道和合并后的测试管道处理方式不同——分离的测试使用源代码，合并后的测试使用合并后的结果