# Implementation Plan: Forecast Pyme Empanadas

# Goal
Implement a monthly forecasting engine (Horizon: 3 months) to reduce planning error below 45%, structured in 8 phases.

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
**Status**: Not Started
- **Goal**: Clean, fill, and aggregate.
- **Tasks**: Cleaning (Sentinels), Imputation (Interp/Ffill), Aggregation.
- **Outputs**: `p2_transformation_stats.json`, `p2_cleaning_report.md`.

### Phase 3: Exploratory Data Analysis (EDA)
**Status**: Not Started
- **Goal**: Analyze series behavior.
- **Tasks**: Visual analysis, Seasonality check, Outlier detection.
- **Outputs**: `p3_eda_metrics.json`, `p3_eda_report.md`.

### Phase 4: Feature Engineering
**Status**: Not Started
- **Goal**: Create predictors.
- **Tasks**: Lags, Rolling windows, Categorical encoding.
- **Outputs**: `p4_feature_stats.json`, `p4_feature_report.md`.

### Phase 5: Training & Modeling (Tournament)
**Status**: Not Started
- **Goal**: Algorithm competition.
- **Tasks**: Train `ForecasterDirect` candidates.
- **Outputs**: `p5_tournament_metrics.json`, `p5_modeling_report.md`.

### Phase 6: Model Selection & Tuning
**Status**: Not Started
- **Goal**: Optimize winner.
- **Tasks**: Hyperparameter tuning.
- **Outputs**: `p6_tuning_metrics.json`, `p6_selection_report.md`.

### Phase 7: Inference
**Status**: Not Started
- **Goal**: Future predictions ($X+1, X+2, X+3$).
- **Tasks**: Retrain and Predict.
- **Outputs**: `p7_forecast_metadata.json`, `p7_inference_report.md`.

### Phase 8: Production Deployment
**Status**: Not Started
- **Goal**: Pipeline automation.
- **Tasks**: Orchestration and Documentation.
- **Outputs**: `p8_pipeline_status.json`, `p8_deployment_report.md`.
