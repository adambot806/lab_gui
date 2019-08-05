"""
    Starting point for running the program.
"""


from multiprocessing import Process
from MainWindow import start_main_win

if __name__ == '__main__':
    p = Process(target=start_main_win)
    p.start()
    p.join()
