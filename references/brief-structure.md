# 简报结构模板（3 板块）

## 文件头部

```markdown
# ICT与协议安全情报简报

**周期**: YYYY-MM-DD
**时间窗口**: 过去7天 (YYYY-MM-DD 至 YYYY-MM-DD)
**生成时间**: YYYY-MM-DD
**数据来源**: N个Twitter安全研究账号

---
```

## 板块结构

### 一、ICT/无线/通信协议安全

涵盖：蜂窝网络(5G/LTE/GSM)、基带、Wi-Fi、蓝牙、SDR/RF、通信协议(Diameter/GTP/SIP/DNS)、协议Fuzzing、二进制漏洞利用。

```markdown
### [N] 标题

**关键词**: `#5G` `#Baseband` `#WiFi`
**来源**: @twitter_handle (Name)
**发布时间**: YYYY-MM-DD

**摘要**:
200-500字技术摘要，包含研究背景、技术核心、主要发现、实际影响。

**相关链接**:
- 论文: https://www.usenix.org/conference/...
- GitHub: https://github.com/...
- 推文: https://x.com/username/status/123456789

---
```

### 二、AI for Sec（AI辅助安全研究/漏洞挖掘）技术洞察

涵盖：AI/ML漏洞挖掘、LLM辅助代码审计、AI驱动Fuzzing、自动化渗透测试、AI恶意软件检测、威胁情报AI应用。

格式同上。

### 三、近期AI技术热点或AI架构解读

涵盖：LLM架构(Transformer/MoE)、AI安全对抗(Prompt注入/Jailbreak)、模型优化(量化/蒸馏)、AI Agent系统安全、新模型发布。

格式同上。

## 统计信息

```markdown
## 统计信息

- **收录条目**: N 条
- **ICT/无线/协议安全**: N 条
- **AI for Sec**: N 条
- **AI 技术热点**: N 条
- **检查账号数**: N 个
- **数据来源**: Twitter 安全研究账号

---

*本简报由 AI 辅助生成，已启用相关性过滤。*
```

## 格式要求

- 中文撰写（专业术语保留英文）
- 关键词 `#tag` 格式
- 摘要 200-500 字
- 日期必须 YYYY-MM-DD（精确到日）
- 时间窗口严格 7 天
- 来源链接必须具体（禁止主页链接、禁止 t.co 短链接）
- Twitter 链接格式: `https://x.com/username/status/tweet_id`
