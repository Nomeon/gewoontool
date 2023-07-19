## Algemeen:
Om te zorgen dat de python code uitgevoerd kan worden, zijn er verschillende extensies nodig. Deze worden beheerd door een [conda omgeving](https://docs.conda.io/projects/conda/en/stable/). Conda beheert de python versie en maakt een lokale omgeving aan met de juiste extensies (packages) geinstalleerd. Dit zorgt ervoor dat alleen de tools die nodig zijn verpakt worden in de .exe, en het maakt het makkelijker om een dev omgeving op te zetten. Verder is [VS Code](https://code.visualstudio.com/download) aan te raden als editor, met de extensies Pylance en Python. Deze zijn te installeren in VS Code zelf onder het kopje Extensions.

## Installatie dev tools:
Allereerst moet [Miniconda3](https://docs.conda.io/en/latest/miniconda.html) gedownload worden. Open de pagina en download en installeer Miniconda3, Python version 3.10 onder het kopje Windows Installers.

Vervolgens kan een nieuwe Anaconda Prompt (Anaconda3) geopend worden door in Windows te zoeken op Anaconda Prompt. Dit zou een nieuwe "Command Prompt" lijkende window moeten openen. Kopieër via de verkenner het pad naar de map waar 'gewoontool' staat (bv: 'C:\Users\DN51\Desktop\gewoontool'), en gebruik de command:
```sh
cd C:\Users\DN51\Desktop\gewoontool
```
Met uiteraarde de juist padnaam voor het mapje.

Vervolgens wordt met één command de juiste Python versie, en alle extensies geinstalleerd in een nieuwe omgeving:
```sh
conda env create -f environment.yml
```

Als deze correct geinstalleerd is, kan de omgeving geactiveerd worden met:
```sh
conda activate gewoontool
```

Vervolgens kan de app gestart worden met twee commands:
```sh
cd gewoontool
python app.py
```

Om de .exe te maken wordt gebruik gemaakt van een .spec file. Hierin staan alle benodigdheden en specificaties om de tool te maken. De .exe kan genereert worden met de command:
```sh
pyinstaller geWOONtool.spec
```
De .exe kan hierna gevonden worden in de dist folder.
