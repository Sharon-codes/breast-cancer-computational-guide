# Data provenance and interpretation

## Diagnostic data

Source: Breast Cancer Wisconsin (Diagnostic), UCI Machine Learning Repository. UCI lists the dataset attribution as Wolberg W, Mangasarian O, Street N, and Street W (1993). DOI: https://doi.org/10.24432/C5DW2B.

Dataset page: https://archive.ics.uci.edu/dataset/17/breast%2Bcancer%2Bwisconsin%2Bdiagnostic

UCI identifies the dataset license as Creative Commons Attribution 4.0 (CC BY 4.0). This project accesses the copy bundled with scikit-learn and exports derived split assignments, labels, predictions, and numerical model parameters. It does not redistribute the full feature matrix. We recode the loader's target from malignant=0 and benign=1 to malignant=1 and benign=0. The project is not endorsed by the dataset contributors.

The 569 records have 30 numeric nuclear features computed from digitized fine needle aspirate images of breast masses. They are diagnostic case data. Stage, population screening eligibility, longitudinal outcomes, and demographic subgroup columns are absent from the bundled feature matrix. Original identifiers are omitted by the loader. A random stratified row split does not independently verify patient grouping.

Loader: https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_breast_cancer.html

Preprocessing and leakage guidance: https://scikit-learn.org/stable/common_pitfalls.html

Calibration guidance: https://scikit-learn.org/stable/modules/calibration.html

Wilson intervals: NIST/SEMATECH e-Handbook of Statistical Methods, section 7.2.4.1, https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm

The array hash, package versions, fixed seed, threshold, split assignments, CV outputs, and fitted parameters are stored in `results/`.

## Hypothetical inputs

The screening exercise assumes sensitivity 0.90 and specificity 0.95 at several chosen prevalence values in a mathematical population of 100,000. These inputs are invented for teaching, not taken from a breast screening study or from the classifier's heldout performance.

The prioritization exercise uses randomly constructed, unitless feature scores and Dirichlet weight draws. No peptide or nucleotide sequences are present. Labels such as expression support are illustrative dimensions, not assay results or calibrated probabilities. No model is trained to generate antigen sequences, and no prediction is tested against biological ground truth.

## Clinical and computational reading

- NCI breast cancer symptoms: https://www.cancer.gov/types/breast/symptoms
- NCI screening: https://www.cancer.gov/types/breast/screening
- Gommers et al., MASAI primary outcome report (2026): https://pubmed.ncbi.nlm.nih.gov/41620232/
- Wells et al., neoantigen prediction and patient-matched testing (2020): https://pubmed.ncbi.nlm.nih.gov/33038342/
- Sahin et al., individualized mRNA vaccination in 14 assessed patients with TNBC (2026): https://pubmed.ncbi.nlm.nih.gov/41708868/
- FDA therapeutic cancer vaccine guidance: https://www.fda.gov/regulatory-information/search-fda-guidance-documents/clinical-considerations-therapeutic-cancer-vaccines

These sources inform interpretation; this code does not reproduce their clinical studies. The small vaccine study's immune-response observations do not establish causal improvement in recurrence or survival.
