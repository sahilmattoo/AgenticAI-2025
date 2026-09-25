# MCP File Organizer Demo

A small, safe demo to understand **what MCP actually gives an AI system** beyond a normal API call.

The project exposes local file operations as MCP tools. You can connect the server to VS Code, let the AI client discover the tools, and then ask it to inspect and reorganize a demo folder.

> **Core teaching idea**
>
> Python gives us capabilities.  
> MCP exposes those capabilities through a standard protocol.  
> The AI host discovers the tools and decides which ones to call.

---

## 1. What you will build

You will create a local MCP server with these tools:

- `list_files()` — inspect files in a demo folder
- `find_duplicates()` — find exact duplicate files using SHA-256
- `create_folder()` — create a folder
- `move_file()` — move a file into a folder
- `file_summary()` — return lightweight metadata about a file

For safety, this first version works only inside a local folder named:

```text
demo_files/
```

It does **not** delete anything.

---

## 2. What you should expect at the end

After setup, you should be able to ask the MCP-enabled AI client something like:

```text
Analyze the demo_files folder.

1. List all files.
2. Find exact duplicates.
3. Create a folder called Teaching.
4. Move files whose names contain Week5 or Embedding into Teaching.
5. Do not delete anything.
6. Tell me exactly what you changed.
```

The important part is that the AI should not just answer with instructions.

It should actually invoke MCP tools such as:

```text
list_files
find_duplicates
create_folder
move_file
```

and you should see the folder change on disk.

That is the "aha" moment of the demo.

---

# 3. Architecture

```text
You
 |
 | "Organize my teaching files"
 v
VS Code / AI Host
 |
 | MCP
 v
Local Python MCP Server
 |
 +-- list_files()
 +-- find_duplicates()
 +-- create_folder()
 +-- move_file()
 +-- file_summary()
 |
 v
demo_files/
```

The MCP server owns the capability.

The AI host decides which capability to invoke and in what sequence.

---

# 4. Prerequisites

You need:

- VS Code
- A working Python environment already available to the agent/project
- MCP support enabled in the AI client/host you want to use
- No custom virtual environment is required for this version

Use the existing environment in the current VS Code/agent session instead of creating a separate local `.venv`.

---

# 5. Create the project

Create a folder:

```bash
mkdir mcp-file-organizer
cd mcp-file-organizer
code .
```

Your final project will look like:

```text
mcp-file-organizer/
|
+-- server.py
+-- create_demo_files.py
+-- demo_files/
+-- .vscode/
|   +-- mcp.json
|
+-- README.md
```

---

# 6. Use the existing environment

Do not create a project-specific virtual environment for this demo.

Use the Python interpreter already available in the current VS Code agent environment.

Check the environment:

```bash
python --version
```

Upgrade pip in the active environment:

```bash
python -m pip install --upgrade pip
```

Install the official MCP Python SDK in that same environment:

```bash
python -m pip install "mcp[cli]"
```

This keeps the project aligned with the existing agent environment and avoids adding another custom venv.

---

# 7. Create `server.py`

Create a file named:

```text
server.py
```

Paste:

```python
from pathlib import Path
import hashlib
import shutil

from mcp.server import MCPServer


mcp = MCPServer("Local File Organizer")

BASE_DIR = Path(__file__).parent.resolve()
DEMO_DIR = (BASE_DIR / "demo_files").resolve()


def safe_path(relative_path: str) -> Path:
    '''
    Resolve a path and ensure the MCP tool cannot escape demo_files/.
    '''
    path = (DEMO_DIR / relative_path).resolve()

    if path != DEMO_DIR and DEMO_DIR not in path.parents:
        raise ValueError("Access outside demo_files is not allowed.")

    return path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as file:
        while chunk := file.read(8192):
            digest.update(chunk)

    return digest.hexdigest()


@mcp.tool()
def list_files() -> list[dict]:
    '''List all files inside demo_files, including files in subfolders.'''

    DEMO_DIR.mkdir(exist_ok=True)

    files = []

    for path in sorted(DEMO_DIR.rglob("*")):
        if path.is_file():
            files.append(
                {
                    "name": path.name,
                    "relative_path": str(path.relative_to(DEMO_DIR)),
                    "extension": path.suffix,
                    "size_bytes": path.stat().st_size,
                }
            )

    return files


@mcp.tool()
def file_summary(relative_path: str) -> dict:
    '''Return basic metadata for one file.'''

    path = safe_path(relative_path)

    if not path.exists() or not path.is_file():
        raise FileNotFoundError(relative_path)

    return {
        "name": path.name,
        "relative_path": str(path.relative_to(DEMO_DIR)),
        "extension": path.suffix,
        "size_bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


@mcp.tool()
def find_duplicates() -> list[dict]:
    '''Find exact duplicate files by comparing SHA-256 hashes.'''

    DEMO_DIR.mkdir(exist_ok=True)

    seen = {}
    duplicates = []

    for path in sorted(DEMO_DIR.rglob("*")):
        if not path.is_file():
            continue

        digest = sha256(path)
        rel = str(path.relative_to(DEMO_DIR))

        if digest in seen:
            duplicates.append(
                {
                    "original": seen[digest],
                    "duplicate": rel,
                    "sha256": digest,
                }
            )
        else:
            seen[digest] = rel

    return duplicates


@mcp.tool()
def create_folder(folder_name: str) -> str:
    '''Create a folder inside demo_files.'''

    folder = safe_path(folder_name)
    folder.mkdir(parents=True, exist_ok=True)

    return f"Created folder: {folder.relative_to(DEMO_DIR)}"


@mcp.tool()
def move_file(relative_path: str, destination_folder: str) -> str:
    '''Move a file into a folder inside demo_files. No files are deleted.'''

    source = safe_path(relative_path)
    destination_dir = safe_path(destination_folder)

    if not source.exists() or not source.is_file():
        raise FileNotFoundError(relative_path)

    destination_dir.mkdir(parents=True, exist_ok=True)

    destination = destination_dir / source.name

    if destination.exists():
        raise FileExistsError(
            f"Destination already exists: {destination.relative_to(DEMO_DIR)}"
        )

    shutil.move(str(source), str(destination))

    return (
        f"Moved {source.relative_to(DEMO_DIR)} "
        f"to {destination.relative_to(DEMO_DIR)}"
    )


if __name__ == "__main__":
    mcp.run()
```

---

# 8. Create demo files automatically

Create:

```text
create_demo_files.py
```

Paste:

```python
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


# Create exact duplicates deliberately
shutil.copy(
    DEMO_DIR / "Week5_Embeddings.txt",
    DEMO_DIR / "Week5_Embeddings_copy.txt",
)

shutil.copy(
    DEMO_DIR / "Customer.csv",
    DEMO_DIR / "Customer_backup.csv",
)

print(f"Demo files created in: {DEMO_DIR}")
```

Run:

```bash
python create_demo_files.py
```

Expected folder:

```text
demo_files/
|
+-- Week5_Embeddings.txt
+-- Week5_Embeddings_copy.txt
+-- EmbeddingEvolution.txt
+-- Customer.csv
+-- Customer_backup.csv
+-- invoice_aug.txt
+-- notes.txt
+-- installer.dmg
```

Two duplicate pairs deliberately exist:

```text
Week5_Embeddings.txt
Week5_Embeddings_copy.txt
```

and

```text
Customer.csv
Customer_backup.csv
```

---

# 9. Test the MCP server before involving an LLM

The MCP SDK includes development tooling.

Run:

```bash
mcp dev server.py
```

or, if needed:

```bash
python -m mcp dev server.py
```

The MCP development/inspection experience should let you inspect the server and verify that tools are being exposed.

You should see tools corresponding to:

```text
list_files
file_summary
find_duplicates
create_folder
move_file
```

Try `list_files`.

Then try `find_duplicates`.

Expected duplicate result conceptually:

```text
[
  {
    "original": "Customer.csv",
    "duplicate": "Customer_backup.csv"
  },
  {
    "original": "Week5_Embeddings.txt",
    "duplicate": "Week5_Embeddings_copy.txt"
  }
]
```

The ordering may differ.

---

# 10. Connect the MCP server to VS Code

VS Code supports local MCP servers over `stdio`.

Create:

```text
.vscode/mcp.json
```

Example configuration:

```json
{
  "servers": {
    "file-organizer": {
      "type": "stdio",
      "command": "python",
      "args": [
        "${workspaceFolder}/server.py"
      ]
    }
  }
}
```

For Windows, use the same approach with the active environment:

```json
{
  "servers": {
    "file-organizer": {
      "type": "stdio",
      "command": "python",
      "args": [
        "${workspaceFolder}\\server.py"
      ]
    }
  }
}
```

Restart/reload the MCP server from VS Code if required.

> Important:
>
> With `stdio`, VS Code launches `server.py` as a subprocess.
> You do not normally start `python server.py` in another terminal for the VS Code connection.

---

# 11. First MCP prompt

Start simple.

Ask:

```text
What tools are available from the file-organizer MCP server?
```

You want to see that the host knows about tools such as:

```text
list_files
file_summary
find_duplicates
create_folder
move_file
```

This demonstrates **tool discovery**.

---

# 12. Second prompt: READ only

Ask:

```text
Use the file-organizer MCP tools.

List the files in demo_files and find exact duplicates.

Do not move or modify anything.
```

Expected behavior:

```text
AI
 |
 +--> list_files()
 |
 +--> find_duplicates()
 |
 +--> explains findings
```

Nothing on disk should change.

---

# 13. Third prompt: take an ACTION

Now ask:

```text
Use the file-organizer MCP tools.

Create a folder called Teaching.

Move files whose filenames clearly relate to Week 5 or Embeddings
into Teaching.

Do not delete anything.

After completing the task, tell me exactly which MCP tools you used
and what changed.
```

Expected result:

```text
demo_files/
|
+-- Teaching/
|   +-- Week5_Embeddings.txt
|   +-- Week5_Embeddings_copy.txt
|   +-- EmbeddingEvolution.txt
|
+-- Customer.csv
+-- Customer_backup.csv
+-- invoice_aug.txt
+-- notes.txt
+-- installer.dmg
```

The AI should have performed something conceptually similar to:

```text
list_files()
     |
     v
reason about filenames
     |
     v
create_folder("Teaching")
     |
     v
move_file(...)
move_file(...)
move_file(...)
```

This is the key classroom moment:

> The model did not contain Python code for your filesystem.
>
> Your MCP server advertised capabilities.
>
> The AI host discovered those capabilities and selected them to accomplish the goal.

---

# 14. The question students will ask

## "Couldn't we do this with an API?"

Yes.

That is an important point, not a weakness in the demo.

You could write:

```python
requests.post("/move-file", ...)
```

or expose Python functions directly through an LLM function-calling framework.

But then your application owns a custom integration.

MCP standardizes how an AI host can discover and invoke capabilities.

Think of the distinction as:

```text
API
    Software <----> Software

Function Calling
    LLM ----> Functions wired into this application

MCP
    AI Host ---- standard protocol ----> Capability Server
```

The value becomes more obvious when the **same MCP server** is connected to another compatible host without rewriting the file-management functions.

---

# 15. Why action makes the demo stronger

If the MCP server only exposes:

```text
search_files()
```

students may reasonably ask:

> "Why not just use an API?"

Instead this demo provides:

```text
Observe
   |
   +-- list_files
   +-- find_duplicates

Reason
   |
   +-- LLM decides what belongs together

Act
   |
   +-- create_folder
   +-- move_file
```

So the flow becomes:

```text
Observe -> Reason -> Act
```

This feels much closer to an agentic system.

---

# 16. Human-in-the-loop extension

Do NOT add deletion immediately.

Instead discuss why:

```text
list_files      -> low risk
find_duplicates -> low risk
create_folder   -> moderate change
move_file       -> moderate change
delete_file     -> destructive
```

A later version can implement:

```text
propose_deletion()
```

and require user confirmation before a real delete operation.

That becomes a natural lesson on:

- permissions
- guardrails
- approval
- reversible vs irreversible actions

---

# 17. Semantic similarity extension

Exact duplicate detection uses SHA-256.

That only detects identical bytes.

Next, add:

```text
find_similar_files()
```

Possible evolution:

```text
Filename similarity
        |
        v
TF-IDF similarity
        |
        v
Embedding similarity
```

For example:

```text
EmbeddingEvolution.txt
Week5_Embeddings.txt
Word2Vec_Notes.txt
```

may be conceptually related even though they are not duplicates.

That gives a very nice bridge from:

```text
NLP / Embeddings
```

to:

```text
Agentic AI / MCP tools
```

---

# 18. Eventually point it at Downloads

Only after the safe demo works.

Current code uses:

```python
DEMO_DIR = (BASE_DIR / "demo_files").resolve()
```

Later you could change it to:

```python
DEMO_DIR = (Path.home() / "Downloads").resolve()
```

But for classroom demos, using a controlled demo folder is strongly recommended.

You do not want accidental movement of genuine personal files while teaching.

---

# 19. What happens if you simply run `python server.py`?

With a `stdio` MCP server, this can look strange.

Run:

```bash
python server.py
```

and the process may appear to sit there doing nothing.

That is expected.

A `stdio` MCP server waits for an MCP host/client to communicate with it through standard input/output.

So:

```text
python server.py
```

does NOT mean:

```text
open a website
print a menu
start a chatbot
```

It means:

```text
MCP server is waiting for an MCP client
```

Normally VS Code launches the server for you from `mcp.json`.

---

# 20. Classroom story

A useful way to present the demo:

### Stage 1 — Python

```text
I can write functions that manipulate files.
```

### Stage 2 — MCP

```text
I expose those functions as standardized AI tools.
```

### Stage 3 — Tool discovery

```text
The host discovers what the server can do.
```

### Stage 4 — Agent reasoning

```text
The model decides which tools it needs.
```

### Stage 5 — Action

```text
The model invokes the tools and changes the environment.
```

And the takeaway:

> **MCP does not make the LLM smarter.**
>
> **MCP gives AI applications a standardized way to discover and use external capabilities.**

---

# 21. Success checklist

You have completed the first version when all of these work:

- [ ] `pip install "mcp[cli]"` succeeds
- [ ] `python create_demo_files.py` creates sample files
- [ ] MCP development tooling sees the server
- [ ] `list_files()` works
- [ ] `find_duplicates()` finds both duplicate pairs
- [ ] VS Code sees the MCP server
- [ ] VS Code discovers the five tools
- [ ] AI can call `list_files`
- [ ] AI can call `find_duplicates`
- [ ] AI creates `Teaching/`
- [ ] AI moves relevant files into `Teaching/`
- [ ] no file is deleted

If all of these work, the basic MCP demo is complete.

---

# 22. Next version

Once Version 1 works, extend the project in this order:

```text
V1
Local files + deterministic tools
        |
        v
V2
Semantic similarity with embeddings
        |
        v
V3
Human approval before destructive actions
        |
        v
V4
Resources + prompts in addition to tools
        |
        v
V5
Expose the MCP server over Streamable HTTP
        |
        v
V6
Connect the same MCP capability to another AI host
```

That progression demonstrates the real benefit of MCP much better than starting with a complicated remote deployment.
