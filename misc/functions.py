import csv
import secrets

def generate_secret_token_hex(nbytes: int = 16) -> str:
    return secrets.token_hex(nbytes)


def get_trends() -> dict:
    trends = {}

    with open('misc/trends.csv') as csvfile:
        csvfile.readline()
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            if row[2] in trends:
                trends[row[2]].append((row[3], row[4]))
            else:
                trends[row[2]] = [(row[3], row[4])]

    return trends
