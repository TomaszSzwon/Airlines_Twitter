import requests
import pandas as pd
import re

# Pobranie pliku CSV z GITa
url = "https://raw.githubusercontent.com/TomaszSzwon/Airlines_Twitter/main/Tweets_noisy.csv"
input_file = "Tweets_noisy.csv"
output_file = "Tweets_cleaned.csv"

response = requests.get(url)
response.encoding = 'mac_roman'
with open(input_file, "w", encoding="utf-8") as outfile:
    outfile.write(response.text)

print(f"Pobrano plik: {input_file}")

# Czyszczenie danych
cleaned_lines = []
with open(input_file, "r", encoding="utf-8") as infile:
    lines = infile.readlines()

for line in lines:
    line = line.strip()
    line = re.sub(r'";{6,}[\r\n]*$', '', line)
    line = re.sub(r'^"', '', line)
    line = re.sub(r'[";]+$', '', line)
    line = re.sub(r'""', '"', line)
    line = re.sub(r'";', ';', line)
    line = re.sub(r';"', ';', line)
    line = re.sub(r'&amp";?', '&amp;', line)
    line = re.sub(r'&gt"', '&gt', line)
    line = re.sub(r'\bhte\b', 'the', line)
    line = re.sub(r'\banohter\b', 'another', line)
    line = re.sub(r'\bhtey\b', 'they', line)
    line = re.sub(r'null', 'Thank', line)
    line = re.sub(r'(?<=,)(\[)', r'"[', line)
    line = re.sub(r'(o])', r']"', line)
    cleaned_lines.append(line)

with open(output_file, "w", encoding="utf-8") as outfile:
    outfile.write("\n".join(cleaned_lines) + "\n")

print(f"Plik oczyszczony i zapisany jako {output_file}")

# Wczytaj do Pandas
df = pd.read_csv(output_file, delimiter=',', on_bad_lines='skip')

# Usuń strefę czasową
df["tweet_created"] = df["tweet_created"].str.split(" -").str[0]

# Konwersja do formatu daty
df["tweet_created"] = pd.to_datetime(df["tweet_created"], errors='coerce')

# Usunięcie wzmiankowań (@username)
df["text"] = df["text"].str.replace(r"@\w+", "", regex=True)

# Usunięcie emotikonów i znaków spoza ASCII (jeśli SSIS ma problem z Unicode)
df["text"] = df["text"].str.encode("ascii", "ignore").str.decode("utf-8")

# Zamiana wielokrotnych spacji na pojedynczą
df["text"] = df["text"].str.replace(r"\s+", " ", regex=True).str.strip()

# Usunięcie \r\n w negativereason_gold
df["negativereason_gold"] = df["negativereason_gold"].astype(str).str.replace(r"\r\n", " ", regex=True)

# Usunięcie HTML-owe encji, linki i poprawi typowe literówki:
df['text'] = df['text'].str.replace(r'&amp;', '&', regex=True).str.replace(r'&lt;', '<', regex=True).str.replace(r'&gt;', '>', regex=True).str.replace(r'http\S+', '', regex=True).str.replace(r'\s+', ' ', regex=True).str.strip()

# Zapisz końcowy plik
final_output = "Tweets_final_cleaned.csv"
df.to_csv(final_output, index=False)

print(f"Plik finalny zapisany jako {final_output}")