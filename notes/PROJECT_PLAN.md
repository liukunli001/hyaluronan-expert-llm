# Hyaluronan Expert LLM — 具体执行计划（v2 · Hugging Face 主线）

日期：2026-10-21（v2 改版：主线由 nanochat 改为 HF 生态；nanochat 仅作从零训练的对照基线）
仓库：https://github.com/liukunli001/hyaluronan-expert-llm

## 0. 路线一句话

拿开源强底座 **Qwen3-8B-Base**（Apache-2.0），用 Hugging Face 全家桶（Transformers + TRL + PEFT + Accelerate）做：**继续预训练（DAPT）→ SFT →（可选 DPO）→ RAG 带引用问答**，用自建的专家验证评测集做四方对比。推理/评测用 vLLM 加速。

**关于"预训练"的口径（重要）**：本路线没有从零预训练（from-scratch）——万亿 token 级预训练是 Qwen 团队已经做完的，自己重做 8B 模型要六位数美元和数月。但管线里保留了预训练性质的阶段：**继续预训练（continued pretraining / domain-adaptive pretraining, DAPT）**——同样的 next-token 目标、同样的原始文本训练，只是起点是训好的权重、语料换成 HA 文献。对外表述只能写 "domain-adaptive (continued) pretraining"，不能写 "pretrained from scratch"；从零训练的说法由 nanochat 对照基线承担（可选，$100 跑一遍）。

## 1. 选型定版

| 项 | 定版 | 备注 |
|---|---|---|
| 底座 | Qwen3-8B-Base | 备选 Llama-3.1-8B（Meta 系，许可证有附加条款）；Qwen3-4B-Base 作家里显卡的开发版 |
| 训练框架 | HF Transformers + Trainer（DAPT）、TRL SFTTrainer / DPOTrainer（SFT/DPO）、PEFT（LoRA） | 版本锁定写进 requirements，chat template 用 Qwen 官方模板 |
| 硬件 | 租 1× H100 80GB（Lambda / RunPod，约 $2–3/h） | 家里若为 4090 级：只跑 4B 的 QLoRA 调试，不跑主线 |
| 推理/评测 | vLLM | 基线与各阶段评测都走它，快且与最终 demo 一致 |
| 检索 | SPECTER2（科学文献 embedding）或 bge-m3 + FAISS | 元数据（标题/年份/DOI）随块保存，回答给引用 |
| 教师/评委 | GPT-5 级 API | 只做三件事：生成 SFT 问答、评测 judge、造陷阱题；预算 $30–80 |

## 2. 数据（Phase 1，进行中）

- **抓取**：`data_pipeline/harvest_pmc.py` 已上线运行——PMC 精确集 16,642 条（标题/摘要命中 hyaluronan），样本产率 87%，预计全文 ~14,000 篇。
- **清洗**（`clean_corpus.py`，抓完即跑）：JATS XML → 纯文本；保留标题/摘要/正文/图注；删参考文献、致谢、版权页；按 DOI 去重 + 标题近重去重；输出 jsonl（字段：pmcid, pmid, doi, year, title, text）。
- **切分**：
  - DAPT 核心集：按子领域相关性（合成修饰 / CD44 / 纳米递送 / 分子量信号优先）+ 综述优先筛 3,000–5,000 篇，估算 40–70M token；
  - RAG 全量集：全部清洗后语料；
  - **hold-out**：用来出评测题的论文（约 30 篇）从所有训练集剔除，防污染。
- **SFT 数据**（`build_sft.py`）：教师模型从核心集段落生成问答（事实/机制/对比/方法/应用/计算六类）10,000–20,000 对，自动过滤（答案须命中原文依据）；混入通用指令数据（Tulu-3 SFT / SmolTalk 抽样约 10,000 条）防聊天能力退化。Kunli 抽查 100 对（约 1 h）。
- **评测集**：HA-Expert-Bench 200–300 题（定义/机制/方法/应用/定量 + 陷阱题），**答案键由 Kunli 本人核定**（2–3 h）；外加 MMLU 化学子集 + nanochat CORE 子集作通用能力对照。

## 3. 执行阶段

| 阶段 | 做什么 | 脚本 | GPU 时间 | 产出 |
|---|---|---|---|---|
| S0 清洗统计 | XML→文本、去重、切分、token 统计 | clean_corpus.py | — | 语料 v1 + 统计报告 |
| S1 基线评测 | 底座原版跑 HA-Bench + MMLU 化学（vLLM） | eval/run_eval.py | ~0.5 h | 基线分数（对比表第一行） |
| S2 DAPT 继续预训练 | HF Trainer 全参：核心集 + 20% FineWeb-Edu 回放；bf16、packing、lr 1e-5 cosine、1 epoch | training/dapt.py | ~3–4 h（H100） | DAPT 检查点 |
| S3 SFT | TRL SFTTrainer：HA 问答 + 通用混训；先 LoRA（r=64）快速版验证，再全参定版；2–3 epoch | training/sft.py | ~1 h | SFT 模型 |
| S4 DPO（可选） | 可验证题构造偏好对（对/错答），TRL DPOTrainer 小步数 | training/dpo.py | ~1 h | DPO 模型 |
| S5 RAG | 全量语料切块向量化建 FAISS；问答端检索注入 + 引用格式；vLLM 服务 | rag/build_index.py, rag/qa.py | ~0.5 h | 带引用问答 demo |
| S6 评测打包 | 四方对比（底座 / +DAPT+SFT / +RAG / +DPO）；judge 打分 + 选择题精确匹配；抽 50 条错误分析 | eval/run_eval.py | ~1 h | 结果表 + 报告卡 |

总 GPU 约 8–10 h（H100 租金约 $30–80），加教师 API，总成本 **< $250**。

## 4. 时间线（与申请季并行，硬止损在内）

- 10/22–10/30：S0 + 评测集骨架（Kunli 抽空核定答案）
- 11/1–11/9：S1–S2（基线 + DAPT）
- 11/10–11/23：S3 + S5（SFT + RAG）
- 11/24–12/5：S6 + 打包（README 结果表、model card、Gradio demo、简历句落数）
- **12/10 硬冻结**：没完成就停在当前状态，不占申请提交时间；1 月面试季前再收尾

Kunli 本人总投入仍约 4 小时：核定评测答案（2–3 h）+ 抽查 SFT 问答（1 h）+ 范围点头。其余脚本与运行由 Zuck 负责。

## 5. 风险与口径

- DAPT 语料只有几千万 token：知识主要靠 RAG 兜底，DAPT 解决领域语言与概念——对外不宣称"记住全部文献"。
- 教师生成数据有错：抽查闸门 + 答案须有原文依据的自动过滤；评测答案 100% 人工核定，与训练数据风险隔离。
- 对比表只和同底座比（底座原版是唯一公平对手），不和 GPT 级大模型比绝对分数。
- 许可证：Qwen3 为 Apache-2.0，产物可公开；语料只用 PMC OA + PubMed 摘要，不爬付费墙。

## 6. 简历句（数字待实测）

"Domain-adapted Qwen3-8B into a hyaluronan expert with Hugging Face TRL: continued pretraining on a [N]-paper corpus, SFT on [N] expert-checked QA pairs, and retrieval-grounded QA with citations; on a self-built expert-verified benchmark ([N] questions), accuracy improved from [A]% (base) to [B]% (+domain training) and [C]% (+retrieval)."
