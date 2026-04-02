---
name: security-brief
description: >
  Automate the generation of security intelligence briefs. Use when user needs to:
  (1) Fetch security content from Twitter accounts using bird CLI,
  (2) Generate Markdown brief following the 3-section structure.
  Sections: (1) ICT/Wireless/Protocol Security, (2) AI for Sec, (3) AI Tech Insights.
  MUST fetch from ALL accounts in config.json (located in this skill directory) BEFORE generating reports.
  MUST strictly filter — only include items clearly belonging to one of the 3 sections.
---

# Security Brief Generator

自动化生成 ICT/无线/协议安全领域情报简报。

## 核心规则

1. **必须检查所有账号** — 从 `config.json` 读取所有 `enabled: true` 的 Twitter 账号，全部检查完毕后才能生成报告
2. **严格内容过滤** — 每条内容必须明确属于 3 个板块之一，不确定则排除
3. **7 天时间窗口** — 脚本自动过滤，只收录过去 7 天内发布的内容（`--days 7`）
4. **日期精确到日** — 格式 YYYY-MM-DD，禁止只有年月
5. **禁止短链接** — 不使用 t.co/bit.ly 等，必须展开为完整 URL
6. **禁止主页链接** — 不使用 syssec.kr/publications、sec.today 等主页作为唯一来源

## 工作流程

### Step 1: 获取推文（分批模式 + 时间过滤）

运行脚本自动获取所有 `config.json` 中 enabled 的账号推文，按账号分批保存到文件，并自动过滤 7 天内的推文：

```bash
python3 .claude/skills/security-brief/scripts/fetch_tweets.py --batch-mode --batch-size 10 --days 7 --count 20
```

脚本行为：
- 从所有 enabled 账号获取推文
- **自动时间过滤**（只保留 7 天内的推文，脚本端完成）
- 按每 10 个账号分批，保存到 `.cache/tweets/batch_N.json`
- 每条推文包含：`id`, `account`, `text`, `date`, `url`（完整推文链接）
- 输出 JSON 到 stdout，包含 `batch_files`（文件路径列表）和 `tweet_ids`（所有推文 ID）

如果 `total_tweets` 为 0，告知用户没有符合条件的推文，流程结束。

### Step 2: 逐条阅读并判断相关性

**关键**：不使用关键词过滤脚本，直接用 AI 逐条判断。

逐个读取 batch 文件，对每条推文：
1. 阅读完整推文文本
2. 判断：是否有技术深度？（参考"相关性判断流程"）
3. 判断：明确属于 3 个板块之一吗？
4. 不确定或无技术深度 = 直接排除

**禁止**：使用 Python 脚本做关键词匹配过滤，这会导致大量误判。

### Step 3: 生成 Markdown 简报

收集通过筛选的推文后，生成简报。每条推文的 URL 已在 batch 文件中（`tweet['url']`），直接使用，无需再调用 bird。

文件名：`Security_Weekly_Brief_YYYY-MM-DD.md`
模板参考：`Security_Weekly_Brief_2026-03-23.md`（优秀案例）

---

## 3 个板块定义

### 一、ICT/无线/通信协议安全

收录：
- 蜂窝网络协议漏洞（5G/LTE/GSM/UMTS/CDMA）
- 基带/核心网/RAN 安全
- 无线协议（Wi-Fi/蓝牙/BLE/Zigbee/LoRa）
- SDR/RF 攻击、信号分析
- 通信协议（Diameter/GTP/SIP/DNS）漏洞
- 协议 Fuzzing、二进制漏洞利用
- 网络基础设施安全

排除：通用 Web 漏洞（SQL注入/XSS）、纯移动 App 漏洞、云安全/容器安全、社会工程学、与协议无关的恶意软件分析。

关键词：`#5G` `#LTE` `#WiFi` `#Bluetooth` `#SDR` `#Baseband` `#Fuzzing` `#RCE` `#Protocol`

### 二、AI for Sec（AI辅助安全研究/漏洞挖掘）

收录：
- LLM/ML 用于漏洞挖掘
- AI 辅助代码审计工具
- AI 驱动的 Fuzzing 框架
- 自动化渗透测试工具
- AI 恶意软件检测
- 威胁情报中的 AI 应用

排除：通用 AI 工具（非安全领域）、AI 论文（不涉及安全应用）、ML 教程、数据科学工具、商业 AI 产品宣传（无技术细节）。

关键词：`#AIforSec` `#LLMfuzzing` `#AISecurity` `#AutomatedSec` `#CodeAudit`

### 三、近期AI技术热点或AI架构解读

收录：
- 新 LLM 架构（Transformer/MoE/新注意力机制）
- AI 安全对抗（Prompt 注入/Jailbreak）
- 模型优化（量化/蒸馏/边缘部署）
- AI Agent 系统安全
- 新模型/框架发布（有技术细节）

排除：通用 AI 新闻（无技术细节）、AI 商业动态/融资新闻、AI 产品评测（非技术）、AI 观点评论（无实质内容）。

关键词：`#LLM` `#GPT` `#Transformer` `#PromptInjection` `#AIModel` `#Agent`

### 分类规则

- Section 1 = 传统 ICT/无线/协议安全（非 AI 或 AI 无关）
- Section 2 = AI 应用于安全问题（工具、漏洞发现技术）
- Section 3 = AI 技术本身（架构、模型、趋势）
- 跨板块内容按主要焦点分类
- 不属于任何板块的内容直接排除

---

## 相关性判断流程

对每条推文依次检查：

1. **有技术细节吗？** → 没有则排除
2. **明确属于 3 个板块之一吗？** → 不属于或不确定则排除
3. **与板块主题直接相关吗？** → 弱相关则排除
4. **是原创研究/深度分析吗？** → 浅层新闻/转发资讯则排除

原则：**不确定 = 排除，宁缺毋滥**。

### 必须排除的内容类型

**资讯类（无技术价值）**：
- 培训课程/会议通知/CFP
- 产品发布/工具更新公告（无技术细节）
- Bug Bounty 计划公告
- 招聘/融资/商业新闻
- 纯转发的新闻（无分析）

**技术深度不足**：
- 通用 Web 漏洞（SQL注入/XSS/CSRF）
- 纯移动 App 逆向（非协议层）
- 云安全/容器安全/DevOps
- 通用安全工具更新（无新技术）
- CVE 公告（无利用细节/技术分析）

**非聚焦领域**：
- 5G 基站建设新闻（与安全无关）
- 通用 AI 工具（非安全领域）
- AI 观点评论（无实质内容）

### 优先收录的内容

- **漏洞原理分析**（内存损坏、协议缺陷、加密问题）
- **利用技术细节**（exploit chain、PoC 代码）
- **原创研究成果**（新攻击面、新工具、新方法）
- **深度技术解读**（架构分析、逆向工程）
- **实战案例**（APT 分析、真实攻击链）

---

## 条目格式要求

每条记录必须包含：

```markdown
### [N] 标题

**关键词**: `#tag1` `#tag2`
**来源**: @twitter_handle (Name)
**发布时间**: YYYY-MM-DD

**摘要**:
200-500字技术摘要。

**相关链接**:
- 推文: https://x.com/username/status/123456789
- 论文/博客: https://具体URL（非主页、非短链接）
```

### 链接规则

- Twitter: `https://x.com/username/status/tweet_id`
- 找不到具体 URL 时：搜索 Google Scholar / 会议网站 / GitHub，最后才用主页并注明"具体链接暂时无法获取"

---

## 输出格式

### Markdown 简报

文件名：`Security_Weekly_Brief_YYYY-MM-DD.md`，中文撰写（专业术语保留英文）。

结构参考 `references/brief-structure.md` 和 `assets/brief-template.md`。
