import os
from rich import print
from rich.markup import escape

from codefox.api.base_api import BaseAPI
from codefox.cli.base_cli import BaseCLI


class Index(BaseCLI):
    def __init__(self, model: type[BaseAPI]):
        self.model = model()

    def execute(self):
        is_upload, error = self.model.upload_files(os.getcwd())
        if not is_upload:
            print(
                "[red]Failed to index files: "
                + escape(str(error))
                + "[/red]"
            )
            return
        
        print(
            "[green]Successful to index files[/green]"
        )
