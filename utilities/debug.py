import pdb
import os

def debug_here():
    """
    Drop this in any file to start the interactive debugger at that point.
    Only activates if DEBUG mode is on (e.g. DEBUG=True in environment).
    """
    if os.getenv("DEBUG", "false").lower() == "true":
        print("\n [Debugger Active] Entering pdb shell... \n")
        pdb.set_trace()
