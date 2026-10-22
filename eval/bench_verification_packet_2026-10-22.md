# HA-Expert-Bench 核定包（240 道草稿题 → 你一次性裁定）

来源文件：`eval/bench_v1_draft.jsonl`（仓库 liukunli001/hyaluronan-expert-llm）。本包只重排顺序、加裁定行和溯源链接，题目与草稿答案逐字未改。

## 怎么核（目标：把 2–3 小时压到最短）
- 每题只需三选一：**过**（答案对，不用标）/ **改**（在裁定行写正确口径）/ **删**（写「删」）。没标记的我按「过」处理，最后统一把 status 改成 verified 并回读计数给你。
- 顺序按核定速度排：先自动判分题（答案是死数字/选项，扫一眼即可），再论文溯源题（附 PMC 链接可点开对原文），再陷阱题（只需确认「假前提确实是假的」），最后其余开放题按类分组。
- 你可以直接在这个文件里标，也可以回聊天里报 ID 清单（如「P05 改成…、G03 删」）。

## 一、自动判分题（MCQ + 定量）（30 道）
这类题最终分数靠精确匹配，答案键错一道就错一道，但核定最快——只看数字/选项对不对。

### A09 · basics · quantitative
**题**：Roughly how much water can HA bind relative to its own weight?
**草稿答案**：Up to about 1,000 times its weight in water (commonly cited figure).
裁定：☐ 过　☐ 改：________　☐ 删

### A11 · basics · mcq
**题**：Where is hyaluronan synthesized?
**草稿答案**：C - plasma membrane, by HAS enzymes that extrude the chain directly outside the cell.
裁定：☐ 过　☐ 改：________　☐ 删

### A14 · basics · quantitative
**题**：Roughly what fraction of the body's total HA resides in the skin?
**草稿答案**：About half (~7-8 g of the ~15 g total in a 70 kg adult).
裁定：☐ 过　☐ 改：________　☐ 删

### A21 · basics · quantitative
**题**：Convert: a filler HA is listed as 2,500 kDa. In MDa and in Da?
**草稿答案**：2.5 MDa = 2,500,000 Da (2.5 x 10^6 Da).
裁定：☐ 过　☐ 改：________　☐ 删

### B11 · receptors_signaling · mcq
**题**：Which organ clears most hyaluronan from the blood?
**草稿答案**：B - liver sinusoidal endothelial cells via HARE/Stabilin-2.
裁定：☐ 过　☐ 改：________　☐ 删

### B12 · receptors_signaling · quantitative
**题**：Approximately how large is the standard CD44 glycoprotein?
**草稿答案**：About 80-95 kDa as a mature glycoprotein (core protein ~37 kDa, heavily glycosylated).
裁定：☐ 过　☐ 改：________　☐ 删

### B19 · receptors_signaling · mcq
**题**：LYVE-1 is most homologous to which receptor?
**草稿答案**：B - LYVE-1 is a CD44 homolog with a Link module, expressed on lymphatic endothelium.
裁定：☐ 过　☐ 改：________　☐ 删

### B22 · receptors_signaling · quantitative
**题**：What is the approximate serum half-life of HA in humans?
**草稿答案**：Only a few minutes (about 2-5 minutes) due to rapid hepatic sinusoidal clearance.
裁定：☐ 过　☐ 改：________　☐ 删

### C19 · mw_biology · mcq
**题**：Which change would INCREASE HA accumulation in a tissue?
**草稿答案**：B - HAS2 overexpression raises synthesis; the others increase degradation or clearance.
裁定：☐ 过　☐ 改：________　☐ 删

### D12 · chemistry_modification · mcq
**题**：Methacrylic anhydride modifies HA mainly at which group?
**草稿答案**：B - hydroxyl groups, chiefly the primary hydroxyl.
裁定：☐ 过　☐ 改：________　☐ 删

### D18 · chemistry_modification · mcq
**题**：EDC/NHS coupling on HA targets which group to form amide bonds?
**草稿答案**：B - the glucuronic-acid carboxyl is activated by EDC/NHS and attacked by an amine to form an amide.
裁定：☐ 过　☐ 改：________　☐ 删

### D30 · chemistry_modification · mcq
**题**：Periodate oxidation of HA generates which reactive group for crosslinking?
**草稿答案**：B - aldehydes, from cleavage of vicinal diols, enabling Schiff-base/hydrazone crosslinking.
裁定：☐ 过　☐ 改：________　☐ 删

### E11 · nano_delivery · mcq
**题**：Which of the following is NOT used as the hydrophobic moiety that makes HA self-assemble?
**草稿答案**：D - PEG is hydrophilic; it cannot form the hydrophobic core (it is sometimes grafted separately for stealth).
裁定：☐ 过　☐ 改：________　☐ 删

### E17 · nano_delivery · mcq
**题**：HA-based nanoparticle uptake by CD44-high tumor cells is mainly via:
**草稿答案**：B - CD44-mediated (receptor-mediated) endocytosis.
裁定：☐ 过　☐ 改：________　☐ 删

### E21 · nano_delivery · quantitative
**题**：A self-assembled HA nanoparticle formulation reports 180 nm diameter and zeta potential -25 mV. Are these values typical?
**草稿答案**：Yes - 100-300 nm with a distinctly negative zeta potential (from ionized carboxyls) is the typical reported range.
裁定：☐ 过　☐ 改：________　☐ 删

### F06 · clinical_quant · quantitative
**题**：What MW range do commercial viscosupplements span?
**草稿答案**：Roughly 0.5 to 6 MDa across products (standard preparations ~0.5-3 MDa; crosslinked hylan G-F 20 averages ~6 MDa).
裁定：☐ 过　☐ 改：________　☐ 删

### F07 · clinical_quant · quantitative
**题**：What HA concentration do most crosslinked dermal fillers contain?
**草稿答案**：About 20 mg/mL (most brands fall in the 17.5-24 mg/mL range).
裁定：☐ 过　☐ 改：________　☐ 删

### F10 · clinical_quant · quantitative
**题**：What is the approximate MW of HA in healthy human synovial fluid?
**草稿答案**：About 6-7 MDa (several million Da), falling in osteoarthritis.
裁定：☐ 过　☐ 改：________　☐ 删

### F11 · clinical_quant · quantitative
**题**：At what concentration is classic ophthalmic viscoelastic HA (Healon-type) supplied?
**草稿答案**：About 10 mg/mL (1%) sodium hyaluronate of high MW (~4-5 MDa).
裁定：☐ 过　☐ 改：________　☐ 删

### F17 · clinical_quant · mcq
**题**：The first HA-based biomedical product (Healon) was used in which surgery?
**草稿答案**：B - ophthalmic (cataract) surgery, as a viscoelastic protecting the corneal endothelium.
裁定：☐ 过　☐ 改：________　☐ 删

### F20 · clinical_quant · quantitative
**题**：What HA concentration is typical in artificial-tear eye drops?
**草稿答案**：About 0.1-0.3% (1-3 mg/mL) sodium hyaluronate, MW-dependent.
裁定：☐ 过　☐ 改：________　☐ 删

### F26 · clinical_quant · quantitative
**题**：Roughly how long do BDDE-crosslinked HA fillers persist by anatomical area?
**草稿答案**：About 6-12 months in mobile areas (lips) and 12-24 months in static areas (cheeks/deep planes), varying with crosslink density, volume, and site metabolism.
裁定：☐ 过　☐ 改：________　☐ 删

### P01 · basics · quantitative
**题**：One HA disaccharide is about 400 Da and a chain can contain up to ~10,000 disaccharides. What maximum molecular weight does that imply?
**草稿答案**：About 4.0 x 10^3 kDa, i.e. roughly 4 MDa.
**溯源**：[PMC10004376](https://pmc.ncbi.nlm.nih.gov/articles/PMC10004376/)
裁定：☐ 过　☐ 改：________　☐ 删

### P05 · clinical_quant · quantitative
**题**：In knee-pain trials of oral HA, what daily dose range was typically used, and how does it compare with glucosamine?
**草稿答案**：Low doses, at most about 240 mg/day of HA, versus roughly 1,500 mg/day for glucosamine (and ~675 mg/day chondroitin).
**溯源**：[PMC4729158](https://pmc.ncbi.nlm.nih.gov/articles/PMC4729158/)
裁定：☐ 过　☐ 改：________　☐ 删

### P07 · hydrogel_scaffold · quantitative
**题**：In a patent overview of HA-hydrogel biosensors (2003-2023), how many patent documents were found, and what share were US filings?
**草稿答案**：50 patent documents (41 applications and 9 granted patents); US-based institutions accounted for about 54% of filings.
**溯源**：[PMC11674427](https://pmc.ncbi.nlm.nih.gov/articles/PMC11674427/)
裁定：☐ 过　☐ 改：________　☐ 删

### P12 · clinical_quant · quantitative
**题**：In the level-I systematic review of IA-HA for hip OA, how many patients were analyzed, and when did HMW-HA separate from placebo on pain (VAS)?
**草稿答案**：982 patients; at 4-6 months the HMW group had significantly lower VAS than placebo (mean difference about -1.6), with no significant between-group differences at 3-4 months.
**溯源**：[PMC12064613](https://pmc.ncbi.nlm.nih.gov/articles/PMC12064613/)
裁定：☐ 过　☐ 改：________　☐ 删

### P13 · clinical_quant · quantitative
**题**：How large was the saline-controlled meta-analysis of US-approved IA-HA for knee OA, and what effect size did it find versus saline?
**草稿答案**：29 randomized trials, 4,866 subjects; versus saline, standardized mean differences were modest, about 0.38-0.43 for pain and 0.32-0.34 for function, with no significant safety differences.
**溯源**：[PMC3767581](https://pmc.ncbi.nlm.nih.gov/articles/PMC3767581/)
裁定：☐ 过　☐ 改：________　☐ 删

### P21 · clinical_quant · quantitative
**题**：In the root-coverage meta-analysis, did adding HA to coronally advanced flap significantly improve mean root coverage?
**草稿答案**：No - the mean difference was about 8.2 percentage points favoring HA but not significant (95% CI roughly -3.1 to 19.5, p = 0.12).
**溯源**：[PMC11755931](https://pmc.ncbi.nlm.nih.gov/articles/PMC11755931/)
裁定：☐ 过　☐ 改：________　☐ 删

### P35 · clinical_quant · quantitative
**题**：In the IA-HA product-properties review, how many investigations addressed basic-science versus clinical differences between products?
**草稿答案**：20 investigations on basic-science differences and 20 on clinical-outcome differences.
**溯源**：[PMC10807741](https://pmc.ncbi.nlm.nih.gov/articles/PMC10807741/)
裁定：☐ 过　☐ 改：________　☐ 删

### P37 · clinical_quant · quantitative
**题**：Describe the hip-OA review cohort: sex split, mean age, mean follow-up.
**草稿答案**：56% women, mean age about 62 years, mean follow-up about 6.4 months (982 patients).
**溯源**：[PMC12064613](https://pmc.ncbi.nlm.nih.gov/articles/PMC12064613/)
裁定：☐ 过　☐ 改：________　☐ 删

## 二、论文溯源开放题（带 PMCID）（30 道）
答案出自 30 篇 holdout 综述（已排除出训练数据）。点开链接对原文即可，不用凭记忆。

### P02 · basics · open
**题**：Why has production shifted from animal-tissue extraction toward microbial fermentation?
**草稿答案**：Fermentation avoids animal-source risks (viral/prion contamination, batch variability, ethical and supply limits) and gives controllable, scalable production of defined HA.
**溯源**：[PMC10004376](https://pmc.ncbi.nlm.nih.gov/articles/PMC10004376/)
裁定：☐ 过　☐ 改：________　☐ 删

### P03 · basics · open
**题**：Beyond vertebrate tissues, where else does HA occur in nature?
**草稿答案**：In the capsules of some bacteria (e.g., group A and C streptococci and Pasteurella multocida), where it aids adherence, protection, and molecular mimicry of the host.
**溯源**：[PMC10299688](https://pmc.ncbi.nlm.nih.gov/articles/PMC10299688/)
裁定：☐ 过　☐ 改：________　☐ 删

### P04 · basics · open
**题**：Microbial hyaluronan-degrading enzymes act as 'molecular scissors' - what bond do they cleave, and why are these enzymes virulence factors?
**草稿答案**：They cleave the glycosidic linkages of HA; by digesting host HA-rich matrices they help pathogens spread through tissue (classic 'spreading factor') and invade the host.
**溯源**：[PMC11669647](https://pmc.ncbi.nlm.nih.gov/articles/PMC11669647/)
裁定：☐ 过　☐ 改：________　☐ 删

### P06 · clinical_quant · open
**题**：By what route is orally administered HA proposed to relieve knee pain?
**草稿答案**：Absorbed HA fragments are proposed to act via receptor binding in the intestinal epithelia (e.g., TLR4-related signaling) and distribution to joints, modulating synovial inflammation - supported by RCT evidence for pain and effusion relief.
**溯源**：[PMC4729158](https://pmc.ncbi.nlm.nih.gov/articles/PMC4729158/)
裁定：☐ 过　☐ 改：________　☐ 删

### P08 · hydrogel_scaffold · open
**题**：Which sensing application dominates patented HA-hydrogel biosensors?
**草稿答案**：In-vivo blood analysis, especially glucose monitoring using enzyme-immobilized (glucose oxidase) electrodes and tissue-impedance measurements.
**溯源**：[PMC11674427](https://pmc.ncbi.nlm.nih.gov/articles/PMC11674427/)
裁定：☐ 过　☐ 改：________　☐ 删

### P09 · cancer · open
**题**：What is the collective name for HA-binding proteins such as CD44 and RHAMM?
**草稿答案**：Hyaladherins.
**溯源**：[PMC9820514](https://pmc.ncbi.nlm.nih.gov/articles/PMC9820514/)
裁定：☐ 过　☐ 改：________　☐ 删

### P10 · cancer · open
**题**：What does abundant HA on a tumor cell surface usually indicate prognostically?
**草稿答案**：An adverse prognosis - HA-rich tumor surfaces/stroma are associated with progression, invasion, and metastasis.
**溯源**：[PMC9820514](https://pmc.ncbi.nlm.nih.gov/articles/PMC9820514/)
裁定：☐ 过　☐ 改：________　☐ 删

### P11 · clinical_quant · open
**题**：What do meta-analyses of intra-articular HA products suggest about HMW versus LMW preparations for knee pain?
**草稿答案**：Pain reduction is superior with high-molecular-weight HA compared with low-molecular-weight HA, consistent with their different receptor interactions in synovial fluid.
**溯源**：[PMC10807741](https://pmc.ncbi.nlm.nih.gov/articles/PMC10807741/)
裁定：☐ 过　☐ 改：________　☐ 删

### P14 · clinical_quant · open
**题**：Which knee-OA patients appear to benefit most from IA-HA injections?
**草稿答案**：Patients with less advanced radiographic OA (lower Kellgren-Lawrence grade) tend to benefit more; advanced disease responds less.
**溯源**：[PMC12460378](https://pmc.ncbi.nlm.nih.gov/articles/PMC12460378/)
裁定：☐ 过　☐ 改：________　☐ 删

### P15 · basics · open
**题**：Did adding topical HA to mechanical periodontal therapy reduce subgingival P. gingivalis prevalence?
**草稿答案**：No - the systematic review/meta-analysis found odds ratios near 1 (0.95 at 3 months, 1.11 at 6 months), i.e., no advantage despite HA's in-vitro antibacterial activity.
**溯源**：[PMC10385933](https://pmc.ncbi.nlm.nih.gov/articles/PMC10385933/)
裁定：☐ 过　☐ 改：________　☐ 删

### P16 · mw_biology · open
**题**：How does hyperglycemia damage the HA of the endothelial glycocalyx in diabetic skin?
**草稿答案**：High glucose drives loss of the HA-rich pericellular glycocalyx on small-vessel endothelium, exposing adhesion molecules and accelerating leukocyte recruitment - a pro-inflammatory state linked to impaired diabetic wound healing.
**溯源**：[PMC4581551](https://pmc.ncbi.nlm.nih.gov/articles/PMC4581551/)
裁定：☐ 过　☐ 改：________　☐ 删

### P17 · chemistry_modification · open
**题**：In thiomer chemistry, chitosan and HA play opposite charge roles - which is which, and what payloads are thiolated-HA nanoparticles used for?
**草稿答案**：Chitosan is the cationic thiomer, HA the anionic one; thiolated-HA nanoparticles are used notably for taxanes and siRNA delivery.
**溯源**：[PMC8227107](https://pmc.ncbi.nlm.nih.gov/articles/PMC8227107/)
裁定：☐ 过　☐ 改：________　☐ 删

### P18 · nano_delivery · open
**题**：Why modify metal nanoparticles with HA for cancer therapy?
**草稿答案**：Bare metal nanoparticles lack specificity and can be toxic to healthy cells; an HA coating adds CD44 targeting to cancer cells, improving specificity and efficacy while improving biocompatibility.
**溯源**：[PMC10302411](https://pmc.ncbi.nlm.nih.gov/articles/PMC10302411/)
裁定：☐ 过　☐ 改：________　☐ 删

### P19 · hydrogel_scaffold · open
**题**：Why is HA considered an ideal base material for 3D-bioprinting bioinks?
**草稿答案**：Histocompatibility, non-immunogenicity, biodegradability, anti-inflammatory/anti-angiogenic character, and easy chemical modifiability for crosslinking and printability.
**溯源**：[PMC10748859](https://pmc.ncbi.nlm.nih.gov/articles/PMC10748859/)
裁定：☐ 过　☐ 改：________　☐ 删

### P20 · clinical_quant · open
**题**：What did the tooth-extraction meta-analysis find about HA and new bone formation?
**草稿答案**：Individual preclinical studies all suggested a positive effect on socket bone formation, but the pooled meta-analysis did not confirm it; clinical studies focused on pain, swelling, and trismus outcomes.
**溯源**：[PMC10713798](https://pmc.ncbi.nlm.nih.gov/articles/PMC10713798/)
裁定：☐ 过　☐ 改：________　☐ 删

### P22 · clinical_quant · open
**题**：Why is vaginal HA used for postmenopausal vaginal atrophy?
**草稿答案**：As a non-hormonal moisturizing alternative to topical estrogen, avoiding estrogen-related adverse effects; comparative studies suggest meaningful symptom relief.
**溯源**：[PMC10520994](https://pmc.ncbi.nlm.nih.gov/articles/PMC10520994/)
裁定：☐ 过　☐ 改：________　☐ 删

### P23 · clinical_quant · open
**题**：What postoperative outcomes is HA used to improve after third-molar surgery?
**草稿答案**：Pain, swelling, and trismus, with faster soft-tissue healing, when HA is applied to the extraction socket area.
**溯源**：[PMC6405346](https://pmc.ncbi.nlm.nih.gov/articles/PMC6405346/)
裁定：☐ 过　☐ 改：________　☐ 删

### P24 · hydrogel_scaffold · open
**题**：What did studies of HA combined with xenografts for alveolar ridge preservation show?
**草稿答案**：HA-enhanced grafts significantly reduced post-extraction bone resorption versus controls, with better radiographic bone density and less graft shrinkage (4 human studies in the review).
**溯源**：[PMC11853319](https://pmc.ncbi.nlm.nih.gov/articles/PMC11853319/)
裁定：☐ 过　☐ 改：________　☐ 删

### P25 · clinical_quant · open
**题**：How many studies supported HA instillation for refractory BCG-induced cystitis in the narrative review, and what improved?
**草稿答案**：Seven studies; bladder pain, urgency, and frequency decreased and bladder capacity increased, with HA often combined with chondroitin sulfate.
**溯源**：[PMC12308125](https://pmc.ncbi.nlm.nih.gov/articles/PMC12308125/)
裁定：☐ 过　☐ 改：________　☐ 删

### P26 · basics · open
**题**：By what mechanism does intravesical HA relieve BCG-induced cystitis?
**草稿答案**：It restores the bladder's glycosaminoglycan barrier layer, reducing urothelial permeability, inflammation, and irritant exposure while tissue repairs.
**溯源**：[PMC12308125](https://pmc.ncbi.nlm.nih.gov/articles/PMC12308125/)
裁定：☐ 过　☐ 改：________　☐ 删

### P27 · clinical_quant · open
**题**：What combination therapy did the early-OA meta-analysis of arthroscopic-guided intra-articular treatment evaluate?
**草稿答案**：Mesenchymal stem cells combined with platelet-rich plasma and varying doses of HA (9 studies met inclusion), assessed on scores including Lysholm, VAS, KSS, and WOMAC.
**溯源**：[PMC10923406](https://pmc.ncbi.nlm.nih.gov/articles/PMC10923406/)
裁定：☐ 过　☐ 改：________　☐ 删

### P28 · chemistry_modification · open
**题**：Which two natural polymers are HA most commonly blended with, per the blends review?
**草稿答案**：Collagen and chitosan - blends aim to combine HA's biology with collagen's cell-adhesive structure or chitosan's cationic, antimicrobial character.
**溯源**：[PMC7570474](https://pmc.ncbi.nlm.nih.gov/articles/PMC7570474/)
裁定：☐ 过　☐ 改：________　☐ 删

### P29 · mw_biology · open
**题**：What role does HA play in atherosclerotic plaques?
**草稿答案**：HA accumulates in plaques and HA-rich matrices influence smooth-muscle-cell phenotype and lesion progression; the comprehensive review lists atherosclerosis among HA's pathological arenas alongside cancer.
**溯源**：[PMC10299688](https://pmc.ncbi.nlm.nih.gov/articles/PMC10299688/)
裁定：☐ 过　☐ 改：________　☐ 删

### P30 · hydrogel_scaffold · open
**题**：Why are HA hydrogels for bone tissue engineering almost always composites?
**草稿答案**：Pure HA gels are mechanically weak and not intrinsically osteoinductive; they are combined with other biomaterials and bioactive agents to gain strength and osteogenic activity while keeping HA's ECM-like environment.
**溯源**：[PMC10379028](https://pmc.ncbi.nlm.nih.gov/articles/PMC10379028/)
裁定：☐ 过　☐ 改：________　☐ 删

### P31 · hydrogel_scaffold · open
**题**：In wound healing, which three processes do HA-based hydrogels regulate, per the biomaterials review?
**草稿答案**：Inflammatory responses, angiogenesis, and extracellular-matrix remodeling.
**溯源**：[PMC12534349](https://pmc.ncbi.nlm.nih.gov/articles/PMC12534349/)
裁定：☐ 过　☐ 改：________　☐ 删

### P32 · basics · open
**题**：Name two biotechnological uses of microbial hyaluronan-degrading enzymes.
**草稿答案**：Controlled production/processing of HA oligosaccharides of defined size, and as molecular-biology tools (e.g., removing HA capsules/coats or digesting HA in samples) - besides their biomedical research uses.
**溯源**：[PMC11669647](https://pmc.ncbi.nlm.nih.gov/articles/PMC11669647/)
裁定：☐ 过　☐ 改：________　☐ 删

### P33 · basics · open
**题**：Why does industry ferment group C streptococci (S. zooepidemicus) rather than group A for HA?
**草稿答案**：Group A streptococci are human pathogens; group C S. zooepidemicus produces comparable capsular HA with a safer production profile.
**溯源**：[PMC10004376](https://pmc.ncbi.nlm.nih.gov/articles/PMC10004376/)
裁定：☐ 过　☐ 改：________　☐ 删

### P34 · clinical_quant · open
**题**：What evidence window supports oral HA for knee pain, per the review?
**草稿答案**：Randomized, double-blind, placebo-controlled trials published between 2008 and 2015 showing relief of synovitis-related symptoms, effusion/inflammation, and improved knee muscle strength.
**溯源**：[PMC4729158](https://pmc.ncbi.nlm.nih.gov/articles/PMC4729158/)
裁定：☐ 过　☐ 改：________　☐ 删

### P36 · clinical_quant · open
**题**：Why is the IA-HA literature a textbook case of large contextual effects?
**草稿答案**：Versus pre-injection baselines, effects look very large (SMD ~1.07-1.37), but versus saline controls they shrink to ~0.4 - most of the apparent benefit is contextual/placebo and natural fluctuation, which is exactly what saline controls exist to reveal.
**溯源**：[PMC3767581](https://pmc.ncbi.nlm.nih.gov/articles/PMC3767581/)
裁定：☐ 过　☐ 改：________　☐ 删

### P38 · clinical_quant · open
**题**：In dental extraction studies, in what forms was HA applied clinically?
**草稿答案**：Directly into the extraction socket, or as a spray or mouthwash, with pain, swelling, and trismus as the main clinical outcomes.
**溯源**：[PMC10713798](https://pmc.ncbi.nlm.nih.gov/articles/PMC10713798/)
裁定：☐ 过　☐ 改：________　☐ 删

## 三、陷阱题（15 道）
只需确认每道题的假前提确实是假的、草稿答案的纠正方向对。

### G01 · traps · trap
**题**：Since hyaluronan is a protein polymer, which amino acids dominate its composition?
**草稿答案**：Premise is false: HA is a polysaccharide (a glycosaminoglycan), not a protein; it contains no amino acids.
裁定：☐ 过　☐ 改：________　☐ 删

### G02 · traps · trap
**题**：Like other GAGs, HA is sulfated in the Golgi before secretion - which sulfotransferases act on it?
**草稿答案**：Premise is false: HA is non-sulfated and is synthesized at the plasma membrane by HAS enzymes, not in the Golgi.
裁定：☐ 过　☐ 改：________　☐ 删

### G03 · traps · trap
**题**：Low-molecular-weight HA is widely used as an anti-inflammatory because it mimics native HMW-HA signaling, correct?
**草稿答案**：No - it is generally the opposite: LMW-HA fragments are pro-inflammatory (TLR2/4, CD44), while native HMW-HA is anti-inflammatory.
裁定：☐ 过　☐ 改：________　☐ 删

### G04 · traps · trap
**题**：CD44 is the only known receptor for hyaluronan, true or false?
**草稿答案**：False: RHAMM, LYVE-1, HARE/Stabilin-2 and TLR2/4 (for fragments) also bind/signal HA.
裁定：☐ 过　☐ 改：________　☐ 删

### G05 · traps · trap
**题**：Crosslinked HA dermal fillers are permanent implants that the body cannot break down, right?
**草稿答案**：False: crosslinked HA is still biodegradable by hyaluronidases and ROS, typically lasting months to ~2 years depending on crosslinking.
裁定：☐ 过　☐ 改：________　☐ 删

### G06 · traps · trap
**题**：HA and heparin are interchangeable anticoagulants because both are sulfated GAGs, correct?
**草稿答案**：False on both counts: HA is non-sulfated and has no anticoagulant activity; heparin is a distinct, highly sulfated GAG.
裁定：☐ 过　☐ 改：________　☐ 删

### G07 · traps · trap
**题**：HA fillers restore youthful skin by permanently replacing the collagen you lost, correct?
**草稿答案**：No: fillers are temporary space-occupying gels that bind water; they are enzymatically degraded over months and do not permanently replace collagen (any collagen stimulation is secondary and modest).
裁定：☐ 过　☐ 改：________　☐ 删

### G08 · traps · trap
**题**：Bacterial-fermentation HA must be more immunogenic than animal HA because it is foreign, right?
**草稿答案**：Wrong: the HA molecule is chemically identical in all species (no species-specific structure), so HA itself is non-immunogenic regardless of source; reactions come from protein/endotoxin contaminants, which fermentation controls better.
裁定：☐ 过　☐ 改：________　☐ 删

### G09 · traps · trap
**题**：For joint injections, the highest-MW HA is always the best choice, correct?
**草稿答案**：Not established: trials do not show a consistent MW-efficacy ordering; higher MW raises viscosity/injectability and local-reaction tradeoffs, so 'highest is best' is an overclaim.
裁定：☐ 过　☐ 改：________　☐ 删

### G10 · traps · trap
**题**：HA is classified as an antioxidant drug because it scavenges free radicals, true?
**草稿答案**：Misleading: HA can scavenge reactive oxygen species and is degraded by them, but it is not classified or approved as an antioxidant drug; the claim overstates a secondary physicochemical property.
裁定：☐ 过　☐ 改：________　☐ 删

### G11 · traps · trap
**题**：Oral HA supplements work because the ingested HA travels intact and is deposited directly into your joints, right?
**草稿答案**：Oversimplified/false as stated: ingested HA is largely degraded; absorbed fragments and gut-receptor signaling are the proposed mechanisms, not intact deposition into cartilage.
裁定：☐ 过　☐ 改：________　☐ 删

### G12 · traps · trap
**题**：Since CD44 drives cancer, blocking CD44 with an approved drug is standard oncology practice, correct?
**草稿答案**：False: no CD44-targeted drug is an approved standard cancer therapy; CD44 remains an experimental target with trial-stage agents.
裁定：☐ 过　☐ 改：________　☐ 删

### G13 · traps · trap
**题**：HA solutions are simple Newtonian fluids, so their viscosity is a single constant, correct?
**草稿答案**：False: HA solutions are non-Newtonian and strongly shear-thinning; viscosity depends on shear rate, concentration, and MW.
裁定：☐ 过　☐ 改：________　☐ 删

### G14 · traps · trap
**题**：All commercial HA today is extracted from rooster combs, true?
**草稿答案**：False: most modern HA is made by microbial fermentation; rooster-comb extraction is the historical source and survives only in niches.
裁定：☐ 过　☐ 改：________　☐ 删

### G15 · traps · trap
**题**：Because HA is natural and non-immunogenic, HA injections carry no risk of inflammatory reactions, correct?
**草稿答案**：False: the HA molecule is non-immunogenic, but products can cause inflammatory/pseudoseptic reactions from contaminants, crosslinker residues, or the delivery procedure - 'natural' does not mean risk-free.
裁定：☐ 过　☐ 改：________　☐ 删

## 四、开放题 · basics（30 道）
### A01 · basics · open
**题**：What is the repeating disaccharide unit of hyaluronan, and how are the sugars linked?
**草稿答案**：D-glucuronic acid and N-acetyl-D-glucosamine, joined by alternating beta(1->4) and beta(1->3) glycosidic bonds.
裁定：☐ 过　☐ 改：________　☐ 删

### A02 · basics · open
**题**：Where in the cell is hyaluronan synthesized, and how does this differ from other glycosaminoglycans?
**草稿答案**：At the plasma membrane by hyaluronan synthases (HAS1/2/3), which extrude the growing chain directly into the extracellular space. Other GAGs are built in the Golgi on a core protein; HA has no core protein.
裁定：☐ 过　☐ 改：________　☐ 删

### A03 · basics · open
**题**：Name two features that make hyaluronan chemically unusual among glycosaminoglycans.
**草稿答案**：It is non-sulfated, and it is not covalently attached to a core protein.
裁定：☐ 过　☐ 改：________　☐ 删

### A04 · basics · open
**题**：Which enzyme families degrade hyaluronan in humans?
**草稿答案**：Hyaluronidases (HYAL1, HYAL2, and PH-20/SPAM1), with additional catabolic routes via CEMIP (KIAA1199) and TMEM2; reactive oxygen species also fragment HA non-enzymatically.
裁定：☐ 过　☐ 改：________　☐ 删

### A05 · basics · open
**题**：What does the Has2 knockout mouse show about hyaluronan's developmental role?
**草稿答案**：It is embryonic lethal, with severe cardiac and vascular defects (failure of endocardial cushion formation), showing HA is essential for development.
裁定：☐ 过　☐ 改：________　☐ 删

### A06 · basics · open
**题**：Who first isolated hyaluronan, from what tissue, and how did it get its name?
**草稿答案**：Karl Meyer (1934), from bovine vitreous humor; the name combines 'hyalos' (Greek for glass, describing the vitreous) with 'uronic acid'.
裁定：☐ 过　☐ 改：________　☐ 删

### A07 · basics · open
**题**：Which two UDP-sugar substrates do hyaluronan synthases polymerize?
**草稿答案**：UDP-glucuronic acid and UDP-N-acetylglucosamine, added alternately to the growing chain.
裁定：☐ 过　☐ 改：________　☐ 删

### A08 · basics · open
**题**：Why are concentrated HMW-HA solutions viscoelastic and shear-thinning?
**草稿答案**：Very long chains entangle into a transient network and bind large amounts of water; under shear the chains align and disentangle, so viscosity falls (shear-thinning) and recovers at rest.
裁定：☐ 过　☐ 改：________　☐ 删

### A10 · basics · open
**题**：Which bacterium is the workhorse of industrial HA fermentation, and which animal tissue was the classic extraction source?
**草稿答案**：Streptococcus zooepidemicus (group C streptococci) for fermentation; rooster combs for animal extraction.
裁定：☐ 过　☐ 改：________　☐ 删

### A12 · basics · open
**题**：What is unusual about the direction of chain growth in HA synthesis?
**草稿答案**：HAS adds new sugars to the REDUCING end of the growing chain (the chain is extruded through the membrane as it grows) - the opposite of most polysaccharide synthesis, which elongates the non-reducing end.
裁定：☐ 过　☐ 改：________　☐ 删

### A13 · basics · open
**题**：Which fetal tissue is famously rich in HA, and in what structure?
**草稿答案**：The umbilical cord - its Wharton's jelly is an HA-rich mucoid connective tissue (an early commercial HA source).
裁定：☐ 过　☐ 改：________　☐ 删

### A15 · basics · open
**题**：How do HAS1, HAS2, and HAS3 differ in the size of HA they produce?
**草稿答案**：HAS2 produces the longest chains (typically >2 MDa); HAS1 and HAS3 produce shorter chains (roughly 0.2-2 MDa), with HAS3 generally the most active enzyme per molecule.
裁定：☐ 过　☐ 改：________　☐ 删

### A16 · basics · open
**题**：What does the carbazole assay measure, and why is it used for HA?
**草稿答案**：It colorimetrically measures uronic acid content after acid hydrolysis; since every HA disaccharide carries one glucuronic acid, it serves as a classic (if not fully specific) HA quantification assay.
裁定：☐ 过　☐ 改：________　☐ 删

### A17 · basics · open
**题**：How do ELISA-like HA assays work?
**草稿答案**：They use HA-binding protein (HABP, e.g., from bovine cartilage) in a sandwich/competitive format - HABP binds HA with high specificity, replacing antibodies that HA (a non-immunogenic molecule) cannot raise.
裁定：☐ 过　☐ 改：________　☐ 删

### A18 · basics · open
**题**：What is the particle exclusion assay used to visualize?
**草稿答案**：The HA-rich pericellular coat (glycocalyx): fixed red blood cells or beads are excluded from a halo around living cells whose thickness reports the HA coat, which collapses after hyaluronidase treatment.
裁定：☐ 过　☐ 改：________　☐ 删

### A19 · basics · open
**题**：Why is fermentation-derived HA polydisperse while chemoenzymatic synthesis can be monodisperse?
**草稿答案**：Fermentation produces a statistical distribution of chain lengths set by enzyme processivity and broth conditions; stepwise enzymatic synthesis with pmHAS and controlled UDP-sugar feeding builds defined-length, near-monodisperse chains.
裁定：☐ 过　☐ 改：________　☐ 删

### A20 · basics · open
**题**：Which enzyme enables chemoenzymatic HA synthesis, and from which organism?
**草稿答案**：pmHAS, the hyaluronan synthase from Pasteurella multocida, a bifunctional glycosyltransferase usable in vitro for one-pot synthesis of size-controlled HA oligosaccharides.
裁定：☐ 过　☐ 改：________　☐ 删

### A22 · basics · open
**题**：Which fermentation variables most strongly influence the MW of microbial HA?
**草稿答案**：UDP-sugar precursor supply and balance, dissolved oxygen/aeration, pH, temperature, and agitation/shear - conditions that change synthase throughput or chain termination shift the MW distribution.
裁定：☐ 过　☐ 改：________　☐ 删

### A23 · basics · open
**题**：Besides vertebrate tissues, from what source was HA isolated in the 1930s by Meyer's contemporaries?
**草稿答案**：Bacterial capsules - HA was isolated from group A streptococci (Kendall and coworkers, 1937), the first hint it is also a microbial product.
裁定：☐ 过　☐ 改：________　☐ 删

### A24 · basics · open
**题**：Why is HA non-immunogenic in every species, including across species barriers?
**草稿答案**：Its chemical structure is identical in all organisms (same disaccharide, no protein, no species-specific epitopes), so the immune system treats it as self everywhere.
裁定：☐ 过　☐ 改：________　☐ 删

### A25 · basics · open
**题**：How is HA molecular weight estimated from intrinsic viscosity?
**草稿答案**：Via the Mark-Houwink relation ([eta] = K x M^a) calibrated for HA in a given solvent; viscometry gives a viscosity-average MW, less absolute than SEC-MALS.
裁定：☐ 过　☐ 改：________　☐ 删

### A26 · basics · open
**题**：Why is HA a polyelectrolyte at physiological pH?
**草稿答案**：Each disaccharide carries one carboxyl group (pKa ~3-4); at pH 7.4 these are ionized, making HA a polyanion whose charges drive its water binding and chain expansion.
裁定：☐ 过　☐ 改：________　☐ 删

### A27 · basics · open
**题**：How should HA solutions be stored, and what degrades them on the shelf?
**草稿答案**：Cold (typically 4 C), protected from extremes of pH and microbial contamination; acid/alkaline hydrolysis, heat, and contaminating hyaluronidases or ROS progressively cut the chains.
裁定：☐ 过　☐ 改：________　☐ 删

### A28 · basics · open
**题**：What purification steps follow microbial HA fermentation?
**草稿答案**：Cell removal, repeated ethanol/isopropanol precipitation or membrane filtration to remove proteins, nucleic acids and media components, endotoxin control, and drying - medical grades demand very low protein and endotoxin limits.
裁定：☐ 过　☐ 改：________　☐ 删

### A29 · basics · open
**题**：What does 'HA6' mean in oligosaccharide nomenclature?
**草稿答案**：An HA oligosaccharide of 6 monosaccharide units (3 disaccharides); oligos are named by total sugar count (HA4, HA6, HA8...).
裁定：☐ 过　☐ 改：________　☐ 删

### A30 · basics · open
**题**：How is HA fluorescently labeled for tracking studies, and what can go wrong?
**草稿答案**：Commonly by coupling fluoresceinamine (or similar) to carboxyls via carbodiimide chemistry; over-labeling consumes the carboxyls needed for CD44 binding and changes the molecule's behavior - labeling degree must stay low.
裁定：☐ 过　☐ 改：________　☐ 删

### A31 · basics · open
**题**：Why is 'hyaluronan' preferred over 'hyaluronic acid' in biochemistry?
**草稿答案**：At physiological pH the molecule exists as a polyanion (a salt), not the free acid; 'hyaluronan' names the molecule regardless of ionization state.
裁定：☐ 过　☐ 改：________　☐ 删

### A32 · basics · open
**题**：How is cartilage's compressive stiffness built from HA?
**草稿答案**：Aggrecan monomers bind along an HA filament (stabilized by link protein) forming huge aggregates that trap water; the swelling pressure of this HA-aggrecan gel, restrained by collagen, gives cartilage its compressive resilience.
裁定：☐ 过　☐ 改：________　☐ 删

### A33 · basics · open
**题**：How does the streptococcal HA capsule help the bacterium evade immunity?
**草稿答案**：The capsule is chemically identical to host HA (molecular mimicry), so it is invisible to the immune system and also resists phagocytosis sterically.
裁定：☐ 过　☐ 改：________　☐ 删

### A34 · basics · open
**题**：HA concentration is highest in which body fluids/compartments?
**草稿答案**：Umbilical cord (Wharton's jelly), synovial fluid, vitreous, and skin dermis are the classic HA-rich compartments; synovial fluid carries roughly 3-4 mg/mL.
裁定：☐ 过　☐ 改：________　☐ 删

## 四、开放题 · chemistry_modification（29 道）
### D01 · chemistry_modification · open
**题**：Which functional group on HA is most commonly used for conjugation chemistry, and with what reagents?
**草稿答案**：The glucuronic-acid carboxyl group, typically via carbodiimide coupling (EDC/NHS) to form amides with amine-bearing molecules.
裁定：☐ 过　☐ 改：________　☐ 删

### D02 · chemistry_modification · open
**题**：How is photocrosslinkable methacrylated HA (HAMA/MeHA) made?
**草稿答案**：By reacting HA hydroxyl groups with methacrylic anhydride (typically at controlled pH), grafting methacrylate groups that later photopolymerize with a photoinitiator.
裁定：☐ 过　☐ 改：________　☐ 删

### D03 · chemistry_modification · open
**题**：Why is thiolated HA useful for hydrogels?
**草稿答案**：Free thiols allow mild crosslinking by disulfide formation or Michael addition to acrylates, giving in-situ-gelling, mucoadhesive networks under physiological conditions.
裁定：☐ 过　☐ 改：________　☐ 删

### D04 · chemistry_modification · open
**题**：What does periodate oxidation do to HA, and what is its drawback?
**草稿答案**：It cleaves vicinal diols on the sugar rings to generate aldehyde groups for Schiff-base crosslinking, but ring opening also fragments/weakens the chain and can reduce bioactivity.
裁定：☐ 过　☐ 改：________　☐ 删

### D05 · chemistry_modification · open
**题**：What is ADH-modified HA used for?
**草稿答案**：Adipic dihydrazide grafting installs pendant hydrazides, which react with aldehydes (e.g., oxidized HA or aldehyde-bearing polymers) to form hydrazone-crosslinked hydrogels.
裁定：☐ 过　☐ 改：________　☐ 删

### D06 · chemistry_modification · open
**题**：What is the degree of substitution (DS) in modified HA, and how is it usually measured?
**草稿答案**：The fraction of disaccharide units (or target groups) bearing the modification; usually quantified by 1H NMR integration, sometimes by colorimetric assays. DS controls crosslink density, stiffness, and degradation rate.
裁定：☐ 过　☐ 改：________　☐ 删

### D07 · chemistry_modification · open
**题**：Why is EDC amidation of HA often run at pH 4.5-5.5, and why is ADH added in excess?
**草稿答案**：Carbodiimide activation of carboxyls is most efficient in mildly acidic (MES-buffered) conditions; excess adipic dihydrazide both raises amidation yield and installs hydrazide handles while minimizing HA-HA crosslinking.
裁定：☐ 过　☐ 改：________　☐ 删

### D08 · chemistry_modification · open
**题**：How does divinyl sulfone (DVS) crosslink HA?
**草稿答案**：Under alkaline conditions, DVS undergoes Michael addition with HA hydroxyl groups, forming sulfonyl-bis-ethyl ether crosslinks (the chemistry behind early hylan-type gels).
裁定：☐ 过　☐ 改：________　☐ 删

### D09 · chemistry_modification · open
**题**：How does tyramine-modified HA (HA-TA) gel enzymatically?
**草稿答案**：Horseradish peroxidase with H2O2 oxidatively couples the tyramine phenols into dityramine crosslinks, giving fast, cytocompatible in-situ gelation whose rate is tuned by H2O2 dose.
裁定：☐ 过　☐ 改：________　☐ 删

### D10 · chemistry_modification · open
**题**：Why use azide-alkyne click chemistry on HA instead of photocrosslinking?
**草稿答案**：Strain-promoted azide-alkyne cycloaddition needs no UV light, photoinitiator, or metal catalyst, so gels form under fully physiological, cell-friendly conditions with spatial uniformity.
裁定：☐ 过　☐ 改：________　☐ 删

### D11 · chemistry_modification · open
**题**：What does benzyl esterification of HA (HYAFF-type materials) achieve?
**草稿答案**：Esterifying the carboxyls makes HA water-insoluble and much slower to degrade, processable into films, membranes, and scaffolds that persist for weeks instead of days.
裁定：☐ 过　☐ 改：________　☐ 删

### D13 · chemistry_modification · open
**题**：Two formulation levers control HAMA hydrogel stiffness besides UV dose - which?
**草稿答案**：Degree of methacrylation (DS) and polymer concentration (wt%); together with light dose they set crosslink density, hence modulus and degradation time.
裁定：☐ 过　☐ 改：________　☐ 删

### D14 · chemistry_modification · open
**题**：Why must periodate oxidation of HA be carefully dosed?
**草稿答案**：Each oxidation opens a sugar ring and weakens the backbone; excess periodate or long reaction times depolymerize HA (large MW drop) and destroy receptor-binding epitopes.
裁定：☐ 过　☐ 改：________　☐ 删

### D15 · chemistry_modification · open
**题**：How do phenylboronic-acid-modified HA gels achieve self-healing?
**草稿答案**：Boronate ester bonds between phenylboronic acid groups and diols are dynamic covalent bonds - they break and reform reversibly, so the network re-knits after damage and is shear-thinning/injectable.
裁定：☐ 过　☐ 改：________　☐ 删

### D16 · chemistry_modification · open
**题**：Why is crosslinked HA gel rheology described by G' and G'' rather than a single viscosity?
**草稿答案**：Gels are viscoelastic solids: the storage modulus G' (elasticity) and loss modulus G'' (viscous flow), and their ratio (tan delta), predict filler lift, cohesivity, and extrusion behavior better than a Newtonian viscosity number.
裁定：☐ 过　☐ 改：________　☐ 删

### D17 · chemistry_modification · open
**题**：What does 'cohesivity' mean for an HA filler gel?
**草稿答案**：The tendency of the gel to hold together as a single mass rather than dispersing into particles under stress - it affects how the filler integrates in tissue and resists migration.
裁定：☐ 过　☐ 改：________　☐ 删

### D19 · chemistry_modification · open
**题**：What side reaction plagues EDC coupling of HA, and how is it reduced?
**草稿答案**：The activated O-acylisourea can rearrange to a stable N-acylurea (dead end) or hydrolyze; NHS (or sulfo-NHS) traps it as an active ester, and acidic pH plus ADH spacers further raise useful yields.
裁定：☐ 过　☐ 改：________　☐ 删

### D20 · chemistry_modification · open
**题**：How are HA hydrogels made enzymatically degradable on demand in cell culture?
**草稿答案**：Adding hyaluronidase dissolves HA networks specifically; gels are also often built with protease-cleavable peptide crosslinks so cells can remodel them - degradation is a design variable, not an accident.
裁定：☐ 过　☐ 改：________　☐ 删

### D21 · chemistry_modification · open
**题**：What is sulfated HA, and why is it made despite native HA being non-sulfated?
**草稿答案**：Chemically sulfating HA's hydroxyls gives a heparin-like, highly charged derivative with growth-factor-binding and anticoagulant-adjacent properties used in scaffolds and coatings - properties native HA lacks.
裁定：☐ 过　☐ 改：________　☐ 删

### D22 · chemistry_modification · open
**题**：Why graft hydrophobic drugs or moieties through a spacer rather than directly onto HA carboxyls in conjugates?
**草稿答案**：Direct dense substitution on carboxyls destroys CD44 binding (the carboxyls are part of receptor recognition) and solubility; spacers and low degrees of substitution preserve targeting and chain behavior.
裁定：☐ 过　☐ 改：________　☐ 删

### D23 · chemistry_modification · open
**题**：What analytical method verifies that BDDE-crosslinked filler has acceptably low residual crosslinker?
**草稿答案**：Chromatographic quantification of residual/free BDDE and its hydrolysis products (e.g., HPLC/GC-MS after extraction) against regulatory limits, since unreacted epoxide is the toxic species.
裁定：☐ 过　☐ 改：________　☐ 删

### D24 · chemistry_modification · open
**题**：Bacterial hyaluronate lyases and vertebrate hyaluronidases cut HA differently - how, and how is the lyase product detected?
**草稿答案**：Lyases cleave by beta-elimination, leaving an unsaturated uronate that absorbs at 232 nm (the standard activity readout); vertebrate hyaluronidases hydrolyze the same beta(1->4) bond without the double bond.
裁定：☐ 过　☐ 改：________　☐ 删

### D25 · chemistry_modification · open
**题**：LAP versus Irgacure 2959 for HAMA photocrosslinking - why choose LAP?
**草稿答案**：LAP absorbs visible light (405 nm) and initiates efficiently at low, cytocompatible doses, whereas Irgacure 2959 needs UV (365 nm) with more phototoxicity risk - LAP is now standard for cell-laden printing.
裁定：☐ 过　☐ 改：________　☐ 删

### D26 · chemistry_modification · open
**题**：Which two routine measurements characterize a crosslinked HA gel batch?
**草稿答案**：Gel fraction (insoluble crosslinked fraction) and equilibrium swelling ratio (water uptake per dry mass), which together report crosslinking efficiency and network density.
裁定：☐ 过　☐ 改：________　☐ 删

### D27 · chemistry_modification · open
**题**：Why can't most HA products simply be autoclaved for sterilization?
**草稿答案**：Moist heat depolymerizes HA (large MW and viscosity loss); sterile filtration is also hard for viscous HMW solutions, so aseptic manufacturing or gentler validated methods are used.
裁定：☐ 过　☐ 改：________　☐ 删

### D28 · chemistry_modification · open
**题**：What are autocrosslinked HA (ACP) gels?
**草稿答案**：HA crosslinked with itself: carbodiimide-mediated internal ester bonds between its own carboxyls and hydroxyls, with no foreign crosslinker molecule in the final network.
裁定：☐ 过　☐ 改：________　☐ 删

### D29 · chemistry_modification · open
**题**：How is HA-CD44 binding affinity of a modified HA typically quantified in vitro?
**草稿答案**：By competitive binding assays (e.g., ELISA-format competition against labeled native HA) giving IC50 values, or by SPR/BLI with immobilized CD44 - always benchmarked against unmodified HA of matched MW.
裁定：☐ 过　☐ 改：________　☐ 删

### D31 · chemistry_modification · open
**题**：Why do HA hydrogel papers report both compressive and shear moduli?
**草稿答案**：Hydrogels are loaded differently in different tissues (compression in cartilage, shear in skin/vocal fold); matching the relevant modulus to the target tissue is the design criterion, so both are reported.
裁定：☐ 过　☐ 改：________　☐ 删

### D32 · chemistry_modification · open
**题**：What does 'in-situ crosslinking' buy clinically for HA gels?
**草稿答案**：The precursor is injected as a liquid and gels in place, conforming to irregular defects and avoiding open surgery - at the cost of needing fast, non-toxic gelation chemistry.
裁定：☐ 过　☐ 改：________　☐ 删

## 四、开放题 · clinical_quant（19 道）
### F01 · clinical_quant · open
**题**：What is viscosupplementation?
**草稿答案**：Intra-articular injection of HA preparations into a joint (classically the osteoarthritic knee) to restore synovial-fluid viscoelasticity and lubrication.
裁定：☐ 过　☐ 改：________　☐ 删

### F02 · clinical_quant · open
**题**：Which crosslinker is most common in commercial crosslinked HA dermal fillers?
**草稿答案**：BDDE (1,4-butanediol diglycidyl ether).
裁定：☐ 过　☐ 改：________　☐ 删

### F03 · clinical_quant · open
**题**：Roughly how much HA does a 70 kg human contain, and how fast does it turn over?
**草稿答案**：About 15 g total, with roughly one-third degraded and replaced daily - among the fastest turnover rates of any body component.
裁定：☐ 过　☐ 改：________　☐ 删

### F04 · clinical_quant · open
**题**：How are HA filler complications such as vascular occlusion reversed clinically?
**草稿答案**：By injecting hyaluronidase to enzymatically dissolve the HA filler.
裁定：☐ 过　☐ 改：________　☐ 删

### F05 · clinical_quant · open
**题**：Why is HA used as a viscoelastic in cataract surgery?
**草稿答案**：Its high viscoelasticity maintains anterior-chamber depth and protects the corneal endothelium during phacoemulsification and lens implantation.
裁定：☐ 过　☐ 改：________　☐ 删

### F08 · clinical_quant · open
**题**：How long does native, uncrosslinked HA survive in skin and in a joint, and what extends filler lifetime?
**草稿答案**：About a day (skin half-life under 24 h; synovial residence under a day). Chemical crosslinking (e.g., BDDE) extends filler persistence to roughly 6-24 months.
裁定：☐ 过　☐ 改：________　☐ 删

### F09 · clinical_quant · open
**题**：Who coined the term 'viscosupplementation' and pioneered HA's biomedical use?
**草稿答案**：Endre (Endel) Balazs, who also developed the first HA-based biomedical products (e.g., Healon for eye surgery).
裁定：☐ 过　☐ 改：________　☐ 删

### F12 · clinical_quant · open
**题**：What are pseudoseptic reactions to intra-articular HA, and with which product type are they associated?
**草稿答案**：Severe acute inflammatory joint reactions (pain, effusion) without infection, reported mainly with crosslinked avian-derived hylan G-F 20; they are immune/inflammatory reactions to the product, managed conservatively and by avoiding re-injection.
裁定：☐ 过　☐ 改：________　☐ 删

### F13 · clinical_quant · open
**题**：What is Seprafilm made of, and what is it for?
**草稿答案**：A membrane of HA with carboxymethylcellulose (chemically modified), placed at surgery to reduce postoperative adhesions; it gels on contact with tissue and resorbs within about a week.
裁定：☐ 过　☐ 改：________　☐ 删

### F14 · clinical_quant · open
**题**：Cohesive versus dispersive ophthalmic viscosurgical devices - what distinguishes them?
**草稿答案**：Cohesive OVDs are high-MW, high-viscosity HA preparations that hold together and are removed as a mass; dispersive OVDs are lower-MW and coat/protect tissues but are harder to remove completely.
裁定：☐ 过　☐ 改：________　☐ 删

### F15 · clinical_quant · open
**题**：Why is HA instilled into the bladder for interstitial cystitis / BCG-induced cystitis?
**草稿答案**：To replenish the bladder's protective glycosaminoglycan layer, whose loss exposes urothelium to irritants; HA (often with chondroitin sulfate) reduces pain, urgency, and frequency and can raise bladder capacity.
裁定：☐ 过　☐ 改：________　☐ 删

### F16 · clinical_quant · open
**题**：What is the rationale for HA in wound dressings beyond simple moisture?
**草稿答案**：HA dressings maintain a moist healing environment and actively modulate the wound: fragment signaling recruits cells early, and HA supports re-epithelialization and ECM remodeling.
裁定：☐ 过　☐ 改：________　☐ 删

### F18 · clinical_quant · open
**题**：Why do regulators treat HA fillers as medical devices rather than drugs in most jurisdictions?
**草稿答案**：Their primary action is physical (space filling and water binding) rather than pharmacological/metabolic, so they are regulated as implantable devices (e.g., FDA Class III devices).
裁定：☐ 过　☐ 改：________　☐ 删

### F19 · clinical_quant · open
**题**：Why is HA used in gels/mouthwash for oral mucositis?
**草稿答案**：It forms a protective, hydrating film over ulcerated mucosa and supports re-epithelialization, reducing pain from chemotherapy/radiation-induced mucositis.
裁定：☐ 过　☐ 改：________　☐ 删

### F21 · clinical_quant · open
**题**：What is distinctive about the 'hybrid cooperative complex' skinbooster (Profhilo-type) formulation?
**草稿答案**：It combines high- and low-MW HA at very high total concentration (64 mg per 2 mL syringe, ~32 mg/mL) thermally stabilized without chemical crosslinker, giving slow release and tissue remodeling claims.
裁定：☐ 过　☐ 改：________　☐ 删

### F22 · clinical_quant · open
**题**：What does the combination product Cingal add to crosslinked HA, and why?
**草稿答案**：A corticosteroid (triamcinolone hexacetonide) in the same single injection: steroid gives fast early pain relief while HA provides the longer viscoelastic effect.
裁定：☐ 过　☐ 改：________　☐ 删

### F23 · clinical_quant · open
**题**：Standard versus single-injection viscosupplementation regimens?
**草稿答案**：Classic products use 3-5 weekly injections; crosslinked/high-MW products are marketed as single-injection regimens for convenience, with broadly comparable evidence.
裁定：☐ 过　☐ 改：________　☐ 删

### F24 · clinical_quant · open
**题**：Which patients were cautioned against avian-derived HA products?
**草稿答案**：Those with known hypersensitivity to avian proteins/feathers/eggs, a labeled caution for rooster-comb-derived preparations.
裁定：☐ 过　☐ 改：________　☐ 删

### F25 · clinical_quant · open
**题**：Why do clinical guidelines disagree about IA-HA for knee OA?
**草稿答案**：Meta-analyses find small average benefits over saline with large contextual/placebo effects, so societies weigh the same data differently (e.g., AAOS has recommended against routine use while other societies are permissive) - an evidence-interpretation, not data-availability, dispute.
裁定：☐ 过　☐ 改：________　☐ 删

## 四、开放题 · mw_biology（31 道）
### C01 · mw_biology · open
**题**：How do high- and low-molecular-weight HA differ in inflammatory signaling?
**草稿答案**：Native HMW-HA (roughly >1000 kDa) is generally anti-inflammatory and immunosuppressive, whereas LMW fragments generated during injury/inflammation are pro-inflammatory, signaling via TLR2/TLR4 and CD44.
裁定：☐ 过　☐ 改：________　☐ 删

### C02 · mw_biology · open
**题**：How do HA oligosaccharides differ from native HMW-HA in angiogenesis?
**草稿答案**：Short HA oligosaccharides (roughly 4-25 disaccharides) are pro-angiogenic, opposite to native HMW-HA, which is anti-angiogenic.
裁定：☐ 过　☐ 改：________　☐ 删

### C03 · mw_biology · open
**题**：Why was pegylated hyaluronidase (PEGPH20) tested in pancreatic cancer, and what limits the strategy?
**草稿答案**：Tumor stroma rich in HMW-HA raises interstitial fluid pressure and collapses vasculature; PEGPH20 degrades stromal HA to decompress vessels and improve drug delivery. Its Phase III trial (HALO-301) nevertheless failed to improve overall survival.
裁定：☐ 过　☐ 改：________　☐ 删

### C04 · mw_biology · open
**题**：Which methods are standard for measuring HA molecular weight?
**草稿答案**：SEC-MALS (size-exclusion chromatography with multi-angle light scattering) as the reference method; also gel electrophoresis and intrinsic viscometry.
裁定：☐ 过　☐ 改：________　☐ 删

### C05 · mw_biology · open
**题**：How does 4-methylumbelliferone (4-MU) suppress HA synthesis?
**草稿答案**：It depletes the UDP-glucuronic acid substrate pool (via UDP-glucose dehydrogenase competition) and downregulates HAS expression, reducing HA production.
裁定：☐ 过　☐ 改：________　☐ 删

### C06 · mw_biology · open
**题**：Why are naked mole rats so resistant to cancer, in HA terms?
**草稿答案**：They make unusually high-MW HA (roughly 6,000-12,000 kDa) due to a distinct HAS2 sequence and very low hyaluronidase activity; removing this HMW-HA abolishes their cancer resistance in experiments.
裁定：☐ 过　☐ 改：________　☐ 删

### C07 · mw_biology · open
**题**：Describe the CD44/HYAL2/HYAL1 relay that degrades extracellular HMW-HA.
**草稿答案**：GPI-anchored HYAL2, cooperating with CD44 at the cell surface, clips HMW-HA into ~20 kDa fragments; these are endocytosed and HYAL1 in lysosomes completes digestion to tetrasaccharides.
裁定：☐ 过　☐ 改：________　☐ 删

### C08 · mw_biology · open
**题**：What happens to HA in osteoarthritic synovial fluid?
**草稿答案**：Both its concentration and molecular weight fall (healthy synovial HA is roughly 3-4 mg/mL at several MDa), reducing viscoelasticity - the rationale for viscosupplementation.
裁定：☐ 过　☐ 改：________　☐ 删

### C09 · mw_biology · open
**题**：Serum HA is used clinically as a biomarker for what?
**草稿答案**：Liver fibrosis/cirrhosis severity (a component of panels such as the ELF test), because hepatic sinusoidal clearance fails as fibrosis progresses.
裁定：☐ 过　☐ 改：________　☐ 删

### C10 · mw_biology · open
**题**：What is the evidence that tumor HA synthesis itself drives malignancy?
**草稿答案**：HAS2 overexpression increases tumor growth/invasion in models, and suppressing HA synthesis (HAS antisense or 4-MU) reduces tumor progression - HA is an active driver, not just a bystander matrix component.
裁定：☐ 过　☐ 改：________　☐ 删

### C11 · mw_biology · open
**题**：4-MU's other name and drug status?
**草稿答案**：4-methylumbelliferone is hymecromone, an approved choleretic/spasmolytic drug in some countries, repurposed experimentally as an HA-synthesis inhibitor.
裁定：☐ 过　☐ 改：________　☐ 删

### C12 · mw_biology · open
**题**：How do ROS-generated HA fragments differ from hyaluronidase products?
**草稿答案**：Reactive oxygen species cleave HA randomly (non-enzymatic scission), giving a broad size distribution; hyaluronidases cut at defined beta(1->4) linkages, giving more uniform oligosaccharide products (ultimately tetrasaccharides for HYAL1).
裁定：☐ 过　☐ 改：________　☐ 删

### C13 · mw_biology · open
**题**：How does skin HA change with aging?
**草稿答案**：Skin HA content falls markedly with age (by roughly half by about age 50), with epidermal HA disappearing almost entirely in aged skin - a contributor to loss of hydration and turgor.
裁定：☐ 过　☐ 改：________　☐ 删

### C14 · mw_biology · open
**题**：What role does HA play in fertilization and early embryo biology?
**草稿答案**：Cumulus cells synthesize an HA-rich matrix (via HAS2) whose expansion is essential for ovulation/fertilization; HA-based sperm-binding assays exploit mature sperm's HA receptors as a maturity marker.
裁定：☐ 过　☐ 改：________　☐ 删

### C15 · mw_biology · open
**题**：What happens to HA size and amount in inflamed joints compared with healthy joints?
**草稿答案**：Inflammation dilutes and depolymerizes synovial HA (ROS and hyaluronidases), so both concentration and MW drop, reducing lubrication and promoting further inflammatory signaling from fragments.
裁定：☐ 过　☐ 改：________　☐ 删

### C16 · mw_biology · open
**题**：Why are HA fragments considered DAMPs?
**草稿答案**：Fragments are generated specifically by tissue damage and are absent from intact tissue; they alert innate immunity (TLR2/4, CD44) that injury occurred - the definition of a damage-associated molecular pattern.
裁定：☐ 过　☐ 改：________　☐ 删

### C17 · mw_biology · open
**题**：What is 'HA fragmentation balance' in wound healing over time?
**草稿答案**：Early wounds are rich in fragments (pro-inflammatory, pro-angiogenic signals that recruit cells); resolution requires clearance of fragments and restoration of HMW-HA, and failure to switch is linked to chronic wounds/fibrosis.
裁定：☐ 过　☐ 改：________　☐ 删

### C18 · mw_biology · open
**题**：How does tumor-derived HA contribute to chemoresistance physically?
**草稿答案**：Dense HMW-HA gel swells with water, raises interstitial pressure, collapses microvessels, and creates a diffusion barrier - limiting drug and immune-cell access independent of any signaling effect.
裁定：☐ 过　☐ 改：________　☐ 删

### C20 · mw_biology · open
**题**：What did experiments adding hyaluronidase to naked-mole-rat cells, or knocking down their HAS2, demonstrate?
**草稿答案**：Removing their very-HMW-HA made the cells susceptible to malignant transformation, demonstrating causality of HMW-HA in their cancer resistance.
裁定：☐ 过　☐ 改：________　☐ 删

### C21 · mw_biology · open
**题**：Why can serum HA be misleading as a pure liver-fibrosis marker?
**草稿答案**：Serum HA also rises with joint inflammation, renal impairment, and other states of increased production or reduced clearance - it is sensitive but not liver-specific.
裁定：☐ 过　☐ 改：________　☐ 删

### C22 · mw_biology · open
**题**：What is the relationship between HA and angiogenesis in tumors specifically?
**草稿答案**：Fragment-rich tumor HA promotes angiogenesis (oligosaccharides stimulate endothelial proliferation/migration), feeding tumor growth, while intact HMW-HA is anti-angiogenic - tumors benefit from partial degradation.
裁定：☐ 过　☐ 改：________　☐ 删

### C23 · mw_biology · open
**题**：What happens to the vitreous HA-collagen gel with age?
**草稿答案**：The gel liquefies (syneresis) as HA depolymerizes/redistributes and collagen aggregates, leading to floaters and posterior vitreous detachment.
裁定：☐ 过　☐ 改：________　☐ 删

### C24 · mw_biology · open
**题**：HA is the backbone of which brain extracellular structures?
**草稿答案**：Perineuronal nets: HA backbones organize lecticans (CSPGs) and link proteins around neurons, gating synaptic plasticity.
裁定：☐ 过　☐ 改：________　☐ 删

### C25 · mw_biology · open
**题**：What has been reported about HA in the lungs of severe COVID-19 patients?
**草稿答案**：Marked HA accumulation in edematous alveolar exudates (with upregulated HAS and downregulated degradation reported), proposed to contribute to the gel-like lung fluid - a finding still being mechanistically debated.
裁定：☐ 过　☐ 改：________　☐ 删

### C26 · mw_biology · open
**题**：How does HA turnover differ between skin and cartilage?
**草稿答案**：Skin HA turns over in under a day, while cartilage HA (locked in aggregates) persists for weeks - turnover is set by local drainage, receptor clearance, and matrix entrapment.
裁定：☐ 过　☐ 改：________　☐ 删

### C27 · mw_biology · open
**题**：How do sex hormones affect dermal HA?
**草稿答案**：Estrogen supports dermal HA content; its postmenopausal fall parallels skin HA loss, dryness, and thinning.
裁定：☐ 过　☐ 改：________　☐ 删

### C28 · mw_biology · open
**题**：Mechanical loading of cartilage regulates HA how?
**草稿答案**：Physiological loading stimulates chondrocyte HA (and aggrecan) synthesis, maintaining the aggregate pool; overload/unloading disturbs this balance toward catabolism.
裁定：☐ 过　☐ 改：________　☐ 删

### C29 · mw_biology · open
**题**：In diabetic kidney disease, what happens to interstitial HA?
**草稿答案**：HA accumulates in the renal interstitium (driven by hyperglycemia and inflammation), where it is associated with leukocyte infiltration and fibrosis progression.
裁定：☐ 过　☐ 改：________　☐ 删

### C30 · mw_biology · open
**题**：Why do senescent/aging fibroblasts produce a different HA environment?
**草稿答案**：Aging fibroblasts shift HAS/HYAL expression and produce less and shorter HA with a thinner pericellular coat, weakening HA-dependent signaling and hydration in aged dermis.
裁定：☐ 过　☐ 改：________　☐ 删

### C31 · mw_biology · open
**题**：What is the evidence that HA accumulation precedes fibrosis rather than only following it?
**草稿答案**：HA rises early in injured tissue, HAS2 overexpression alone can drive fibrotic phenotypes in models, and blocking HA synthesis (4-MU) attenuates fibrosis - supporting a causal, not merely reactive, role.
裁定：☐ 过　☐ 改：________　☐ 删

### C32 · mw_biology · open
**题**：HA in amniotic fluid and fetal wound healing - what is special?
**草稿答案**：Fetal wounds heal scarlessly in an HA-rich environment with prolonged HMW-HA presence, a contrast with adult wounds where HA is rapidly fragmented - one rationale for HA-based scar-modulating products.
裁定：☐ 过　☐ 改：________　☐ 删

## 四、开放题 · nano_delivery（28 道）
### E01 · nano_delivery · open
**题**：How do self-assembled HA nanoparticles form?
**草稿答案**：Hydrophobic moieties (e.g., 5-beta-cholanic acid or deoxycholic acid) are conjugated to the HA backbone, making an amphiphile that self-assembles in water into nanoparticles with a hydrophobic core and an HA shell.
裁定：☐ 过　☐ 改：________　☐ 删

### E02 · nano_delivery · open
**题**：Why are HA nanoparticles used for cancer drug delivery?
**草稿答案**：The HA shell targets CD44, which is overexpressed on many tumor cells and cancer stem cells, while the core loads hydrophobic drugs; HA is also biocompatible and biodegradable.
裁定：☐ 过　☐ 改：________　☐ 删

### E03 · nano_delivery · open
**题**：What is a major clearance liability of intravenously injected HA nanoparticles?
**草稿答案**：Rapid hepatic uptake via HARE/Stabilin-2 on liver sinusoidal endothelium (plus hyaluronidase degradation), which competes with tumor accumulation.
裁定：☐ 过　☐ 改：________　☐ 删

### E04 · nano_delivery · open
**题**：How does HA molecular weight affect CD44-targeted nanoparticle binding?
**草稿答案**：Binding is multivalent and MW-dependent: longer HA chains generally give stronger avidity for CD44, but also faster clearance; an intermediate MW is usually optimal and must be tuned empirically.
裁定：☐ 过　☐ 改：________　☐ 删

### E05 · nano_delivery · open
**题**：Give an example of an HA-drug conjugate strategy and its rationale.
**草稿答案**：Covalent conjugates such as HA-paclitaxel: the HA backbone targets CD44 and solubilizes the hydrophobic drug, with release by linker cleavage or hyaluronidase at the tumor site.
裁定：☐ 过　☐ 改：________　☐ 删

### E06 · nano_delivery · open
**题**：What size and surface charge do self-assembled HA nanoparticles typically have, and why?
**草稿答案**：Roughly 100-300 nm, with negative zeta potential from the ionized carboxyls of the HA shell.
裁定：☐ 过　☐ 改：________　☐ 删

### E07 · nano_delivery · open
**题**：Which two accumulation mechanisms are usually claimed for HA nanoparticles in tumors?
**草稿答案**：Passive accumulation via the EPR effect (leaky tumor vasculature) plus active CD44-mediated binding and endocytosis by tumor cells.
裁定：☐ 过　☐ 改：________　☐ 删

### E08 · nano_delivery · open
**题**：How can hyaluronidase be exploited for triggered drug release from HA carriers?
**草稿答案**：Tumors and endolysosomes are rich in hyaluronidase; enzymatic degradation of the HA shell/backbone at the target site disassembles the carrier and releases the payload locally.
裁定：☐ 过　☐ 改：________　☐ 删

### E09 · nano_delivery · open
**题**：Give two ways HA is combined with liposomes for delivery.
**草稿答案**：Surface-coating preformed liposomes with HA by adsorption/conjugation, or anchoring HA-lipid conjugates (e.g., HA-phospholipid) directly in the bilayer - both give a CD44-targeting, negatively charged corona.
裁定：☐ 过　☐ 改：________　☐ 删

### E10 · nano_delivery · open
**题**：How are self-assembled HA nanoparticles used in tumor imaging (not just therapy)?
**草稿答案**：Their hydrophobic core can carry imaging payloads - NIR dyes, Raman reporters, or contrast agents - so CD44 targeting concentrates the probe in tumors for fluorescence/photoacoustic/SERS imaging and image-guided surgery.
裁定：☐ 过　☐ 改：________　☐ 删

### E12 · nano_delivery · open
**题**：Name three payloads demonstrated in self-assembled HA nanoparticles.
**草稿答案**：Hydrophobic small-molecule drugs such as paclitaxel and doxorubicin, and nucleic acids such as siRNA (also imaging agents in theranostic versions).
裁定：☐ 过　☐ 改：________　☐ 删

### E13 · nano_delivery · open
**题**：How do HA nanoparticle size and HA molecular weight affect liver accumulation?
**草稿答案**：Larger particles and longer HA chains are cleared faster by the liver (HARE-mediated uptake and Kupffer/sinusoidal capture); smaller (~100 nm), moderately sized HA coatings reduce hepatic sequestration.
裁定：☐ 过　☐ 改：________　☐ 删

### E14 · nano_delivery · open
**题**：Why do HA nanoparticles sometimes show WORSE tumor delivery despite CD44 targeting?
**草稿答案**：The same HA that targets CD44 is scavenged by liver HARE and degraded by hyaluronidases; high HA density/MW can accelerate clearance enough to erase the targeting gain - targeting and clearance are the same interaction.
裁定：☐ 过　☐ 改：________　☐ 删

### E15 · nano_delivery · open
**题**：How is siRNA loaded into HA-based nanoparticles if both are anionic?
**草稿答案**：By pre-condensing siRNA with a cationic component (e.g., PEI, polylysine, or cationic lipids) inside the particle, or via thiolated-HA/disulfide-stabilized assemblies - bare HA cannot complex siRNA directly.
裁定：☐ 过　☐ 改：________　☐ 删

### E16 · nano_delivery · open
**题**：What is a theranostic HA nanoparticle?
**草稿答案**：A single HA nanoparticle carrying both a therapeutic payload and an imaging reporter (e.g., NIR dye, Raman tag, or metal core), so the same CD44-targeted particle enables diagnosis/imaging and treatment.
裁定：☐ 过　☐ 改：________　☐ 删

### E18 · nano_delivery · open
**题**：Why add a PEG layer to some HA nanoparticles, and what is the tradeoff?
**草稿答案**：PEG reduces protein adsorption and liver uptake, extending circulation; the tradeoff is that a dense PEG corona can shield HA and reduce CD44 binding ('PEG dilemma').
裁定：☐ 过　☐ 改：________　☐ 删

### E19 · nano_delivery · open
**题**：How can HA coating change the biodistribution of a metal nanoparticle such as gold?
**草稿答案**：It shifts uptake away from nonspecific RES clearance patterns toward CD44-expressing tissues/tumors and improves colloidal stability and biocompatibility, though liver uptake remains substantial.
裁定：☐ 过　☐ 改：________　☐ 删

### E20 · nano_delivery · open
**题**：What release mechanism do HA-coated carriers gain inside CD44-positive endolysosomes?
**草稿答案**：Lysosomal hyaluronidase (HYAL1) plus acidic pH degrade the HA coat after endocytosis, destabilizing the carrier and releasing the payload intracellularly.
裁定：☐ 过　☐ 改：________　☐ 删

### E22 · nano_delivery · open
**题**：Why do DLS and TEM sizes disagree for HA nanoparticles?
**草稿答案**：DLS measures the hydrated particle including the swollen HA corona in solution; TEM measures dried, collapsed particles - TEM sizes are systematically smaller, and both should be reported.
裁定：☐ 过　☐ 改：________　☐ 删

### E23 · nano_delivery · open
**题**：What is the protein corona problem for HA nanoparticles in blood?
**草稿答案**：Serum proteins adsorb within seconds, masking HA, changing size/charge, and redirecting uptake (often to macrophages) - in-vitro targeting often degrades in vivo for this reason.
裁定：☐ 过　☐ 改：________　☐ 删

### E24 · nano_delivery · open
**题**：Why are HA nanoparticle batches often made by microfluidic mixing at scale-up?
**草稿答案**：Controlled, rapid mixing gives reproducible nucleation/self-assembly, tightening size distribution versus bulk mixing - critical for a size-dependent delivery product.
裁定：☐ 过　☐ 改：________　☐ 删

### E25 · nano_delivery · open
**题**：How are HA nanoparticle suspensions usually stabilized for storage?
**草稿答案**：Lyophilization with cryo/lyoprotectants such as trehalose or sucrose, which prevents aggregation and HA degradation during drying and storage.
裁定：☐ 过　☐ 改：________　☐ 删

### E26 · nano_delivery · open
**题**：Compare hydrazone, ester, and disulfide linkers in HA-drug conjugates.
**草稿答案**：Hydrazone: acid-labile, releases in endosomes/tumor acidity. Ester: hydrolyzes/esterase-cleaved, slower systemic release. Disulfide: reduced by intracellular glutathione, releasing in the cytosol. Linker choice sets where and how fast the drug frees.
裁定：☐ 过　☐ 改：________　☐ 删

### E27 · nano_delivery · open
**题**：Name an HA-drug conjugate that reached clinical trials and its payload.
**草稿答案**：ONCOFID-P, an HA-paclitaxel conjugate investigated clinically (e.g., intravesical use in bladder cancer and systemic studies); HA-irinotecan conjugates have also been trialed. (Investigational, not approved.)
裁定：☐ 过　☐ 改：________　☐ 删

### E28 · nano_delivery · open
**题**：Beyond tumors, which inflamed tissue is targeted with HA nanoparticles via CD44?
**草稿答案**：Inflamed joints in rheumatoid arthritis, where activated macrophages and synoviocytes overexpress CD44; inflamed intestinal mucosa in IBD models is another target.
裁定：☐ 过　☐ 改：________　☐ 删

### E29 · nano_delivery · open
**题**：How are HA conjugates used for fluorescence-guided surgery?
**草稿答案**：HA is conjugated to near-infrared dyes (e.g., ICG derivatives) so CD44-positive tumor tissue fluoresces under NIR imaging, helping surgeons delineate margins.
裁定：☐ 过　☐ 改：________　☐ 删

### E30 · nano_delivery · open
**题**：Has any HA-nanoparticle drug been approved by the FDA?
**草稿答案**：No - approved HA products are devices/fluids (fillers, viscosupplements, OVDs, barriers); HA nanoparticle therapeutics remain investigational/preclinical or in trials.
裁定：☐ 过　☐ 改：________　☐ 删

### E31 · nano_delivery · open
**题**：Why might an HA nanoparticle perform well in cell culture but fail in animals?
**草稿答案**：Culture lacks serum corona, liver HARE clearance, hyaluronidase-rich blood/tissue, and flow; in vivo these strip or clear the particles before tumor accumulation - the standard translation gap for HA carriers.
裁定：☐ 过　☐ 改：________　☐ 删

## 四、开放题 · receptors_signaling（28 道）
### B01 · receptors_signaling · open
**题**：Which molecule is the principal cell-surface receptor for hyaluronan, and which domain binds HA?
**草稿答案**：CD44; binding is mediated by its N-terminal Link module (hyaluronan-binding domain).
裁定：☐ 过　☐ 改：________　☐ 删

### B02 · receptors_signaling · open
**题**：What is the difference between CD44s and CD44 variant isoforms?
**草稿答案**：CD44s (standard) lacks the alternatively spliced variant exons in the membrane-proximal stem region; CD44v isoforms insert combinations of variant exons (v1-v10), altering interactions and signaling, and are enriched in many cancers.
裁定：☐ 过　☐ 改：________　☐ 删

### B03 · receptors_signaling · open
**题**：What does RHAMM (CD168) do, and where is it found?
**草稿答案**：RHAMM is a hyaluronan-mediated motility receptor found both intracellularly and at the cell surface; it promotes cell migration and signals through ERK and focal adhesion pathways.
裁定：☐ 过　☐ 改：________　☐ 删

### B04 · receptors_signaling · open
**题**：Which receptor clears circulating hyaluronan from blood, and where?
**草稿答案**：HARE (Stabilin-2) on liver sinusoidal endothelial cells; it gives serum HA a half-life of only a few minutes.
裁定：☐ 过　☐ 改：________　☐ 删

### B05 · receptors_signaling · open
**题**：Which HA receptor is a marker of lymphatic endothelium?
**草稿答案**：LYVE-1, a CD44 homolog expressed on lymphatic endothelial cells.
裁定：☐ 过　☐ 改：________　☐ 删

### B06 · receptors_signaling · open
**题**：Is CD44-HA binding constitutive? What regulates it?
**草稿答案**：No. Binding is tightly regulated by CD44 glycosylation/sialylation, clustering, and cell activation state; many resting cells express CD44 but bind little HA until activated.
裁定：☐ 过　☐ 改：________　☐ 删

### B07 · receptors_signaling · open
**题**：How does CD44 connect HA binding to the cytoskeleton?
**草稿答案**：Its cytoplasmic tail binds ERM proteins (ezrin/radixin/moesin) and ankyrin, coupling extracellular HA binding to actin and to migration/signaling machinery.
裁定：☐ 过　☐ 改：________　☐ 删

### B08 · receptors_signaling · open
**题**：What does TSG-6 do to HA, and why is the product anti-inflammatory?
**草稿答案**：TSG-6 binds HA and catalyzes transfer of heavy chains from inter-alpha-inhibitor onto HA, forming HC-HA complexes that dampen neutrophil migration and inflammation.
裁定：☐ 过　☐ 改：________　☐ 删

### B09 · receptors_signaling · open
**题**：Besides HA, what else does the HARE/Stabilin-2 receptor clear?
**草稿答案**：Other GAGs (chondroitin sulfates, dermatan sulfate, heparin), plus acetylated LDL and other scavenger ligands - it is a broad clearance receptor, with HA its highest-turnover ligand.
裁定：☐ 过　☐ 改：________　☐ 删

### B10 · receptors_signaling · open
**题**：Which innate immune receptors do LMW-HA fragments engage, and what is the caveat?
**草稿答案**：TLR2 and TLR4 (DAMP-like signaling to NF-kB). Caveat: effects are preparation- and purity-dependent, and endotoxin contamination confounded some early studies.
裁定：☐ 过　☐ 改：________　☐ 删

### B13 · receptors_signaling · open
**题**：What is the minimum HA chain length that binds CD44 detectably, and what does high-affinity binding require?
**草稿答案**：A hexasaccharide is about the minimum for detectable binding; stable, high-avidity binding needs longer chains (roughly decasaccharide and up, and in practice much longer/multivalent presentation).
裁定：☐ 过　☐ 改：________　☐ 删

### B14 · receptors_signaling · open
**题**：What is the gene symbol for RHAMM?
**草稿答案**：HMMR (hyaluronan-mediated motility receptor).
裁定：☐ 过　☐ 改：________　☐ 删

### B15 · receptors_signaling · open
**题**：How does HMW-HA clustering of CD44 differ from fragment binding in signaling outcome?
**草稿答案**：HMW-HA multivalently clusters CD44 into assemblies that favor homeostatic/anti-inflammatory signaling, whereas short fragments bind without the same clustering and instead engage TLR2/4-type pro-inflammatory pathways - one basis of MW-dependent biology.
裁定：☐ 过　☐ 改：________　☐ 删

### B16 · receptors_signaling · open
**题**：Name two signaling pathways commonly activated downstream of HA-CD44 in cancer cells.
**草稿答案**：PI3K/Akt (survival) and Ras/MAPK-ERK (proliferation/migration), with additional links to Rho GTPases and EMT transcription programs.
裁定：☐ 过　☐ 改：________　☐ 删

### B17 · receptors_signaling · open
**题**：What are HA cables, and what do they do in inflammation?
**草稿答案**：Long HA strands crosslinked by TSG-6-catalyzed heavy-chain transfer (HC-HA cables) that form on stressed smooth-muscle/epithelial cells and capture monocytes/macrophages via CD44, organizing inflammatory cell adhesion.
裁定：☐ 过　☐ 改：________　☐ 删

### B18 · receptors_signaling · open
**题**：How does HAS2 promote epithelial-mesenchymal transition (EMT) in cancer models?
**草稿答案**：HAS2-driven HA production and CD44 signaling upregulate EMT programs (e.g., Twist/Snail activity and loss of epithelial markers); HAS2 knockdown reverses the mesenchymal, invasive phenotype.
裁定：☐ 过　☐ 改：________　☐ 删

### B20 · receptors_signaling · open
**题**：Why does CD44 need post-translational 'activation' on many leukocytes before it binds HA?
**草稿答案**：On resting cells the HA-binding site is masked (notably by sialylated glycans and receptor conformation); cytokine activation remodels glycosylation/clustering and unmasks binding, letting HA adhesion be switched on at inflammatory sites.
裁定：☐ 过　☐ 改：________　☐ 删

### B21 · receptors_signaling · open
**题**：What stem-cell niches is HA known to help maintain?
**草稿答案**：Hematopoietic and neural stem-cell niches (and MSC pericellular matrices): HMW-HA-rich coats support quiescence, self-renewal, and niche retention via CD44.
裁定：☐ 过　☐ 改：________　☐ 删

### B23 · receptors_signaling · open
**题**：What does link protein (HAPLN1) do in cartilage?
**草稿答案**：It stabilizes the non-covalent binding of aggrecan's G1 domain to HA, locking the aggregate together.
裁定：☐ 过　☐ 改：________　☐ 删

### B24 · receptors_signaling · open
**题**：CD44v6 has a co-receptor role beyond HA binding - for what?
**草稿答案**：It acts as a co-receptor for receptor tyrosine kinases such as c-Met (HGF receptor) and VEGFR-2, coupling CD44v6 to growth-factor signaling in cancer and angiogenesis.
裁定：☐ 过　☐ 改：________　☐ 删

### B25 · receptors_signaling · open
**题**：What happens to CD44 after sequential proteolytic cleavage?
**草稿答案**：Ectodomain shedding (metalloproteinases) followed by gamma-secretase cleavage releases the CD44 intracellular domain (CD44-ICD), which translocates to the nucleus and influences transcription, including of CD44 itself.
裁定：☐ 过　☐ 改：________　☐ 删

### B26 · receptors_signaling · open
**题**：How does endothelial HA participate in leukocyte trafficking?
**草稿答案**：Inflamed endothelium displays HA (often as TSG-6-modified cables) that supports CD44-mediated rolling/adhesion of lymphocytes and monocytes, an auxiliary capture pathway alongside selectins.
裁定：☐ 过　☐ 改：________　☐ 删

### B27 · receptors_signaling · open
**题**：Stabilin-1 versus Stabilin-2 - how do their roles differ?
**草稿答案**：Stabilin-2 (HARE) on liver/lymph sinusoidal endothelium is the systemic HA-clearance receptor; Stabilin-1 is mainly a macrophage scavenger receptor with broader expression in immune regulation, not the main HA sink.
裁定：☐ 过　☐ 改：________　☐ 删

### B28 · receptors_signaling · open
**题**：Why is LYVE-1 relevant to cancer metastasis?
**草稿答案**：Tumors drain through lymphatics; LYVE-1-positive lymphatic endothelium and its HA interactions are implicated in lymphatic invasion and nodal metastasis routes.
裁定：☐ 过　☐ 改：________　☐ 删

### B29 · receptors_signaling · open
**题**：Intracellular RHAMM does what besides surface signaling?
**草稿答案**：It associates with microtubules and the mitotic spindle and with ERK complexes, regulating spindle integrity and cell division - functions independent of extracellular HA.
裁定：☐ 过　☐ 改：________　☐ 删

### B30 · receptors_signaling · open
**题**：What is HABP, the probe used in HA histochemistry and assays?
**草稿答案**：Hyaluronan-binding protein - typically the aggrecan G1/link-protein complex isolated from cartilage - which binds HA specifically and is biotinylated/labeled for detection.
裁定：☐ 过　☐ 改：________　☐ 删

### B31 · receptors_signaling · open
**题**：What is soluble CD44 and where does it come from?
**草稿答案**：The shed CD44 ectodomain, released by metalloproteinase cleavage (e.g., ADAM10, MT1-MMP); it circulates and can act as a decoy for HA binding.
裁定：☐ 过　☐ 改：________　☐ 删

### B32 · receptors_signaling · open
**题**：What is chemically unique about heavy-chain modification of HA?
**草稿答案**：It is the only known covalent attachment of a protein to HA: inter-alpha-inhibitor heavy chains are transesterified onto HA's GlcNAc residues by TSG-6.
裁定：☐ 过　☐ 改：________　☐ 删
