import os
import hashlib
import argparse
from rich.console import Console
from rich.table import Table
from rich import box
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
import psutil

console = Console()


def file_hash(filepath, chunk_size=4096):
    """Calculate SHA256 hash of a file."""
    hash_func = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(chunk_size):
                hash_func.update(chunk)
    except Exception as e:
        console.print(f"[red]Error reading {filepath}: {e}[/red]")
        return None
    return hash_func.hexdigest()


def get_file_hashes(folder, max_depth=None):
    """Get a dict of hashes to file paths with progress display."""
    file_hashes = {}

    # Collect files first to estimate progress
    all_files = []
    base_depth = folder.rstrip(os.sep).count(os.sep)

    for root, _, files in os.walk(folder):
        current_depth = root.count(os.sep) - base_depth
        if max_depth is not None and current_depth > max_depth:
            continue
        for name in files:
            full_path = os.path.join(root, name)
            all_files.append(full_path)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
        TimeElapsedColumn(),
        console=console
    ) as progress:
        task = progress.add_task(f"[green]Scanning {folder}...", total=len(all_files))

        for filepath in all_files:
            hash_value = file_hash(filepath)
            if hash_value:
                file_hashes.setdefault(hash_value, []).append(filepath)
            progress.update(task, advance=1)

    return file_hashes


def compare_folders(folder1, folder2, max_depth, show_unique = False):
    hashes1 = get_file_hashes(folder1, max_depth)
    hashes2 = get_file_hashes(folder2, max_depth)

    duplicates = []
    unique1 = []
    unique2 = []

    for h, paths1 in hashes1.items():
        if h in hashes2:
            for p1 in paths1:
                for p2 in hashes2[h]:
                    duplicates.append((p1, p2))
        else:
            unique1.extend(paths1)

    if show_unique:
        for h, paths2 in hashes2.items():
            if h not in hashes1:
                unique2.extend(paths2)

    return duplicates, unique1, unique2


def print_results(duplicates, unique1, unique2, show_unique = False):
    table = Table(title="Duplicate Files", box=box.HORIZONTALS, show_edge=True, show_lines=True, header_style="bold green")
    table.add_column("Folder 1", style="cyan")
    table.add_column("Folder 2", style="magenta")

    if duplicates:
        for p1, p2 in duplicates:
            table.add_row(p1, p2)
        console.print(table)
    else:
        console.print("[yellow]No duplicate files found.[/yellow]")

    if unique1 and show_unique:
        console.print("\n[bold red]Unique files in Folder 1:[/bold red]")
        for f in unique1:
            console.print(f"[red]- {f}[/red]")

    if unique2 and show_unique:
        console.print("\n[bold blue]Unique files in Folder 2:[/bold blue]")
        for f in unique2:
            console.print(f"[blue]- {f}[/blue]")


def main():
    parser = argparse.ArgumentParser(description="Find duplicate files between two folders.")
    parser.add_argument("folder1", help="First folder path")
    parser.add_argument("folder2", help="Second folder path")
    parser.add_argument("-l", "--max-depth", type=int, default=None,
                        help="Maximum directory depth to search (default: unlimited)")
    parser.add_argument('-u', '--unique', help = 'Show uniques', action = 'store_true')

    args = parser.parse_args()

    folder1 = os.path.abspath(args.folder1)
    folder2 = os.path.abspath(args.folder2)

    console.print(f"\n📁 Comparing: [cyan]{folder1}[/cyan] vs [magenta]{folder2}[/magenta]")
    if args.max_depth is not None:
        console.print(f"🔎 Max scan depth: [bold]{args.max_depth}[/bold]\n")

    duplicates, unique1, unique2 = compare_folders(folder1, folder2, args.max_depth, args.unique)
    print_results(duplicates, unique1, unique2, args.unique)


if __name__ == "__main__":
    main()
