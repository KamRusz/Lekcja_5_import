import sys

obiekty = []
suma_saldo = 0
towary = {}

def czytaj_sys():
    try:
        opcje = sys.argv[1:]
        sciezka = opcje[0]
    except IndexError:
        print("nie podano argumentów")
        sciezka = None
    else:
        opcje = sys.argv[1:]
        sciezka = opcje[0]
    return sciezka, opcje

def wczytywanie_danych(sciezka):
    if not sciezka:
        print("nie podano argumentów")
    else:
        with open(f"{sciezka}") as baza:
            operacje = []
            for line in baza:
                operacje.append(line.strip())
            return operacje 


class Saldo:
    def __init__(self):
        self.rodzaj = "saldo"
        self.wartosc = 0
        self.komentarz = ""

    def pobor_danych(self, operacje, i, suma_saldo, towary):
        self.wartosc = int(operacje[i+1])
        if suma_saldo:
            suma_saldo += int(self.wartosc)
        else:
            suma_saldo = int(self.wartosc)   
        self.komentarz = operacje[i+2]
        i+=3
        return int(i), int(suma_saldo)
     
    def tworz_liste(self, operacje_zatwierdzone):
        operacje_zatwierdzone.append(self.rodzaj) 
        operacje_zatwierdzone.append(self.wartosc)  
        operacje_zatwierdzone.append(self.komentarz) 

    def dopisz_log(self, operacje_zatwierdzone, opcje, suma_saldo, obiekty, sciezka):
        if len(opcje)<3:
            print("za mało argumentów")
        else:
            self.wartosc = opcje[1]
            self.komentarz = opcje[2]
            if suma_saldo + int(self.wartosc) >=0:
                obiekty.append(self)
                operacje_zatwierdzone.append(self.rodzaj) 
                operacje_zatwierdzone.append(self.wartosc) 
                operacje_zatwierdzone.append(self.komentarz) 
                with open(f"{sciezka}", "a") as baza:
                    baza.write("\n") 
                    baza.write(f"{self.rodzaj}\n") 
                    baza.write(f"{self.wartosc}\n") 
                    baza.write(f"{self.komentarz}") 
            else:
                print("saldo nie może być ujemne!")
           

class Sprzedaz:
    def __init__(self):
        self.rodzaj = "sprzedaz"
        self.id = ""
        self.cena = 0
        self.liczba = 0

    def pobor_danych(self, operacje, i, suma_saldo, towary):
        if operacje[i+1] not in towary:
            print (f"\nnie mamy na stanie {self.id}\n") 
        else:
            self.id = operacje[i+1]
            self.cena = int(operacje[i+2])
            if towary[operacje[i+1]] - int(operacje[i+3]) < 0:
                print (f"nie wystarczająca ilość {self.id} na stanie")
            else:
                self.liczba = int(operacje[i+3])
                towary[self.id] -= self.liczba
                suma_saldo += int(self.cena) * int(self.liczba)
                i+=4
        return int(i), int(suma_saldo)

    def tworz_liste(self, operacje_zatwierdzone):
        operacje_zatwierdzone.append(self.rodzaj) 
        operacje_zatwierdzone.append(self.id)  
        operacje_zatwierdzone.append(self.cena) 
        operacje_zatwierdzone.append(self.liczba)

    def dopisz_log(self, operacje_zatwierdzone, opcje, suma_saldo, obiekty, sciezka, towary):
        if len(opcje)<4:
            print("za mało argumentów")
        else:
            self.id = opcje[1]
            self.cena = opcje[2]
            self.liczba = opcje[3]
            if self.id not in towary:
                print (f"\nw ogóle nie mamy na stanie {self.id}\n")
            else:
                if towary[self.id] - int(self.liczba) <0:
                    print(f"nie wystarczająca ilość {self.id} na stanie")
                else:
                    obiekty.append(self)
                    operacje_zatwierdzone.append(self.rodzaj) 
                    operacje_zatwierdzone.append(self.id) 
                    operacje_zatwierdzone.append(self.cena) 
                    operacje_zatwierdzone.append(self.liczba) 
                    with open(f"{sciezka}", "a") as baza:
                        baza.write("\n") 
                        baza.write(f"{self.rodzaj}\n") 
                        baza.write(f"{self.id}\n")
                        baza.write(f"{self.cena}\n")  
                        baza.write(f"{self.liczba}")     


class Zakup:
    def __init__(self):
        self.rodzaj = "zakup"
        self.id = ""
        self.cena = 0
        self.liczba = 0

    def pobor_danych(self, operacje, i, suma_saldo, towary):
        self.id = operacje[i+1]
        self.cena = int(operacje[i+2])
        self.liczba = int(operacje[i+3])
        if suma_saldo - self.cena * self.liczba <0:
            print("\nbłąd - saldo nie może być ujemne\n")
        else:
            suma_saldo -= self.cena * self.liczba 
            if self.id in towary:
                towary[self.id] += self.liczba
            else:
                towary[self.id] = self.liczba   
            i+=4
        return int(i), int(suma_saldo)

    def tworz_liste(self, operacje_zatwierdzone):
        operacje_zatwierdzone.append(self.rodzaj) 
        operacje_zatwierdzone.append(self.id)  
        operacje_zatwierdzone.append(self.cena) 
        operacje_zatwierdzone.append(self.liczba)  

    def dopisz_log(self, operacje_zatwierdzone, opcje, suma_saldo, obiekty, sciezka, towary):
        if len(opcje)<4:
            print("za mało argumentów")
        else:
            self.id = opcje[1]
            self.cena = opcje[2]
            self.liczba = opcje[3]
            if suma_saldo - int(self.cena) * int(self.liczba) < 0:
                print("\nbłąd - saldo nie może być ujemne\n")
            else:
                obiekty.append(self)
                operacje_zatwierdzone.append(self.rodzaj) 
                operacje_zatwierdzone.append(self.id) 
                operacje_zatwierdzone.append(self.cena) 
                operacje_zatwierdzone.append(self.liczba) 
                with open(f"{sciezka}", "a") as baza:
                    baza.write("\n") 
                    baza.write(f"{self.rodzaj}\n") 
                    baza.write(f"{self.id}\n")
                    baza.write(f"{self.cena}\n")  
                    baza.write(f"{self.liczba}")

   
typy = {"zakup":Zakup, "saldo":Saldo, "sprzedaz":Sprzedaz}


def glowna_petla(sciezka):
    i = 0 
    towary = {}
    obiekty = []
    operacje = wczytywanie_danych(sciezka)
    operacje_zatwierdzone = []
    suma_saldo = 0 
    if not sciezka:
        print("nie podano argumentów")
    else:    
        while i < len(operacje):
            typ = ""
            typ = operacje[i]
            if typ == "":
                i+=1
                continue
            if typ not in typy:
                print("zonk")
                break
            obj = typy[typ]()
            obj.pobor_danych(operacje, i, suma_saldo, towary)
            obj.tworz_liste(operacje_zatwierdzone)
            i, suma_saldo = obj.pobor_danych(operacje, i, suma_saldo, towary)
            obiekty.append(obj) 
        return towary, obiekty, suma_saldo, operacje_zatwierdzone

def zapytanie_magazynowe():
    sciezka, opcje = czytaj_sys()
    if len(opcje) == 1:
        print("nie podano towaru")
    else:    
        for i in opcje[1:]:
            towary, obiekty, suma_saldo, operacje_zatwierdzone = glowna_petla(sciezka)
            if i in towary:
                print(f"stan {i} wynosi: {towary[i]}")  
            else:
                print(f"stan {i} wynosi: 0")

def zapytanie_log():
    sciezka, opcje = czytaj_sys()
    towary, obiekty, suma_saldo, operacje_zatwierdzone = glowna_petla(sciezka)
    if len(opcje) < 2:
        print("nie podano argumentów")
    elif len(opcje) == 2:
        zakres_od = int(opcje[1])-1
        zakres_do = len(operacje_zatwierdzone)
        for i in range (int(zakres_od),int(zakres_do)):
            print(operacje_zatwierdzone[i]) 
    elif len(opcje) > 2:
        zakres_od = int(opcje[1])-1
        zakres_do = int(opcje[2])
        if zakres_do >= len(operacje_zatwierdzone):
            zakres_do = len(operacje_zatwierdzone)
        for i in range (int(zakres_od),int(zakres_do)):
            print(operacje_zatwierdzone[i]) 

def zapytanie_saldo():
    sciezka, opcje = czytaj_sys()
    if len(opcje)>=1:
        towary, obiekty, suma_saldo, operacje_zatwierdzone = glowna_petla(sciezka)
        print(f"Saldo wynosi {suma_saldo}")
 
def zapytanie_sprzedaz():
    sciezka, opcje = czytaj_sys()
    if len(opcje)>=1:
        towary, obiekty, suma_saldo, operacje_zatwierdzone = glowna_petla(sciezka)
        obj = Sprzedaz()
        obj.dopisz_log(operacje_zatwierdzone, opcje, suma_saldo, obiekty, sciezka, towary)

def zapytanie_zakup():
    sciezka, opcje = czytaj_sys()
    if len(opcje)>=1:
        towary, obiekty, suma_saldo, operacje_zatwierdzone = glowna_petla(sciezka)
        obj = Zakup()
        obj.dopisz_log(operacje_zatwierdzone, opcje, suma_saldo, obiekty, sciezka, towary)