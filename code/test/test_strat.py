import time
import pyautogui
import keyboard

PC_TOKKY  = 1
PC_FEBZ   = 2
PC_ARKUVE = 3

PC = PC_TOKKY

if PC == PC_TOKKY:
    POSITION_RESET   = (180, 370)
    POSITION_START   = (180, 264)
    POSITION_NB_STEP = (430, 480)
    POSITION_CSV     = (1700, 980)
    
    POSITION_NEUTRE  = (200, 800)

attente_reset          =  5 # secondes
attente_fin_simulation = 50 # secondes

def copier():
    time.sleep(0.5)
    keyboard.press_and_release('ctrl+c', do_release=False)
    time.sleep(0.5)
    keyboard.press_and_release('ctrl+c', do_press=False)
    
def coller():
    time.sleep(0.5)
    keyboard.press_and_release('ctrl+v', do_release=False)
    time.sleep(0.5)
    keyboard.press_and_release('ctrl+v', do_press=False)

def clic(position):
    pyautogui.click(*position)
    time.sleep(0.25)

def double_clic(position):
    pyautogui.doubleClick(*position)
    time.sleep(0.25)

def tapper(texte):
    time.sleep(0.5)
    keyboard.write(texte)

def sauvegarder():
    time.sleep(0.5)
    keyboard.press_and_release('ctrl+s', do_release=False)
    time.sleep(0.5)
    keyboard.press_and_release('ctrl+s', do_press=False)

def tout_selectionner():
    time.sleep(0.5)
    keyboard.press_and_release('ctrl+a', do_release=False)
    time.sleep(0.5)
    keyboard.press_and_release('ctrl+a', do_press=False)

def main():

    double_clic(POSITION_RESET)
    time.sleep(attente_reset)
    
    clic(POSITION_START)
    
    time.sleep(attente_fin_simulation)
    
    
    double_clic(POSITION_NEUTRE)
    tout_selectionner()
    copier()
    
    clic(POSITION_CSV)
    tapper(";")
    coller()
    tapper(";\n")
    
    sauvegarder()
    
if __name__ == "__main__":
    while True : 
        main()
