import click

from fix_imports.config import (config_parse, get_config_path,
                                update_pred_imports)
from fix_imports.file import get_file_text, write_to_file
from fix_imports.package import import_string
from fix_imports.pyflake import pyflake


@click.command()
@click.option(
    "-f", "--fix", is_flag=True, default=False, help="format the file in place"
)
@click.option(
    "-c",
    "--config-file",
    is_flag=False,
    type=click.Path(exists=True, dir_okay=False, readable=True),
    help="path of the config file",
)
@click.argument("filename")
def cli(filename: str, fix: bool, config_file) -> str | None:
    if config_file:
        data = config_parse(config_file)
        update_pred_imports(data)
    else:
        default_config_data = config_parse(get_config_path())
        update_pred_imports(default_config_data)

    output = get_file_text(filename)
    mod_list = pyflake(output)
    imports = import_string(mod_list)

    if not fix:
        if imports:
            click.echo(imports + 2 * "\n" + output, nl=True)
        else:
            click.echo(output, nl=True)
    else:
        if imports:
            write_to_file(filename, imports + 2 * "\n" + output)
            click.echo("Written to file successfully")
        else:
            click.echo("Nothing to do")
            pass

    return imports + "\n" + output + "\n"


if __name__ == "__main__":
    cli()
