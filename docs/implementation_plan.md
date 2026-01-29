# Implementation Plan: Forecast Pyme Empanadas

# Goal
Implement a monthly forecasting engine (Horizon: 3 months) to reduce planning error below 45%, structured in 9 phases.

## Standard Deliverables per Phase
> [!IMPORTANT]
> **Reporting Rules:**
> 1.  All reports MUST be saved in **`outputs/reports/`**. Create this directory if it does not exist.
> 2.  **`results.json`**: Structural data of findings.
> 3.  **`report.md`**: Human-readable summary (Findings, Issues, Recommendations, Conclusions).
> 4.  **Tests**: Unit/Integration tests are mandatory.

## Phases

### Phase 1: Data Loading (Supabase)
**Status**: Completed
- **Goal**: Fetch raw daily data.
- **Tasks**: Connect and download `ventas_raw`.
- **Outputs**: `p1_load_stats.json`, `p1_loading_report.md`.

### Phase 2: Transformation (Daily -> Monthly)
**Status**: Completed
- **Goal**: Clean and aggregate to monthly grain (Strict No-Imputation).
- **Tasks**: Cleaning (Sentinels), Category Normalization, Strict Aggregation.
- **Outputs**: `p2_transformation_stats.json`, `p2_transformation_report.md`.

### Phase 3: Data Preparation
**Status**: Not Started
- **Goal**: Audit data quality and apply controlled imputation.
- **Tasks**: Identify missing values, duplicates, and check series completeness. Implement imputation (strategy to be defined).
- **Outputs**: `p3_prep_stats.json`, `p3_preparation_report.md`.

### Phase 4: Exploratory Data Analysis (EDA)
**Status**: Not Started
- **Goal**: Analyze series behavior.
- **Tasks**: Visual analysis, Seasonality check, Outlier detection.
- **Outputs**: `p4_eda_metrics.json`, `p4_eda_report.md`.

### Phase 5: Feature Engineering
**Status**: Not Started
- **Goal**: Create predictors.
- **Tasks**: Lags, Rolling windows, Categorical encoding.
- **Outputs**: `p5_feature_stats.json`, `p5_feature_report.md`.

### Phase 6: Training & Modeling (Tournament)
**Status**: Not Started
- **Goal**: Algorithm competition.
- **Tasks**: Train `ForecasterDirect` candidates.
- **Outputs**: `p6_tournament_metrics.json`, `p6_modeling_report.md`.

### Phase 7: Model Selection & Tuning
**Status**: Not Started
- **Goal**: Optimize winner.
- **Tasks**: Hyperparameter tuning.
- **Outputs**: `p7_tuning_metrics.json`, `p7_selection_report.md`.

### Phase 8: Inference
**Status**: Not Started
- **Goal**: Future predictions ($X+1, X+2, X+3$).
- **Tasks**: Retrain and Predict.
- **Outputs**: `p8_forecast_metadata.json`, `p8_inference_report.md`.

### Phase 9: Production Deployment
**Status**: Not Started
- **Goal**: Pipeline automation.
- **Tasks**: Orchestration and Documentation.
- **Outputs**: `p9_pipeline_status.json`, `p9_deployment_report.md`.
