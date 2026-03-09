#!/usr/bin/env python3
import typer

from codefox.cli_manager import CLIManager


app = typer.Typer()

@app.command()
def scan(
    sourceBranch: str = typer.Option(None, help="Source branch"),
    targetBranch: str = typer.Option(None, help="Target branch"),
):
    """Run AI code review."""
    manager = CLIManager(
        command="scan",
        args={
            "sourceBranch": sourceBranch,
            "targetBranch": targetBranch
        }
    )
    manager.run()

@app.command()
def init():
    """Initialize CodeFox."""
    CLIManager(command="init", args={}).run()

@app.command()
def list():
    """List available models."""
    CLIManager(command="list", args={}).run()

@app.command()
def version():
    """Show version."""
    CLIManager(command="version", args={}).run()

def cli():
    app()

if __name__ == "__main__":
    cli()