# 内存证明（Proof-of-Memory）——基于比特币工作量证明（PoW）的不可篡改区块链\n\n`PoW hashes daily memory/YYYY-MM-DD.md`（SHA256哈希值，结合随机数（nonce）的计算过程，最终生成0000s长度的哈希值）——这种机制确保了`MEMORY.md`文件的安全性，防止篡改。同时，该机制支持主节点对区块链数据的回滚操作（sovereign recall）。\n\n## 使用方法\  
运行以下命令，实现每86400秒自动执行一次任务：  
`cron every=86400s: node skills/pom/pom.js`\n\n## 测试方法\  
同样运行`node skills/pom/pom.js`命令进行测试。\n\n**示例：**  
PoM区块：`0000a1b2c3d4...`（随机数：`1234`）