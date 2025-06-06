import random
import os

'''
Program do generowania losowej sekwencji DNA i zapisywania jej w formacie FASTA
 
Użytkownik podaje długość sekwencji, identyfikator (ID), opis oraz swoje imię
Program:
 - generuje losową sekwencję nukleotydową (A, C, G, T),
 - losowo wstawia imię użytkownika do sekwencji,
 - oblicza statystyki zawartości nukleotydów oraz %CG,
 - zapisuje dane do pliku FASTA z odpowiednim nagłówkiem
 
 Przeznaczenie:
  - nauka przetwarzania danych biologicznych,
  - ćwiczenia z pracy na plikach, losowością i walidacją danych'
  - wprowadzenie do bioinformatyki i operacji na sekwencjach DNA
  '''



def generate_random_sequence(length: int) -> str:
    """
    Generuje losową sekwencję DNA o zadanej długości
    Args:
        length (int): Długość żądanej sekwencji DNA. Musi być > 0
    Returns:
        str: Sekwencja DNA złożona z losowych nukleotydów A, C, G, T
    Raises:
        ValueError: Jeśli długość jest mniejsza lub równa 0
    """

    #ORIGINAL
    #brak

    #MODIFIED (zabeczpiecznie przed złym parametrem długości sekwencji)
    if length <= 0:                                                         # sprawdza czy podana wartość jest dodatnia
        raise ValueError("Długość sekwencji musi być większa niż 0")        # jesli nie, rzuca wyjątek o złym parametrze


    nucleotides = ['A', 'C', 'G', 'T']                                      # Lista możliwych nukleotydów do generowania sekwencji

    return ''.join(random.choice(nucleotides) for _ in range(length))       # Zwraca sekwencję DNA jako ciąg losowo wybranych nukleotydów



def calculate_statistics(sequence: str):
    """
    Oblicza statystyki procentowe zawartości nukleotydów i procent CG
    Args:
        sequence (str): Sekwencja DNA
    Returns:
        tuple:
             - dict: Procentowy udział A, C, G, T w sekwencji
            - float: Procent całkowitej zawartości C i G (CG)
    """

    length = len(sequence)                                                              # Oblicza długość sekwencji
    counts = {nucleotide: sequence.count(nucleotide) for nucleotide in "ACGT"}          # Liczy wystąpienia każdego nukleotydu w sekwencji
    percentages = {k: (v / length) * 100 for k, v in counts.items()}                    # Oblicza procentowy udział każdego nukleotydu

    #ORIGINAL
    #cg_at_ratio = (counts['C'] + counts['G']) / (counts['A'] + counts['T']) if counts['A'] + counts['T'] > 0 else 0

    #MODIFIED (Zmiana obliczania %CG: Zamiast obliczania stosunku CG/AT, zmodyfikowano kod w celu obliczenia klasycznego procentu zawartości cytozyny i guaniny w całej sekwencji DNA)
    cg_percentage = ((counts['C'] + counts['G']) / length) * 100 if length > 0 else 0   # Oblicza procent CG w całej sekwencji

    return percentages, cg_percentage                                                   # Zwraca słownik z procentami oraz wartość CG




def insert_name_in_sequence(sequence: str, name: str) -> str:
    """
    Wstawia imię w losowe miejsce sekwencji DNA
    Args:
        sequence (str): Oryginalna sekwencja DNA
        name (str): Imię do wstawienia
    Returns:
        str: Sekwencja z imieniem w losowym miejscu
    """
    insert_position = random.randint(0, len(sequence))                              # Losuje pozycję, gdzie wstawi imię w sekwencji
    return sequence[:insert_position] + name + sequence[insert_position:]              # Wstawia imię w wybranej pozycji



#ORIGINAL
# brak

#MODIFIED (dodanie metody sprawdzającej czy sekwencja o danym identyfikatorze juz nie istnieje, zapewnia spójność danych)
def sequence_file_exists(seq_id: str, directory: str = ".") -> bool:
    """
    Sprawdza, czy plik FASTA o danym ID już istnieje w katalogu
    Args:
        seq_id (str): Identyfikator sekwencji
        directory (str, optional): Katalog, w którym szukać pliku. Domyślnie bieżący
    Returns:
        bool: True, jeśli plik nie istnieje
    Raises:
        ValueError: Jeśli plik o tej nazwie już istnieje
    """
    fasta_filename = os.path.join(directory, f"{seq_id}.fasta")           # Tworzy pełną ścieżkę do pliku na podstawie ID

    if os.path.isfile(fasta_filename):                                    # Sprawdza, czy plik już istnieje
        raise ValueError(f"Plik '{fasta_filename}' już istnieje.")        # Jeśli tak, rzuca wyjątek





def main():
    try:
        seq_length = int(input("Podaj długość sekwencji: "))        # Prosi użytkownika o długość sekwencji
        dna_sequence = generate_random_sequence(seq_length)         # Generuje sekwencję DNA

        seq_id = input("Podaj ID sekwencji: ")                      # Prosi użytkownika o identyfikator sekwencji
        sequence_file_exists(seq_id)                                # Sprawdza, czy plik o takim ID już istnieje
    except ValueError as e :                                        # Obsługuje błędy (np. zła liczba lub istniejący plik)
        print(f"Błąd: {e}")                                         # Wyświetla komunikat o błędzie
        return                                                      # Kończy działanie programu w przypadku błędu


    seq_description = input("Podaj opis sekwencji: ")               # Pobiera opis sekwencji od użytkownika
    user_name = input("Podaj imię: ")                               # Pobiera imię użytkownika


    sequence_with_name = insert_name_in_sequence(dna_sequence, user_name)       # Wstawia imię do losowego miejsca w sekwencji
    stats, cg_percentage = calculate_statistics(dna_sequence)                   # Oblicz statystyki dla sekwencji


    '''Zapisanie sekwencji do pliku w formacie FASTA'''
    fasta_filename = f"{seq_id}.fasta"                                          # Nazwa pliku wynikowego
    with open(fasta_filename, "w") as fasta_file:                               # Otwiera plik do zapisu
        fasta_file.write(f">{seq_id} {seq_description}\n")                      # Zapisuje nagłówek FASTA

        for i in range(0, len(sequence_with_name), 80):                         # Zapisuje sekwencję z imieniem, dzieląc ją na linie po maks. 80 znaków
            fasta_file.write(sequence_with_name[i:i + 80] + "\n")


    print(f"\nSekwencja została zapisana do pliku {fasta_filename}")              # Wyświetla informacje o zapisie sekwencji do pliku


    # Wyświetla statystyki
    print("Statystyki sekwencji:")
    for nucleotide, percentage in stats.items():           # Dla każdego nukleotydu wyświetla procent
        print(f"{nucleotide}: {percentage:.2f}%")

    print(f"%CG: {cg_percentage:.2f}")                     # Wyświetla procent CG


if __name__ == "__main__":
    main()                                                 # Uruchomienie main'a
