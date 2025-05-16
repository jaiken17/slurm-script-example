from typing import List
import shutil

param_placeholders = ['PARAM1', 'PARAM2', 'PARAM3']
files_to_replace = ["initial_conditions.txt"]


def replace_params(new_wd: str, new_params: List[str]):
    for file in files_to_replace:
        file_path = new_wd + '/' + file
        with open(file_path, 'r') as f:
            text = f.read()
        
        for i,param in enumerate(param_placeholders):
            text = text.replace(param,new_params[i])

        with open(file_path,'w') as f:
            f.write(text)


def copy_dir(template_dir: str, new_wd: str):
    # better methods might be available
    shutil.copytree(template_dir,new_wd) # copies template_dir to new_wd


def main(params_file: str, template_dir: str):

    with open(params_file, 'r') as file:
        for line in file:
            entries = line.strip().split()
            new_wd = entries[0]
            params = entries[1:-1]
            if len(params) != len(param_placeholders):
                raise Exception(f'Found {len(params)} parameters; expected {len(param_placeholders)}')
            copy_dir(template_dir,new_wd)
            replace_params(new_wd, params)


def get_command_line_args() -> (str,str):
    args = sys.argv
    args.pop[0] # remove script name
    num_args_expected = 3
    if len(args) != num_args_expected:
        raise Exception(f'{len(args)} command line args provided; {num_args_expected} command line args expected.')
    params_file = args[1]
    template_dir = args[2]

    return (params_file, template_dir)


if __name__ == '__main__':

    (params_file,template_dir) = get_command_line_args()
    main(params_file, template_dir)
