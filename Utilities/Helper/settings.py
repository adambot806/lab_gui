
def inintParams():
    global widget_params, instrument_params, imgData
    widget_params = {
        "Image Display Setting": {
            "bkgStatus": False,
            "pfStatus": False,
            "magStatus": False,
            "imgSource": "disk",
            "mode": None,
            "magValue": 2,
            "pfMin": 20,
            "pfMax": 200,
            "img_queue_size": 3,
            "img_stack_num": 5

        },
        "Analyse Data Setting": {
            "roiStatus": False,
            "crossHStatus": False,
            "calAtomStatus": False,
            "fittingStatus": False,
            "ToPwr": 10,
            "Detu": 100,
            "Dia": 100,
            "roiRange": {"pos": [], "size": []},  # {'pos': pos(), 'size': size()}
            "atomNum": 0,
            "cursorPos": [],
            "crossSectionData": {
                "horizontalAxes": [],
                "verticalAxes": []
                           }
        },
        "Miscellanea": {
            "MagStatus": False,
            "MagFactor": 1,
            "tmpfactor": 1,
            "GSFittingStatue": False,
            "ROILength": 100,
            "NCountStatus": False,
            "NCountsfitting": False,
            "MotionRPStatus": False,
            "MOTBeamOD": 0,
            "MOTDetuning": 0,
            "MotPower": 0,


        }
    }
    instrument_params = {
        "Camera": {
            # "camera model": "Chameleon",
            "camera model": "DummyCamera",
            "exposure time": 20,
            "shutter time": 20,
            "gain value": 1,
            "CCD pixel size": 25,  # not sure about it, need to confirm

        },
        "SLM": {
            "slm model": "LCSLM",
        }
    }
    imgData = {
        "MainImg": [], # contain the main plot window's image data
        "BkgImg": [], # contain the background image data when load from disk
        "WI": [],
        "WO": []
        }
    print("Initialize parameters finished")
