import csv
import secrets

def generate_secret_token_hex(nbytes: int = 16) -> str:
    return secrets.token_hex(nbytes)


def get_trends() -> dict:
    trends = {}

    with open('misc/trends.csv', encoding='utf-8') as csvfile:
        csvfile.readline()
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            if row[0] in ['Russia', 'Global']:
                try:
                    if row[1] in trends:
                        if row[2] in trends[row[1]]:
                            trends[row[1]][row[2]].append((row[3], row[4]))
                        else:
                            trends[row[1]][row[2]] = [(row[3], row[4])]
                    else:
                        trends[row[1]] = {row[2]: [(row[3], row[4])]}
                except:
                    pass

    return trends
