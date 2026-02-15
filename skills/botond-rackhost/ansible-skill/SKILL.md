---
name: ansible
description: "使用 Ansible 实现基础设施自动化。它可以用于服务器配置、应用程序部署以及多主机协调管理。其中包含了用于 OpenClaw VPS 设置、安全加固以及常见服务器配置的 playbook（脚本）。"
metadata: {"openclaw":{"requires":{"bins":["ansible","ansible-playbook"]},"install":[{"id":"ansible","kind":"pip","package":"ansible","bins":["ansible","ansible-playbook"],"label":"Install Ansible (pip)"}]}}
---

# Ansible 技能

Ansible 是一种用于服务器配置管理、自动化部署和流程编排的工具，它实现了基础设施即代码（Infrastructure as Code）的理念。

## 快速入门

### 先决条件

```bash
# Install Ansible
pip install ansible

# Or on macOS
brew install ansible

# Verify
ansible --version
```

### 运行你的第一个 Playbook

```bash
# Test connection
ansible all -i inventory/hosts.yml -m ping

# Run playbook
ansible-playbook -i inventory/hosts.yml playbooks/site.yml

# Dry run (check mode)
ansible-playbook -i inventory/hosts.yml playbooks/site.yml --check

# With specific tags
ansible-playbook -i inventory/hosts.yml playbooks/site.yml --tags "security,nodejs"
```

## 目录结构

```
skills/ansible/
├── SKILL.md              # This file
├── inventory/            # Host inventories
│   ├── hosts.yml         # Main inventory
│   └── group_vars/       # Group variables
├── playbooks/            # Runnable playbooks
│   ├── site.yml          # Master playbook
│   ├── openclaw-vps.yml  # OpenClaw VPS setup
│   └── security.yml      # Security hardening
├── roles/                # Reusable roles
│   ├── common/           # Base system setup
│   ├── security/         # Hardening (SSH, fail2ban, UFW)
│   ├── nodejs/           # Node.js installation
│   └── openclaw/         # OpenClaw installation
└── references/           # Documentation
    ├── best-practices.md
    ├── modules-cheatsheet.md
    └── troubleshooting.md
```

## 核心概念

### Inventory（清单）

在 `inventory/hosts.yml` 文件中定义你的主机：

```yaml
all:
  children:
    vps:
      hosts:
        eva:
          ansible_host: 217.13.104.208
          ansible_user: root
          ansible_ssh_pass: "{{ vault_eva_password }}"
        plane:
          ansible_host: 217.13.104.99
          ansible_user: asdbot
          ansible_ssh_private_key_file: ~/.ssh/id_ed25519_plane
    
    openclaw:
      hosts:
        eva:
```

### Playbook（剧本）

自动化任务的入口点：

```yaml
# playbooks/site.yml - Master playbook
---
- name: Configure all servers
  hosts: all
  become: yes
  roles:
    - common
    - security

- name: Setup OpenClaw servers
  hosts: openclaw
  become: yes
  roles:
    - nodejs
    - openclaw
```

### Role（角色）

可重用的、模块化的配置配置：

```yaml
# roles/common/tasks/main.yml
---
- name: Update apt cache
  ansible.builtin.apt:
    update_cache: yes
    cache_valid_time: 3600
  when: ansible_os_family == "Debian"

- name: Install essential packages
  ansible.builtin.apt:
    name:
      - curl
      - wget
      - git
      - htop
      - vim
      - unzip
    state: present
```

## 包含的角色

### 1. common（通用角色）
- 基础系统配置：
  - 系统更新
  - 必需软件包的安装
  - 时区设置
  - 创建带有 SSH 密钥的用户

### 2. security（安全角色）
  - 根据 CIS 标准进行系统加固：
    - SSH 安全配置（仅使用密钥登录，禁止 root 用户登录）
    - 使用 fail2ban 防止暴力登录尝试
    - 配置 UFW 防火墙
    - 自动更新系统安全补丁

### 3. nodejs（Node.js 角色）
  - 通过 NodeSource 安装 Node.js：
    - 可配置的版本（默认为 22.x LTS）
    - 安装全局 npm 包
    - 使用 pm2 进程管理器（可选）

### 4. openclaw（OpenClaw 角色）
  - 完整的 OpenClaw 配置：
    - 安装 Node.js
    - 安装 OpenClaw 的 npm 包
    - 配置 systemd 服务
    - 设置配置文件

## 使用模式

### 模式 1：新 VPS 的设置（包含 OpenClaw）

```bash
# 1. Add host to inventory
cat >> inventory/hosts.yml << 'EOF'
        newserver:
          ansible_host: 1.2.3.4
          ansible_user: root
          ansible_ssh_pass: "initial_password"
          deploy_user: asdbot
          deploy_ssh_pubkey: "ssh-ed25519 AAAA... asdbot"
EOF

# 2. Run OpenClaw playbook
ansible-playbook -i inventory/hosts.yml playbooks/openclaw-vps.yml \
  --limit newserver \
  --ask-vault-pass

# 3. After initial setup, update inventory to use key auth
# ansible_user: asdbot
# ansible_ssh_private_key_file: ~/.ssh/id_ed25519
```

### 模式 2：仅进行安全加固

```bash
ansible-playbook -i inventory/hosts.yml playbooks/security.yml \
  --limit production \
  --tags "ssh,firewall"
```

### 模式 3：滚动更新

```bash
# Update one server at a time
ansible-playbook -i inventory/hosts.yml playbooks/update.yml \
  --serial 1
```

### 模式 4：执行特定命令

```bash
# Check disk space on all servers
ansible all -i inventory/hosts.yml -m shell -a "df -h"

# Restart service
ansible openclaw -i inventory/hosts.yml -m systemd -a "name=openclaw state=restarted"

# Copy file
ansible all -i inventory/hosts.yml -m copy -a "src=./file.txt dest=/tmp/"
```

## 变量与秘密信息

### Group Variables（组变量）

```yaml
# inventory/group_vars/all.yml
---
timezone: Europe/Budapest
deploy_user: asdbot
ssh_port: 22

# Security
security_ssh_password_auth: false
security_ssh_permit_root: false
security_fail2ban_enabled: true
security_ufw_enabled: true
security_ufw_allowed_ports:
  - 22
  - 80
  - 443

# Node.js
nodejs_version: "22.x"
```

### 使用 Vault 存储秘密信息

```bash
# Create encrypted vars file
ansible-vault create inventory/group_vars/all/vault.yml

# Edit encrypted file
ansible-vault edit inventory/group_vars/all/vault.yml

# Run with vault
ansible-playbook site.yml --ask-vault-pass

# Or use vault password file
ansible-playbook site.yml --vault-password-file ~/.vault_pass
```

Vault 文件结构：
```yaml
# inventory/group_vars/all/vault.yml
---
vault_eva_password: "y8UGHR1qH"
vault_deploy_ssh_key: |
  -----BEGIN OPENSSH PRIVATE KEY-----
  ...
  -----END OPENSSH PRIVATE KEY-----
```

## 常用模块

| 模块        | 用途                        | 示例                                      |
|-------------|-----------------------------------------|-----------------------------------------|
| `apt`       | Debian 系统的包管理                | `apt: name=nginx state=present`                   |
| `yum`       | RHEL 系统的包管理                | `yum: name=nginx state=present`                   |
| `copy`      | 复制文件                      | `copy: src=file dest=/path/`                        |
| `template`    | 使用 Jinja2 模板进行文件生成            | `template: src=nginx.conf.j2 dest=/etc/nginx/nginx.conf`         |
| `file`      | 文件/目录操作                    | `file: path=/dir state=directory mode=0755`                |
| `user`      | 用户管理                      | `user: name=asdbot groups=sudo shell=/bin/bash`               |
| `authorized_key` | SSH 密钥管理                  | `authorized_key: user=asdbot key="{{ ssh_key }}"               |
| `systemd`     | systemd 服务管理                | `systemd: name=nginx state=started enabled=yes`            |
| `ufw`       | Ubuntu 系统的防火墙管理            | `ufw: rule=allow port=22 proto=tcp`                   |
| `lineinfile`    | 修改 `/etc/ssh/sshd_config` 文件            | `lineinfile: path=/etc/ssh/sshd_config regexp='^PermitRootLogin' line='PermitRootLogin no'` |
| `git`       | 从 Git 仓库克隆代码                | `git: repo=https://github.com/x/y.git dest=/opt/y`              |
| `npm`       | 安装 npm 包                    | `npm: name=openclaw global=yes`                     |
| `command`     | 运行命令                      | `command: /opt/script.sh`                         |
| `shell`      | 执行 shell 命令                    | `shell: cat /etc/passwd \| grep root`                     |

## 最佳实践

### 1. 为任务命名
```yaml
# Good
- name: Install nginx web server
  apt:
    name: nginx
    state: present

# Bad
- apt: name=nginx
```

### 2. 使用完全限定的集合名称（FQCN）
```yaml
# Good
- ansible.builtin.apt:
    name: nginx

# Acceptable but less clear
- apt:
    name: nginx
```

### 明确指定任务的状态
```yaml
# Good - explicit state
- ansible.builtin.apt:
    name: nginx
    state: present

# Bad - implicit state
- ansible.builtin.apt:
    name: nginx
```

### 3. 保证任务的可重复执行性
编写可以安全地多次运行的任务：

```yaml
# Good - idempotent
- name: Ensure config line exists
  ansible.builtin.lineinfile:
    path: /etc/ssh/sshd_config
    regexp: '^PasswordAuthentication'
    line: 'PasswordAuthentication no'

# Bad - not idempotent
- name: Add config line
  ansible.builtin.shell: echo "PasswordAuthentication no" >> /etc/ssh/sshd_config
```

### 4. 使用处理程序来处理重启操作
```yaml
# tasks/main.yml
- name: Update SSH config
  ansible.builtin.template:
    src: sshd_config.j2
    dest: /etc/ssh/sshd_config
  notify: Restart SSH

# handlers/main.yml
- name: Restart SSH
  ansible.builtin.systemd:
    name: sshd
    state: restarted
```

### 5. 使用标签进行选择性执行任务
```yaml
- name: Security tasks
  ansible.builtin.include_tasks: security.yml
  tags: [security, hardening]

- name: App deployment
  ansible.builtin.include_tasks: deploy.yml
  tags: [deploy, app]
```

## 故障排除

### 连接问题

```bash
# Test SSH connection manually
ssh -v user@host

# Debug Ansible connection
ansible host -i inventory -m ping -vvv

# Check inventory parsing
ansible-inventory -i inventory --list
```

### 常见错误

- **“Permission denied”**：检查 SSH 密钥权限：`chmod 600 ~/.ssh/id_*`
- 确保用户具有 sudo 权限
- 在 playbook 中添加 `become: yes` 选项

- **“Host key verification failed”**：在 `ansible.cfg` 中设置 `host_key_checking = False`；或使用 `ssh-keyscan -H host >> ~/.ssh/known_hosts` 添加主机密钥

- **“Module not found”**：使用完全限定的集合名称（FQCN），例如 `ansible.builtin.apt` 而不是 `apt`；通过 `ansible-galaxy collection install community.general` 安装相关模块

### 调试 Playbook

```bash
# Verbose output
ansible-playbook site.yml -v    # Basic
ansible-playbook site.yml -vv   # More
ansible-playbook site.yml -vvv  # Maximum

# Step through tasks
ansible-playbook site.yml --step

# Start at specific task
ansible-playbook site.yml --start-at-task="Install nginx"

# Check mode (dry run)
ansible-playbook site.yml --check --diff
```

## 与 OpenClaw 的集成

### 从 OpenClaw 代理进行集成

```bash
# Run playbook via exec tool
exec command="ansible-playbook -i skills/ansible/inventory/hosts.yml skills/ansible/playbooks/openclaw-vps.yml --limit eva"

# Ad-hoc command
exec command="ansible eva -i skills/ansible/inventory/hosts.yml -m shell -a 'systemctl status openclaw'"
```

### 存储凭据

- 可以使用 OpenClaw 的 Vaultwarden 功能来存储凭据；
- 更好的做法是使用 Ansible Vault，并通过 `--ask-vault-pass` 参数来获取凭据。

## 参考资料

- `references/best-practices.md` - 详细的最佳实践指南
- `references/modules-cheatsheet.md` - 常用模块快速参考
- `references/troubleshooting.md` - 扩展的故障排除指南

## 外部资源

- [Ansible 官方文档](https://docs.ansible.com/)
- [Ansible Galaxy](https://galaxy.ansible.com/) - 社区提供的角色库
- [geerlingguy 的角色库](https://github.com/geerlingguy?tab=repositories&q=ansible-role) - 高质量的 Ansible 角色资源
- [《Ansible for DevOps》](https://www.ansiblefordevops.com/) - Jeff Geerling 著的书籍