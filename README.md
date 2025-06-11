
# 🧠 AI-Powered Wallet Credit Scoring

A real-world AI implementation designed to evaluate **DeFi wallet reliability** by analyzing user behavior on platforms like Compound V2. This project blends traditional credit risk logic with decentralized finance, enabling smarter lending decisions in Web3.

---

### 📌 Problem Statement

> “DeFi lacks credit scoring mechanisms, making risk assessment unreliable.”

* No concept of **creditworthiness** like in traditional finance.
* Wallets may **borrow, repay, or get liquidated** with no consequence.
* We aim to evaluate a wallet’s **trustworthiness** based on its raw transaction behavior.

---

### 🧱 Architecture Overview

```text
Raw DeFi JSON (Compound V2)
        ↓
Feature Extraction (behavioral metrics)
        ↓
Rule-Based Score + ML Model
        ↓
Scored Wallet CSV + Streamlit Dashboard
```

* Parsed JSON transaction logs (deposits, borrows, repays, liquidations).
* Extracted behavioral features (e.g., repay delay, liquidation count, borrow-repay ratio).
* Built explainable ML model (Random Forest Regressor).
* Output: final score, tier, and behavioral justification.

---

### 🧪 Modeling

* **Model**: Random Forest Regressor
* **MAE**: \~0.80
* **R² Score**: \~0.96
* **Validation**: Cross-validation, distribution plots, error interpretation
* **Tools Used**:

  * `pandas`, `scikit-learn` for ML pipeline
  * `Streamlit` for dashboard interface
  * `Plotly` for visualizations

---

### 📊 Features Used

* `repay_to_borrow_ratio`
* `days_delayed_between_borrow_and_repay`
* `liquidation_flag` (binary)
* `borrow_normalized_amount`
* `repay_normalized_amount`

---

### 📈 Results & Output

* CSV of wallet scores with:

  * Final credit score
  * Tier (A, B, C, etc.)
  * Reasoning summary (e.g., "Low repay ratio, no liquidations")
* Interactive **Streamlit dashboard**:

  * Filter by score/tier
  * Histogram and box plots
  * Search wallet address

---

### 🚀 Use Cases

* **DeFi lenders**: Assess wallet trustworthiness before loans.
* **Auditors**: Detect wallets with suspicious behavior.
* **Analysts**: Segment users based on risk profile.

---

### 🌐 Future Work

> "I'm also working on an AI project to reduce road accidents by detecting high-risk zones using animal crossing + vehicle interaction patterns from geo-tagged data."

* Adds to the vision of **AI-for-impact** systems.
* Future goal: Expand into real-time risk prediction.

---

### 🧑‍💻 Author

**Bayoju Vikas**
[LinkedIn](https://www.linkedin.com/in/bayoju-vikas-81578726a)

