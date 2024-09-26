import pytest

from keras_hub.src.models.electra.electra_tokenizer import ElectraTokenizer
from keras_hub.src.tests.test_case import TestCase


class ElectraTokenizerTest(TestCase):
    def setUp(self):
        self.vocab = ["[PAD]", "[UNK]", "[CLS]", "[SEP]", "[MASK]"]
        self.vocab += ["THE", "QUICK", "BROWN", "FOX"]
        self.vocab += ["the", "quick", "brown", "fox"]
        self.init_kwargs = {"vocabulary": self.vocab}
        self.input_data = ["THE QUICK BROWN FOX", "THE FOX"]

    def test_tokenizer_basics(self):
        self.run_preprocessing_layer_test(
            cls=ElectraTokenizer,
            init_kwargs=self.init_kwargs,
            input_data=self.input_data,
            expected_output=[[5, 6, 7, 8], [5, 8]],
        )

    def test_lowercase(self):
        tokenizer = ElectraTokenizer(vocabulary=self.vocab, lowercase=True)
        output = tokenizer(self.input_data)
        self.assertAllEqual(output, [[9, 10, 11, 12], [9, 12]])

    def test_tokenizer_special_tokens(self):
        input_data = ["[CLS] THE [MASK] FOX [SEP] [PAD]"]
        tokenizer = ElectraTokenizer(
            **self.init_kwargs, special_tokens_in_strings=True
        )
        output_data = tokenizer(input_data)
        expected_output = [[2, 5, 4, 8, 3, 0]]

        self.assertAllEqual(output_data, expected_output)

    def test_errors_missing_special_tokens(self):
        with self.assertRaises(ValueError):
            ElectraTokenizer(vocabulary=["a", "b", "c"])

    @pytest.mark.large
    def test_smallest_preset(self):
        self.run_preset_test(
            cls=ElectraTokenizer,
            preset="electra_small_discriminator_uncased_en",
            input_data=["the quick brown fox."],
            expected_output=[[1996, 4248, 2829, 4419, 1012]],
        )

    @pytest.mark.extra_large
    def test_all_presets(self):
        for preset in ElectraTokenizer.presets:
            self.run_preset_test(
                cls=ElectraTokenizer,
                preset=preset,
                input_data=self.input_data,
            )
