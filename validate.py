from pathlib import Path
import os

def validate_form(values):
    is_valid = True
    values_invalid = []

    '''
    check path to root is valid
    later check for FS as names of folders
    check folder has runs in it
    '''
    path = values['PATH']
    if len(os.listdir(path)) == 0: # or 
        values_invalid.append('path should be to directory with scenarios in separate folders')
        is_valid = False

    return is_valid, values_invalid

def generate_error_message(values_invalid):
    error_message = ''
    for value_invalid in values_invalid:
        error_message += ('\nInvalid' + ':' + value_invalid)

    return error_message


if __name__ == '__main__':
    path_to_root_directory = Path(r"C:\Users\IanShaw\Dropbox\Projects CFD\9. 100 Avenue Road\Jan 2023 Corridor Models")
    validate_form({"PATH": path_to_root_directory})