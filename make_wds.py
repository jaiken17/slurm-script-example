from typing import List
import shutil
import sys


# Global variables that need to be modified for use

# placeholder values in initial condition files (within files copied from template dir)
param_placeholders = ['PARAM1', 'PARAM2', 'PARAM3']
# which files need initial parameters to be replaced
files_to_replace = ["initial_conditions.txt"]


def replace_params(new_wd: str, new_params: List[str]):
    """Function that replaces the placeholders values with the desired initial
       parameters in the copied run directory.

    Function takes two parameters: new_wd the path to the new working directory
    and new_params the list of values that will replace the placeholders.
    """

    for file in files_to_replace:
        file_path = new_wd + '/' + file
        with open(file_path, 'r') as f:
            text = f.read()
        
        for i,param in enumerate(param_placeholders):
            text = text.replace(param,new_params[i])

        with open(file_path,'w') as f:
            f.write(text)


def copy_dir(template_dir: str, new_wd: str):
    """Function that copies 'template_dir' to 'new_wd'.

    Function copies all subdirectories and files from the template directory
    to a new working directory (run directory). Currently will throw an error
    if new_wd already exists.
    """

    # better methods might be available
    shutil.copytree(template_dir,new_wd)


def main(params_file: str, template_dir: str, index: int):
    """Main script function.

    Function opens file containing list of runs and their initial parameters
    (params_file) and reads the line associated with the SLURM_ARRAY_TASK_ID
    (index). This line contains the name of the new run and its initial 
    parameters. A new working directory is created with the run's name by
    copying the template directory (template_dir). Then the placeholder 
    initial parameters within the copied files are changed with the desired
    initial parameters. Finally, the name of the new directory is printed to
    the screen to be read by the BASH script that invoked this script.
    """

    # Open and read line from initial parameters file 
    file = open(params_file,'r')
    lines = file.readlines()
    file.close()
    line = lines[index]
    
    # Split line into run name and its initial parameters
    entries = line.strip().split()
    new_wd = entries[0]
    params = entries[1:]
    if len(params) != len(param_placeholders):
        raise Exception(f'Found {len(params)} parameters; expected {len(param_placeholders)}')
    
    # Copy templated directory to make new run directory
    copy_dir(template_dir,new_wd)
    # Substitute in initial parameters for run
    replace_params(new_wd, params)

    # Print run name for use in BASH script
    print(new_wd)


def get_command_line_args() -> (str,str,int):
    """Function that gets and verifies the command line args present when
       this script was inoked.
    
    Three arguments are expected (besides the python script name): the name
    of the initial parameters file (params_file), the path to the template
    directory (template_dir), and the SLURM_ARRAY_TASK_ID. The arguments are
    assumed to be in this order. Note: the SLURM_ARRAY_TASK_ID is 1-indexed
    and this function modifies this to be 0-indexed.
    """

    args = sys.argv
    args = args[1:]
    num_args_expected = 3
    if len(args) != num_args_expected:
        raise Exception(f'{len(args)} command line args provided; {num_args_expected} command line args expected.')
    params_file = args[0]
    template_dir = args[1]
    array_index = args[2] 
    try:
        array_index = int(array_index)
        array_index -= 1 # note slurm array is 1-indexed (starts at 1 not 0)
    except ValueError:
        print("Expected array index to be integer")


    return (params_file, template_dir, array_index)

# Entry point of script
if __name__ == '__main__':

    # Get necessary command line args first
    (params_file,template_dir,index) = get_command_line_args()
    # Call main script function
    main(params_file, template_dir, index)
