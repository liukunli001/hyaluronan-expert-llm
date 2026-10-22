# Hyaluronan Expert LLM — 项目计划

日期：2026-10-21
定位：用 Karpathy 的 nanochat 管线做一个**透明质酸（hyaluronan / HA）领域专家模型**：领域训练 + 检索增强（RAG）问答 + 专家验证的评测集。用途：简历项目、CS PhD 申请（面试谈资 + SOP 方向一 "AI to accelerate scientific discovery" 的实证）、后续研究练手。
技术路线：nanochat（fork）→ 基线跑通 → HA 语料 mid-training（领域自适应）→ SFT 问答 → RAG 带引用问答 → 三方对比评测。Raschka《Build a Large Language Model (From Scratch)》作随查参考书；Lambert《RLHF Book》作后训练参考。

---

## 一、你要收集的数据（五类）

### A. 领域语料（给 mid-training 用，教模型"懂" HA）

| 来源 | 内容 | 获取方式 | 规模目标 |
|---|---|---|---|
| PMC Open Access 全文 | HA 相关研究论文 + 综述全文（XML） | NCBI E-utilities + PMC OA 接口，检索词：hyaluronan OR "hyaluronic acid" OR hyaluronate | 目标 1,000–3,000 篇全文（实际数以抓取为准） |
| PubMed 摘要 | 无 OA 全文者的摘要 + 标题 + MeSH 词 | E-utilities efetch | 数千条，作补充语料 |
| 综述与权威章节 | HA 领域大综述（糖科学、Adv Drug Deliv Rev、Biomaterials 等）、Glycoforum/Glycoscience 的 HA 专辑 | 从 PMC OA 里按 review 类型筛 + 手工列必读清单（约 30–50 篇） | 语料里的高质量核心，训练时可多过 1 个 epoch |
| 你自己的成果 | 你的 HA 综述（Carbohydr. Res. 2022）、Carbohydr. Polym. 2023、Small Science 2024 等一作/合作论文 + MSU 博士论文全文 | 你手头原文 | 必入；这是语料里与你方向最贴的部分 |
| 基础教材文本 | 糖生物学 / ECM / 多糖化学的基础章节、Wikipedia 的 HA 相关词条群 | 公开来源整理 | 少量，作概念地基 |

子领域配比（按你的方向加权）：HA 合成与化学修饰、分子量与信号转导、CD44 / RHAMM 生物学、HA 纳米颗粒与药物递送、HA 与肿瘤、HA 水凝胶与组织工程、临床与医美（低权重）。

**处理要求**：XML → 纯文本；去掉参考文献列表段（降噪）、保留图注；去重（同 DOI/标题）；按预估 token 统计总量。预期语料量级：数千万 token——比通用预训练小得多，所以训练策略是 **多 epoch（2–4）+ 混入通用数据回放（FineWeb 抽样，约 30–50%）防灾变遗忘**，这是领域自适应预训练（DAPT）的标准做法。

### B. SFT 数据（教模型"答"，问答格式）

- **机器生成 + 抽查**：用强教师模型（Claude / GPT 级 API）从 A 的语料段落生成问答对，六类题型：事实问答、机制解释（如高/低分子量 HA 的不同效应）、对比辨析（如 HA-CD44 vs 其他靶向）、方法类（合成与表征怎么做）、应用类（递送/成像/临床）、计算类（分子量、浓度、结合常数换算）。
- **数量**：5,000–20,000 对；生成后做自动过滤（去重、长度、答案须能在原文段落里找到依据）。
- **你的种子集**：从你的综述和博士论文里手工出 100–200 对高质量问答（或口述要点、助手成稿你改）。
- **质量闸门（只能你做）**：随机抽查 100 对，错误率 >5% 就回炉改生成提示词。
- 格式：与 nanochat 的 SFT / task mixture 格式对齐；同时混一部分通用指令数据（nanochat 自带的 SmolTalk 抽样），防止模型只会答 HA、不会正常聊天。

### C. RL 数据（可选阶段，时间紧先砍）

- 可验证题：选择题（有唯一正确答案）+ 计算题（精确匹配判分），从教材题与 B 中筛出，1,000–3,000 题，给 GRPO 用（nanochat 自带 GRPO 阶段，原用 GSM8K，此处换成 HA 可验证题）。

### D. 评测集（最重要，先建或与 A 并行建——这是项目的credibility所在）

- **HA-Expert-Bench：200–300 题**，来源：你的综述内容、教材课后题、你自拟；覆盖定义事实、机制（CD44 信号）、方法（合成/表征）、应用（递送/成像）、定量推理，外加一组**陷阱题**（问不存在的相互作用/编造的数值，测幻觉——答"不确定/无此证据"才算对）。
- **答案键全部由你本人核定**（约 2–3 小时，这是整个项目里只有你能做、也最值钱的一步）。
- **防污染铁律**：用来出评测题的论文/段落从训练语料里剔除（hold-out），否则分数作废。
- 通用能力对照：nanochat 自带 CORE + MMLU（化学相关子集可单列），用来证明"学了 HA 没忘掉其他"。

### E. 检索索引（给 RAG 用）

- 与 A 同一语料，切块（500–1,000 token / 块，带重叠），用小型开源 embedding 模型向量化，存 FAISS 索引；每块保留元数据（标题、作者、年份、期刊、DOI/PMID）——回答时按此给出**可核查的引用**。

**合规**：只用 PMC OA（许可允许再利用）与 PubMed 摘要；不爬付费墙全文；你自己的论文与博士论文自由使用。

---

## 二、执行步骤

分工原则：脚本与管线由 Zuck 代写、代跑（抓取、清洗、生成、索引、评测脚本）；**只有你能做的**只有三件——① 定语料范围（本计划即默认版，你点头即行）② 核定评测集答案（2–3 h）③ 抽查 SFT 问答 100 对（约 1 h）。

| Phase | 内容 | 时间 | 成本 |
|---|---|---|---|
| 0 环境与基线 | fork nanochat；租 8×H100 节点（Lambda / RunPod / Vast 等）；原样跑 speedrun，确认管线 + 拿到基线 report card | 半天 | ~$100 |
| 1 数据 | 按第一节写抓取/清洗脚本 → 语料 v1；生成 SFT 问答；建评测集骨架（你核定答案）；建检索索引 | 3–5 天（多为脚本与等待，你的时间约 3–4 h） | 教师 API ~$20–50 |
| 2 基线评测 | 基线模型跑 HA-Bench + CORE，记录分数（后面所有提升都对着这张表） | GPU ~1 h | 含在租金内 |
| 3 领域训练 | 从 speedrun 检查点继续训练：HA 语料（2–4 epoch）+ FineWeb 回放混训；中途检查点各跑一次评测探针 | GPU 半天 | ~$100–200 |
| 4 SFT | HA 问答 + 通用指令混训；评测 | GPU 1–2 h | 含在租金内 |
| 5 RAG | FAISS 索引接入问答（在 nanochat 的推理/聊天界面外包一层检索），回答带文献引用；评测三方对比：基线 / 训练后 / 训练后+RAG | 开发 1–2 天，GPU 占用很小 | ~$0–50 |
| 6 RL（可选） | GRPO 跑 C 类可验证题；评测 | GPU ~1 天 | ~$100 |
| 7 打包 | README（方法 + 结果表 + 示例问答）、代码仓库整理、简历句落数、面试讲稿要点（3 分钟版） | 1 天 | — |

**总计**：日历约 2 周（与申请材料并行、业余时间）；GPU + API 约 **$300–600**。

## 三、时间线（与申请季的关系，硬约束）

- 优先级排序不变：Amanda Yin 推荐信、SOP 各校版本、12 月申请提交 > 本项目。
- 建议节奏：10 月底–11 月初做 Phase 0–1（数据期不占注意力）；11 月中一个周末集中做 Phase 2–5；Phase 7 在 12 月上旬完成，数字赶得上写进 CV 就写、赶不上就留给 1–2 月面试用。
- **硬止损**：12 月中还没完成 Phase 5，就冻结在当前状态，不许挤占申请提交时间；面试前再解冻收尾也来得及。

## 四、风险与取舍（如实）

- 语料小（数千万 token 级）→ 模型的"知识"主要靠 RAG 兜底，训练解决的是领域语言、概念与答题方式；不要对外宣称"模型记住了全部 HA 文献"，宣称口径 = 领域训练 + 检索 grounding + 专家验证评测。
- 教师生成的问答会有错 → 靠你的抽查闸门 + 答案须有原文依据的自动过滤控制；评测集答案 100% 你本人核定，与训练数据的质量风险隔开。
- 付费墙 → 语料以 OA 为主会有偏倚（偏新、偏开放获取期刊），在 README 里如实写明语料构成。
- 小模型天花板 → 目标不是比过 GPT 级大模型，是"同尺寸下领域能力的可测提升 + 带引用的可信问答"；对比表里同尺寸基线才是对手。

## 五、产出与简历句（数字待实测填入）

产出物：GitHub 仓库（代码 + 报告卡）、HA-Expert-Bench 评测集、三方对比结果表、带引用的问答 Demo。

简历句模板：
"Built a hyaluronan expert LLM: domain-adaptive training of a [depth/参数] nanochat model on a [N]-paper hyaluronan corpus with retrieval-grounded, citation-backed QA; on a self-built, expert-verified 250-question benchmark, accuracy improved from [A]% (base) to [B]% (domain-trained) and [C]% (+retrieval), with general CORE score retained within [N] points."
