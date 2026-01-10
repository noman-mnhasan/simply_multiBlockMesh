#! /usr/bin/bash

#---------------------------------------
### This is the working directory
### This shell doesn't need to be in the working directory.
export_directory="/path/to/the/export/directory"

#---------------------------------------
### Read multi-block edit file? "yes" or "no"
read_edit_file="yes"

#---------------------------------------
### For scaling the mesh
### All dimensions gets multiplied by
### the value of "convert_to_meters" globally

convert_to_meters=1

#---------------------------------------

bounding_box='{
    "x-min" : 0.0,
    "x-max" : 1.0,
    "y-min" : 0.0,
    "y-max" : 1.0,
    "z-min" : 0.0,
    "z-max" : 1.0
}'

#---------------------------------------
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

#---------------------------------------

gid_spacing='{
    "x" : 0.01,
    "y" : 0.005,
    "z" : 0.01
}'

#---------------------------------------

hex2exclude='{
    "exclude-list" : []
}'

#---------------------------------------

export export_directory
export read_edit_file
export bounding_box
export convert_to_meters
export split_plane_list
export gid_spacing
export hex2exclude

#---------------------------------------
### Provide the path of the python interpreter
python="path/to/the/python/interpreter"

#---------------------------------------
### Provide the path where the "simply_multiblockmesh.py" file is located
### Make sure the "classes" file and the "case_system_template" directory (with its contents) are also in the same directory.
simply_multiblockmesh="path/to/the/'simply_multiblockmesh.py'/script/in/local/disk"

#---------------------------------------

VSEP="----------------------------------------"

$python $simply_multiblockmesh

#---------------------------------------

if [[ "$?" == 0 ]]; then
    printf "\n\n\n"
    printf "%s\n" $VSEP
    printf "### Running 'blockMesh' ###\n"
    printf "%s\n\n\n\n" $VSEP
    
    printf "%s\n" $VSEP
    if ! command -v "blockMesh" &> /dev/null; then
        echo "Command 'blockMesh' does not exist. Please install/source it."
        exit 1
    fi
    # Continue with your script if the command exists
    echo "Command 'blockMesh' found. Proceeding..."
    printf "\n\n"
    
    cd ./case
    blockMesh
    cd ..
    
else
    printf "\n\n\n"
    printf "%s\n" $VSEP
    printf "'blockMeshDict' generation failed\n"
    printf "%s\n\n\n" $VSEP
    
fi

#---------------------------------------



