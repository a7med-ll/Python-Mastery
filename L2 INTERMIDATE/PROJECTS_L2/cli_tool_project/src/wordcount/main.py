import typer

app = typer.Typer()

@app.command()
def count(filename: str):
    """Count words, lines and characters in file"""
    with open(filename, "r") as f:

        text = f.read()
        words = len(text.split())
        lines = len(text.splitlines())
        characters = len(text)

        typer.echo(f"Words: {words}")
        typer.echo(f"Lines: {lines}")
        typer.echo(f"Characters: {characters}")

if __name__ == "__main__":
    app()

