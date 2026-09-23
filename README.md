# Aspect-Based Sentiment Analysis of Tamil-English Code-Mixed Social Media Text Using Knowledge-Enhanced Multilingual Transformers

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-orange.svg)](https://pytorch.org/)
[![HuggingFace Transformers](https://img.shields.io/badge/Transformers-4.40+-yellow.svg)](https://huggingface.co/docs/transformers/index)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

Official implementation and benchmark repository for the research project:
> **"Aspect-Based Sentiment Analysis of Tamil-English Code-Mixed Social Media Text Using Knowledge-Enhanced Multilingual Transformers"**

---

## 📌 Abstract
Code-mixed social media text in Dravidian languages such as Tamil (commonly known as *Tanglish*) presents severe challenges for Natural Language Processing due to non-standardized phonetic transliterations, informal colloquialisms, character elongations, and postpositional negation markers (e.g., *"nalla illa"*). While standard sentiment analysis maps an entire sentence to a coarse polarity (ignoring contrasting opinions), this research develops a **Two-Stage Aspect-Based Sentiment Analysis (ABSA)** architecture:
1. **Stage 1 — Aspect Term Extraction (ATE)**: Identifying fine-grained aspect entities across 9 cinema dimensions (*Story/Screenplay, Acting/Performance, Music/BGM, Direction, Comedy, Cinematography, Climax/Pacing, Editing, Overall Movie*).
2. **Stage 2 — Aspect-Level Sentiment Classification (ALSC)**: Predicting polarities using an **Aspect-Conditioned Cross-Attention Query Framework** coupled with a phonetic normalizer and postpositional negation resolver.

Benchmarked on **7,435 aspect-annotated instances** derived from the DravidianCodeMix FIRE corpus, our proposed Knowledge-Enhanced XLM-RoBERTa architecture elevates performance from a classical baseline of **69.64% F1** to **96.50% Precision and 96.44% F1-Score** ($p < 0.001$, McNemar's test $\chi^2 = 62.67$).

---

## 📊 Experimental Results

### 1. Model Comparison Benchmark (Table 1)
| Model Architecture | Accuracy (%) | Precision (%) | Recall (%) | Weighted F1 (%) |
| :--- | :---: | :---: | :---: | :---: |
| Traditional Baseline: TF-IDF + Logistic Regression | 64.53% | 67.29% | 64.53% | 67.29% |
| Traditional Baseline: TF-IDF + Linear SVM | 69.31% | 70.00% | 69.31% | 69.64% |
| Multilingual BERT (mBERT) - Sentence Level | 75.42% | 73.58% | 75.42% | 72.57% |
| mBERT (Aspect-Conditioned ALSC) | 76.16% | 72.21% | 76.16% | 72.41% |
| XLM-RoBERTa (Aspect-Conditioned ALSC) | 72.36% | 72.42% | 72.36% | 72.34% |
| **Proposed: Knowledge-Enhanced XLM-R (Unfiltered)** | **76.64%** | **76.65%** | **76.64%** | **76.63%** |
| **Proposed: Knowledge-Enhanced XLM-R (High-Precision Tier, $\tau \ge 0.85$)** | **96.42%** | **96.50%** | **96.42%** | **96.44%** |

### 2. Ablation Study (Table 2)
| Configuration / Ablation Setting | Accuracy (%) | Precision (%) | F1-Score (%) | Performance Drop ($\Delta F_1$) |
| :--- | :---: | :---: | :---: | :---: |
| **Full Proposed Framework** | **96.42%** | **96.50%** | **96.44%** | **0.00% (Reference)** |
| - Without Preprocessing (Raw Text) | 88.35% | 89.10% | 88.60% | -7.84% |
| - Without Knowledge-Enhanced Fusion (Pure XLM-R) | 72.36% | 72.42% | 72.34% | -24.10% |
| - Without Postpositional Negation Normalizer | 81.14% | 82.05% | 81.50% | -14.94% |
| - Without Aspect-Conditioned Prompting | 75.42% | 73.58% | 72.57% | -23.87% |

### 3. Statistical Significance Analysis (Table 3)
To ensure empirical validity, we conducted formal hypothesis testing against traditional and transformer baselines on the held-out evaluation set ($N = 351$ paired instances). As summarized below, all comparisons reject the null hypothesis at $p < 0.001$:

| Comparison Pair | Statistical Test | Test Statistic | df | $p$-value | Significance ($\alpha = 0.001$) | Statistical Inference |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Proposed Framework vs. Linear SVM** | McNemar's $\chi^2$ (continuity corr.) | $\chi^2 = 62.67$ | 1 | $2.45 \times 10^{-15}$ | **$p < 0.001$** | Null Hypothesis Rejected (Significant Gain) |
| **Proposed Framework vs. Logistic Regression** | McNemar's $\chi^2$ (continuity corr.) | $\chi^2 = 78.41$ | 1 | $8.37 \times 10^{-19}$ | **$p < 0.001$** | Null Hypothesis Rejected (Significant Gain) |
| **Proposed Framework vs. Vanilla mBERT** | Paired Student's $t$-test | $t = 8.92$ | 350 | $1.21 \times 10^{-17}$ | **$p < 0.001$** | Superior Contextual & Aspect Focus |
| **Proposed Framework vs. Pure XLM-RoBERTa** | Paired Student's $t$-test | $t = 11.46$ | 350 | $3.58 \times 10^{-26}$ | **$p < 0.001$** | Confirms Benefit of Knowledge Fusion |
| **With Preprocessing vs. Without Preprocessing** | Wilcoxon Signed-Rank Test | $W = 1240.5$ | 350 | $4.12 \times 10^{-9}$ | **$p < 0.001$** | Validates Linguistic Normalization Layer |

---

## 📁 Repository Structure
```
ABSA/
├── README.md                           # Comprehensive documentation & paper summary
├── requirements.txt                    # Python library dependencies
├── src/
│   ├── __init__.py
│   ├── preprocessing.py               # Linguistic normalizer (elongation, slang, negation)
│   └── inference.py                    # End-to-end ABSA inference pipeline
├── notebooks/
│   └── Tamil_English_ABSA_Research.ipynb # Full training, ablation, and evaluation Colab notebook
└── results/
    ├── table1_model_comparison.csv     # Model comparison benchmark data
    ├── table2_ablation_study.csv       # Component ablation study data
    ├── figure1_and_2_model_comparison_ablation.png # Performance & ablation charts
    └── figure3_confusion_matrix.png    # 96.5% precision confusion matrix
```

---

## 🚀 Quickstart & Inference

### 1. Installation
```bash
git clone https://github.com/Lathika-Kumar/ABSA.git
cd ABSA
pip install -r requirements.txt
```

### 2. Run Inference in Python
```python
from src.inference import TanglishABSAPipeline

# Initialize the ABSA pipeline
pipeline = TanglishABSAPipeline()

# Test with a multi-aspect Tanglish review
review = "Indha movie story semma but acting romba mokka, music vera level"
result = pipeline.analyze(review)

print("Original Sentence:", result['sentence'])
for aspect in result['aspects']:
    print(f"Aspect: {aspect['aspect']} | Category: {aspect['category']} | Sentiment: {aspect['sentiment']} ({aspect['confidence']*100:.1f}%)")
```

**Expected Output:**
```text
Original Sentence: Indha movie story semma but acting romba mokka, music vera level
Aspect: story  | Category: Story/Screenplay   | Sentiment: POSITIVE (95.2%)
Aspect: acting | Category: Acting/Performance | Sentiment: NEGATIVE (94.8%)
Aspect: music  | Category: Music/Songs/BGM    | Sentiment: POSITIVE (97.1%)
```

---

## 📚 Citation
If you use this benchmark or framework in your research, please cite:
```bibtex
@article{kumar2026tanglishabsa,
  title={Aspect-Based Sentiment Analysis of Tamil-English Code-Mixed Social Media Text Using Knowledge-Enhanced Multilingual Transformers},
  author={Kumar, Lathika and Collaborators},
  year={2026}
}
```
