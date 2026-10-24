# Breast cancer computational guide

Educational companion for a beginner text on breast cancer early detection and personalized vaccine research.

The exercises teach evaluation and the limits of computational claims. They do not diagnose cancer, establish early-stage detection, manufacture a vaccine, or reproduce a published generative vaccine model.

## Run

Use Python 3.12. The committed run used Python 3.12 and the versions pinned in `requirements.txt`.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python run_analysis.py --bootstrap 2000
python -m unittest discover -s tests -v
```

On Windows, activate the virtual environment with `.venv\Scripts\activate`.
The dataset is bundled with scikit-learn; execution does not require patient records or an external data download.

## Exercises

1. **Diagnostic case classification.** Use 569 Wisconsin Diagnostic Breast Cancer records with 30 nuclear measurements from fine needle aspirates of breast masses. Malignant is the positive class. Freeze a stratified 25% row holdout before fitting. Select regularization using five training-only folds around a scaling and logistic regression pipeline. Evaluate once at the prespecified probability threshold of 0.5. Compare with a training-prior baseline.
2. **Hypothetical screening arithmetic.** Hold assumed sensitivity and specificity fixed while changing assumed prevalence. The resulting positive predictive values are mathematical illustrations, not clinical estimates and not transported from the diagnostic classifier.
3. **Hypothetical prioritization.** Rank 12 fictional numeric candidate records under 2,000 arbitrary weight draws. The features and weights are invented teaching inputs. This is a heuristic sensitivity exercise with no sequences, patients, trained generative model, immunogenicity prediction, or biological validation. A fraction ranked first is not a probability of vaccine efficacy.

## Results and uncertainty

See [RESULTS.md](RESULTS.md) and [results/analysis.json](results/analysis.json). Saved outputs include split indices, heldout predictions, training selection results, fitted numerical parameters, reliability-bin counts, hypothetical counts, and fictional ranking results.

Proportion metrics use 95% Wilson intervals, including when no errors were observed. ROC AUC, average precision, and Brier score use 2,000 heldout case bootstrap samples. These intervals describe internal test-sample uncertainty conditional on the fitted model and split; they exclude full training uncertainty and external validity. The selected best cross-validation score is a model-selection statistic, not an unbiased performance estimate. Undefined metrics are JSON `null`, never zero.

## Scientific limits

- The Wisconsin data contain diagnostic breast-mass samples, not a population screening cohort, mammograms, or stage labels. Early-stage sensitivity and screening benefit cannot be measured here.
- The bundled copy omits original identifiers. This is a row/case split, not independently verified grouped patient separation.
- Demographic subgroup fairness is not assessable because the relevant columns are absent.
- Brier score is a probabilistic accuracy score; the small reliability plot is descriptive and does not establish calibrated clinical risk.
- No external clinical validation or mortality analysis was performed. Observing zero false positives in 90 benign cases does not establish perfect specificity.
- The candidate exercise cannot produce a patient-specific vaccine. Clinical translation requires evidence and oversight beyond computational ranking.

See [DATA_PROVENANCE.md](DATA_PROVENANCE.md) for sources and licensing. No license has been selected for the newly written code. Third-party data and software retain their own licenses.
