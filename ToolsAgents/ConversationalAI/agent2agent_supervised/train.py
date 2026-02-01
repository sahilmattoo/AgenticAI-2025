import argparse
from datasets import load_dataset
from transformers import (
    DataCollatorForSeq2Seq,
    TrainingArguments,
    Trainer
)
from agent2agent_model import load_model_and_tokenizer


def tokenize_function(examples, tokenizer, max_input_length=256, max_target_length=128):
    inputs = examples["input"]
    targets = examples["target"]
    model_inputs = tokenizer(
        inputs,
        max_length=max_input_length,
        truncation=True,
        padding="max_length"
    )
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(
            targets,
            max_length=max_target_length,
            truncation=True,
            padding="max_length"
        )
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True, help="JSONL file with input/target pairs")
    parser.add_argument("--model", default="t5-small")
    parser.add_argument("--output_dir", default="./agent2agent-model")
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch_size", type=int, default=8)
    args = parser.parse_args()

    model, tokenizer = load_model_and_tokenizer(args.model)

    raw_datasets = load_dataset("json", data_files={"train": args.data})
    tokenized = raw_datasets["train"].map(
        lambda ex: tokenize_function(ex, tokenizer),
        batched=True,
        remove_columns=["input", "target"],
    )

    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

    training_args = TrainingArguments(
        output_dir=args.output_dir,
        per_device_train_batch_size=args.batch_size,
        num_train_epochs=args.epochs,
        logging_steps=10,
        save_strategy="epoch",
        fp16=False,
        push_to_hub=False,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized,
        tokenizer=tokenizer,
        data_collator=data_collator,
    )

    trainer.train()
    trainer.save_model(args.output_dir)


if __name__ == "__main__":
    main()
