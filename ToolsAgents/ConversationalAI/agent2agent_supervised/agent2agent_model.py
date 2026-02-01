from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


def load_model_and_tokenizer(model_name: str = "t5-small"):
    """Return (model, tokenizer) ready for training or inference."""
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return model, tokenizer
