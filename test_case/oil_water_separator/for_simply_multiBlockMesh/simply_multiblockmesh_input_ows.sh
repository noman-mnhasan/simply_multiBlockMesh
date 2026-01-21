#! /usr/bin/bash

### This is the working directory
### This shell doesn't need to be in the working directory.
export_directory="/path/to/export/or/working/directory"

bounding_box='{
    "x-min" : -0.012,
    "x-max" : 0.2,
    "y-min" : -0.012,
    "y-max" : 0.112,
    "z-min" : -0.1,
    "z-max" : 0.1
}'


### CUT PLANE LIST
###
### x --> x-coordinate for YZ plane
### y --> x-coordinate for ZX plane
### z --> x-coordinate for XY plane

split_plane_list='{
    "x" : [0.0, 0.04, 0.06, 0.09, 0.11, 0.14, 0.16],
    "y" : [0.0, 0.05, 0.07, 0.09, 0.1],
    "z" : [-0.01, 0.01]
}'

gid_spacing='{
    "x" : 0.005,
    "y" : 0.005,
    "z" : 0.005
}'

# ### For generating single cell blocks
# gid_spacing='{
#     "x" : 1,
#     "y" : 1,
#     "z" : 1
# }'

hex2exclude='{
    "exclude-list" : [0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 16, 24, 32, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 51, 52, 53, 55, 56, 60, 64, 80, 88, 89, 90, 91, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 108, 112, 120, 128, 136, 137, 138, 139, 140, 141, 142, 143]
}'

export export_directory
export bounding_box
export split_plane_list
export gid_spacing
export hex2exclude


### Provide the path of the python interpreter
python="/path/to/the/python/interpreter"


### Provide the path where the "simply_multiblockmesh.py" file is located
### Make sure the "classes" file and the "case_system_template" directory (with its contents) are also in the same directory.
simply_multiblockmesh="/path/to/the/'simply_multiblockmesh.py'/script/"


$python $simply_multiblockmesh





