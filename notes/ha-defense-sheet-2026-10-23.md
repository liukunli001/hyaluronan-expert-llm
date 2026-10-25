# HA-Expert 答辩一页纸（2026-10-23）

用途：教授/面试被追问时用。中文是理解，英文是可直接说出口的版本。所有数字与 S6 成绩单、项目记录对齐。

链接：Demo https://huggingface.co/spaces/liukunli/ha-expert-demo ｜ SFT 模型 https://huggingface.co/liukunli/ha-expert-qwen3-8b ｜ DAPT 检查点 https://huggingface.co/liukunli/ha-expert-qwen3-8b-dapt ｜ 索引 https://huggingface.co/datasets/liukunli/ha-expert-index

## 30 秒版（项目一句话）

Qwen3-8B-Base → 在 12,306 篇透明质酸论文上做 domain-adaptive pretraining（DAPT）→ 用 DAPT 模型自生成、经原文证据过滤的 12,003 条 QA 做 SFT → 外挂 RAG。自建 HA-Expert-Bench（240 题，答案键经证据核定）：base 0.300 → DAPT+SFT 0.601 → 最好成绩（base+RAG）0.710。

## 成绩单（HA-Expert-Bench，240 题；对=1 / 部分对=0.5 / 错=0）

| Cell | Overall | MCQ | Quant | Open | Trap |
|---|---|---|---|---|---|
| Qwen3-8B-Base | 0.300 | 0.800 | 0.250 | 0.282 | 0.267 |
| DAPT+SFT（本模型） | 0.601 | 0.900 | 0.300 | 0.631 | 0.500 |
| Base + RAG | 0.710 | 0.900 | 0.450 | 0.719 | 0.867 |
| 本模型 + RAG | 0.662 | 0.700 | 0.550 | 0.676 | 0.633 |

题型：MCQ 选择题 10 道（考记忆，选项字母自动判分）；Quant 定量题 20 道（考精确数值，容差判分，四格里最难）；Open 开放题 195 道（考理解，评审模型对照证据核定的标准答案打分）；Trap 陷阱题 15 道（题面埋错误前提，考会不会先纠正前提、拒绝顺着错误往下答）。

## 追问 1：为什么 Base+RAG 分数最高？那 training 有什么用？

先认账（这是加分项，别遮）：只看这张考卷、且检索随时可用时，这一版训练确实没赢过 base+RAG。机制有三层：

1. **RAG 正好补上 base 最大的短板。** base 差在缺领域知识；RAG 把原文直接塞进 prompt，知识短板瞬间消失，剩下的"读材料、组织答案"恰是 base 本来擅长的。所以 Trap 从 0.267 暴涨到 0.867——正确原文在眼前，模型有底气反驳错误前提。
2. **SFT 的增益与 RAG 大量重叠。** SFT 存进参数的知识，RAG 在场时是冗余的，只剩答题格式/行为的优势，所以单独能翻倍（0.300→0.601），叠加 RAG 后加成变小。
3. **SFT 在 RAG 场景下有反作用（输掉的 0.048 主要在这）：** 12,003 条 SFT 数据全是"裸问题→答案"，模型没见过"问题+检索片段+引用要求"的格式——5/240 条崩成引用标记循环；自蒸馏遗传了教师的重度重复（SFT 35/240 vs base 10/240、base+RAG 7/240），重复吃掉 token 预算导致答案截断。

训练的用处（不在这一格里）：

- **没有检索时，训练就是全部差距**：0.300→0.601 是纯训练挣的；base+RAG 的 0.710 租的是索引，不是模型自己的。低延迟、离线、模型单独部署时，参数里的知识才是自己的。
- **训练治行为病，RAG 只是盖住**：base 会自编后续问题、不答题、顺错误前提往下说；检索漏检时立刻打回原形。Trap 裸考 0.267→0.500 就是训练的差别。
- **Quant 上训练+RAG 是全场最高（0.550）**：数值题要"读懂检索来的数字再算"，这一格两者真叠加。
- **没有训练就没有这条流水线**：SFT 数据是 DAPT 模型自己当老师生成的；base 那个自编问题的毛病恰恰最不能当老师。训练既是产品，也是生产工具。
- **"没赢"本身是消融的价值**：病因定位到数据格式（缺 retrieval-format 样本），对应文献里的做法是 retrieval-aware fine-tuning（RAFT 一线）。修复路径已写进论文：SFT 混入 RAG 格式样本 + 过滤教师重复输出，做完 SFT+RAG 应能反超。

英文一句话（现成版）："Training doubles the model on its own and gives the best quantitative score with retrieval; the reason SFT+RAG trails base+RAG is a format mismatch I diagnosed in the ablation — no retrieval-context examples in SFT — and the fix is retrieval-formatted training data."

## 数字口径卡（最容易被问穿的 5 个，别说错）

- **12,306 篇**是语料总量（约 126M token）；真正喂进 DAPT 的是核心集 4,952 篇 / 60M token + 退火集 498 篇 / 5.7M token。全量 12,306 篇用在 SFT 素材与检索索引上。
- **0.710 是 base+RAG 的成绩，不是本模型的。** 本模型裸考 0.601、本模型+RAG 0.662；demo 简介写的是 "best with retrieval 0.710"，完整四格表在模型卡里兜底。
- **SFT 数据是自生成的**：DAPT 模型经 vLLM 本地服务当老师出题答题、按原文证据过滤，$0 API 成本；没有用 GPT 老师。
- **Bench 答案键不是我拍的**：240 题中 212 题经证据核定定案（v3：72 道存疑题确认、3 道改正 B22/F07/G14、28 道仍存疑）；改过的题逐格重判，S6 四格分数不变。评审（judge）是本地 SFT 模型、按核定答案锚定打分——被问到要主动披露 judge 也给自己那格打分、用的是同一锚定标准。
- **训练量**：DAPT 212/212 步、约 5 小时 34 分、final loss ≈1.55；SFT 752 步、train loss 1.214、token accuracy 0.725。RAG 索引 636,959 个向量（Qwen3-Embedding-0.6B + FAISS），答题时取最相关的 4 段原文。

## 还会被问的两个

- **为什么选 Qwen3-8B-Base 不用现成 instruct 模型？** 要测的是"领域训练本身贡献多少"，基座是干净的起点；instruct 模型的提升无法归因到 DAPT/SFT。这也是四格消融能成立的前提。
- **下一步做什么？** 两件事已定位：① SFT 混入 RAG 格式数据重训（retrieval-aware），目标 SFT+RAG 反超 0.710；② 过滤教师输出的重复样本。S7 在跑：用新颖性检索从模型生成原始 HA 研究想法，top 想法扩成完整 proposal 待审。
