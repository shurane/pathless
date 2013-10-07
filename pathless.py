import subprocess
import os
import json
from colorama import init, Fore
from prettytable import PrettyTable
init(autoreset=True)

def get_env(variable):
    output = os.popen("cmd /C set {0}".format(variable)).readlines()
    variable_contents = None
    for line in output:
        left, right = line.split("=",1)
        # Windows environment variables are case insensitive.
        if left.lower() == variable.lower():
            #print("{0} = {1}".format(left,right))
            variable_contents = right
            break
    return variable_contents

def set_env(variable,contents):
    # TODO
    pass

def existent_paths(paths):
    return [d for d in paths if os.path.isdir(d)]

def get_paths():
    unsplit = get_env("PATH").strip()
    return [d for d in unsplit.split(";") if d ]

def get_pathexts():
    unsplit = get_env("PATHEXT").strip()
    return [d.lower() for d in unsplit.split(";") if d ]

def binaries_in_path(path):
    pathexts = get_pathexts()
    files = []
    if not os.path.isdir(path):
        return files

    for f in os.listdir(path):
        f = f.lower()
        for p in pathexts:
            if f.endswith(p):
                files.append(f)
                break
    return files

def get_binaries(paths):
    binaries = dict(zip(paths,map(binaries_in_path, paths)))
    return binaries

if __name__ == "__main__":
    field_names=["Path", "Exists", "# of Binaries"]
    pt = PrettyTable(field_names=field_names)
    pt.align[field_names[0]] = "l"
    pt.align[field_names[2]] = "r"
    paths = get_paths()
    #binaries = binaries_in_path("C:\Windows\system32")
    for d in paths:
        pt.add_row([d, os.path.isdir(d), len(binaries_in_path(d))])
    print pt

