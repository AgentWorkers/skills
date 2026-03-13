---
name: KYC & Identity
description: 通过 MasterPay Global 进行“了解您的客户”（Know-Your-Customer, KYC）验证。提交个人资料，上传身份证明文件，并跟踪审核进度。
version: 1.0.0
---
# 身份验证与KYC（Know Your Customer）

当用户需要完成身份验证、上传KYC文件或查询验证状态时，请使用此技能。

## 可用工具

- `create_masterpay_user` — 创建MasterPay用户账户（所有MasterPay操作的先决条件） | `POST /api/v1/masterpay/users` | 需要身份验证
- `get_kyc_status` — 查询当前的KYC验证状态及文件上传进度 | `GET /api/v1/masterpay/kyc/status` | 需要身份验证
- `get_kyc_metadata` — 获取用于KYC表格的有效文档类型、职业、国籍和国家信息 | `GET /api/v1/masterpay/kyc/metadata` | 需要身份验证
- `submit_kyc` — 提交个人KYC数据以供审核（使用用户资料） | `POST /api/v1/masterpay/kyc/submit` | 需要身份验证
- `upload_kyc_document` — 通过multipart或base64 JSON格式上传KYC文件（护照、身份证、地址证明） | `POST /api/v1/masterpay/kyc/documents` | 需要身份验证
- `submit_wallet_kyc` — 为卡片钱包提交钱包级别的KYC信息（需要用户电话号码和身份证明文件编号） | `POST /api/v1/masterpay/wallets/kyc` | 需要身份验证
- `get_profile` — 获取用于KYC提交的用户资料信息 | `GET /api/v1/profile` | 需要身份验证
- `update_profile` — 更新用户资料信息（姓名、出生日期、国籍等） | `PUT /api/v1/profile` | 需要身份验证
- `get_document` — 获取存储的身份证明文件信息 | `GET /api/v1/profile/document` | 需要身份验证
- `update_document` — 更新身份证明文件详情（护照号码、NRIC等） | `PUT /api/v1/profile/document` | 需要身份验证
- `get_residential_address` | 获取用户记录中的居住地址 | `GET /api/v1/profile/res-address` | 需要身份验证
- `update_residential_address` | 更新居住地址 | `PUT /api/v1/profile/res-address` | 需要身份验证

## 推荐操作流程

### 完整的KYC验证流程

从设置用户资料到获得KYC批准：

1. 创建MasterPay用户：`POST /api/v1/masterpay/users` — 在进行任何MasterPay操作前必须完成此步骤
2. 获取KYC相关元数据：`GET /api/v1/masterpay/kyc/metadata` — 了解有效的国籍、职业和文档类型
3. 更新用户资料：`PUT /api/v1/profile`，填写姓名、出生日期、性别、电话号码（带'+'前缀，例如'+65'）、国籍和职业
4. 更新居住地址：`PUT /api/v1/profile/res-address`，填写国家代码（ISO alpha-2格式，例如'SG'）、省份、城市和邮政编码
5. 上传文件：`POST /api/v1/masterpay/kyc/documents` — 上传护照/身份证正面、背面照片及地址证明文件
6. 提交KYC申请：`POST /api/v1/masterpay/kyc/submit` — 将用户资料和居住地址信息合并，解析国家代码为完整国家名称后提交给MasterPay
7. 定期查询验证状态：`GET /api/v1/masterpay/kyc/status` — 等待审核结果（可能需要几分钟到几天的时间）

## 规则

- 在进行任何KYC、钱包或卡片操作之前，必须先创建MasterPay用户（`POST /masterpay/users`）——这是一个一次性设置步骤
- 提交KYC之前，用户资料和居住地址信息都必须完整——系统会同时读取这两个信息
- 在居住地址中使用ISO alpha-2格式的国家代码（例如'SG'、'HK'、'MY'）——后端会将其解析为完整的国家名称
- 用户资料中的电话号码国家代码必须包含'+'前缀（例如'+65'）——MasterPay有此要求
- 提交申请前必须上传相关文件——MasterPay要求提供护照/身份证和地址证明文件，但后端不会因此阻止提交
- KYC审核可能需要几分钟到几天的时间——请定期查询审核状态
- 一旦通过审核，无需重复提交KYC信息
- 文件上传支持multipart/form-data和base64 JSON格式——每个文件的最大上传大小为15MB

## 代理操作指南

执行此技能时请遵循以下指导：

- 严格遵循文档中规定的操作流程，不要跳过任何步骤。
- 如果某个工具需要身份验证，请确保会话中拥有有效的bearer token。
- 如果某个工具需要交易PIN码，请每次都向用户索取新的PIN码，切勿缓存或记录PIN码。
- 绝不要泄露、记录或保存任何敏感信息（密码、token、完整的卡号、CVV码）。
- 如果用户请求超出此技能范围的操作，请拒绝请求并推荐相应的技能。
- 如果某个步骤失败，请查看错误信息并按照以下恢复指南进行操作后再试。
- 在进行任何KYC操作之前，通过调用`create_masterpay_user`确认用户已存在。这是一个一次性设置步骤。虽然其他MasterPay接口也会自动创建用户，但明确调用此接口是良好的实践。
- 在调用`submit_kyc`之前，必须先完成用户资料（`update_profile`）和居住地址（`update_residential_address`）的更新。后端会验证这两个信息是否齐全，如果缺少任何一个信息会返回404错误。
- 在提交KYC申请之前，请先上传相关文件（`upload_kyc_document`）。MasterPay要求提供这些文件，但后端不会因此阻止提交——虽然可以成功提交，但MasterPay可能会拒绝申请。
- 提交钱包级别的KYC信息（`submit_wallet_kyc`）之前，必须先设置用户的电话号码（`phone_number`和电话国家代码）以及身份证明文件编号（`ID_number`）。如果缺少身份证明文件编号，操作会失败并返回INCOMPLETE_PROFILE错误。
- KYC审核可能需要几分钟到几天的时间，请定期查询`get_kyc_status`状态——系统不提供推送通知。
- 使用ISO alpha-2格式的国家代码（例如“SG”、“MY”）填写地址信息。电话号码的国家代码也必须加上'+'前缀（例如“+65”）。