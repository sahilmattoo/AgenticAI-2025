from pathlib import Path
import shutil


BASE_DIR = Path(__file__).parent
DEMO_DIR = BASE_DIR / "demo_files"

DEMO_DIR.mkdir(exist_ok=True)

files = {
    "Week5_Embeddings.txt":
        "Week 5 teaching material about embeddings, BOW, TF-IDF and Word2Vec.",

    "EmbeddingEvolution.txt":
        "Teaching deck notes for embedding evolution from BOW to Word2Vec.",

    "Customer.csv":
        "customer_id,income,spending\n1,60,70\n2,40,25\n",

    "invoice_aug.txt":
        "Invoice for August. Amount: 1250.",

    "notes.txt":
        "General notes from class preparation.",

    "installer.dmg":
        "This is only a fake installer file for the MCP demo.",
}


for filename, content in files.items():
    (DEMO_DIR / filename).write_text(content)


shutil.copy(
    DEMO_DIR / "Week5_Embeddings.txt",
    DEMO_DIR / "Week5_Embeddings_copy.txt",
)

shutil.copy(
    DEMO_DIR / "Customer.csv",
    DEMO_DIR / "Customer_backup.csv",
)

print(f"Demo files created in: {DEMO_DIR}")
