import time
import pyautogui
import keyboard

# Coordonnées des boutons (Moitié écran)
POSITION_RESET   = (180, 370)
POSITION_START   = (180, 264)
POSITION_NB_STEP = (430, 480)
POSITION_CSV     = (1700, 980)

attente_reset          =  5 # secondes
attente_fin_simulation = 60 # secondes

def main():

    # Clic sur RESET et attente
    pyautogui.click(*POSITION_RESET)
    pyautogui.click(*POSITION_RESET)
    time.sleep(attente_reset)
    
    # Clic sur START
    pyautogui.click(*POSITION_START)
    
    # Attente de la fin de la simulation
    time.sleep(attente_fin_simulation)
    
    # Récupération du nombre de pas
    pyautogui.click(*POSITION_NB_STEP)
    pyautogui.click(*POSITION_NB_STEP)
    
    keyboard.press_and_release('ctrl+c')
    
    # Copie sur le terminal
    pyautogui.click(*POSITION_CSV)
    time.sleep(2)
    keyboard.press(';')
    time.sleep(0.5)
    keyboard.press_and_release('ctrl+v', do_release=False)
    time.sleep(0.5)
    keyboard.press_and_release('ctrl+v', do_press=False)
    time.sleep(0.5)
    keyboard.press(';')
    time.sleep(0.5)
    keyboard.press('enter')
    time.sleep(0.5)
    keyboard.press_and_release('ctrl+s')
    
if __name__ == "__main__":
    while True : 
        main()
