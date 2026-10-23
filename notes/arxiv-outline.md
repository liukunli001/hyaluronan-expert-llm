# arXiv 稿大纲（2026-10-22 定框架；当晚由 bioRxiv 改定 arXiv；S6 出数后填结果）

类别：cs.CL（可 cross-list cs.LG / q-bio.BM）。定位纪律（与 bioRxiv 相反）：标题与摘要以
训练与评测方法领起，透明质酸是验证领域——这是给 CS 读者看的论文。

**拟题**：HA-Expert: A Domain-Adapted Language Model and Evidence-Checked Benchmark
for Hyaluronan Research

**摘要骨架**（约 250 词）：领域问题（HA 文献分散、跨糖化学/材料/临床）→ 资源：
12,306 篇全文语料 → 方法：DAPT + SFT + 带引用 RAG → 评测：HA-Expert-Bench 240 题
（答案经原文证据核定）+ 四格消融 → 结果 [S6 数字] → 可用性：权重/数据/demo 公开链接。

**章节**
1. Introduction — HA 研究的知识整合痛点；通用 LLM 在专业领域的幻觉与引用缺失；
   本工作的三件产出（语料、模型、benchmark）。
2. Corpus — PMC 采集 16,642→12,945 全文→清洗 12,306 篇 / ~126M tokens；去重；
   holdout 30 篇综述隔离（防评测泄漏）；Release v0.1-data。
3. Methods — 基座 Qwen3-8B-Base；DAPT（文档边界切块、FA2 varlen 打包、FineWeb-Edu
   回放 12%、退火集垫尾、2 epochs）；SFT（自蒸馏生成 + grounding 过滤 ≥0.55）；
   RAG（向量索引 + 引用格式）。
4. HA-Expert-Bench — 240 题构成（定量/选择/open/trap）；草稿答案的证据锚定核定流程
   （118 verified / 19 corrected / 103 uncertain→向量索引重核）；陷阱题设计（错误前提）。
5. Results — [S6 四格表：base / base+RAG / DAPT+SFT / full]；基线病理（自问自答、
   陷阱全败）→ 训练后改善；loss 曲线（如实报告 1.56 平台期与解读）。
6. Case studies — 2–3 个问答对照（基线 vs 成品，带引用）。
7. Discussion — 局限：单卡规模、8B 上限、103 题重核口径、SFT 数据自生成偏差；
   对其他小领域的可复制性（管线开源）。
8. Availability — GitHub / HF 权重与 Space / 数据 Release 链接。

**投稿动作**（作者本人）：arXiv 注册 → **先解决 endorsement**（2026-01 新政：无 arXiv
记录的新作者需 cs.CL/cs.LG 领域资深作者 personally endorse；候选池 = 在 arXiv 发过文的
Meta 同事）→ 提交 LaTeX 源码 → moderation 后上线、分配 arXiv ID。
作者：Kunli Liu（单作者；单位写 Independent Researcher / San Francisco Bay Area —
注： Meta 是雇主但本项目为个人研究，单位口径投稿前与他再确认一次）。
