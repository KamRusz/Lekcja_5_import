import sys

obiekty = []
suma_saldo = 0
towary = {}


def czytaj_sys():
    opcje = sys.argv[1:]
    if len(opcje)>=1:
        sciezka = opcje[0]
    else:
        print("nie podano argumentów")
        sciezka=None    
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
           

class Sprzedaz:
    def __init__(self):
        self.rodzaj = "sprzedaz"
        self.id = ""
        self.cena = 0
        self.liczba = 0

    def pobor_danych(self, operacje, i, suma_saldo, towary):
        if operacje[i+1] not in towary:
            print (f"\nnie mamy na stanie {identyfikator}\n") 
        else:
            self.id = operacje[i+1]
            self.cena = int(operacje[i+2])
            if towary[operacje[i+1]] - int(operacje[i+3]) < 0:
                print (f"nie wystarczająca ilość {identyfikator} na stanie")
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
            if typ not in typy:
                break
                print("zonk")
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
 