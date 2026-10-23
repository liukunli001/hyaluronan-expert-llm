# Sample data

Readable samples from the released artifacts. Full files are in the [v0.1-data release](https://github.com/liukunli001/hyaluronan-expert-llm/releases/tag/v0.1-data): `corpus_v1.jsonl.gz` (all 12,306 papers) and `chunks.jsonl.gz` (all 636,959 chunks).

## Corpus sample

Three records from `corpus_v1.jsonl` (12,306 papers; fields: pmcid, pmid, doi, year, title, journal, text). Excerpts shown; full texts are in the release file.

### 1. Effect of Hyaluronic Acid and Kappa-Carrageenan on Milk Properties: Rheology, Protein Stability, Foaming, Water-Holding, and Emulsification Properties

- PMCID: PMC10000474 · Journal: Foods · Year: 2023

> Effect of Hyaluronic Acid and Kappa-Carrageenan on Milk Properties: Rheology, Protein Stability, Foaming, Water-Holding, and Emulsification Properties Hyaluronic acid (HA) is now widely known for its ability to bind water and impart texture. The combined effects of HA and kappa-carrageenan (KC) have not yet been investigated, though. In this study, we looked at the synergistic effects of HA and KC (concentrations of 0.1 and 0.25%, and ratios of 85:15, 70:30, and 50:50 for each concentration) on the rheological properties, heat stability, protein phase separation, water-holding capacity, emulsi…

### 2. A Novel Hyaluronic Acid Matrix Ingredient with Regenerative, Anti-Aging and Antioxidant Capacity

- PMCID: PMC10002543 · Journal: International Journal of Molecular Sciences · Year: 2023

> A Novel Hyaluronic Acid Matrix Ingredient with Regenerative, Anti-Aging and Antioxidant Capacity Hyaluronic acid (HA) and proteoglycans (such as dermatan sulphate (DS) and chondroitin sulphate (CS)) are the main components of the extracellular matrix of the skin, along with collagen and elastin. These components decrease with age, which implies a loss of skin moisture causing wrinkles, sagging and aging. Currently, the external and internal administration of effective ingredients that can reach the epidermis and dermis is the main alternative for combating skin aging. The objective of this wor…

### 3. Sustained ACE2 Expression by Probiotic Improves Integrity of Intestinal Lymphatics and Retinopathy in Type 1 Diabetic Model

- PMCID: PMC10003436 · Journal: Journal of Clinical Medicine · Year: 2023

> Sustained ACE2 Expression by Probiotic Improves Integrity of Intestinal Lymphatics and Retinopathy in Type 1 Diabetic Model Intestinal lymphatic, known as lacteal, plays a critical role in maintaining intestinal homeostasis by regulating several key functions, including the absorption of dietary lipids, immune cell trafficking, and interstitial fluid balance in the gut. The absorption of dietary lipids relies on lacteal integrity, mediated by button-like and zipper-like junctions. Although the intestinal lymphatic system is well studied in many diseases, including obesity, the contribution of …

## RAG chunks sample

Three records from `chunks.jsonl` (636,959 chunks; fields: pmcid, title, year, text). Each chunk is embedded with Qwen3-Embedding-0.6B into the FAISS index used for retrieval. Excerpts shown.

### 1. Effect of Hyaluronic Acid and Kappa-Carrageenan on Milk Properties: Rheology, Protein Stability, Foaming, Water-Holding, and Emulsification Properties

- PMCID: PMC10000474 · Year: 2023

> Effect of Hyaluronic Acid and Kappa-Carrageenan on Milk Properties: Rheology, Protein Stability, Foaming, Water-Holding, and Emulsification Properties Hyaluronic acid (HA) is now widely known for its ability to bind water and impart texture. The combined effects of HA and kappa-carrageenan (KC) have not yet been investigated, though. In this study, we looked at the synergistic effects of HA and KC (concentrations of 0.1 and 0.25%, and ratios of 85:15, 70:30, and 50:50 for each concentration) on the rheological properties, heat stability, protein phase separation, water-holding capacity, emulsi…

### 2. Effect of Hyaluronic Acid and Kappa-Carrageenan on Milk Properties: Rheology, Protein Stability, Foaming, Water-Holding, and Emulsification Properties

- PMCID: PMC10000474 · Year: 2023

> ser protein phase separation and a higher water-holding capacity than when HA and KC were utilized separately. Similarly, for the sample with a 0.1% concentration, the combination of HA + KC blends demonstrated a synergistic impact with greater emulsifying activity and stability. The samples with a concentration of 0.25% did not exhibit this synergistic effect, and the emulsifying activity and stability were mostly due to the HA’s higher emulsifying activity and stability at 0.25% concentration. Similarly, for rheological (apparent viscosity, consistency coefficient K, and flow behavior index …

### 3. Effect of Hyaluronic Acid and Kappa-Carrageenan on Milk Properties: Rheology, Protein Stability, Foaming, Water-Holding, and Emulsification Properties

- PMCID: PMC10000474 · Year: 2023

> n the amount of KC in the HA + KC blend ratios. When HC-control and KC-control samples were compared to various HA + KC mix ratios, there was no discernible difference in the heat stability. With the added benefits of protein stability (reduced phase separation), increased water-holding capacity, improved emulsification capabilities, and foaming abilities, the combination of HA + KC would be highly helpful in many texture-modifying applications.
