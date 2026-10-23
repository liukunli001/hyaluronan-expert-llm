#!/bin/bash
# S6 full-bench chain (240 q, bench_v2_verified key), run on the Pod.
# Order: wait for RAG index -> retrieval smoke -> 4 generation cells
# (no judge reachable during generation; open/trap stay 'ungraded')
# -> local judge server (the SFT model itself) -> grade all 4 files.
cd /workspace/hyaluronan-expert-llm || exit 1
LOG=/workspace/s6-chain.log
echo "chain start $(date)" >> $LOG

for i in $(seq 1 120); do grep -q "index built" /workspace/rag-index.log && break; sleep 30; done
grep "index built" /workspace/rag-index.log >> $LOG || { echo "INDEX FAILED" >> $LOG; exit 1; }

python3 rag/qa.py "How does hyaluronan bind CD44?" > /workspace/qa-smoke.log 2>&1
echo "qa smoke done" >> $LOG

BENCH="--bench eval/bench_v2_verified.jsonl --split all"
python3 -u eval/run_eval.py $BENCH --model Qwen/Qwen3-8B-Base --tag full-base >> $LOG 2>&1
python3 -u eval/run_eval.py $BENCH --model training/runs/sft-v1/final --tag full-sft --chat >> $LOG 2>&1
python3 -u eval/run_eval.py $BENCH --model Qwen/Qwen3-8B-Base --tag full-base-rag --rag >> $LOG 2>&1
python3 -u eval/run_eval.py $BENCH --model training/runs/sft-v1/final --tag full-sft-rag --chat --rag >> $LOG 2>&1
echo "generation cells done $(date)" >> $LOG

setsid nohup vllm serve training/runs/sft-v1/final --port 8000 --served-model-name ha-judge >> /workspace/judge-server.log 2>&1 < /dev/null &
for i in $(seq 1 90); do curl -s localhost:8000/v1/models > /dev/null && break; sleep 10; done
export TEACHER_API_BASE=http://localhost:8000/v1 TEACHER_API_KEY=local JUDGE_MODEL=ha-judge
for t in full-base full-sft full-base-rag full-sft-rag; do
  python3 -u eval/grade_results.py --results eval/results/$t.jsonl --bench eval/bench_v2_verified.jsonl >> $LOG 2>&1
done
echo "CHAIN-DONE $(date)" >> $LOG
