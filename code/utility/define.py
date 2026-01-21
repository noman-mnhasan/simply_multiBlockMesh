
"""  VERSION """
__version__ = "0.1.1"


wspace = " "
indent = wspace * 4
VSEP = "-"*40

quadrantCompressionFactor = 0.20

templateDirName = "input_template"
templateFilenameBlockEdit = "block_edit.py"

ofCaseTemplateDirname = "case_system_template"

blockFaceName = ["front", "back", "left", "right", "bottom", "top"]

quadrantEdgeRule = {
    "xy": {
            1 : {
                "collapse-edge-location" : ["top", "right"],
                "axis-edge-location" : ["bottom", "left"],
                "arc-edge-location" : {
                        "top-block" : [
                                ["top", "front"],
                                ["top", "back"]
                            ],
                        "side-block" : [
                                ["right", "front"],
                                ["right", "back"]
                            ],
                    },
                "radial-edge-location" : {
                        "top-block" : ["top", "left"],
                        "side-block" : ["bottom", "right"]
                    },
            },
            2 : {
                "collapse-edge-location" : ["top", "left"],
                "axis-edge-location" : ["bottom", "right"],
                "arc-edge-location" : {
                        "top-block" : [
                                ["top", "front"],
                                ["top", "back"]
                            ],
                        "side-block" : [
                                ["left", "front"],
                                ["left", "back"]
                            ],
                    },
                "radial-edge-location" : {
                        "top-block" : ["top", "right"],
                        "side-block" : ["bottom", "left"]
                    },
            },
            3 : {
                "collapse-edge-location" : ["bottom", "left"],
                "axis-edge-location" : ["top", "right"],
                "arc-edge-location" : {
                        "top-block" : [
                                ["bottom", "front"],
                                ["bottom", "back"]
                            ],
                        "side-block" : [
                                ["left", "front"],
                                ["left", "back"]
                            ],
                    },
                "radial-edge-location" : {
                        "top-block" : ["bottom", "right"],
                        "side-block" : ["top", "left"]
                    },
            },
            4 : {
                "collapse-edge-location" : ["bottom", "right"],
                "axis-edge-location" : ["top", "left"],
                "arc-edge-location" : {
                        "top-block" : [
                                ["bottom", "front"],
                                ["bottom", "back"]
                            ],
                        "side-block" : [
                                ["right", "front"],
                                ["right", "back"]
                            ],
                    },
                "radial-edge-location" : {
                        "top-block" : ["bottom", "left"],
                        "side-block" : ["top", "right"]
                    },
            },
        },
    "yz": {
            1 : {
                "collapse-edge-location" : ["top", "front"],
                "axis-edge-location" : ["bottom", "back"],
                "arc-edge-location" : {
                        "top-block" : [
                                ["front", "right"],
                                ["front", "left"]
                            ],
                        "side-block" : [
                                ["top", "right"],
                                ["top", "left"]
                            ],
                    },
                "radial-edge-location" : {
                        "top-block" : ["top", "front"],
                        "side-block" : ["bottom", "back"]
                    },
            },
            2 : {
                "collapse-edge-location" : ["bottom", "front"],
                "axis-edge-location" : ["top", "back"],
                "arc-edge-location" : {
                        "top-block" : [
                                ["front", "right"],
                                ["front", "left"]
                            ],
                        "side-block" : [
                                ["bottom", "right"],
                                ["bottom", "left"]
                            ],
                    },
                "radial-edge-location" : {
                        "top-block" : ["top", "back"],
                        "side-block" : ["bottom", "front"]
                    },
            },
            3 : {
                "collapse-edge-location" : ["bottom", "back"],
                "axis-edge-location" : ["top", "front"],
                "arc-edge-location" : {
                        "top-block" : [
                                ["back", "right"],
                                ["back", "left"]
                            ],
                        "side-block" : [
                                ["bottom", "right"],
                                ["bottom", "left"]
                            ],
                    },
                "radial-edge-location" : {
                        "top-block" : ["bottom", "back"],
                        "side-block" : ["top", "front"]
                    },
            },
            4 : {
                "collapse-edge-location" : ["top", "back"],
                "axis-edge-location" : ["bottom", "front"],
                "arc-edge-location" : {
                        "top-block" : [
                                ["back", "right"],
                                ["back", "left"]
                            ],
                        "side-block" : [
                                ["top", "right"],
                                ["top", "left"]
                            ],
                    },
                "radial-edge-location" : {
                        "top-block" : ["bottom", "front"],
                        "side-block" : ["top", "back"]
                    },
            },
        },
    "zx": {
            1 : {
                "collapse-edge-location" : ["front", "right"],
                "axis-edge-location" : ["back", "left"],
                "arc-edge-location" : {
                        "top-block" : [
                                ["right", "top"],
                                ["right", "bottom"]
                            ],
                        "side-block" : [
                                ["front", "top"],
                                ["front", "bottom"]
                            ],
                    },
                "radial-edge-location" : {
                        "top-block" : ["right", "back"],
                        "side-block" : ["left", "front"]
                    },
            },
            2 : {
                    "collapse-edge-location" : ["back", "right"],
                    "axis-edge-location" : ["front", "left"],
                    "arc-edge-location" : {
                            "top-block" : [
                                    ["right", "top"],
                                    ["right", "bottom"]
                                ],
                            "side-block" : [
                                    ["back", "top"],
                                    ["back", "bottom"]
                                ],
                    },
                "radial-edge-location" : {
                        "top-block" : ["right", "front"],
                        "side-block" : ["felt", "back"]
                    },
            },
            3 : {
                "collapse-edge-location" : ["back", "left"],
                "axis-edge-location" : ["front", "right"],
                "arc-edge-location" : {
                        "top-block" : [
                                ["left", "top"],
                                ["left", "bottom"]
                            ],
                        "side-block" : [
                                ["back", "top"],
                                ["back", "bottom"]
                            ],
                    },
                "radial-edge-location" : {
                        "top-block" : ["left", "front"],
                        "side-block" : ["right", "back"]
                    },
            },
            4 : {
                "collapse-edge-location" : ["front", "left"],
                "axis-edge-location" : ["back", "right"],
                "arc-edge-location" : {
                        "top-block" : [
                                ["left", "top"],
                                ["left", "bottom"]
                            ],
                        "side-block" : [
                                ["front", "top"],
                                ["front", "bottom"]
                            ],
                    },
                "radial-edge-location" : {
                        "top-block" : ["left", "back"],
                        "side-block" : ["right", "front"]
                    },
            },
        },
}

edgePosition = [
        "back-bottom",
        "back-top",
        "front-bottom",
        "front-top",
        "back-left",
        "back-right",
        "front-left",
        "front-right",
        "left-bottom",
        "left-top",
        "right-bottom",
        "right-top"
    ]

slicePlaneAxisIndex = {
    "xy" : {
        "index1" : 0,
        "index2" : 1
    },
    "yz" : {
        "index1" : 1,
        "index2" : 2
    },
    "zx" : {
        "index1" : 2,
        "index2" : 0
    }
}

taskTypeCheck = [
    "vertexEdit", 
    "edgeEdit",
    "faceEdit",
    "blockEdit",
    "boundary",
]


blockShiftCoefficient = {
    1: {
            "top" : 1,
            "side" : 1,
        },
    2: {
            "top" : 1,
            "side" : -1,
        },
    3: {
            "top" : -1,
            "side" : -1,
        },
    4: {
            "top" : -1,
            "side" : 1,
        },
}

angleForQuadrant = {
    1: {
            "theta-corner" : 45,
            "theta-side-arc" : 45/2.0,
            "theta-top-arc" : 3*45/2.0,
        },
    2: {
            "theta-corner" : (1*90) + 45,
            "theta-side-arc" : (1*90) + (3*45/2.0),
            "theta-top-arc" : (1*90) + (45/2.0),
        },
    3: {
            "theta-corner" : (2*90) + 45,
            "theta-side-arc" : (2*90) + (45/2.0),
            "theta-top-arc" : (2*90) + (3*45/2.0),
        },
    4: {
            "theta-corner" : (3*90) + 45,
            "theta-side-arc" : (3*90) + (3*45/2.0),
            "theta-top-arc" : (3*90) + (45/2.0),
        },
}