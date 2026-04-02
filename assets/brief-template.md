# ICT与协议安全情报简报

**周期**: 2026-03-16
**时间窗口**: 过去7天 (2026-03-09 至 2026-03-16)
**生成时间**: 2026-03-16
**数据来源**: Twitter安全研究账号

---

## 一、ICT/无线/通信协议安全

### [1] Wi-Fi客户端隔离机制可被绕过 - NDSS 2026论文

**关键词**: `#WiFiSecurity` `#ClientIsolation` `#NDSS26` `#AirSnitch`
**来源**: @vanhoefm (Mathy Vanhoef)
**发布时间**: 2026-03-10

**摘要**:
Mathy Vanhoef团队在NDSS 2026上发表研究，揭示Wi-Fi客户端隔离机制存在可被绕过的安全漏洞。攻击者通过连接到同一网络或共址的开放Wi-Fi，可拦截其他用户的流量。研究指出加密技术经常被绕过而非被破解，AirSnitch工具实现了这种加密绕过。影响范围包括企业Wi-Fi网络和公共热点。

**相关链接**:
- 论文: https://www.ndss-symposium.org/ndss-paper/example/
- GitHub: https://github.com/vanhoefm/airsnitch
- 推文: https://x.com/vanhoefm/status/2027084671780290994

---

### [2] 5G核心网安全：从物理接入到核心网妥协

**关键词**: `#5GSecurity` `#CoreNetwork` `#RedTeam`
**来源**: @p1security (P1 Security)
**发布时间**: 2026-03-11

**摘要**:
P1 Security在MWC 2026后总结指出，5G核心环境红队测试中，物理访问可通过管理平面、弱分段、不安全的远程访问或凭据窃取等途径成为网络立足点。"临时开放网络"的做法导致5G网络永久暴露的风险，在缺乏防火墙矩阵和流量可见性的情况下，运营商为解决问题而开放的网络配置往往被永久保留。

**相关链接**:
- 推文: https://x.com/p1security/status/2031653890228142321

---

## 二、AI for Sec（AI辅助安全研究/漏洞挖掘）技术洞察

### [3] Julius: LLM服务指纹识别工具

**关键词**: `#LLMFingerprinting` `#AISecurity` `#RedTeaming`
**来源**: @pentest_swissky / @praetorianlabs
**发布时间**: 2026-03-12

**摘要**:
Praetorian Labs发布Julius，用于LLM服务指纹识别。该工具通过分析AI服务的响应特征，识别模型提供商、版本、配置等信息。在AI安全领域，了解目标使用的具体模型是攻击链的第一步，这些信息对后续的提示注入、对抗样本攻击至关重要。从防御角度看，Julius帮助组织发现AI部署中的信息泄漏问题。

**相关链接**:
- 项目介绍: https://x.com/praetorianlabs/status/2032117266767061032

---

## 三、近期AI技术热点或AI架构解读

### [4] Excel Copilot Agent数据泄露漏洞 (CVE-2026-26144)

**关键词**: `#Copilot` `#AIAgent` `#DataExfiltration` `#Microsoft`
**来源**: @thezdi (TrendAI Zero Day Initiative)
**发布时间**: 2026-03-10

**摘要**:
TrendAI ZDI将CVE-2026-26144选为3月"漏洞之月"，这是Excel中利用Copilot Agent窃取数据的严重漏洞(CVSS: Critical)。该漏洞表明AI集成到传统应用时可能引入新攻击面。随着更多应用集成AI能力（Office 365 Copilot、Adobe Firefly等），此类漏洞可能变得更加常见。

**相关链接**:
- 详细分析: https://www.zerodayinitiative.com/blog/2026/3/10/cve-2026-26144

---

## 统计信息

- **收录条目**: 4 条
- **ICT/无线/协议安全**: 2 条
- **AI for Sec**: 1 条
- **AI 技术热点**: 1 条
- **检查账号数**: 50 个
- **数据来源**: Twitter 安全研究账号

---

*本简报由 AI 辅助生成，已启用相关性过滤。*
