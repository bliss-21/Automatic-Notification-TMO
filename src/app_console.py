import typer
from rich.console import Console
from rich.table import Table
import os

from util import get_all_mangas

app = typer.Typer()
console = Console()

@app.command()
def show():
    mangas = get_all_mangas()
    os.system("cls")
    console.print("[bold magenta]Todos[/bold magenta]!", "💻")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=6)
    table.add_column("Todo", min_width=20)
    table.add_column("Ultimo Capitulo", min_width=12, justify="center")
    table.add_column("Done", min_width=12, justify="right")

    for idx, manga in enumerate(mangas, start=1):
        is_active_str = '✅' if manga.activo  else '❌'
        table.add_row(str(idx), manga.titulo_manga, f'{manga.ultimo_capitulo}', is_active_str)
    console.print(table)

if __name__ == "__main__":
    app()