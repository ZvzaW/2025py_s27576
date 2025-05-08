import random


def generate_random_sequence(length: int) -> str:
    """Generuje losową sekwencję DNA"""
    #ORIGINAL
    #brak

    #MODIFIED (zabeczpiecznie przed złym parametrem długości sekwencji)
    if length <= 0:
        raise ValueError("Długość sekwencji musi być większa niż 0")


    nucleotides = ['A', 'C', 'G', 'T']
    return ''.join(random.choice(nucleotides) for _ in range(length))


def calculate_statistics(sequence: str):
    """Oblicza statystyki sekwencji DNA."""
    length = len(sequence)
    counts = {nucleotide: sequence.count(nucleotide) for nucleotide in "ACGT"}
    percentages = {k: (v / length) * 100 for k, v in counts.items()}

    #ORIGINAL
    #cg_at_ratio = (counts['C'] + counts['G']) / (counts['A'] + counts['T']) if counts['A'] + counts['T'] > 0 else 0

    #MODIFIED (Zmiana obliczania %CG: Zamiast obliczania stosunku CG/AT, zmodyfikowano kod w celu obliczenia klasycznego procentu zawartości cytozyny i guaniny w całej sekwencji DNA)
    cg_percentage = ((counts['C'] + counts['G']) / length) * 100 if length > 0 else 0

    return percentages, cg_percentage


def insert_name_in_sequence(sequence: str, name: str) -> str:
    """Wstawia imię w losowe miejsce sekwencji."""
    insert_position = random.randint(0, len(sequence))
    return sequence[:insert_position] + name + sequence[insert_position:]


def main():
    try:
        seq_length = int(input("Podaj długość sekwencji: "))
        dna_sequence = generate_random_sequence(seq_length)
    except ValueError as e :
        print(f"Błąd: {e}")
        return

    # Pobierz dane od użytkownika
    seq_id = input("Podaj ID sekwencji: ")
    seq_description = input("Podaj opis sekwencji: ")
    user_name = input("Podaj imię: ")

    # Generuj losową sekwencję DNA


    # Wstaw imię do losowego miejsca w sekwencji
    sequence_with_name = insert_name_in_sequence(dna_sequence, user_name)

    # Oblicz statystyki dla sekwencji
    stats, cg_percentage = calculate_statistics(dna_sequence)

    # Zapisz sekwencję do pliku w formacie FASTA
    fasta_filename = f"{seq_id}.fasta"
    with open(fasta_filename, "w") as fasta_file:
        fasta_file.write(f">{seq_id} {seq_description}\n")
        # Dodaj sekwencję z imieniem - każda linia w pliku FASTA powinna mieć do 80 znaków
        for i in range(0, len(sequence_with_name), 80):
            fasta_file.write(sequence_with_name[i:i + 80] + "\n")

    print(f"Sekwencja została zapisana w pliku: {fasta_filename}")

    # Wyświetl statystyki
    print("\nStatystyki sekwencji:")
    for nucleotide, percentage in stats.items():
        print(f"{nucleotide}: {percentage:.2f}%")
    print(f"%CG: {cg_percentage:.2f}")


if __name__ == "__main__":
    main()
