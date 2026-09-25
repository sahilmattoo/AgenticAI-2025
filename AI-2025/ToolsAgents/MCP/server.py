from pathlib import Path
import hashlib
import shutil

from mcp.server import MCPServer


mcp = MCPServer("Local File Organizer")

BASE_DIR = Path(__file__).parent.resolve()
DEMO_DIR = (BASE_DIR / "demo_files").resolve()


def safe_path(relative_path: str) -> Path:
    """
    Resolve a path and ensure the MCP tool cannot escape demo_files/.
    """
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
    """List all files inside demo_files, including files in subfolders."""

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
    """Return basic metadata for one file."""

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
    """Find exact duplicate files by comparing SHA-256 hashes."""

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
    """Create a folder inside demo_files."""

    folder = safe_path(folder_name)
    folder.mkdir(parents=True, exist_ok=True)

    return f"Created folder: {folder.relative_to(DEMO_DIR)}"


@mcp.tool()
def move_file(relative_path: str, destination_folder: str) -> str:
    """Move a file into a folder inside demo_files. No files are deleted."""

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
