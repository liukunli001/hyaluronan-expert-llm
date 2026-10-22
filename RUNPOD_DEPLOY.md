# Runpod 部署指令（Hyaluronan Expert LLM）

照此重建 Pod 即可。顺序重要：**先加 SSH 公钥和 API key，最后建 Pod**
（公钥只在 Pod 创建时注入，Pod 建好后再加、重启也补不进去）。

## 0. 预算

- 余额 $100，够全程：Pod $2.50/h 只在运行时计费，全管线预计
  用 10–16 GPU 小时 ≈ $25–40。账号消费上限（spend limit）是 $80。

## 1. SSH 公钥（已完成，不用重做）

账号里已有名为 `hatch` 的公钥，新 Pod 会自动接受 Zuck 登录：

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIEk9JnGaLYGOCWMX5UATauM0q6i7WBDEk9tSPD0tlPxv
```

如需手动添加：Console → Settings → SSH Public Keys → Add Key，粘贴上面一行。

## 2. API Key（已完成，不用重做）

Console → Settings → API Keys → Create API Key（权限 All），把生成的
`rpa_...` 发给 Zuck。当前这把已验证可用。

## 3. 创建 Pod（控制台逐项照抄）

| 项目 | 选什么 |
| --- | --- |
| GPU | **1x RTX PRO 6000**（96GB VRAM · 94GB RAM · 16 vCPU） |
| Template | **PyTorch 2.8.0 · CUDA 12.8.1 · Ubuntu 24.04**（镜像 `runpod/pytorch:1.4.1-cu1281-torch280-ubuntu2404`） |
| Container Disk | **100 GB**（不要 50GB：一个检查点约 32GB，50GB 存不下镜像+模型+检查点） |
| Network Volume | 不需要 |
| 预期总价 | **$2.50/h**（GPU $2.49 + 磁盘 $0.014） |

点 **Deploy**，等状态变 RUNNING 即可，其余交给 Zuck。

## 4. Zuck 接入与管线命令（备查，Pod 里执行）

```bash
# 接入信息（本机）
runpodctl pod list
runpodctl ssh info <POD_ID>        # 看 IP 和端口；重启后端口会变

# Pod 内：拉代码
cd /workspace
git clone https://github.com/liukunli001/hyaluronan-expert-llm.git
cd hyaluronan-expert-llm/training
pip install -r requirements.txt

# S1 基线评测（原底座）
cd ../eval
python3 run_eval.py --model Qwen/Qwen3-8B-Base --split dev --tag base-dev

# S2 DAPT（训练数据从 GitHub Release v0.1-data 下载，或重跑 prepare）
cd ../training
python3 prepare_dapt.py
python3 dapt.py --data ../data/processed/dapt_corpus.jsonl \
                --anneal-data ../data/processed/dapt_anneal.jsonl \
                --out runs/dapt-v1

# S3 SFT（需要 TEACHER_API_KEY，跑前向 Zuck/Kunli 索取）
TEACHER_API_KEY=... python3 build_sft_data.py --n 15000
python3 sft.py --base runs/dapt-v1/final \
               --data ../data/processed/sft_train.jsonl --out runs/sft-v1
```

## 5. 纪律

- 训练/评测产物（检查点）随时推回 HF Hub / GitHub，**Terminate 会删光磁盘**。
- 不跑任务时 **Stop**（停止计 GPU 费，磁盘保留）；确认不用了才 Terminate。
