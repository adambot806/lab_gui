def inintParams():
    global widget_params, instrument_params, imgData
    widget_params = {
        "Image Display Setting": {
            "bkgStatus": False,
            "pfStatus": False,
            "magStatus": False,
            "imgSource": "disk",  # default is disk, once click the start experiment button, then change to camera
            "mode": 0,  # 0 is video mode; 2 is hardware mode
            "magValue": 2,
            "pfMin": 20,
            "pfMax": 200,
            "img_stack_num": 6
        },
        "Analyse Data Setting": {
            "roiStatus": False,
            "add_cross_axes": False,
            "ToPwr": 10,
            "Detu": 100,
            "Dia": 100,
        },
        "Miscellanea": {
            "MagStatus": False,
            "MagFactor": 1,
            "tmpfactor": 1,
            "GSFittingStatue": False,
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
            "index": None,
            "exposure time": 20,
            "shutter time": 20,
            "gain value": 1,
        },
        "SLM": {
            "slm model": "LCSLM",
        }
    }
    imgData = {
        "BkgImg": [],  # contain the background image data when load from disk
        "WI": [],
        "WO": []
        }
    print("Initialize parameters finished")
