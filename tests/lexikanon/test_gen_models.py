from lexikanon.tokenizers import NLTKTagger, MecabTagger, Tokenizer


def test_gen_model_configs():
    print(NLTKTagger.generate_config())
    print(MecabTagger.generate_config())
    print(Tokenizer.generate_config())


if __name__ == "__main__":
    test_gen_model_configs()
