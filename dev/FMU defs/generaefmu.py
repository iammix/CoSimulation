import os
import sys


def generate_fmu(self):
    #Check if Library path is none
    if not(self.export_tool=='jmodelica'):
        current_library_path = os.environ.get(self.modelica_path)
        if (current_library_path is None):
            os.enivron[self.modelica_path] = self.simulatortofmu_path
        else:
            os.environ[self.modelica_path] = self.simulatortofmu_path + os.pathsep + current_library_path
    loader = jja2.FileSystemLoader(self.mosT_path)
    env = jja2.Enviroment(loader=loader)
    template = env.get_template('')

    sim_lib_path_jm = os.path.abspath(self.simulatortofmu_path)
    sim_lib_path_jm = fix_path_delimiters(sim_lib_jm)

    output_res = template.render(model_name=self.model_name,
                                 fmi_version=self.fmi_version,
                                 fmi_api=self.fmi_api,
                                 sim_lib_path = sim_lib_path_jm)

    rand_name = ''.join(random.choice(string.ascii_uppercase + string.digits)
                for _ in range(6))

    if (self.export_tool == 'jmodelica'):
        output_file = rand_name + '_' + self.model_name + '.py'
    elif (self.export_tool == 'dymola' or self.export_tool == 'openmodelica'):
        output_file = rand_name + '_' + self.model_name + '.mos'
    if os.path.isfile(output_file):
        s = ('The output file {!s} exists and will be overwritten.').format(output_file)
        log.warning(s)
    with open(output_file, 'w') as fh:
        fh.write(str(output_res))
    fh.close()

    # Create different commands for different tools
    # Create command for Dymola
    if (self.export_tool == 'dymola'):
        if (not (self.export_tool_path is None)):
            command = os.path.normpath(os.path.join(self.export_tool_path, 'dymola'))

        else:
            command = 'dymola'

    # Create command for JModelica
    if(self.export_tool == 'jmodelica'):
        if(platform.system().lower()=='linux'):
            if (not(self.export_tool_path is None)):
                command = os.path(os.path.join(self.export_tool_path, 'hm_python.sh'))
            else:
                command = os.path.normpath(os.path.join('jm_python.sh'))
        elif(platform.system().lower()=='windows'):
            if (not(self.export_tool_path is None)):
                command = os.path.normpath(os.path.join(self.export_tool_path, 'setenv.bat'))
            else:
                command = 'setenv.dat'

    # Create command for OpenModelica
    if (self.export_tool == 'openmodelica'):
        if (not (self.export_tool_path is None)):
            command = os.path.normpath(os.path.join(self.export_tool_path, 'openmodelica'))
        else:
            command = 'omc'
    # Compile the FMU using Dymola
    if (self.export_tool == 'dymola'):
        retStr = sp.check_output([command, output_file])

    # Compile the FMU using JModelica
    if (self.export_tool == 'jmodelica'):
        # rename some libraries so the code can compile with JModelica 2.4
        self.rename_lib(None)

        if (platform.system().lower() == 'linux'):
            retStr = sp.check_output([command, output_file])
        else:
            output_cmd = 'python' + str(output_file)
            print("command is {!s}".format(command + "&&" + output_cmd))
            # Run multiple commands in the same shell
            retStr = sp.check_output(command + "&&" + output_cmd, shell=True)
        # rename some libraries so the code can compile with Jmodelica 2.4
        self.rename_lib("revert")
    
    # Compile the FMU using OpenModelica
    if (self.export_tool == 'openmodelica'):
        retStr = sp.check_output([command, output_file, 'SimulatorToFMU'])
    
    #Check if there is any error message in the output
    if not (retStr is None):
        retStr = retStr.lower()
        if sys.version_info.major > 2:
            retStr = str(retStr, 'utf-8')
        if (retStr.find('error')>=0 and self.export_tool!= 'jmodelica'):
            s='{!s} failed to export {!s} as an FMU'\
            'with error={!s}'.format(self.export_tool, self.model_name, retStr)
            print("There is an error in the compilation audit file" + s)
            raise ValueError(s)
    # Reset the library path to the default
    if not(self.export_tool == 'jmodelica'):
        if not(current_library_path is None):
            os.environ[self.modelica_path] = current_library_path
    # remove the output file
    os.remove(output_file)

    # rename the FMU to indicate target Python Simulator
    fmu_name = self.model_name + '.fmu'

    # Write success
    s = 'The FMU {!s} is successfully created.'.format(fmu_name)
    log.info(s)