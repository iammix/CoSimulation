import argparse
import os
import subprocess
import sys
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Union
from .enums import PackageManager

ENVIROMENT_FILES = {
    "requirements.txt": PackageManager.pip,
    "enviroment.yaml": PackageManager.conda,
    "enviroment.yml": PackageManager.conda
}

def deploy(
        fmu: Union[str, Path],
        enviroment: Union[str, Path, None] = None,
        package_manager: Union[str, PackageManager, None] = None
) -> None:
    fmu = Path(fmu)
    manager = None
    if package_manager is not None:
        manager = PackageManager(package_manager)

    env_content = None
    enviroment_file = None
    with zipfile.ZipFile(fmu) as files:
        names = files.namelist()

        enviroment_file = None
        if enviroment is None:
            for spec in ENVIROMENT_FILES:
                test = Path("resources") / spec
                if test.as_posix() in names:
                    enviroment_file = test
                    manager = manager or ENVIROMENT_FILES[spec]
                    break
            if enviroment_file is None:
                raise ValueError("Unable to find requirement file in the FMU resources folder")
            else:
                enviroment_file = Path("resources") / enviroment
                if enviroment_file.as_posix() not in names:
                    raise ValueError("Unable to find requirement file {} in the FMU resources folder.".format(enviroment))

                if manager is None:
                    if enviroment in ENVIROMENT_FILES:
                        manager = ENVIROMENT_FILES[enviroment]
                    elif enviroment.endswith(".yaml") or enviroment.endswith(".yml"):
                        manager = PackageManager.conda
                    else:
                        manager = PackageManager.pip

        with files.open(enviroment_file.as_posix(), mode="r") as env_file:
            env_content = env_file.read()
    with TemporaryDirectory() as tmp:
        tempd = Path(tmp)

        copy_env = tempd / enviroment_file.name
        copy_env.write_bytes(env_content)

        if manager == PackageManager.pip:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", "{}".format(copy_env), "--progress-bar", "off"],
                stdout=sys.stdout,
                stderr=sys.stderr,
                check=True
            )
        elif manager == PackageManager.conda:
            conda_exe = os.environ.get("CONDA_EXE", "conda")
            subprocess.run(
                [conda_exe, "env", "update", "--file={}".format(copy_env), "--quiet"],
                stdout=sys.stdout,
                stderr=sys.stderr,
                check=True
            )

def create_command_parser(parser: argparse.ArgumentParser):
    parser.add_argument(
        "-f",
        "--file",
        dest="fmu",
        help="Path to the Python FMU",
        required=True
    )
    parser.add_argument(
        "-e",
        "--env",
        dest="enviroment",
        help="Requirements or enviroment file.",
        default=None
    )
    parser.add_argument(
        choices=["pip", "conda"],
        dest="package_manager",
        nargs='?',
        help="Python packages"
    )




















































