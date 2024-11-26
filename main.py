from src.App import App
import sys
import os

if __name__ == "__main__":
    serivce_name = 'MyApp'
    if hasattr(sys, '_MEIPASS'):
        working_path = sys._MEIPASS
    else:
        working_path = os.path.dirname(p=__file__)

    App(service_name=serivce_name,working_path=working_path)