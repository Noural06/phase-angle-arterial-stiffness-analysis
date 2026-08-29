# Data availability

The analysis used a 2023–24 Middlesex University teaching dataset containing
pseudonymous participant codes and sensitive physiological and demographic
measurements. Participant-level records are intentionally not redistributed in
this repository.

To run the pipeline, place an authorised local copy at `data/raw/input.xlsx`.
The raw-data directory is excluded from Git. The script reads only four fields:
participant code, age, phase angle, and heart-rate-standardised augmentation
index (AIx@75).

The repository publishes aggregate results only. This demonstrates responsible
data handling while preserving the analytical workflow.

