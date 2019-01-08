import time


def chrono():
    seconds = 60


    for i in range(seconds):
        seconds=seconds-1
        if seconds%5==0:
            print(str(seconds) + " Secondes restantes avant controle des pins.")
        time.sleep(1)
        
    