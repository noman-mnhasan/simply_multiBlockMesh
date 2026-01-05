#! /usr/bin/bash

### This is the working directory
### This shell doesn't need to be in the working directory.
export_directory="/path/to/the/export/directory"

bounding_box='{
    "x-min" : 0.0,
    "x-max" : 1.0,
    "y-min" : 0.0,
    "y-max" : 1.0,
    "z-min" : 0.0,
    "z-max" : 1.0
}'


### CUT PLANE LIST
###
### x --> x-coordinate for YZ plane
### y --> x-coordinate for ZX plane
### z --> x-coordinate for XY plane

split_plane_list='{
    "x" : [0.2, 0.6, 0.8],
    "y" : [0.3, 0.5, 0.7],
    "z" : [0.1, 0.3, 0.6, 0.8]
}'

gid_spacing='{
    "x" : 0.01,
    "y" : 0.005,
    "z" : 0.01
}'

hex2exclude='{
    "exclude-list" : []
}'

export export_directory
export bounding_box
export split_plane_list
export gid_spacing
export hex2exclude


### Provide the path of the python interpreter
python="path/to/the/python/interpreter"


### Provide the path where the "simply_multiblockmesh.py" file is located
### Make sure the "classes" file and the "case_system_template" directory (with its contents) are also in the same directory.
simply_multiblockmesh="path/to/the/'simply_multiblockmesh.py'/script/in/local/disk"


$python $simply_multiblockmesh





