#importujeme potrebne knihovny
import _thread
import sys
import time
from pygame import mixer
import hoangAI
#funkce zvuku (nacte si prehravac, nacte si mp3 soubor a prehraje ho
def zvuk():
    mixer.init()
    mixer.music.load("bid.mp3")
    mixer.music.play()
    #pokud hoangAI ukonci svuj beh, vypneme program
    if hoangAI.start():
        mixer.music.stop()
        print("vypinam...")
        time.sleep(2)
        exit(0)


# samotna funkce budiku, vypise za jak dlouho se budik zapne a pocka nez je cas na start zvuku neboli aktivniho buzeni
def budik(pocet_sekund):
    pocet_hodin = sys.argv[1]
    print(" Do zvoneni zbyva ",pocet_hodin,"hodin")
    time.sleep(pocet_sekund)
    print("VSTAVAT A CVICIT, VSTAVAT A CVICIT!!\n")
    zvuk()


#nastavi budik
def nastav_budik():
    data = sys.argv[1]
    try:
        pocetsekund = float(data) * 60
    except ValueError:
        print("prosim zadejte spravne casovou jednotku (napr. 1)")
        exit(1)

    _thread.start_new_thread(budik(pocetsekund))

#dokud program bezi, tak se nastavuji budiky( vola funkci)
def main():
    #vypise uzivateli zacatek programu
    print("Budik(TM) v.1.0.0....")
    print("pro ukonceni programu stisknete ctrl+c")
    try:
        nastav_budik()
    except KeyboardInterrupt:
        print("konec programu")
        exit(0)

if len(sys.argv) !=2:
    print("nezadali jste casovou jednotku\n priklad pouziti programu: python3 budik.py 1 (pocet hodin, za ktere se ma budik aktivovat)")
    exit(0)



main()
