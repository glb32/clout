#importujeme potrebne knihovny
import _thread
import time
from pygame import mixer
import hoangAI
#funkce zvuku (nacte si prehravac, nacte si mp3 soubor a prehraje ho
def zvuk():
    mixer.init()
    mixer.music.load("")
    mixer.music.play()
    #pokud hoangAI ukonci svuj beh, vypneme program
    if hoangAI.start():
        mixer.music.stop()
        print("vypinam...")
        time.sleep(2)
        exit(0)


# samotna funkce budiku, vypise za jak dlouho se budik zapne a pocka nez je cas na start zvuku neboli aktivniho buzeni
def budik(pocet_sekund):
    print(" Do zvoneni zbyva ", pocet_sekund, "sekund")
    time.sleep(pocet_sekund)
    print("VSTAVAT A CVICIT, VSTAVAT A CVICIT!!\n")
    zvuk()

# ziska vstup od uzivatele (tedy casouou jednotku a cas v dane casove jednotce)
def vstup(uzivatel_vstup):

    pocet_sekund = 0
    if uzivatel_vstup == "1":
        uzivatel_vstup = int(input("Zadej za kolik hodin chces byt vzbuzen/a"))
        pocet_sekund = (uzivatel_vstup * 60) * 60
    elif uzivatel_vstup == "2":
        uzivatel_vstup = int(input("Zadej za kolik minut chces byt vzbuzen/a"))
        pocet_sekund = uzivatel_vstup * 60
    elif uzivatel_vstup == "3":
        uzivatel_vstup = int(input("Zadej za kolik sekund chces byt vzbuzen/a"))
        pocet_sekund = uzivatel_vstup
    elif uzivatel_vstup == "4":
        hodiny = int(input("hodiny"))
        minuty = int(input("minuty"))
        sekundy = int(input("sekundy"))
        pocet_sekund = ((hodiny * 60) * 60) + (minuty * 60) + sekundy
        print(pocet_sekund)
    #pokud uzivatel zada slovo 'konec' tak ukoncime program
    elif uzivatel_vstup == "konec":

        print("vypinam...")
        time.sleep(2)
        exit(0)
    #pokud pri vyberu casu uzivatel zada spatne cislo tak ukoncime program
    elif uzivatel_vstup <= 0 :
        print("zadali jste nespravnou hodnotu, zadejte hodnotu mezi 1 az 4")

    else:
        pocet_sekund = 0
        exit(0)

    return pocet_sekund

#nastavi budik
def nastav_budik():
    uzivatel_vstup = input(
        "Za jaku jednotku casu chces budik zapnout\n (1)Hodiny\n (2)Minuty\n (3)Sekundy\n (4)Hodiny,Minuty a sekundy dohromady\n")
    pocetsekund = vstup(uzivatel_vstup)
    _thread.start_new_thread(budik, (pocetsekund,))
#dokud program bezi, tak se nastavuji budiky( vola funkci)
def main():
    #vypise uzivateli zacatek programu
    print("Budik(TM) v.1.0.0....")
    print("pro ukonceni zadej 'konec'")

    while True:
        nastav_budik()


main()
