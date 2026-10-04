# Så fixar ni datan lokalt

Vi lägger **inte** upp rådatan eller de genererade CSV-filerna på GitHub eftersom filerna är stora och för att undvika att redistribuera datasetet direkt då vi inte vet om det finns licens eller liknande på det.

1. Ladda ner datan

Gå till:
https://amazon-reviews-2023.github.io/

Leta upp kategorin:
`All_Beauty`

Ladda ner:
- `review`
- `meta`

Filerna laddas ner som `.jsonl.gz`.

Packa upp dem så att ni får:
`All_Beauty.jsonl`
`meta_All_Beauty.jsonl`

Lägg båda i:
`data/raw/`

Så här ska de se ut:

data/
└── raw/
    ├── .gitkeep **Behåll gitkeep filerna för att strukturen av mapparna ska bevaras**
    ├── All_Beauty.jsonl
    └── meta_All_Beauty.jsonl

2. Installera projektets paket och skapa miljö

Öppna terminalen i projektets huvudmapp.

Skapa en virtuell miljö som vanligt:
`python -m venv .venv`

Aktivera miljön:
`.venv\Scripts\activate`

När miljön är aktiv ska `(.venv)` synas i början av terminalraden.

Installera sedan projektets paket:

`python -m pip install -r requirements.txt`

3. Skapa den bearbetade datan

När råfilerna ligger i `data/raw/` och miljön är aktiv kör ni:

`python scripts/prepare_data.py`

Scriptet läser in rådatan, rensar den och skapar två filer automatiskt:

`data/processed/all_beauty_cleaned.csv`

`data/processed/all_beauty_sample_100k.csv`

`all_beauty_cleaned.csv` innehåller hela den rensade review-datan.

`all_beauty_sample_100k.csv` innehåller ett reproducerbart sample på 100 000 recensioner med ungefär samma sentimentfördelning som hela datasetet.

**Viktigt:** Om ni öppnar CSV-filerna i VS Code kan ni få upp en ruta med "Unusual Line Terminators". Välj **Ignore** och inte "Remove Unusual Line Terminators", eftersom filinnehållet annars kan ändras manuellt.

Så här ska det ungefär se ut efter att scriptet har körts:

data/
├── raw/
│   ├── .gitkeep
│   ├── All_Beauty.jsonl
│   └── meta_All_Beauty.jsonl
└── processed/
    ├── .gitkeep
    ├── all_beauty_cleaned.csv
    └── all_beauty_sample_100k.csv

Både raw- och processed-filerna är ignorerade av Git och ska alltså inte pushas till GitHub.

4. Viktigt när de genererade CSV-filerna läses in

När ni läser in någon av de genererade CSV-filerna med pandas ska ni använda:

`keep_default_na=False`

Exempel:

```python
import pandas as pd

reviews = pd.read_csv(
    "data/processed/all_beauty_sample_100k.csv",
    keep_default_na=False,
)
```

Det behövs eftersom det finns riktiga recensioner med text som `NA`, `N/A` och `None`.

Utan `keep_default_na=False` kan pandas tolka dessa som saknade värden trots att de egentligen är vanlig recensionstext.

5. Vilken fil ska vi använda?

Under utvecklingen använder vi främst:

`all_beauty_sample_100k.csv`

Den är mindre och snabbare att arbeta med eftersom den innehåller 100 000 recensioner.

Den fullständiga datan finns också lokalt i:

`all_beauty_cleaned.csv`

Den kan senare användas om vi vill köra en större/slutlig analys på all data.

6. Om något inte fungerar

Kontrollera först att:
- `.venv` är aktiverad
- `requirements.txt` har installerats
- `All_Beauty.jsonl` och `meta_All_Beauty.jsonl` ligger i `data/raw/` korrekt enligt strukturen ovan
- scriptet körs från projektets huvudmapp

Kör sedan scriptet igen:
`python scripts/prepare_data.py`