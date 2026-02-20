---
summary: "Hostinger VPS Optimizer: Performance tweaks & cost-saving configs for Hostinger VPS plans."
description: "Apply battle-tested optimizations for KVM/Cloud VPS: kernel tuning, caching, security hardening, auto-scaling."
triggers:
  - "optimize hostinger VPS"
  - "hostinger tweaks"
  - "VPS cost save"
  - "hostinger performance"
read_when:
  - "hostinger VPS" in message
---

# Hostinger VPS 优化工具 v1.0.0

## 🎯 目的
通过以下方法显著提升 Hostinger VPS 的性能，并降低 20-50% 的成本：
- 调整系统内核参数（sysctl，涉及 TCP 和虚拟机相关设置）
- 优化 Nginx 和 Apache 服务器的配置
- 使用 Fail2ban 和 UFW 实现安全防护
- 设置资源使用限制
- 对不同套餐的成本进行详细分析

## 🚀 快速入门
```
!hostinger-vps-optimizer --plan kvm2 --focus speed
```

## 所需文件
- `scripts/optimize.sh`：一键优化脚本
- `configs/hostinger.sysctl`：预先调整好的系统内核参数配置文件

## 支持的套餐
KVM 1-8、Cloud Startup/Pro。