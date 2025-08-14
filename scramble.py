import polars as pl
import random
import typer
from rich.console import Console
from rich.table import Table
from pathlib import Path

app = typer.Typer()
console = Console()

@app.command()
def scramble(
    input_csv: Path = typer.Argument(..., help="Path to the input CSV file"),
    output_csv: Path = typer.Option("scrambled_output.csv", help="Path to save the scrambled CSV"),
    show: bool = typer.Option(False, help="Show the scrambled DataFrame in the terminal"),
):
    if not input_csv.exists():
        console.print(f"[red]File not found:[/red] {input_csv}")
        raise typer.Exit(1)

    df = pl.read_csv(str(input_csv))
    df = df.sample(frac=1.0, with_replacement=False)
    columns = df.columns
    random.shuffle(columns)
    df = df.select(columns)
    df.write_csv(str(output_csv))
    console.print(f"[green]Scrambled CSV saved to:[/green] {output_csv}")

    if show:
        table = Table(show_header=True, header_style="bold magenta")
        for col in df.columns:
            table.add_column(col)
        for row in df.rows():
            table.add_row(*[str(cell) for cell in row])
        console.print(table)

if __name__ == "__main__":
    app()