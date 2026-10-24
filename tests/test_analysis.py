"""Meaningful checks on class coding, mathematical counts, and saved evaluation."""
import json
import unittest
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from run_analysis import expected_screening_counts, metrics, json_safe, wilson_interval


class AnalysisChecks(unittest.TestCase):
    def test_positive_class_is_malignant(self):
        ds = load_breast_cancer()
        self.assertEqual(ds.target_names[0], "malignant")
        self.assertEqual(int((ds.target == 0).sum()), 212)

    def test_confusion_matrix_orientation(self):
        m = metrics(np.array([1, 1, 0, 0, 0]), np.array([.9, .2, .7, .1, .3]))
        self.assertEqual((m["true_positives"], m["false_negatives"], m["false_positives"], m["true_negatives"]), (1, 1, 1, 2))
        self.assertAlmostEqual(m["sensitivity"], .5)
        self.assertAlmostEqual(m["specificity"], 2 / 3)

    def test_prevalence_counts_and_bayes(self):
        r = expected_screening_counts(.005, .9, .95)
        self.assertAlmostEqual(r["tp"], 450)
        self.assertAlmostEqual(r["fn"], 50)
        self.assertAlmostEqual(r["fp"], 4975)
        self.assertAlmostEqual(sum(r[x] for x in ["tp", "fn", "fp", "tn"]), 100000)
        self.assertAlmostEqual(r["ppv"], 450 / 5425)
        self.assertLess(r["ppv"], expected_screening_counts(.05, .9, .95)["ppv"])

    def test_invalid_probability(self):
        with self.assertRaises(ValueError):
            expected_screening_counts(1.2, .9, .95)

    def test_undefined_precision_is_null(self):
        m = metrics(np.array([1, 0]), np.array([.1, .1]))
        self.assertIsNone(json_safe(m)["positive_predictive_value"])

    def test_wilson_interval_with_no_observed_errors(self):
        interval = wilson_interval(90, 90)
        self.assertLess(interval["lower"], .97)
        self.assertGreater(interval["lower"], .95)
        self.assertAlmostEqual(interval["upper"], 1)
        self.assertIsNone(wilson_interval(0, 0)["lower"])

    def test_saved_split_and_prediction_consistency(self):
        out = Path(__file__).resolve().parents[1] / "results"
        data = json.loads((out / "analysis.json").read_text())
        split = pd.read_csv(out / "split_indices.csv")
        pred = pd.read_csv(out / "heldout_predictions.csv")
        self.assertEqual(split.row_index.nunique(), 569)
        self.assertEqual(set(pred.row_index), set(split.loc[split.split == "test", "row_index"]))
        actual = metrics(pred.malignant.to_numpy(), pred.probability_malignant.to_numpy())
        for key, value in actual.items():
            self.assertAlmostEqual(value, data["diagnostic"]["model"][key], places=12)
        rel = pd.read_csv(out / "reliability_bins.csv")
        self.assertEqual(int(rel.n.sum()), len(pred))
        fit = json.loads((out / "fitted_parameters.json").read_text())
        X = load_breast_cancer().data[pred.row_index.to_numpy()]
        z = (X - np.array(fit["scaler_mean"])) / np.array(fit["scaler_scale"])
        p = 1 / (1 + np.exp(-(z @ np.array(fit["coefficients"]) + fit["intercept"])))
        np.testing.assert_allclose(p, pred.probability_malignant.to_numpy(), atol=1e-12)


if __name__ == "__main__":
    unittest.main()
