import re
from helper_functions import round_to, return_paths_to_files, find_all_files_of_type, return_all_subfolders
from os import listdir
from pathlib import Path

# C:\Users\IanShaw\Fire Dynamics Group Limited\CFD - Files\Research CFD\1. Graph Generation\Test Cases\Test2
# def return_paths_to_files(scenario_name, dir_path='graph_generation', new_folder_structure=False):
#     if new_folder_structure == False:
#         path_to_scen_directory = f'./{dir_path}/{scenario_name}/Graph_{scenario_name}'
#         path_to_fds_file = f'{path_to_scen_directory}/Graph_{scenario_name}.fds'
#         path_to_devc_file = f'{path_to_scen_directory}/Graph_{scenario_name}_devc.csv'
#         path_to_hrr_file = f'graph_generation\{scenario_name}\Graph_{scenario_name}\Graph_{scenario_name}_hrr.csv'

#     else:
#         path_to_scen_directory = f'{dir_path}/{scenario_name}'
#         fds_name = find_all_files_of_type(path_to_directory=path_to_scen_directory, suffix=".fds")[0]
#         devc_name = find_all_files_of_type(path_to_directory=path_to_scen_directory, suffix="devc.csv")[0]
#         hrr_name = find_all_files_of_type(path_to_directory=path_to_scen_directory, suffix="hrr.csv")[0]

#         # find all files - ones with x and y ending
#         path_to_hrr_file = f'{path_to_scen_directory}/{hrr_name}'
#         path_to_fds_file = f'{path_to_scen_directory}/{fds_name}'
#         path_to_devc_file = f'{path_to_scen_directory}/{devc_name}'

#     return path_to_hrr_file, path_to_scen_directory, path_to_fds_file, path_to_devc_file

# def find_all_files_of_type(path_to_directory, suffix=".csv"):
#     filenames = listdir(path_to_directory)
#     return [ f for f in filenames if f.endswith( suffix )]

def return_scenario_names(path_to_directory):
    scenario_names = [f for f in listdir(Path(__file__).parent/path_to_directory)] 
    return scenario_names
# TODO: just use line_list for all below
def find_venting_from_fds(path_to_file):
    line_list = []
    extract_rate_list = []
    supply_rate_list = []
    natural_inlet_list = []
    supply_count = 0
    extract_count = 0
    regex = "\d+\.\d+"
    aov_area = 0
    with open(path_to_file, "r+") as f:
        line_list = f.readlines()
    with open(path_to_file, "r+") as f:
        for index, line in enumerate(f):
            line_stripped_lowercase = line.strip().lower()
            if line != None: 
                if "ID=\'Extract".lower()  in line_stripped_lowercase or "ID=\'Supply".lower() in line_stripped_lowercase  or "ID=\'Exhaust".lower() in line_stripped_lowercase:
                    isExtract = "extract" in line_stripped_lowercase or "exhaust" in line_stripped_lowercase 
                    # scope next line with VOLUME_FLOW
                    # for next_line_index in range(5):
                    if index+5 < len(line_list): 
                        for next_line_index in range(1, 4):
                            # use readlines
                            
                            next_line = line_list[index+next_line_index]

                            if 'VOLUME_FLOW' in next_line:
                                flow = re.findall(regex, next_line)
                                # use f.next() using loop above
                                print(flow)
                                if isExtract:
                                    # push to extract array
                                    extract_rate_list.append(flow)
                                else: 
                                    supply_rate_list.append(flow)
                                #extract float from line
                # vents
    with open(path_to_file) as f:
        for line in f:
            line_stripped_lowercase = line.strip().lower()
            if line != None: 
                if "ID=\'AOV".lower() in line_stripped_lowercase:
                    # regex = '\d*?\.\d+'
                    position_array = re.findall(regex, line)
                    # find smallest in array
                    # TODO: create generic function for opening in any plane
                    # opening_area = abs(float(position_array[0]) - float(position_array[1])) * abs(float(position_array[2]) - float(position_array[3]))
                    opening_area = find_area_opening(line_with_position=line)
                    aov_area = opening_area
                    print(opening_area)
                elif "ID=\'Hole".lower() in line_stripped_lowercase:
                    # TODO: loop through vents
                    opening_area = find_area_opening(line_with_position=line)
                    inlet_vent_area = opening_area  
                    natural_inlet_list.append(opening_area)                  
                elif "&VENT ID=".lower() in line_stripped_lowercase:
                    # supply and extract count

                    if "ID=\'Supply".lower() in line_stripped_lowercase:
                        supply_count += 1
                    elif "ID=\'Extract".lower() in line_stripped_lowercase or "ID=\'Exhaust".lower() in line_stripped_lowercase:
                        extract_count += 1
    # TODO: include other natural openings
    return extract_rate_list, supply_rate_list, aov_area, extract_count, supply_count, natural_inlet_list


def find_area_opening(line_with_position):
    regex = "\d+\.\d+"
    position_array = re.findall(regex, line_with_position)
    lengths = [abs(float(position_array[0]) - float(position_array[1])), abs(float(position_array[2]) - float(position_array[3])), abs(float(position_array[4]) - float(position_array[5]))]
    min_index = lengths.index(min(lengths))
    # remove two items from position_list
    doable_min_index = min_index*2
    area_array = position_array[:doable_min_index]+position_array[doable_min_index+2:]
    opening_area = abs(float(area_array[0]) - float(area_array[1])) * abs(float(area_array[2]) - float(area_array[3]))
    opening_area = round_to(opening_area)
    return opening_area

def is_sprinklered(path_to_file):
     with open(path_to_file) as f:
        for line in f:
            if "SPRK".lower() in line.strip().lower():
                return True
        return False

def return_fds_version(path_to_directory):
    subfolder_list = return_all_subfolders(path_to_directory)
    # scope if 
    if len(subfolder_list) > 0:
        path_to_directory += f'/{subfolder_list[0]}'
    file_name = find_all_files_of_type(path_to_directory, suffix=".out")[0]
    path_to_file = f'{path_to_directory}/{file_name}'
    with open(path_to_file, "r+") as f:
        line_list = f.readlines()
    regex = "\d+\.\d+\.\d+"
    version_line = [f for f in line_list if "FDS" in f][0]
    # use regex on above line
    version = re.findall(regex, version_line)[0]
    return version
