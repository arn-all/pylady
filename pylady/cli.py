import click
from os.path import expanduser
import json
from pathlib import Path

@click.group()
# @click.option('--debug/--no-debug', default=False)
def cli():
    # click.echo(f"Debug mode is {'on' if debug else 'off'}")
    pass

set_env_help = "Pre-run command (e.g. `module load openmpi`)"
run_milady_help = "Milady run command (e.g. `mpirun -np 2 /path/to/milady.exe`)"

@cli.command(help="Create a global milady_config.json config file.")
@click.option('--set-env-cmd', prompt=set_env_help, help=set_env_help)
@click.option('--run-milady-cmd', prompt=run_milady_help, help=run_milady_help)
@click.option('-f', '--force', is_flag=True, help="Override any existing config. file without asking.")
@click.option('--location', default="~/.config/milady_config.json", show_default=True, help="Full path of the config file. Has to be put in the default location eventually.")
def create_config(set_env_cmd, run_milady_cmd, force, location):
    config_location = expanduser(location)
    click.echo(f'Setting up configuration file at {config_location}')
    
    def save_config():
        with open(config_location, "w") as f:
                    json.dump({"set_env_cmd": set_env_cmd,
                                "run_milady_cmd": run_milady_cmd}, f, indent=2)
        click.echo(click.style("Saved config file.", bold=True))

    if force:
        save_config()
    else:
        try:
            with open(config_location, "r") as f:
                json.load(f)
        except:
            click.echo("No valid config exist at location.")
            save_config()
        else:
            if input(f'File exists in {config_location}. Override ? y/(n): ')=='y':    
                save_config()


@cli.command(help="Check the config file contains needed keys.")
@click.option('--location', 
                default="~/.config/milady_config.json", 
                show_default=True, 
                help="Full path of the config file. Has to be put in the default location to be found by the Python package.")
def check_config(location):
    click.echo("Check config file...")
    try:
        with open(expanduser(location), "r") as f:
            contents = json.load(f)
    except Exception as e:
        click.secho("Invalid file. \nError is:", bold=True)
        click.secho(e, fg="red")
    else:
        if isinstance(contents["set_env_cmd"], str) & isinstance(contents["run_milady_cmd"], str):
            click.secho(f"Config file seems valid: {contents}")
        else:
            click.secho(f"Config file doesn't have the necessary keys: {contents}", fg="bright_red")