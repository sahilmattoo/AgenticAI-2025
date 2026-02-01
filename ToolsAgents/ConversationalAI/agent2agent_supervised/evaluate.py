from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from datasets import load_dataset
import evaluate


def evaluate_model(model_dir: str, data_file: str, max_input_length=256, max_target_length=128):
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_dir)

    ds = load_dataset("json", data_files={"test": data_file})["test"]

    gen = model.generate
    rouge = evaluate.load("rouge")
    bleu = evaluate.load("bleu")

    hyps = []
    refs = []
    for ex in ds:
        inp = ex["input"]
        tgt = ex["target"]
        inputs = tokenizer(inp, return_tensors="pt", truncation=True, max_length=max_input_length)
        out = model.generate(**inputs, max_new_tokens=128)
        pred = tokenizer.decode(out[0], skip_special_tokens=True)
        hyps.append(pred)
        refs.append(tgt)

    r = rouge.compute(predictions=hyps, references=refs)
    b = bleu.compute(predictions=hyps, references=[[r] for r in refs])
    print("ROUGE:", r)
    print("BLEU:", b)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python evaluate.py <model_dir> <test.jsonl>")
        sys.exit(1)
    evaluate_model(sys.argv[1], sys.argv[2])
