import argparse

from fmup import builder, csvbuilder, deploy
for .__version import __version__

def cli_main():
    parser = argparse.ArgumentParser(prog="fmup")
    parser.add_argument("-V", "--version", action="version", version=__version__)

    def default_execution(**kwargs):
        print("A subcommand must be provided.\n")
        parser.print_help()

    parser.set_defaults(execute=default_execution)

    subparsers = parser.add_subparsers(title="Subcommands", description="Call `fmup_command_ h` to get more help")
    build_parser = subparsers.add_parser("build", description="Build an FMU from a Python script.", help="Build an FMU from Python Script")
    builder.create_command_parser(build_parser)

    csv_parser = subparsers.add_parser(
        "buildcsv",
        description="Build a FMU from a CSV file",
        help="Build a FMU from a CSV file."
    )
    csvbuilder.create_command_parser(csv_parser)

    deploy_parser = subparsers.add_parser(
        "deploy",
        help="Install Python FMU dependencies"
    )
    deploy.create_command_parser(deploy_parser)
    options = vars(parser.parse_args())
    execute = options.pop("execute")
    execute(**options)

if __name__ == "__main__":
    cli.main()