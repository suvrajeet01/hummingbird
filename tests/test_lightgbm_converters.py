"""
Tests sklearn TruncatedSVD converter
"""
import unittest

import numpy as np
import torch
import lightgbm as lgb
from hummingbird import convert_sklearn
from hummingbird.common.data_types import Float32TensorType
from hummingbird.common.exceptions import WrongExtraConfig


class TestLGBMConverter(unittest.TestCase):

    def _run_lgbm_classifier_converter(self, num_classes, extra_config={}):
        for max_depth in [1, 3, 8, 10, 12, None]:
            model = lgb.LGBMClassifier(n_estimators=10, max_depth=max_depth)
            X = np.random.rand(100, 200)
            X = np.array(X, dtype=np.float32)
            y = np.random.randint(num_classes, size=100)

            model.fit(X, y)

            pytorch_model = convert_sklearn(
                model,
                [("input", Float32TensorType([1, 200]))],
                extra_config=extra_config
            )
            self.assertTrue(pytorch_model is not None)
            np.testing.assert_allclose(model.predict_proba(
                X), pytorch_model(torch.from_numpy(X))[1].data.numpy(), rtol=1e-06, atol=1e-06)

    # binary
    def test_lgbm_binary_classifier_converter(self):
        self._run_lgbm_classifier_converter(2)

    # multi
    def test_lgbm_multi_classifier_converter(self):
        self._run_lgbm_classifier_converter(3)

    # batch
    def test_lgbm_batch_classifier_converter(self):
        self._run_lgbm_classifier_converter(3, extra_config={"tree_implementation": "batch"})

    # beam
    def test_lgbm_beam_classifier_converter(self):
        self._run_lgbm_classifier_converter(3, extra_config={"tree_implementation": "beam"})

    # beam++
    def test_lgbm_beampp_classifier_converter(self):
        self._run_lgbm_classifier_converter(3, extra_config={"tree_implementation": "beam++"})

    # failure case
    def test_lgbm_fail_classifier_converter(self):
        self.assertRaises(
            WrongExtraConfig, self._run_lgbm_classifier_converter, 3, extra_config={"tree_implementation": "nonsense"})

    def _run_lgbm_regressor_converter(self, num_classes, extra_config={}):
        for max_depth in [1, 3, 8, 10, 12, None]:
            model = lgb.LGBMRegressor(n_estimators=10, max_depth=max_depth)
            X = np.random.rand(100, 200)
            X = np.array(X, dtype=np.float32)
            y = np.random.randint(num_classes, size=100)

            model.fit(X, y)
            pytorch_model = convert_sklearn(
                model,
                [("input", Float32TensorType([1, 200]))],
                extra_config=extra_config
            )
            self.assertTrue(pytorch_model is not None)
            np.testing.assert_allclose(model.predict(X), pytorch_model(
                torch.from_numpy(X)).numpy().flatten(), rtol=1e-06, atol=1e-06)

    # binary
    def test_lgbm_binary_regressor_converter(self):
        self._run_lgbm_regressor_converter(2)

    # multi
    def test_lgbm_multi_regressor_converter(self):
        self._run_lgbm_regressor_converter(3)

    # batch
    def test_lgbm_batch_regressor_converter(self):
        self._run_lgbm_regressor_converter(3, extra_config={"tree_implementation": "batch"})

    # beam
    def test_lgbm_beam_regressor_converter(self):
        self._run_lgbm_regressor_converter(3, extra_config={"tree_implementation": "beam"})

    # beam++
    def test_lgbm_beampp_regressor_converter(self):
        self._run_lgbm_regressor_converter(3, extra_config={"tree_implementation": "beam++"})

    # failure case
    def test_lgbm_fail_regressor_converter(self):
        self.assertRaises(
            WrongExtraConfig, self._run_lgbm_regressor_converter, 3, extra_config={"tree_implementation": "nonsense"})


if __name__ == "__main__":
    unittest.main()
