from lexikanon.tokenizers import NLTKTagger, MecabTagger


def test_gen_model_configs():
    print(NLTKTagger.generate_config())
    print(MecabTagger.generate_config())


if __name__ == "__main__":
    test_gen_model_configs()
