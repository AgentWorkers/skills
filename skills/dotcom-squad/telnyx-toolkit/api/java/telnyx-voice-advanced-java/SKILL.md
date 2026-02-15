---
name: telnyx-voice-advanced-java
description: >-
  Advanced call control features including DTMF sending, SIPREC recording, noise
  suppression, client state, and supervisor controls. This skill provides Java
  SDK examples.
metadata:
  author: telnyx
  product: voice-advanced
  language: java
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Voice Advanced - Java

## 安装

```text
// See https://github.com/team-telnyx/telnyx-java for Maven/Gradle setup
```

## 设置

```java
import com.telnyx.sdk.client.TelnyxClient;
import com.telnyx.sdk.client.okhttp.TelnyxOkHttpClient;

TelnyxClient client = TelnyxOkHttpClient.fromEnv();
```

以下所有示例均假设 `client` 已按上述方式初始化。

## 更新客户端状态

更新客户端状态：

`PUT /calls/{call_control_id}/actions/client_state_update` — 必需参数：`client_state`

```java
import com.telnyx.sdk.models.calls.actions.ActionUpdateClientStateParams;
import com.telnyx.sdk.models.calls.actions.ActionUpdateClientStateResponse;

ActionUpdateClientStateParams params = ActionUpdateClientStateParams.builder()
    .callControlId("call_control_id")
    .clientState("aGF2ZSBhIG5pY2UgZGF5ID1d")
    .build();
ActionUpdateClientStateResponse response = client.calls().actions().updateClientState(params);
```

## SIP 转接呼叫

在呼叫控制过程中发起 SIP 转接：

`POST /calls/{call_control_id}/actions/refer` — 必需参数：`sip_address`

```java
import com.telnyx.sdk.models.calls.actions.ActionReferParams;
import com.telnyx.sdk.models.calls.actions.ActionReferResponse;

ActionReferParams params = ActionReferParams.builder()
    .callControlId("call_control_id")
    .sipAddress("sip:username@sip.non-telnyx-address.com")
    .build();
ActionReferResponse response = client.calls().actions().refer(params);
```

## 发送 DTMF 音调

从当前通话链路发送 DTMF 音调：

`POST /calls/{call_control_id}/actions/send_dtmf` — 必需参数：`digits`

```java
import com.telnyx.sdk.models.calls.actions.ActionSendDtmfParams;
import com.telnyx.sdk.models.calls.actions.ActionSendDtmfResponse;

ActionSendDtmfParams params = ActionSendDtmfParams.builder()
    .callControlId("call_control_id")
    .digits("1www2WABCDw9")
    .build();
ActionSendDtmfResponse response = client.calls().actions().sendDtmf(params);
```

## 启动 SIPREC 会话

启动在 SIPREC 连接器中配置的 SIPREC 会话：

`POST /calls/{call_control_id}/actions/siprec_start`

```java
import com.telnyx.sdk.models.calls.actions.ActionStartSiprecParams;
import com.telnyx.sdk.models.calls.actions.ActionStartSiprecResponse;

ActionStartSiprecResponse response = client.calls().actions().startSiprec("call_control_id");
```

## 停止 SIPREC 会话

停止 SIPREC 会话：

`POST /calls/{call_control_id}/actions/siprec_stop`

```java
import com.telnyx.sdk.models.calls.actions.ActionStopSiprecParams;
import com.telnyx.sdk.models.calls.actions.ActionStopSiprecResponse;

ActionStopSiprecResponse response = client.calls().actions().stopSiprec("call_control_id");
```

## 启用噪声抑制（测试版）

启用噪声抑制功能：

`POST /calls/{call_control_id}/actions/suppression_start`

```java
import com.telnyx.sdk.models.calls.actions.ActionStartNoiseSuppressionParams;
import com.telnyx.sdk.models.calls.actions.ActionStartNoiseSuppressionResponse;

ActionStartNoiseSuppressionResponse response = client.calls().actions().startNoiseSuppression("call_control_id");
```

## 停用噪声抑制（测试版）

停用噪声抑制功能：

`POST /calls/{call_control_id}/actions/suppression_stop`

```java
import com.telnyx.sdk.models.calls.actions.ActionStopNoiseSuppressionParams;
import com.telnyx.sdk.models.calls.actions.ActionStopNoiseSuppressionResponse;

ActionStopNoiseSuppressionResponse response = client.calls().actions().stopNoiseSuppression("call_control_id");
```

## 切换监督者角色

切换桥接呼叫的监督者角色：

`POST /calls/{call_control_id}/actions/switch_supervisor_role` — 必需参数：`role`

```java
import com.telnyx.sdk.models.calls.actions.ActionSwitchSupervisorRoleParams;
import com.telnyx.sdk.models.calls.actions.ActionSwitchSupervisorRoleResponse;

ActionSwitchSupervisorRoleParams params = ActionSwitchSupervisorRoleParams.builder()
    .callControlId("call_control_id")
    .role(ActionSwitchSupervisorRoleParams.Role.BARGE)
    .build();
ActionSwitchSupervisorRoleResponse response = client.calls().actions().switchSupervisorRole(params);
```

---

## Webhook

以下 webhook 事件会被发送到您配置的 webhook URL。所有 webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 标头以进行验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `callReferStarted` | 转接呼叫开始 |
| `callReferCompleted` | 转接呼叫完成 |
| `callReferFailed` | 转接呼叫失败 |
| `callSiprecStarted` | SIPREC 会话开始 |
| `callSiprecStopped` | SIPREC 会话停止 |
| `callSiprecFailed` | SIPREC 会话失败 |
```