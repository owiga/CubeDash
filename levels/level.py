import csv


def level(numero):
    with open(f"levels/level{numero}.csv", mode="r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=';')
        return list(reader)


