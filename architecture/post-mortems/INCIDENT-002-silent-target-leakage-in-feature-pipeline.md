# INCIDENT-002: Silent Temporal Target Leakage in Feature Pipeline

## Metadata
* **Incident Date:** 2026-06-20 (Discovery of 90-day silent regression)
* **Severity Level:** `SEV-1` (Silent Financial Failure)
* **Incident Commander:** Principal ML Architect & Risk Engineering Lead
* **Time to Detect (TTD):** 84 days (Lagging cohort financial reporting)
* **Time to Mitigate (TTM):** 72 hours (Pipeline refactor & model retraining)

---

## 1. Executive Summary & Impact

In March 2026, we deployed a real-time risk assessment model to approve instant merchant working capital credit lines up to \$25,000. In offline backtesting on 2 years of historical applications, the LightGBM + Transformer ensemble model showed stellar metrics: a **0.94 ROC-AUC**, a **92% precision score**, and a projected default rate of **under 1.8%**.

Based on these results, risk leadership authorized 100% autonomous decisioning for applications under \$10,000.

Eighty-four days later, the finance division alerted engineering that the 90-day delinquency rate on the newly onboarded merchant cohort had surged to **4.7%**—an unexpected credit write-off of **\$1,420,000**. Throughout the entire 84-day period, our ML monitoring dashboards were completely green, reporting a mean model approval confidence of 91.2% with zero operational infrastructure crashes.

The investigation revealed a catastrophic **Silent Statistical Failure**: a point-in-time extraction query in our offline training data pipeline had an insidious **temporal target leakage bug**. One of the strongest predictive features—`chargeback_count_last_30d`—was queried from a mutable operational database table that updated retroactively when a chargeback resolved, rather than taking an immutable historical snapshot at the exact microsecond of the credit application. 

In offline training, the model had learned to "look into the future." In live production, future chargebacks had not occurred yet, causing the model to approve high-risk merchants with supreme confidence.

### Blast Radius Metrics
* **Financial Impact:** **\$1,420,000** in unrecoverable merchant credit defaults.
* **Duration of Silent Failure:** 84 days without operational alarms.
* **Underwriting Disruption:** Halted automated approvals above \$10k, forcing 4,200 applications into manual review queues.

---

## 2. Root Cause Analysis (The 5 Whys)

1. **Why did the real-world default rate jump from 1.8% to 4.7%?**  
   Because the production model approved thousands of merchants who had high hidden credit risk.
2. **Why did the model approve these merchants with 91% confidence?**  
   Because the model's feature weights heavily relied on `chargeback_count_last_30d == 0` as a definitive indicator of merchant safety.
3. **Why did the feature indicate zero risk during training?**  
   Because in historical training data, `chargeback_count_last_30d` was extracted using `WHERE user_id = X` on a live operational table that was constantly updated, retroactively altering historical rows after disputes were resolved.
4. **Why was offline backtesting unable to catch this discrepancy?**  
   Because the offline training set and test set were BOTH generated using the same corrupted point-in-time extraction query, yielding a false 0.94 ROC-AUC across both sets.
5. **Why was there no automated drift alert?**  
   Because standard covariate drift monitors (Kolmogorov-Smirnov and PSI) compare the distribution of individual features. The marginal distribution of integers (0, 1, 2) looked identical; only the *joint temporal correlation with the target label* was corrupted.

---

## 3. The Broken SQL vs. Correct Event-Sourced Architecture

```sql
-- ❌ CATASTROPHIC ANTI-PATTERN: Querying mutable operational table retroactively
-- When run in 2026 for a 2025 application, this pulls chargebacks that happened AFTER application time!
SELECT 
    app.application_id,
    app.application_timestamp,
    COUNT(cb.chargeback_id) AS chargeback_count_last_30d
FROM applications app
LEFT JOIN operational_chargebacks cb ON app.merchant_id = cb.merchant_id
GROUP BY app.application_id;

-- ✅ THE ARCHITECTURAL FIX: Immutable Event Store with Strict Point-in-Time AS OF Join
SELECT 
    app.application_id,
    app.application_timestamp,
    COUNT(cb.chargeback_id) AS chargeback_count_last_30d
FROM applications app
LEFT JOIN immutable_chargeback_events cb 
    ON app.merchant_id = cb.merchant_id
    AND cb.event_timestamp BETWEEN app.application_timestamp - INTERVAL '30 days' 
                               AND app.application_timestamp -- Strict Temporal Barrier!
GROUP BY app.application_id;
```

---

## 4. Immediate Triage & Containment

1. **Threshold Fallback:** Halted autonomous approvals above \$5,000 immediately, routing applications to human underwriters.
2. **Feature Store Quarantine:** Isolated the corrupted feature `chargeback_count_last_30d` from production scoring pipelines.
3. **Retraining on Verified Slices:** Rebuilt the historical training dataset from immutable audit logs (Kafka event stream) with strict `AS OF` temporal join semantics.

---

## 5. Architectural Inoculation (Permanent Systemic Guardrails)

### 1. Mandatory Event-Sourced Feature Store (Feast / BigQuery)
We migrated all ML feature pipelines to an immutable, event-sourced feature store. Features are strictly computed using **point-in-time (`AS OF`) joins**, mathematically guaranteeing that no observation can access events timestamped after the prediction request.

### 2. The "Temporal Consistency Linter"
Every new feature definition must pass an automated temporal verification test in CI/CD:
* Compute feature values on a frozen 30-day historical snapshot.
* Compare those values against live streaming values captured in shadow production over the same period.
* If any discrepancy exists (Δ > 0), the PR is blocked.

### 3. The "Too Good to Be True" Policy Gate
We instituted an organizational rule in our ML RFC process: **Any model achieving ROC-AUC > 0.90 on tabular risk data triggers a mandatory 3-person peer review specifically searching for target leakage.**
