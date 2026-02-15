---
name: aws-cost-expert
description: AWS成本优化：EC2预留实例、节省计划（Savings Plans）、按需实例（Spot Instances）、Lambda函数优化、成本管理工具（Cost Explorer）以及可信顾问（Trusted Advisor）。
---

# AWS 成本优化专家

在 AWS 特定的成本优化策略和服务方面拥有深厚的专业知识。

## AWS 成本管理服务

### 1. 成本探索器 (Cost Explorer)
```bash
# Get monthly costs by service
aws ce get-cost-and-usage \
  --time-period Start=2025-01-01,End=2025-02-01 \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --group-by Type=SERVICE

# Get EC2 costs by instance type
aws ce get-cost-and-usage \
  --time-period Start=2025-01-01,End=2025-02-01 \
  --granularity DAILY \
  --metrics UnblendedCost \
  --filter file://ec2-filter.json \
  --group-by Type=INSTANCE_TYPE
```

### 2. AWS 预算 (AWS Budgets)
```yaml
Budget Configuration:
  - Monthly budget: $30,000
  - Alert at 80% ($24,000)
  - Alert at 90% ($27,000)
  - Alert at 100% ($30,000)
  - Alert at 110% ($33,000) - critical
  
Actions:
  - Stop non-production instances
  - Deny new resource creation
  - Email C-level executives
```

### 3. 计算优化器 (Compute Optimizer)
```bash
# Get EC2 right-sizing recommendations
aws compute-optimizer get-ec2-instance-recommendations \
  --max-results 100

# Get Lambda function recommendations
aws compute-optimizer get-lambda-function-recommendations
```

### 可信赖顾问 (Trusted Advisor)
```bash
# Get cost optimization checks
aws support describe-trusted-advisor-checks \
  --language en \
  --query 'checks[?category==`cost_optimizing`]'

# Check results
aws support describe-trusted-advisor-check-result \
  --check-id <check-id>
```

## EC2 成本优化

### 节省计划 vs 预留实例 (Savings Plans vs Reserved Instances)
```typescript
interface Comparison {
  option: string;
  flexibility: string;
  discount: string;
  commitment: string;
  bestFor: string;
}

const options: Comparison[] = [
  {
    option: 'On-Demand',
    flexibility: 'Maximum',
    discount: '0%',
    commitment: 'None',
    bestFor: 'Unpredictable workloads',
  },
  {
    option: 'Spot Instances',
    flexibility: 'Medium',
    discount: '50-90%',
    commitment: 'None',
    bestFor: 'Fault-tolerant batch workloads',
  },
  {
    option: 'Compute Savings Plans',
    flexibility: 'High (any instance, any region)',
    discount: '30-70%',
    commitment: '1 or 3 years',
    bestFor: 'Flexible compute usage',
  },
  {
    option: 'EC2 Instance Savings Plans',
    flexibility: 'Medium (same instance family, same region)',
    discount: '35-72%',
    commitment: '1 or 3 years',
    bestFor: 'Consistent instance family usage',
  },
  {
    option: 'Reserved Instances',
    flexibility: 'Low (specific instance type)',
    discount: '40-75%',
    commitment: '1 or 3 years',
    bestFor: 'Predictable, steady-state workloads',
  },
];
```

### Graviton 实例 (ARM)
```yaml
Benefits:
  - 20% better price/performance vs x86
  - 40% better price/performance for many workloads
  - Lower power consumption

Migration:
  - t4g (general purpose, burstable)
  - m6g (balanced)
  - c6g (compute optimized)
  - r6g (memory optimized)

Compatibility:
  - Most Linux distributions
  - Container workloads (Docker, ECS, EKS)
  - Not for: Windows, x86-only software
```

## Lambda 成本优化

### 性能调优 (Power Tuning)
```typescript
// Use AWS Lambda Power Tuning tool
// https://github.com/alexcasalboni/aws-lambda-power-tuning

interface PowerTuningResult {
  optimalMemory: number;
  currentCost: number;
  optimalCost: number;
  savings: number;
}

// Example: Image processing function
const result: PowerTuningResult = {
  optimalMemory: 2048, // MB
  currentCost: 0.0000133, // per invocation at 1024MB
  optimalCost: 0.0000119, // per invocation at 2048MB
  savings: 10.5, // % (faster execution despite higher memory cost)
};
```

### Lambda 成本优化检查清单 (Lambda Cost Optimization Checklist)
```yaml
Memory Optimization:
  - ✅ Run power tuning for all production functions
  - ✅ Monitor cold start vs warm execution cost
  - ✅ Consider provisioned concurrency for latency-sensitive APIs
  
Architecture:
  - ✅ Avoid VPC Lambda unless necessary (saves NAT costs)
  - ✅ Use Lambda Layers for shared dependencies
  - ✅ Enable Lambda SnapStart for Java functions (faster cold starts)
  
Invocation:
  - ✅ Batch process vs streaming (fewer invocations)
  - ✅ Async invocation where possible
  - ✅ Use Step Functions for orchestration (not nested Lambdas)
```

## S3 成本优化

### 智能分层 (Intelligent-Tiering)
```yaml
Automatic Cost Optimization:
  - Frequent Access tier (default)
  - Infrequent Access tier (30 days no access)
  - Archive Instant Access (90 days)
  - Archive Access (90-730 days, optional)
  - Deep Archive Access (180-730 days, optional)
  
Monitoring fee: $0.0025 per 1000 objects
Cost: Worth it for > 128KB objects with unpredictable access

Best for:
  - Unknown access patterns
  - Data lakes
  - Long-term storage with occasional access
```

### 生命周期策略示例 (Lifecycle Policy Example)
```json
{
  "Rules": [
    {
      "Id": "Optimize application logs",
      "Status": "Enabled",
      "Filter": { "Prefix": "logs/app/" },
      "Transitions": [
        { "Days": 30, "StorageClass": "STANDARD_IA" },
        { "Days": 90, "StorageClass": "GLACIER_IR" },
        { "Days": 365, "StorageClass": "DEEP_ARCHIVE" }
      ],
      "Expiration": { "Days": 2555 }
    },
    {
      "Id": "Delete incomplete multipart uploads",
      "Status": "Enabled",
      "AbortIncompleteMultipartUpload": {
        "DaysAfterInitiation": 7
      }
    }
  ]
}
```

## RDS 成本优化

### 预留实例 vs Aurora 无服务器版 (Reserved Instance vs Aurora Serverless)
```typescript
interface DBCostComparison {
  option: string;
  monthlyCost: number;
  usagePattern: string;
  pros: string[];
  cons: string[];
}

const comparison: DBCostComparison[] = [
  {
    option: 'On-Demand (db.t3.medium)',
    monthlyCost: 50,
    usagePattern: 'Variable, testing',
    pros: ['No commitment', 'Easy to change'],
    cons: ['Highest cost'],
  },
  {
    option: 'Reserved Instance 1yr (db.t3.medium)',
    monthlyCost: 32,
    usagePattern: 'Steady-state, 24/7',
    pros: ['36% savings', 'Predictable cost'],
    cons: ['1-year commitment', 'Capacity reserved'],
  },
  {
    option: 'Aurora Serverless v2',
    monthlyCost: 15,
    usagePattern: 'Intermittent, dev/test',
    pros: ['Auto-scaling', 'Pay per ACU-second', '70% savings for low usage'],
    cons: ['Cold start latency', 'Not for steady 24/7'],
  },
];
```

### RDS 存储优化 (RDS Storage Optimization)
```yaml
Storage Types:
  gp2 (General Purpose SSD):
    - $0.115/GB/month
    - 3 IOPS per GB (min 100, max 16,000)
    - Burstable to 3,000 IOPS
    
  gp3 (Newer General Purpose SSD):
    - $0.08/GB/month (30% cheaper!)
    - 3,000 IOPS baseline (free)
    - 125 MB/s throughput (free)
    - Additional IOPS: $0.005 per IOPS/month
    - Additional throughput: $0.04 per MB/s/month
    
  io1/io2 (Provisioned IOPS):
    - $0.125/GB + $0.065 per IOPS
    - For high-performance databases

Migration: gp2 → gp3 saves 30% with no performance impact
```

## DynamoDB 成本优化

### 按需存储 vs 预配存储 (On-Demand vs Provisioned Storage)
```typescript
// Decision matrix
function chooseBillingMode(usage: UsagePattern): string {
  const { requestsPerDay, peakTPS, averageTPS, predictability } = usage;
  
  // On-demand if:
  // - Unpredictable traffic
  // - Spiky workloads
  // - New applications
  // - < 20% peak utilization
  
  if (predictability < 0.5 || (peakTPS / averageTPS) > 2) {
    return 'On-Demand';
  }
  
  // Provisioned if:
  // - Predictable traffic
  // - Steady-state workloads
  // - High utilization (> 20%)
  
  if (predictability > 0.7 && (peakTPS / averageTPS) < 2) {
    return 'Provisioned (with auto-scaling)';
  }
  
  return 'On-Demand (then migrate to Provisioned after 3 months)';
}
```

### 预留容量 (Reserved Capacity)
```yaml
Savings: 53-76% discount
Commitment: 1 year
Minimum: 100 WCU or RCU

Cost Comparison (100 WCU):
  - On-Demand: $1.25 per 1M writes = $3,600/month (100 writes/sec)
  - Provisioned: 100 WCU * $0.00065/hour * 730 = $47.45/month
  - Reserved: $47.45 * 0.47 = $22.30/month

Best for: Predictable write-heavy workloads
```

## 成本异常检测

### 设置 (Setup)
```bash
# Create anomaly monitor
aws ce create-anomaly-monitor \
  --anomaly-monitor Name=ProductionMonitor,MonitorType=DIMENSIONAL,MonitorDimension=SERVICE

# Create anomaly subscription
aws ce create-anomaly-subscription \
  --anomaly-subscription Name=ProductionAlerts,MonitorArnList=arn:aws:ce::123456789012:anomalymonitor/abc123,Subscribers=[{Address=team@example.com,Type=EMAIL}],Threshold=100
```

### 异常模式 (Anomaly Patterns)
```yaml
Common Anomalies:
  - Unexpected EC2 instance launches (compromised credentials)
  - Data transfer spikes (DDoS, misconfigured app)
  - Lambda invocation explosion (infinite loops)
  - S3 GET request flood (hotlinked content)
  - RDS storage growth (missing retention policies)

Alert Thresholds:
  - Service cost: > 50% increase from baseline
  - Daily spend: > 20% above 7-day average
  - Total cost: > 10% above monthly forecast
```

## 用于成本分配的标签策略 (Tagging Strategy for Cost Allocation)

### 标签策略 (Tag Policy)
```yaml
Required Tags (enforced via AWS Config):
  Environment: [prod, staging, dev, test]
  Team: [platform, api, frontend, data]
  Project: [alpha, beta, gamma]
  CostCenter: [engineering, product, sales]
  Owner: [email@example.com]

Auto-Tagging:
  - Use AWS Organizations tag policies
  - Terraform: default_tags in provider
  - CloudFormation: Tags parameter
  - Lambda: Environment variables → tags
```

### 成本分配标签 (Cost Allocation Tags)
```bash
# Activate cost allocation tags
aws ce update-cost-allocation-tags-status \
  --cost-allocation-tags-status TagKey=Environment,Status=Active TagKey=Team,Status=Active

# View costs by tag
aws ce get-cost-and-usage \
  --time-period Start=2025-01-01,End=2025-02-01 \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --group-by Type=TAG,Key=Environment
```

## AWS 特定的最佳实践

### 多账户策略 (Multi-Account Strategy)
```yaml
Organization Structure:
  - Management account (billing only)
  - Production account (prod workloads)
  - Staging account (pre-prod)
  - Development account (dev/test)
  - Shared Services account (logging, monitoring)

Benefits:
  - Consolidated billing (volume discounts)
  - Reserved Instance sharing across accounts
  - Savings Plans apply organization-wide
  - Isolated blast radius
  - Clear cost attribution
```

### AWS 免费 tier 监控 (AWS Free Tier Monitoring)
```bash
# Set up budget for free tier limits
aws budgets create-budget \
  --account-id 123456789012 \
  --budget file://free-tier-budget.json \
  --notifications-with-subscribers file://free-tier-alerts.json
```

像云财务工程师一样优化 AWS 成本！