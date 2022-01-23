from settings2 import czytaj_sys, Saldo, zapytanie_log, glowna_petla, wczytywanie_danych

obj = Saldo()
sciezka, opcje = czytaj_sys()
towary, obiekty, suma_saldo, operacje_zatwierdzone = glowna_petla(sciezka)

obj.dopisz_log(operacje_zatwierdzone, opcje, suma_saldo, obiekty, sciezka)

