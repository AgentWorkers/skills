---
name: kafka-iac-deployment
description: **Terraform 部署专家：专注于 Apache Kafka、AWS MSK 和 Azure Event Hubs 的部署**  
擅长使用 Terraform 部署 Kafka 相关基础设施，包括与基础设施即代码（IaC）的集成；对比托管平台与自托管平台的优缺点；以及自动化 Kafka 集群的部署流程。
---

# Kafka基础设施即代码（IaC）部署

本文档提供了使用Terraform在多个平台上部署Apache Kafka的专业指导。

## 适用场景

当您需要以下帮助时，请参考本文档：
- **Terraform部署**：如何使用Terraform部署Kafka集群
- **平台选择**：应选择AWS MSK还是自托管Kafka？
- **基础设施规划**：如何规划Kafka基础设施的规模？
- **IaC自动化**：如何自动化Kafka的部署过程？
- **持续集成/持续部署（CI/CD）**：如何为Kafka基础设施实现CI/CD流程？

## 我所掌握的知识

### 可用的Terraform模块

本插件提供了3个适用于生产环境的Terraform模块：

#### 1. **Apache Kafka（自托管，KRaft模式）**
- **位置**：`plugins/specweave-kafka/terraform/apache-kafka/`
- **平台**：AWS EC2（可适配其他云平台）
- **架构**：KRaft模式（无需依赖ZooKeeper）
- **特点**：
  - 多 broker集群（建议使用3-5个broker）
  - 支持SASL_SSL的安全组
  - 为S3备份配置IAM角色
  - 提供CloudWatch指标和警报功能
  - 支持自动扩展组
  - 可自定义VPC和子网配置
- **适用场景**：
  - 需要对Kafka配置有完全控制权
  - 需要运行Kafka 3.6及以上版本（KRaft模式）
  - 希望避免ZooKeeper带来的运营开销
  - 需要进行多云或混合环境部署
- **相关变量**：
  ```hcl
  module "kafka" {
    source = "../../plugins/specweave-kafka/terraform/apache-kafka"

    environment         = "production"
    broker_count        = 3
    kafka_version       = "3.7.0"
    instance_type       = "m5.xlarge"
    vpc_id              = var.vpc_id
    subnet_ids          = var.subnet_ids
    domain              = "example.com"
    enable_s3_backups   = true
    enable_monitoring   = true
  }
  ```

#### 2. **AWS MSK（Kafka的托管服务）**
- **位置**：`plugins/specweave-kafka/terraform/aws-msk/`
- **平台**：AWS托管服务
- **特点**：
  - Kafka服务由AWS全权管理
  - 支持IAM认证和SASL/SCRAM身份验证
  - 支持自动扩展（根据需求调整吞吐量）
  - 内置监控功能（CloudWatch）
  - 支持多AZ部署
  - 数据传输和存储均采用加密
- **适用场景**：
  - 希望由AWS负责Kafka的运营管理
  - 需要与AWS的其他服务（如IAM、KMS、CloudWatch）紧密集成
  - 更注重运营简便性而非成本
  - 需要在AWS VPC中运行Kafka
- **相关变量**：
  ```hcl
  module "msk" {
    source = "../../plugins/specweave-kafka/terraform/aws-msk"

    cluster_name           = "my-kafka-cluster"
    kafka_version          = "3.6.0"
    number_of_broker_nodes = 3
    broker_node_instance_type = "kafka.m5.large"

    vpc_id     = var.vpc_id
    subnet_ids = var.private_subnet_ids

    enable_iam_auth      = true
    enable_scram_auth    = false
    enable_auto_scaling  = true
  }
  ```

#### 3. **Azure Event Hubs（Kafka API）**
- **位置**：`plugins/specweave-kafka/terraform/azure-event-hubs/`
- **平台**：Azure托管服务
- **特点**：
  - 支持Kafka 1.0及以上协议
  - 支持弹性扩展
  - 提供高级版本（Premium SKU）以支持高吞吐量
  - 支持区域冗余
  - 支持私有端点（VNet集成）
  - 支持将事件数据存储到Azure存储中
- **适用场景**：
  - 需要在Azure云环境中运行Kafka
  - 需要Kafka兼容的API但无需自行管理Kafka服务
  - 希望实现无服务器扩展（自动扩展）
  - 需要与Azure生态系统集成
- **相关变量**：
  ```hcl
  module "event_hubs" {
    source = "../../plugins/specweave-kafka/terraform/azure-event-hubs"

    namespace_name        = "my-event-hub-ns"
    resource_group_name   = var.resource_group_name
    location              = "eastus"

    sku                   = "Premium"
    capacity              = 1
    kafka_enabled         = true
    auto_inflate_enabled  = true
    maximum_throughput_units = 20
  }
  ```

## 平台选择决策树

```
Need Kafka deployment? START HERE:

├─ Running on AWS?
│  ├─ YES → Want managed service?
│  │  ├─ YES → Use AWS MSK module (terraform/aws-msk)
│  │  └─ NO → Use Apache Kafka module (terraform/apache-kafka)
│  └─ NO → Continue...
│
├─ Running on Azure?
│  ├─ YES → Use Azure Event Hubs module (terraform/azure-event-hubs)
│  └─ NO → Continue...
│
├─ Multi-cloud or hybrid?
│  └─ YES → Use Apache Kafka module (most portable)
│
├─ Need maximum control?
│  └─ YES → Use Apache Kafka module
│
└─ Default → Use Apache Kafka module (self-hosted, KRaft mode)
```

## 部署工作流程

### 工作流程1：部署自托管Kafka（使用Apache Kafka模块）

**场景**：您希望在AWS EC2上完全控制Kafka集群的配置和运行

```bash
# 1. Create Terraform configuration
cat > main.tf <<EOF
module "kafka_cluster" {
  source = "../../plugins/specweave-kafka/terraform/apache-kafka"

  environment         = "production"
  broker_count        = 3
  kafka_version       = "3.7.0"
  instance_type       = "m5.xlarge"

  vpc_id     = "vpc-12345678"
  subnet_ids = ["subnet-abc", "subnet-def", "subnet-ghi"]
  domain     = "kafka.example.com"

  enable_s3_backups = true
  enable_monitoring = true

  tags = {
    Project     = "MyApp"
    Environment = "Production"
  }
}

output "broker_endpoints" {
  value = module.kafka_cluster.broker_endpoints
}
EOF

# 2. Initialize Terraform
terraform init

# 3. Plan deployment (review what will be created)
terraform plan

# 4. Apply (create infrastructure)
terraform apply

# 5. Get broker endpoints
terraform output broker_endpoints
# Output: ["kafka-0.kafka.example.com:9093", "kafka-1.kafka.example.com:9093", ...]
```

### 工作流程2：部署AWS MSK（Kafka的托管服务）

**场景**：您希望让AWS负责Kafka的运营管理

```bash
# 1. Create Terraform configuration
cat > main.tf <<EOF
module "msk_cluster" {
  source = "../../plugins/specweave-kafka/terraform/aws-msk"

  cluster_name           = "my-msk-cluster"
  kafka_version          = "3.6.0"
  number_of_broker_nodes = 3
  broker_node_instance_type = "kafka.m5.large"

  vpc_id     = var.vpc_id
  subnet_ids = var.private_subnet_ids

  enable_iam_auth     = true
  enable_auto_scaling = true

  tags = {
    Project = "MyApp"
  }
}

output "bootstrap_brokers" {
  value = module.msk_cluster.bootstrap_brokers_sasl_iam
}
EOF

# 2. Deploy
terraform init && terraform apply

# 3. Configure IAM authentication
# (module outputs IAM policy, attach to your application role)
```

### 工作流程3：部署Azure Event Hubs（Kafka API）

**场景**：您在Azure环境中，需要使用Kafka兼容的API

```bash
# 1. Create Terraform configuration
cat > main.tf <<EOF
module "event_hubs" {
  source = "../../plugins/specweave-kafka/terraform/azure-event-hubs"

  namespace_name      = "my-kafka-namespace"
  resource_group_name = "my-resource-group"
  location            = "eastus"

  sku                  = "Premium"
  capacity             = 1
  kafka_enabled        = true
  auto_inflate_enabled = true
  maximum_throughput_units = 20

  # Create hubs (topics) for your use case
  hubs = [
    { name = "user-events",    partitions = 12 },
    { name = "order-events",   partitions = 6 },
    { name = "payment-events", partitions = 3 }
  ]
}

output "connection_string" {
  value = module.event_hubs.connection_string
  sensitive = true
}
EOF

# 2. Deploy
terraform init && terraform apply

# 3. Get connection details
terraform output connection_string
```

## 基础设施规模规划建议

### 小型环境（开发/测试）
```hcl
# Self-hosted: 1 broker, m5.large
broker_count  = 1
instance_type = "m5.large"

# AWS MSK: 1 broker per AZ, kafka.m5.large
number_of_broker_nodes = 3
broker_node_instance_type = "kafka.m5.large"

# Azure Event Hubs: Basic SKU
sku = "Basic"
capacity = 1
```

### 中型环境（预发布/生产环境）
```hcl
# Self-hosted: 3 brokers, m5.xlarge
broker_count  = 3
instance_type = "m5.xlarge"

# AWS MSK: 3 brokers, kafka.m5.xlarge
number_of_broker_nodes = 3
broker_node_instance_type = "kafka.m5.xlarge"

# Azure Event Hubs: Standard SKU with auto-inflate
sku = "Standard"
capacity = 2
auto_inflate_enabled = true
maximum_throughput_units = 10
```

### 大型环境（高吞吐量生产环境）
```hcl
# Self-hosted: 5+ brokers, m5.2xlarge or m5.4xlarge
broker_count  = 5
instance_type = "m5.2xlarge"

# AWS MSK: 6+ brokers, kafka.m5.2xlarge, auto-scaling
number_of_broker_nodes = 6
broker_node_instance_type = "kafka.m5.2xlarge"
enable_auto_scaling = true

# Azure Event Hubs: Premium SKU with zone redundancy
sku = "Premium"
capacity = 4
zone_redundant = true
maximum_throughput_units = 20
```

## 最佳实践

### 安全最佳实践
1. **确保数据传输过程中的加密**：
  - 自托管环境：启用SASL_SSL加密
  - AWS MSK：设置`encryption_in_transit_client_broker = "TLS"`
  - Azure Event Hubs：默认启用HTTPS/TLS加密
2. **尽可能使用IAM身份验证**：
  - AWS MSK：设置`enable_iam_auth = true`
  - Azure Event Hubs：使用Azure管理的身份验证机制
3. **网络隔离**：
  - 将Kafka集群部署在私有子网中
  - 严格使用安全组/网络安全组（NSGs）进行访问控制
  - （Azure Premium SKU支持使用私有端点）

### 高可用性最佳实践
1. **多AZ部署**：
  - 自托管环境：将broker分布在3个及以上的AZ中
  - AWS MSK：自动实现多AZ部署
  - Azure Event Hubs：启用`zone_redundant = true`（高级版本）
2. **复制因子设置为3**：
  - 自托管环境：`default.replication.factor=3`
  - AWS MSK：自动配置复制因子
  - Azure Event Hubs：该参数由Azure自动管理
3. **设置最小同步副本数（min.insync.replicas = 2）**：
  - 以确保即使一个broker发生故障，系统仍能正常运行

### 成本优化建议
1. **合理选择实例规格**：
  - 使用`ClusterSizingCalculator`工具进行实例规模规划
  - 从小规模开始部署，根据实际运行情况逐步扩展
2. **启用自动扩展**：
  - AWS MSK：`enable_auto_scaling = true`
  - Azure Event Hubs：`auto_inflate_enabled = true`
3. **设置合适的日志保留策略**：
  - 根据实际需求设置`log_retention_hours`（默认为168小时，即7天）
  - 较短的保留时间可以降低存储成本

## 监控集成

所有模块都支持监控集成：
- **自托管Kafka**：通过JMX Exporter将数据发送到CloudWatch，然后使用Prometheus和Grafana进行监控
- **AWS MSK**：提供内置的CloudWatch指标，支持自定义警报
- **Azure Event Hubs**：内置Azure Monitor指标，支持与Azure Alerts的集成

## 常见问题及解决方法

### “Terraform部署失败：安全组相关问题”
**原因**：某些资源仍然依赖于旧的安全组设置
**解决方法**：
```bash
# 1. Find dependent resources
aws ec2 describe-network-interfaces --filters "Name=group-id,Values=sg-12345678"

# 2. Delete dependent resources first
# 3. Retry terraform destroy
```

### “AWS MSK集群创建耗时过长（超过20分钟）”
**原因**：AWS MSK的配置过程本身较为耗时
**解决方法**：可以使用`--auto-approve`选项加速部署流程：
```bash
terraform apply -auto-approve
```

### “Azure Event Hubs连接失败”
**原因**：Kafka协议未启用或连接字符串设置错误
**解决方法**：
1. 确保在Terraform配置中启用了`kafka_enabled`选项
2. 使用正确的Kafka连接字符串（而非Event Hubs的连接字符串）
3. 检查防火墙规则（Azure Premium SKU支持使用私有端点）

## 与其他技能的集成
- **kafka-architecture**：用于规划Kafka集群的规模和分区策略
- **kafka-observability**：用于部署后配置Prometheus和Grafana监控工具
- **kafka-kubernetes**：用于在Kubernetes上部署Kafka（作为Terraform的替代方案）
- **kafka-cli-tools**：用于使用kcat工具测试已部署的Kafka集群

## 快速参考命令

```bash
# Terraform workflow
terraform init          # Initialize modules
terraform plan          # Preview changes
terraform apply         # Create infrastructure
terraform output        # Get outputs (endpoints, etc.)
terraform destroy       # Delete infrastructure

# AWS MSK specific
aws kafka list-clusters # List MSK clusters
aws kafka describe-cluster --cluster-arn <arn> # Get cluster details

# Azure Event Hubs specific
az eventhubs namespace list # List namespaces
az eventhubs eventhub list --namespace-name <name> --resource-group <rg> # List hubs
```

---

**部署后的后续步骤**：
1. 使用`kafka-observability`技能配置Prometheus和Grafana监控
2. 使用`kafka-cli-tools`工具通过kcat测试Kafka集群的性能
3. 部署生产者/消费者应用程序
4. 定期监控Kafka集群的运行状态和性能表现