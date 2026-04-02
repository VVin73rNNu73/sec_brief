# Security Weekly Brief

安全情报简报自动化生成系统。从 Twitter 安全研究者账号收集内容，生成 ICT/无线/协议安全领域的中文情报简报。

基于 `Claude Code` + `bird CLI` 。

## 快速开始

### 1. 安装依赖 bird CLI

```bash
npm install -g @steipete/bird
```

### 2. 配置twitter认证（`.env`）

编辑 `.env`，需要两个值，都从浏览器获取：

<img width="2181" height="652" alt="571801918-07e43486-f138-449b-b324-314d2e9cd36d" src="https://github.com/user-attachments/assets/bc5c391b-2eb8-4576-bea9-d0728aafc7fb" />

```
CT0=你的ct0值
AUTH_TOKEN=你的auth_token值
```

### 3. 配置信息源（`config.json`）

编辑 `config.json`，管理要监控的 Twitter 账号：

```json
{
  "sources": {
    "twitter_accounts": [
      {
        "handle": "vanhoefm",
        "name": "Mathy Vanhoef",
        "focus": "Wi-Fi Security",
        "enabled": true
      }
    ]
  }
}
```

| 字段 | 说明 |
|------|------|
| `handle` | Twitter 用户名（不含 @） |
| `name` | 显示名称 |
| `focus` | 研究方向标签 |
| `enabled` | `true` 表示纳入简报采集，`false` 表示跳过 |

新增账号只需在数组末尾追加一项，设置 `"enabled": true` 即可。

## 生成简报

在 Claude Code 中执行：

```
/security-brief
```

或输入“生成安全简报”相关的提示词。

输出markdown报告主题：

| 分类 | 覆盖范围 |
|------|----------|
| ICT/无线/通信协议安全 | 5G/LTE/GSM、基带、Wi-Fi、蓝牙、SDR/RF、协议 fuzzing |
| AI for Sec | AI/ML 漏洞发现、LLM 辅助审计、自动化渗透测试 |
| AI 技术热点 | LLM 架构、AI 安全、模型优化、Agent 系统 |

## 注意事项

默认时间窗口为 7 天，可在 skill 参数中调整
