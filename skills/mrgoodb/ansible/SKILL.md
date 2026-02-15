---
name: ansible
description: 通过 API 运行 Ansible 演示剧本并管理 AWX/Tower，实现基础设施配置的自动化。
metadata: {"clawdbot":{"emoji":"🅰️","requires":{"env":["AWX_URL","AWX_TOKEN"]}}}
---
# Ansible / AWX  
基础设施自动化工具  

## 环境配置  
```bash
export AWX_URL="https://awx.example.com"
export AWX_TOKEN="xxxxxxxxxx"
```  

## 作业模板列表  
```bash
curl "$AWX_URL/api/v2/job_templates/" -H "Authorization: Bearer $AWX_TOKEN"
```  

## 启动作业  
```bash
curl -X POST "$AWX_URL/api/v2/job_templates/{id}/launch/" \
  -H "Authorization: Bearer $AWX_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"extra_vars": {"host": "webserver"}}'
```  

## 获取作业状态  
```bash
curl "$AWX_URL/api/v2/jobs/{jobId}/" -H "Authorization: Bearer $AWX_TOKEN"
```  

## 运行 Ansible 命令行工具  
```bash
ansible-playbook -i inventory.yml playbook.yml
ansible all -m ping -i inventory.yml
```  

## 链接  
- 文档：https://docs.ansible.com