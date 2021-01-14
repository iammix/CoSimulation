# FMU Generator from Python code

> A lightweight framework that enables the packaging of Python 3 code or CSV files as co-simulation FMUs (following FMI version 2.0).

## 01.How do I build an FMU from python code?

1. Create a new class extending the `Fmi2Slave` class declared in the `fmup.fmi2slave` module (see below for an example).
2. Run `fmup build` in your terminal to create the fmu.

```bash
usage: fmup build [-h] -f SCRIPT_FILE [-d DEST] [--doc DOCUMENTATION_FOLDER] [--no-external-tool]
                       [--no-variable-step] [--interpolate-inputs] [--only-one-per-process] [--handle-state]
                       [--serialize-state] [--use-memory-management]
                       [Project files [Project files ...]]
```
Build an FMU from a Python script.
```bash
positional arguments:
  Project files         Additional project files required by the Python script.

optional arguments:
  -h, --help            show this help message and exit
  -f SCRIPT_FILE, --file SCRIPT_FILE
                        Path to the Python script.
  -d DEST, --dest DEST  Where to save the FMU.
  --doc DOCUMENTATION_FOLDER
                        Documentation folder to include in the FMU.
  --no-external-tool    If given, needsExecutionTool=false
  --no-variable-step    If given, canHandleVariableCommunicationStepSize=false
  --interpolate-inputs  If given, canInterpolateInputs=true
  --only-one-per-process
                        If given, canBeInstantiatedOnlyOncePerProcess=true
  --handle-state        If given, canGetAndSetFMUstate=true
  --serialize-state     If given, canSerializeFMUstate=true
  --use-memory-management
                        If given, canNotUseMemoryManagementFunctions=false
```

## 02.How do I build an FMU from python code with third-party dependencies?

Often, Python scripts depends on non-builtin libraries like `numpy`, `scipy`, etc.
`fmup` does not package a full environment within the FMU.
However you can package a `requirements.txt` or `environment.yml` file within your FMU following these steps:

1. Create a new class extending the `Fmi2Slave` class declared in the `fmup.fmi2slave` module (see below for an example).
2. Create a `requirements.txt` file (to use _pip_ manager) and/or a `environment.yml` file (to use _conda_ manager) that defines your dependencies.
3. Run `fmup build -f myscript.py requirements.txt` to create the fmu including the dependencies file.

And using `fmup deploy`, end users will be able to update their local Python environment. The steps to achieve that:


1. Be sure to be in the Python environment to be updated. Then execute `fmup deploy -f my.fmu`

```bash
usage: fmup deploy [-h] -f FMU [-e ENVIRONMENT] [{pip,conda}]

Deploy a Python FMU. The command will look in the `resources` folder for one of the following files:
`requirements.txt` or `environment.yml`. If you specify a environment file but no package manager, `conda` will be selected for `.yaml` and `.yml` otherwise `pip` will be used. The tool assume the Python environment in which the FMU should be executed is the current one.

positional arguments:
  {pip,conda}           Python packages manager

optional arguments:
  -h, --help            show this help message and exit
  -f FMU, --file FMU    Path to the Python FMU.
  -e ENVIRONMENT, --env ENVIRONMENT
                        Requirements or environment file.
```

---
## 03.Create the FMU

```bash
fmup build -f pythonslave.py myproject
```

In this example a python class named `PythonSlave` that extends `Fmi2Slave` is declared in a file named `pythonslave.py`,
where `myproject` is an optional folder containing additional project files required by the python script.
Project folders such as this will be recursively copied into the FMU. Multiple project files/folders may be added.

### 04.Note

fmup does not bundle Python, which makes it a tool coupling solution.
This means that you can not expect the generated FMU to work on a different system (The system would need a compatible Python version and libraries).
But to ease its usage the wrapper uses the limited Python API, making the pre-built binaries for Linux and Windows 64-bits
compatible with any Python 3 environment. If you need to compile the wrapper for a specific configuration,
you will need CMake and a C++ compiler.
fmup does not automatically resolve 3rd party dependencies. If your code includes e.g. `numpy`, the target system also needs to have `numpy` installed.

---

### COMMIT SPECIFICATIONS
To push a commit to the current repository please use the following commit name tag  
**Ch dd/mm/yyyy hh:mm - "Small description"**

## Contributing

Thank you for the time you spend to develop a feature or fix a mistake of this repository. Your help is essential for keeping it great.  
Contributions to this project are released after the cordinator check.

## Submitting a pull request

For major and big contributions
1. Fork and clone the repository
2. Create a new branch: git chekout -b my-branch-name
3. Make your changes
4. Push to your fork and submit a pull request
5. Make sure that checks in your pull request are green (in your fork)

Here are a few things you can do that will increase the likelihood of your pull request being accepted:
* Please include a summary of the change and which issue is fixed. Also include relevant motivation and context.
* Follow the style guide of the rest of the source code
* Write good commit messages

## Version Notation

![VersionNotation](/dev/Package/fmup/doc/img/version.jpg)

**Major versions:** consists of scope expansions or deletions and may have changes that break compatibility.
**Minor versions:** consists of feature extensions, where compatibility is guaranteed for the "core" schema, but not for other definitions
**Addendums:** consists of improvements to existing features, where the schema may change but upward compatibility is guaranteed.
**Corrigendums:** consists of improvements to documentation, where the schema does not change though deprecation is possible






### Credits

All rights served.