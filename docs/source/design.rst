Design 
======================================

Om de GUI te ontwerpen, wordt de tool "Qt Designer" gebruikt. Nadat de ontwikkelomgeving is ingericht 
kan deze design tool worden gestart door de command:

.. code:: sh

   designer

Daarna kan in de Qt Designer alles naar wens worden aangepast door het .ui bestand te openen. 
Om hiervan een nieuwe .py te genereren die nodig is voor het programma, kan het volgende
command worden uitgevoerd in de folder design:

.. code:: sh

   pyuic5 -x design.ui -o design.py

Dit nieuwe bestand wordt dan in de folder design geplaatst, en ingelezen door het programma.

.. automodule:: design
   :members: