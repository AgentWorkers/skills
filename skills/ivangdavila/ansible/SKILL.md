---
name: Ansible
description: 避免常见的 Ansible 错误——YAML 语法陷阱、变量优先级问题、幂等性失败以及处理程序（handler）相关的常见问题。
metadata: {"clawdbot":{"emoji":"🔧","requires":{"bins":["ansible"]},"os":["linux","darwin"]}}
---

## YAML 语法陷阱
- 在 `value` 中使用 Jinja2 时需要加上引号：`{{ variable }}` 而不是 `{{ variable }`
- 字符串中的 `:` 也需要加上引号：`msg: "Note: this works"` 而不是 `msg: Note: this`
- 布尔值（`yes`, `no`, `true`, `false`）会被解析为布尔类型；如果是字面字符串，则需要加上引号
- 缩进必须一致：标准格式是两个空格，禁止使用制表符

## 变量优先级
- 额外定义的变量（`-e`）会覆盖所有其他变量——具有最高的优先级
- 主机相关的变量优先于组变量——更具体的变量优先被使用
- 在 playbook 中定义的变量优先于 inventory 中定义的变量——优先级顺序为：inventory < playbook < 额外变量
- 如果变量未定义，可以使用 `{{ var | default('fallback') }}` 来获取默认值

## 函数的幂等性
- `command`/`shell` 模块不具备幂等性（执行后状态会改变），应使用 `creates:` 模块
- `apt`, `yum`, `copy` 等模块是设计为具备幂等性的
- 对于不会改变状态的命令（如查询操作），可以使用 `changed_when: false`
- 使用 `creates:`/`removes:` 可确保命令的幂等性（例如：如果文件已存在则跳过执行）

## 处理器（Handlers）
- 处理器仅在任务状态发生变化时才会被执行——不会在任务状态为 “ok” 时执行
- 处理器在 play 结束时执行一次——不会在通知操作（notify）之后立即执行
- 对同一个处理器多次发送通知只会执行一次——系统会自动去重
- 可以使用 `--force-handlers` 选项强制处理器执行，即使任务失败也会执行——或者使用 `meta: flushHandlers` 来控制处理器的执行

## 权限提升（Privilege Escalation）
- `become: yes` 用于以 root 用户身份执行任务
- `become_user:` 用于切换到特定用户
- 默认的权限提升方法是 `become_method: sudo`；如果需要，也可以使用 `su` 或 `doas`
- 使用 `--ask-become-pass` 或 `ansible.cfg` 文件来设置 sudo 密码
- 有些模块需要在任务级别执行权限提升操作——即使 playbook 中设置了 `become: yes` 也是如此

## 条件判断
- 使用 `when:` 时不需要 Jinja2 的大括号：`when: ansible_os_family == "Debian"` 而不是 `when: "{{ ... }}`
- 多个条件判断可以使用 `and`/`or` 来组合——也可以使用列表形式表示逻辑与/或关系
- 对于可选变量，可以使用 `is defined`/`is not defined` 来判断变量是否已定义：`when: my_var is defined`
- 布尔变量判断时使用 `when: my_bool` 而不是 `== true`

## 循环结构
- `loop:` 是现代推荐的循环方式，`with_items:` 是旧式的；建议使用 `loop`
- 使用 `loop_control.loop_var` 可以避免循环变量冲突
- `item` 是循环中的迭代变量；可以使用 `loop_control.label` 来美化输出结果
- `until:` 用于实现重试逻辑：`until: result.rc == 0 retries: 5 delay: 10`

## 数据收集（Facts）
- 设置 `gather_facts: no` 可以提高执行速度——但这样就不能使用 `ansible_*` 系列的变量
- 数据会通过 `fact_caching` 被缓存——在不同执行过程中保持一致
- 自定义数据可以保存在 `/etc/ansible/facts.d/*.fact` 文件中——格式为 JSON 或 INI，可以通过 `ansible_local` 访问

## 常见错误
- `register:` 会捕获任务执行的全部输出，即使任务失败也会记录——应该检查 `result.rc` 或 `result_FAILED`
- 设置 `ignore_errors: yes` 会让任务继续执行，但不会改变任务的状态——在 `register` 中任务仍会被标记为 “失败”
- 对于本地命令，可以使用 `delegate_to: localhost`，但 `local_action` 是更简洁的写法
- 对于加密文件，可以使用 `--ask-vault-pass` 或 `vault_password` 文件来设置密码
- 并非所有模块都支持 `--check`（用于执行 dry run）选项——`command` 和 `shell` 模块总是忽略这个选项