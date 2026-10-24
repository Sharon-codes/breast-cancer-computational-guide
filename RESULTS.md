# Executed teaching results

The committed run used seed 20261024 with 426 training cases and 143 heldout cases. Hyperparameters were selected using training data only. Malignant is the positive class, and the decision threshold was fixed at 0.5.

## Diagnostic case classifier

| Metric | Estimate | 95% interval |
| --- | ---: | ---: |
| Sensitivity | 90.57% | 79.75–95.90% |
| Specificity | 100.00% | 95.91–100.00% |
| Positive predictive value | 100.00% | 92.59–100.00% |
| Negative predictive value | 94.74% | 88.27–97.73% |
| Accuracy | 96.50% | 92.08–98.50% |
| ROC AUC | 0.9866 | 0.9663–0.9988 |
| Average precision | 0.9838 | 0.9601–0.9981 |
| Brier score | 0.0345 | 0.0126–0.0616 |

Proportions use Wilson intervals; the remaining intervals use 2,000 ordinary heldout case bootstrap samples. All intervals concern internal test-sample uncertainty and do not establish external performance.

Confusion counts: 48 true positives, 5 false negatives, 90 true negatives, and 0 false positives. Zero observed false positives does not establish perfect specificity. The 95% specificity interval is approximately 95.91–100%.

The training-prior baseline has ROC AUC 0.5. The selected regularization parameter C was 1.0. Its best training cross-validation AUC is a selection statistic and is not a separate holdout result.

These FNA breast-mass measurements cannot establish population screening benefit, early-stage sensitivity, demographic fairness, or fewer deaths.

## Hypothetical screening arithmetic

At assumed prevalence 0.5%, sensitivity 90%, specificity 95%, and population 100,000, expected counts are 450 true positives, 50 false negatives, 4,975 false positives, and 94,525 true negatives. The positive predictive value is 8.29%. None of these counts are observations from a screening programme.

## Fictional prioritization

Four different fictional candidates rank first under the 2,000 sampled weight vectors. This shows dependence on arbitrary scoring assumptions. It does not identify a vaccine, estimate efficacy, test immunogenicity, or validate a generative model.

## Verification

Seven unit tests check class coding, confusion counts, Bayes arithmetic, invalid inputs, undefined metrics, nondegenerate Wilson intervals, saved predictions, split assignments, bin counts, and reconstruction from fitted parameters. A second run in a separate output directory reproduced the scientific contents of all 9 numerical JSON and CSV files. Eight files matched byte for byte; the CV table matched exactly after excluding its four wall-clock timing columns. Plot-file bytes were not part of this numerical check.
