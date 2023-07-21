geWOONtool Documentation
======================================

Gebruik:
---------

Allereerst is het belangrijk toegang te hebben tot de I: schijf; hier staan een aantal bestanden op die de tool 
automatisch inleest. Deze bestanden zijn nodig om de PDF te genereren en de categoriën te controleren bijvoorbeeld. 
Ook staan hier de icons voor de tool, en de overige bestanden die nodig zijn om er een .exe van te genereren.

Verder zijn er een paar extra bestanden nodig die per project aangepast dienen te worden. 
Het gaat hier om 2 extra bestanden: productcodes.csv en prioriteit.csv. Aangezien dit CSV bestanden zijn, hoort elke
regel met een comma gescheiden te zijn.

LET OP! De headers ("Productcode" en "Condition", "Value") moeten exact zo geschreven worden als hieronder.

* productcodes.csv
    In dit bestand staan de productcodes van de elementen die naar Boerboom gaan i.p.v. naar Van Hulst.
    Deze elementen zijn niet de elementen LVLQ 90, LVLQ 100 of LVLQ 144, maar de overige elementen die naar Boerboom gaan.
    De tool is zo ingericht dat alle elementen die hier in staan, uit de CSV van Van Hulst gehaald worden, en in de CSV
    van Boerboom gezet worden. Dit bestand wordt ingeladen via de knop "BB CSV". Dit bestand heeft de volgende structuur:

.. list-table:: productcodes.csv
    :widths: 100
    :header-rows: 1

    *   - Productcode
    *   - CE-000553-0009
    *   - CE-000151-0008
    *   - CE-000135-0006
    *   - UN-001446-0001
    *   - etc.

* prioriteit.csv
    In dit bestand staan de werkstations van dit project, met de bijbehorende prioriteiten. Alleen de modules die in een project
    horen hier in te staan. Dit bestand wordt ingeladen via de knop "Prio CSV". Dit bestand heeft de volgende structuur:

.. list-table:: prioriteit.csv
    :widths: 100, 100
    :header-rows: 1

    *   - Condition
        - Value
    *   - MT01
        - 3
    *   - MT02
        - 1
    *   - MT03
        - 2
    *   - etc.
        -

Verder spreekt de tool voor het CSV proces voor zich. De map met IFCs dient geselecteerd te worden, de map waar de CSVs 
opgeslagen moeten worden dient geselecteerd te worden, de CSV die gegenereerd dienen te worden moeten 
aangevinkt worden bij de checkboxen, en de knop "Start" dient ingedrukt te worden. De rest van de velden 
zijn optioneel als er een test CSV gemaakt moet worden, maar wel handig om in te vullen als er een echte
CSV gemaakt moet worden. De prioriteit staat standaard op "Normaal", wat gehanteerd wordt voor de echte
CSV. "Uitgebreid" geeft een prioriteit per bouwnummer, moduletype en werkstation. 
Dit zorgt voor een groot verschil in de prioriteiten, maar kan nuttig zijn om mee testen.

Voor het IFC proces, dient een map met IFCs geselecteerd te worden, en een locatie voor het rapport. Vervolgens dient 
er alleen op "Start" gedrukt te worden, en de tool doet de rest. Het kan zijn dat de tool soms even vastloopt, maar
dat is normaal, gezien het feit dat de IFCs inladen nogal wat tijd kost. Achteraf kan er via het menu IFCs (linksbovenin) 
nog naar de IFCs die problemen hebben gekeken worden, mochten deze er zijn. Hierin staat een menu met IFCs met een submenu:

* Show all
    Hierin staan alle elementen, met in rood de elementen die foutief zijn.

* Show part
    Hierin staan alle elementen die foutief zijn. Deze komen overeen met de rode elementen in de hele module.


.. toctree::
   :maxdepth: 2
   :caption: Ontwikkelen:

   installation

.. toctree::
   :maxdepth: 2
   :caption: Functies:

   app
   helpers
   partijen
   design

Indexen en tabellen
===================

* :ref:`genindex`
* :ref:`modindex`