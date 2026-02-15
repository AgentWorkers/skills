---
name: kradleverse:cleanup
description: 删除所有存储的 Kradleverse 会话信息。
---

首先，停止所有正在进行的会话，然后：

```bash
rm -rf ~/.kradle/kradleverse/sessions
```