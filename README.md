# Phase Angle and Arterial Stiffness in Young Adults

A reproducibility-focused analysis of the relationship between bioelectrical
impedance phase angle and heart-rate-standardised augmentation index (AIx@75),
completed in 2025 as a BSc Medical Physiology research project at Middlesex University.

## Project question

Is a higher phase angle—an indicator associated with cellular integrity—related
to lower AIx@75, a marker of arterial wave reflection, in young adults?

## Skills demonstrated

- Cleaning and validating physiological data
- Descriptive statistics and quality checks
- Pearson correlation and simple linear regression
- Sensitivity and reproducibility analysis
- Translating a biomedical question into a clear analytical workflow
- Responsible handling of sensitive human-participant data

## Reported findings

The dissertation reported an analytical sample of 100 participants aged 18–30:

| Measure | Result |
|---|---:|
| Mean phase angle | 6.05° (SD 0.98) |
| Mean AIx@75 | 6.97% (SD 11.36) |
| Pearson correlation | r = -0.228, p = 0.022 |
| Regression slope | -2.64 percentage points per degree |
| Explained variance | R² = 0.052 |

The association was small and inverse. It supports further investigation but
does not establish causality or justify using phase angle as a standalone
clinical screening test.

## Reproducibility audit

The supplied 2023–24 master workbook contains 212 complete records meeting the
documented age criterion. The dissertation reports 100 records, but the final
100-row selection is not encoded in the workbook or fully documented in the
report. Running the stated age and complete-case filter on the master workbook
therefore does not reproduce the exact dissertation summary.

This repository preserves that distinction:

- `results/reported_results.csv` contains the dissertation's reported values.
- `results/reproducibility_audit.csv` compares them with the auditable master-
  workbook filter.
- `src/analyse.py` provides a reusable, privacy-conscious analysis pipeline.
- Participant-level data are not published.

## Run locally

With an authorised copy of the workbook:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/analyse.py data/raw/input.xlsx
```

The script produces aggregate JSON and a scatter plot in `results/local_run/`.
It does not export participant-level rows.

## Data governance

The source is a shared university teaching dataset with pseudonymous codes and
sensitive physiological and demographic measurements. It is not redistributed.
See `data/README.md`.

## Limitations

- Cross-sectional analysis cannot demonstrate causality.
- The reported model explains only a small proportion of AIx@75 variation.
- The sampling frame and undocumented final-row selection limit reproducibility.
- AIx@75 is influenced by factors beyond arterial stiffness.
- Findings from a student sample should not be generalised clinically without
  larger, prospectively designed studies.

## Author

Noura Lakrimdi — MSc Data Science student with a First-Class BSc in Medical
Physiology.
