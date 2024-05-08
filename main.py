from abc import ABC, abstractmethod
import datetime

class Szoba(ABC):
    def __init__(self, ar, szobaszam):
        self.ar = ar
        self.szobaszam = szobaszam

class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(ar=15000, szobaszam=szobaszam)

class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(ar=20000, szobaszam=szobaszam)

class HaromagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(ar=25000, szobaszam=szobaszam)

class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.foglalasok = []

    def szoba_hozzaadas(self, szoba):
        self.szobak.append(szoba)

    def szoba_foglalas(self, szobaszam, datum):
        foglalasi_datum = datetime.datetime.strptime(datum, "%Y-%m-%d")
        if foglalasi_datum <= datetime.datetime.now():
            print("A megadott dátum nem jövőbeli. Kérem, adjon meg egy jövőbeli dátumot.")
            return None
        
        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam:
                for foglalas in self.foglalasok:
                    if foglalas.szoba.szobaszam == szobaszam and foglalas.datum == datum:
                        print("Ez a szoba már foglalt ezen a napon.")
                        return None
                foglalas = Foglalas(szoba, datum)
                self.foglalasok.append(foglalas)
                return foglalas.szoba.ar
        print("Nem található szoba a megadott szobaszámmal.")
        return None

    def foglalas_lemondas(self, szobaszam, datum):
        for foglalas in self.foglalasok:
            if foglalas.szoba.szobaszam == szobaszam and foglalas.datum == datum:
                self.foglalasok.remove(foglalas)
                return True
        return False  

    def foglalasok_listazasa(self):
        return [(foglalas.szoba.szobaszam, foglalas.datum) for foglalas in self.foglalasok]

class Foglalas:
    def __init__(self, szoba, datum):
        self.szoba = szoba
        self.datum = datum

def main_menu():
    while True:
        print("\nÜdvözöljük a Szalloda Foglalási Rendszerben!")
        print("1. Szoba foglalása")
        print("2. Foglalás lemondása")
        print("3. Foglalások listázása")
        print("4. Kilépés")
        choice = input("Kérjük, válasszon egy opciót (1-4): ")

        if choice == "1":
            szobaszam = input("Adja meg a szobaszámot: ")
            datum = input("Adja meg a foglalás dátumát (éééé-hh-nn): ")
            try:
                ar = szalloda.szoba_foglalas(int(szobaszam), datum)
                if ar:
                    print(f"A foglalás sikeres. Az ár: {ar} Ft")
                else:
                    print("Hiba: Nem létező szobaszám vagy a szoba már foglalt.")
            except ValueError:
                print("Érvénytelen szobaszám vagy dátum formátum!")
        elif choice == "2":
            szobaszam = input("Adja meg a szobaszámot, amit le szeretne mondani: ")
            datum = input("Adja meg a foglalás dátumát (éééé-hh-nn): ")
            sikeres_lemondas = szalloda.foglalas_lemondas(int(szobaszam), datum)
            if sikeres_lemondas:
                print("A foglalás sikeresen lemondva.")
            else:
                print("Nincs ilyen foglalás.")
        elif choice == "3":
            foglalasok = szalloda.foglalasok_listazasa()
            if foglalasok:
                print("Aktuális foglalások:")
                for f in foglalasok:
                    print(f"Szobaszám: {f[0]}, Dátum: {f[1]}")
            else:
                print("Nincsenek jelenlegi foglalások.")
        elif choice == "4":
            print("Kilépés a programból.")
            break
        else:
            print("Érvénytelen választás, próbálja újra!")

if __name__ == "__main__":
    szalloda = Szalloda("Balaton Hotel")
    szalloda.szoba_hozzaadas(EgyagyasSzoba(szobaszam=101))
    szalloda.szoba_hozzaadas(KetagyasSzoba(szobaszam=102))
    szalloda.szoba_hozzaadas(HaromagyasSzoba(szobaszam=103))
    szalloda.szoba_foglalas(101, "2024-06-10")
    szalloda.szoba_foglalas(102, "2024-06-11")
    szalloda.szoba_foglalas(103, "2024-06-12")
    szalloda.szoba_foglalas(101, "2024-06-13")
    szalloda.szoba_foglalas(102, "2024-06-14")
    main_menu()
