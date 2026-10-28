# Text Mining – Amazon Reviews

Gruppmedlemmar - Dariel Riera Carrillo, Miralem Idriz, Mst Anarkoli, Rasmus Svensson, Salam Lababneh och Ummulbanin.

## Om projektet

I det här grupparbetet analyserar vi produktrecensioner från Amazon inom kategorin All Beauty.

Syftet är att använda textanalys och maskininlärning för att klassificera recensioner som positiva, negativa eller neutrala. Vi jämför två olika modeller och undersöker även om det finns något samband mellan produktpris och sentiment.

## Tänkt användare

Den tänkta användaren är exempelvis en produktansvarig
eller dataanalytiker som vill få en snabb överblick över
vad kunderna tycker om olika produkter.

Med hjälp av sentimentanalysen kan användaren se om
recensionerna är positiva, negativa eller neutrala
utan att behöva läsa varje recension manuellt.

Resultaten kan användas som stöd för att förstå
kundernas upplevelser och förbättra produkter.

## Projektets delar

Projektet är uppdelat i sex block:

1. **Datainspektion** – Vi undersöker datasetet och kontrollerar datakvaliteten.
2. **Textförbehandling** – Vi rensar recensionstexterna och använder TF-IDF för att omvandla text till numeriska värden.
3. **Logistisk regression** – Vi tränar en första modell för sentimentklassificering.
4. **Naive Bayes och modelljämförelse** – Vi tränar en andra modell och jämför resultaten på samma testdata.
5. **Utvärdering och felanalys** – Vi analyserar modellernas resultat med bland annat confusion matrix och undersöker felklassificerade recensioner.
6. **Prisanalys** – Vi undersöker hur sentiment och genomsnittliga betyg skiljer sig mellan olika prissegment.

Del 4 och 5 finns i samma notebook.

## Datakälla

Vi använder datasetet Amazon Reviews 2023 från McAuley Lab,
med fokus på kategorin All_Beauty.

Datasetet innehåller kundrecensioner, stjärnbetyg och
produktinformation som används för sentiment- och prisanalys.

Datakällan finns här:
https://amazon-reviews-2023.github.io/

## Projektstruktur

```text
text_mining_amazon_reviews/
├── data/
│   ├── raw/
│   └── processed/
├── models/
├── notebooks/
│   ├── 01_data_inspection.ipynb
│   ├── 02_text_preprocessing.ipynb
│   ├── 03_baseline_logistic_regression.ipynb
│   ├── 04_naive_bayes_comparison.ipynb
│   └── 06_price_analysis.ipynb
├── outputs/
├── scripts/
├── DATA_SETUP.md
├── README.md
└── requirements.txt
```

## Installation och körning

**1. Klona projektet från GitHub.**

**2. Öppna projektet i VS Code.**

**3. Skapa en virtuell Python-miljö:**

```bash
python -m venv .venv
```

**4. Aktivera miljön (Windows):**

```bash
.venv\Scripts\activate
```

**5. Installera biblioteken:**

```bash
python -m pip install -r requirements.txt
```

**6. Förbered datan.**

Följ instruktionerna i [DATA_SETUP.md](DATA_SETUP.md) för att ladda ner datasetet och skapa de bearbetade CSV-filerna.

**7. Kör notebookarna.**

Öppna mappen `notebooks` och kör analyserna i ordning. Välj projektets `.venv` som Python-miljö.

## Resultat från modelljämförelsen

Vi jämförde logistisk regression med Multinomial Naive Bayes på samma testdata.

| Modell | Accuracy | Macro F1 |
|---|---|---|
| Logistisk regression | 86,3 % | 0,648 |
| Naive Bayes | 84,4 % | 0,571 |

Logistisk regression presterade bäst på båda måtten.

Felanalysen visade att båda modellerna hade svårast att identifiera neutrala recensioner.

## Resultat från prisanalysen

Vi jämförde sentiment mellan produkter i olika prissegment.

- Andelen positiva recensioner var 72,9 % i det lägsta prissegmentet och 77,8 % i det högsta.
- Genomsnittsbetyget ökade från 4,04 till 4,18 stjärnor.
- De dyraste 10 % av produkterna hade en högre andel positiva recensioner än de billigaste 10 %.

Resultaten visar ett visst samband mellan pris och sentiment, men vi kan inte dra slutsatsen att ett högre pris orsakar mer positiva recensioner.

## Begränsningar

Projektet har några begränsningar:

- Vi använde ett urval på 100 000 recensioner från
  kategorin All_Beauty och inte hela Amazons dataset.

- Sentimentklasserna baserades på stjärnbetygen.
  Ett högt betyg behöver inte alltid betyda att
  recensionstexten är positiv.

- Modellerna hade svårast att klassificera neutrala
  recensioner, vilket påverkade resultaten.

- Prisanalysen visade ett visst samband mellan pris
  och sentiment, men det betyder inte att högre
  priser orsakar mer positiva recensioner.

## Sammanfattning

Projektet visar hur textförbehandling och maskininlärning kan användas för att analysera kundrecensioner.

Logistisk regression gav bäst resultat i modelljämförelsen, medan prisanalysen visade mindre skillnader i sentiment mellan olika prissegment.

En viktig lärdom är att det inte räcker att enbart titta på accuracy. Vi behöver också undersöka vilka typer av recensioner modellerna har svårt att klassificera.

## Användning av generativ AI

Generativ AI har inte använts som en gemensam metod
för gruppens analyser eller beslut.

Eventuell individuell användning av AI som stöd för
exempelvis kodförståelse och felsökning redovisas
separat av respektive gruppmedlem.

## Licens och användningsvillkor

Projektet använder Amazon Reviews 2023 från McAuley Lab.

Datasetet används i utbildningssyfte.
Rådata och genererade CSV-filer laddas inte upp
till GitHub.

Datakälla:
https://amazon-reviews-2023.github.io/

För information om datasetets användningsvillkor,
se den officiella källan.

Ingen separat licens har valts för projektets kod.

