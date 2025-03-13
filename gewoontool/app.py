import os
import re
import sys
import math
import glob
import logging

app_module_path = 'app_module'
if sys.platform == 'win32':
    casroot_path = 'casroot'
    if os.path.exists(casroot_path):
        os.environ['CASROOT'] = casroot_path

import itertools
import pandas as pd
import ifcopenshell
import ifcopenshell.util.element
from multiprocessing import freeze_support, Pool, cpu_count
from functools import partial
from OCC.Display.backend import load_backend
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QAction, QMenuBar
from PyQt5.QtCore import QCoreApplication, QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from OCC.Core.Graphic3d import Graphic3d_NOM_TRANSPARENT, Graphic3d_NOM_GOLD
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepBndLib import brepbndlib

import helpers
import partijen
import design

try:
    from ctypes import windll
    myappid = 'geWOONtool.1.0.0'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass


class CSVProcess(QThread):
    """Handles the IFC to CSV conversion process.

    Args:
        QThread (QThread): Thread class from PyQt5.

    Raises:
        ValueError: Raised when there are no files found in the given directory.
    """

    messageSignal = pyqtSignal(str)
    """Message signal for the status box."""
    errorSignal = pyqtSignal(str)
    """Error signal for the error box."""
    csvProgress = pyqtSignal(int)
    """Progress signal for the progress bar."""
    lcdChanged = pyqtSignal(int)
    """LCD signal for the LCD display."""
    resetSignal = pyqtSignal(str)
    """Signal for resetting the process."""

    def __init__(        
        self,
        ifc_path: str,
        csv_path: str,
        vh_nesting: str,
        bulk_path: str,
        meterkast_path: str,
        orderVH: str,
        orderBB: str,
        orderVMG: str,
        bnormt: bool,
        bbChecked: bool,
        vhChecked: bool,
        vmgChecked: bool,
        erpChecked: bool,
        cassettes: bool,
        ws198Checked: bool
    ) -> None:
        super().__init__()
        self.ifc_path = ifc_path
        self.ifc_list = helpers.get_ifc_list(self.ifc_path)
        self.csv_path = csv_path
        self.bulk_path = bulk_path
        self.meterkast_path = meterkast_path
        self.vh_nesting = vh_nesting
        self.orderVH = orderVH
        self.orderBB = orderBB
        self.orderVMG = orderVMG
        self.bnormt = bnormt
        self.bbChecked = bbChecked
        self.vhChecked = vhChecked
        self.vmgChecked = vmgChecked
        self.erpChecked = erpChecked
        self.cassettes = cassettes
        self.ws198Checked = ws198Checked

    def run(self):
        """Executes the IFC to CSV conversion process.

        Raises:
            FileNotFoundError: Raised when the priority CSV is not found.
            ValueError: Raised when there are no files found in the given directory.
        """        
        try:
            prog, length = 1, len(self.ifc_list)
            df_list = []
            bborder, vhorder, vmgorder = "IO-000000", "IO-000000", "IO-000000"
            if self.orderBB != "":
                bborder = self.orderBB
            if self.orderVH != "":
                vhorder = self.orderVH
            if self.orderVMG != "":
                vmgorder = self.orderVMG

            try: 
                prioriteit = pd.read_csv(self.vh_nesting)
                self.messageSignal.emit("Prioriteit CSV gevonden.")
            except FileNotFoundError:
                self.messageSignal.emit("Geen prioriteit CSV gevonden, de standaard nesting wordt gebruikt.")
                prioriteit = pd.DataFrame()

            try:
                bulk = pd.read_csv(self.bulk_path)
                self.messageSignal.emit("Bulk CSV gevonden.")
                bulkbb = bulk["BB"].tolist()
                bulkvh = bulk["VH"].tolist()
                bulkvmg = bulk["VMG"].tolist()
            except FileNotFoundError:
                self.messageSignal.emit("Geen bulk CSV gevonden.")
                bulkbb, bulkvh, bulkvmg = [], [], []

            try:
                meterkast = pd.read_csv(self.meterkast_path)
                self.messageSignal.emit("Meterkast CSV gevonden.")
                meterkast = meterkast["Meterkast"].tolist()
            except FileNotFoundError:
                self.messageSignal.emit("Geen meterkast CSV gevonden.")
                meterkast = []

            if self.csv_path == "":
                raise ValueError("Geen CSV locatie geselecteerd.")
            
            if length == 0:
                raise ValueError(f"Geen IFCs gevonden in {self.ifc_path}.")
            
            if len(self.csv_path) == 0:
                raise ValueError("Geen CSV locatie geselecteerd.")

            pool = Pool(processes=(cpu_count() - 2))
            self.messageSignal.emit(f"Start verwerken van {length} IFCs...")
            self.lcdChanged.emit(length)

            for df in pool.imap(partial(helpers.ifc_to_df, shape=False, schroef=True, lucht=True), self.ifc_list):
                df_list.append(df)
                self.csvProgress.emit(int(prog / length * 100))
                self.lcdChanged.emit(int(length - prog))
                prog += 1
            pool.close()
            pool.join()

            self.messageSignal.emit(f"IFCs zijn verwerkt, de CSVs worden gemaakt...")
            df = helpers.combine_dfs(df_list=df_list)
            bns = df["Bouwnummer"].unique()
            prio = helpers.create_nesting(combined_df=df, prioriteit=prioriteit)

            # VH Meterkast CSV:
            if self.vhChecked and meterkast != []:
                partijen.VH(df=df, ordernummer=vhorder, path=self.csv_path, prio_dict=prio, bulk_file=bulkvh, meterkast_file=meterkast, bulk=False, cassettes=False, cass_global=self.cassettes, meterkast=True)

            # Normaal:
            #     Normaal-Normaal op BN (inc prio)
            #     Normaal-BULK	per Batch
            # Cassettes:
            #     Cas-Normaal	op BN (inc prio)
            #     Cas-BULK	op Batch

            # Normaal-BULK
            if self.bbChecked and bulkbb != []:
                partijen.BB(df=df, ordernummer=bborder, path=self.csv_path, prio_dict=prio, bulk_file=bulkbb, bulk=True, cassettes=False, cass_global=self.cassettes)
            if self.vhChecked and bulkvh != []:
                partijen.VH(df=df, ordernummer=vhorder, path=self.csv_path, prio_dict=prio, bulk_file=bulkvh, meterkast_file=meterkast, bulk=True, cassettes=False, cass_global=self.cassettes)
            if self.vmgChecked and bulkvmg != []:
                partijen.VMG(df=df, ordernummer=vmgorder, path=self.csv_path, prio_dict=prio, bulk_file=bulkvmg, bulk=True, cassettes=False, cass_global=self.cassettes)

            # Cas-BULK
            if self.bbChecked and bulkbb != [] and self.cassettes:
                partijen.BB(df=df, ordernummer=bborder, path=self.csv_path, prio_dict=prio, bulk_file=bulkbb, bulk=True, cassettes=True, cass_global=self.cassettes)
            if self.vhChecked and bulkvh != [] and self.cassettes:
                partijen.VH(df=df, ordernummer=vhorder, path=self.csv_path, prio_dict=prio, bulk_file=bulkvh, meterkast_file=meterkast, bulk=True, cassettes=True, cass_global=self.cassettes)
            if self.vmgChecked and bulkvmg != [] and self.cassettes:
                partijen.VMG(df=df, ordernummer=vmgorder, path=self.csv_path, prio_dict=prio, bulk_file=bulkvmg, bulk=True, cassettes=True, cass_global=self.cassettes)

            for bn in bns:
                df_bn = df[df["Bouwnummer"] == bn]
                if self.erpChecked:
                    partijen.ERP(df=df_bn, path=self.csv_path, bnormt=self.bnormt)

                if self.ws198Checked:
                    partijen.WS198(df=df_bn, path=self.csv_path)

                # Normaal-Normaal
                if self.bbChecked:
                    partijen.BB(df=df_bn, ordernummer=bborder, path=self.csv_path, prio_dict=prio, bulk_file=bulkbb, bulk=False, cassettes=False, cass_global=self.cassettes)
                if self.vhChecked:
                    partijen.VH(df=df_bn, ordernummer=vhorder, path=self.csv_path, prio_dict=prio, bulk_file=bulkvh, meterkast_file=meterkast, bulk=False, cassettes=False, cass_global=self.cassettes)
                if self.vmgChecked:
                    partijen.VMG(df=df_bn, ordernummer=vmgorder, path=self.csv_path, prio_dict=prio, bulk_file=bulkvmg, bulk=False, cassettes=False, cass_global=self.cassettes)

                # Cas-Normaal
                if self.bbChecked and self.cassettes:
                    partijen.BB(df=df_bn, ordernummer=bborder, path=self.csv_path, prio_dict=prio, bulk_file=bulkbb, bulk=False, cassettes=True, cass_global=self.cassettes)
                if self.vhChecked and self.cassettes:
                    partijen.VH(df=df_bn, ordernummer=vhorder, path=self.csv_path, prio_dict=prio, bulk_file=bulkvh, meterkast_file=meterkast, bulk=False, cassettes=True, cass_global=self.cassettes)
                if self.vmgChecked and self.cassettes:
                    partijen.VMG(df=df_bn, ordernummer=vmgorder, path=self.csv_path, prio_dict=prio, bulk_file=bulkvmg, bulk=False, cassettes=True, cass_global=self.cassettes)

            self.messageSignal.emit(f"Klaar met converteren naar CSVs!")
            self.messageSignal.emit(f"De tool kan afgesloten worden.")
            self.resetSignal.emit("enable")

        except Exception as e:
            logging.exception("error:")
            output = f"Er is iets fout gegaan: {e}"
            self.errorSignal.emit(output)
            self.resetSignal.emit("enable")


class IFCProcess(QThread):
    """Handles the IFC quality check process.

    Args:
        QThread (QThread): Thread class from PyQt5.

    Raises:
        ValueError: Raised when there are no files found in the given directory.
    """

    messageSignal = pyqtSignal(str)
    """Message signal for the status box."""
    errorSignal = pyqtSignal(str)
    """Error signal for the error box."""
    ifcProgress = pyqtSignal(int)
    """Progress signal for the progress bar."""
    displaySignal = pyqtSignal(list, str, object, float, bool, bool, bool, bool)
    """Signal for displaying the IFCs in the viewer."""
    menuSignal = pyqtSignal(str, list, list)
    """Signal for adding the IFCs to the menu."""
    resetSignal = pyqtSignal(str)
    """Signal for resetting the process."""

    def __init__(self, ifc_path: str, report_loc: str, schroef: bool, dichting: bool) -> None:
        super().__init__()
        self.ifc_path = ifc_path
        self.ifc_list = helpers.get_ifc_list(self.ifc_path)
        self.report_loc = report_loc
        self.schroef = schroef
        self.dichting = dichting
    
    def run(self):
        """Runs the IFC quality check process.

        Raises:
            FileExistsError: Raised when the TEMP folder already exists.
            ValueError: Raised when there are no files found in the given directory.
        """        
        try:
            self.ifcProgress.emit(0)
            os.mkdir('TEMP')
            werknr = ''

            prog, length = 1, len(self.ifc_list)
            data = []

            if length == 0:
                raise ValueError(f"Geen IFCs gevonden in {self.ifc_path}.")
            
            if self.report_loc == "":
                raise ValueError("Geen rapport locatie geselecteerd.")

            ifc = ifcopenshell.open(self.ifc_list[0])
            if ifc.schema == 'IFC4' or ifc.schema == 'IFC2X3':
                self.messageSignal.emit(f'IFC schema: {ifc.schema}')
            else:
                raise ValueError(f'IFC schema: {ifc.schema} is niet ondersteund.')

            self.messageSignal.emit(f"Start verwerken van {length} IFCs...")

            settings = ifcopenshell.geom.settings()
            settings.set(settings.USE_PYTHON_OPENCASCADE, True)

            pool = Pool(processes=(cpu_count() - 2))
            for ifc_df in pool.imap(partial(helpers.ifc_to_df, shape=True, schroef=self.schroef, lucht=self.dichting), self.ifc_list):
                ifc_name = self.ifc_list[prog - 1].split('\\')[-1]
                df_errors = pd.DataFrame()
                df_basic = ifc_df[['Modulenaam', 'Productcode', 'Name', 
                   'Categorie', 'Dikte', 'Breedte', 'Lengte', 'Gewicht', 
                   'Materiaal', 'Station', 'Aantal', 'Eenheid']]
                if werknr == '':
                    werknr = ifc_df['Projectnummer'].iloc[0]
                    
                df_format = self.formatting(df_basic.copy()) if 'kozijn' not in ifc_name and 'gevel' not in ifc_name else pd.DataFrame()
                df_empty = self.empty(df_basic.copy())
                df_unit = self.units(df_basic.copy())
                df_null = self.null_values(df_basic.copy())
                df_nonunique = self.nonunique(df_basic.copy())
                df_category = self.categories(df_basic.copy())
                df_list = [df_empty, df_format, df_unit, df_null, df_nonunique, df_category]

                df_errors = pd.concat(df_list, ignore_index=True)
                df_errors = df_errors.drop(['Gewicht', 'Modulenaam'], axis=1)

                df_duplicate, shapesA = self.comparisons(ifc_df, schroef=self.schroef, luchtdichting=self.dichting)
                df_dup = df_duplicate['Hoeveel dubbelen'].sum() if not df_duplicate.empty else 0

                self.generate_images(ifc_df, ifc_name, shapesA) if len(shapesA) != 0 else None
                # Refresh the list of images
                glob.glob("TEMP/*.png")
                helpers.create_html(df_errors, df_duplicate, self.ifc_list[prog - 1])

                data.append([len(df_empty), len(df_format), len(df_unit), len(df_null), len(df_nonunique), len(df_category), df_dup])

                self.messageSignal.emit(f"IFC {ifc_name} ingeladen.")
                self.ifcProgress.emit(int(prog / length * 100))
                if len(shapesA) != 0:
                    self.menuSignal.emit(ifc_name, ifc_df.Shape.values.tolist(), shapesA)
                prog += 1

            pool.close()
            pool.join()

            results = [sum(column) for column in zip(*data)]
            self.messageSignal.emit("Alle IFCs gecontroleerd. Het rapport wordt gegenereerd...")

            try: 
                self.ifc_list = [x.split('\\')[-1] for x in self.ifc_list]
            except ValueError:
                pass
            ifc_string = ', '.join(str(ifc) for ifc in self.ifc_list)
            helpers.create_empty_html(ifc_string, results)
            helpers.combine_html()
            helpers.html_to_pdf(self.report_loc, werknr)
            self.messageSignal.emit("Het rapport is gegenereerd. Opschonen van de TEMP map...")
            for file in os.listdir("TEMP"):
                os.remove(f"TEMP/{file}")
            os.rmdir("TEMP")
            self.messageSignal.emit("Klaar! De tool kan afgesloten worden.")
            self.resetSignal.emit("enable")

        except FileExistsError as e:
            output = f'De TEMP folder bestond al, maar is nu verwijderd. genereer opnieuw!\n\n Meer informatie: {e}'
            self.errorSignal.emit(output)
            self.resetSignal.emit("restart")

        except Exception as e:
            if os.path.isdir("TEMP"):
                for file in os.listdir("TEMP"):
                    os.remove(f"TEMP/{file}")
                os.rmdir("TEMP")
            output = f"Er is iets fout gegaan: {e}"
            self.errorSignal.emit(output)
            self.resetSignal.emit("enable")


    def generate_images(self, df: pd.DataFrame, file: str, shapesA: list) -> None:
        """Generates images of the IFCs for the report.

        Args:
            df (pd.DataFrame): dataframe with the IFC data
            file (str): name of the IFC file
            shapesA (list): first list of shapes
            shapesB (list): second list of shapes
        """        
        try:
            ifc_name = file.split('.')[-2].split('\\')[-1]
        except ValueError:
            ifc_name = file.split('.')[-2]

        self.displaySignal.emit(shapesA, f"TEMP/{ifc_name}.png", Graphic3d_NOM_GOLD, 0.8, True, True, True, True)
        self.displaySignal.emit(df.Shape.values.tolist(), f"TEMP/Hele module {ifc_name}.png", Graphic3d_NOM_TRANSPARENT, 0.95, False, True, False, False)

    # TODO How to load this from checks.py using pyinstaller???
    def empty(self, df: pd.DataFrame) -> pd.DataFrame:
        """Checks if there are empty values in the dataframe.

        Args:
            df (pd.DataFrame): The dataframe with all the parts.

        Returns:
            pd.DataFrame: A dataframe with all the empty values.
        """    
        df = df.convert_dtypes()
        mask = df.eq('') | df.isna()
        df_empty = df[mask]
        df_empty = df_empty.dropna(axis=0, how='all')
        if not df_empty.empty:
            df_empty['Type Fout'] = 'Ontbrekende data'
        return df_empty
    
    def formatting(self, df: pd.DataFrame) -> pd.DataFrame:
        """Checks if the formatting of the dataframe is correct.

        Args:
            df (pd.DataFrame): The dataframe with all the parts.

        Returns:
            pd.DataFrame: A dataframe with all the formatting errors.
        """
        productcode = re.compile(r'[A-Z]{2}-\d{6}-\d{4}')
        mask = df.apply(lambda row: bool(re.search(productcode, row['Productcode'])), axis=1)
        df_format = df[~mask]
        if not df_format.empty:
            df_format['Type Fout'] = 'Productcode fout'
        return df_format


    def units(self, df: pd.DataFrame) -> pd.DataFrame:
        """Checks if the units of the dataframe are correct.

        Args:
            df (pd.DataFrame): The dataframe with all the parts.

        Returns:
            pd.DataFrame: A dataframe with all the unit errors.
        """
        df = df.loc[df['Eenheid'] != 'unit']
        df_unit = df[df['Productcode'].apply(lambda x: True if 'UN' in x else (
                                                    True if 'CE' in x else False))]
        if not df_unit.empty:
            df_unit['Type Fout'] = 'Unit fout'
        return df_unit


    def null_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Checks if there are null values in the dataframe.

        Args:
            df (pd.DataFrame): The dataframe with all the parts.

        Returns:
            pd.DataFrame: A dataframe with all the null values.
        """
        df[['Dikte', 'Breedte', 'Lengte', 'Gewicht']] = df[['Dikte', 'Breedte', 'Lengte', 'Gewicht']].apply(pd.to_numeric)
        dfDikte = df[df['Dikte'].apply(lambda x: True if math.isclose(x, 0) else False)]
        dfBreedte = df[df['Breedte'].apply(lambda x: True if math.isclose(x, 0) else False)]
        dfLengte = df[df['Lengte'].apply(lambda x: True if math.isclose(x, 0) else False)]
        dfGewicht = df[df['Gewicht'].apply(lambda x: True if math.isclose(x, 0) else False)]
        df_null = pd.concat([dfDikte, dfBreedte, dfLengte, dfGewicht], ignore_index=True)
        if not df_null.empty:
            df_null['Type Fout'] = 'Null waarde'
        return df_null


    def volume(self, df: pd.DataFrame) -> pd.DataFrame:
        """Checks if the volume of the dataframe is correct.

        Args:
            df (pd.DataFrame): The dataframe with all the parts.

        Returns:
            pd.DataFrame: A dataframe with all the volume errors.
        """
        df = df.apply(pd.to_numeric, errors='ignore')
        df['Volume_1'] = (df['Dikte'] * df['Breedte'] * df['Lengte'])/1_000_000_000
        filter1 = (100 * ((df['Volume_1'] - df['Volume']) / ((df['Volume_1'] + df['Volume']) / 2))) < -50
        df_volume = df.where(filter1).dropna()
        df_volume = df_volume.drop(['Volume_1'], axis=1)
        if not df_volume.empty:
            df_volume['Type Fout'] = 'Volume error'
        return df_volume


    def nonunique(self, df: pd.DataFrame) -> pd.DataFrame:
        """Checks if there are non-unique values in the dataframe.

        Args:
            df (pd.DataFrame): The dataframe with all the parts.

        Returns:
            pd.DataFrame: A dataframe with all the non-unique values.
        """
        try: 
            df['Product'] = df['Productcode'].apply(lambda x: x[3:9])
            df['Code'] = df['Productcode'].apply(lambda x: x[10:14])
            df[['Dikte', 'Breedte', 'Lengte', 'Gewicht', 'Aantal', 'Product', 'Code']] = (
                    df[['Dikte', 'Breedte', 'Lengte', 'Gewicht', 'Aantal', 'Product', 'Code']].apply(pd.to_numeric))
            df_original = df.drop(columns=['Product', 'Code']).copy()
            df = df.groupby(['Productcode'])['Name'].apply(lambda x: ','.join(x)).reset_index()
            df = df[df['Name'].str.contains(',')]
            df['Name'] = df.Name.apply(lambda x: x.split(',')).apply(lambda x: list(set(x)))
            df['Len'] = df.Name.str.len()
            df = df[df['Len'] > 1]
            names = [name for list in df.Name.tolist() for name in list]
            non_unique = df_original[df_original['Name'].isin(names)].copy()
            non_unique = non_unique[non_unique['Productcode'].isin(df.Productcode.tolist())].groupby(
                                        ['Name', 'Productcode', 'Modulenaam'], as_index=False).agg(
                                        dict(map((lambda x: (x, 'first') if x != 'Aantal' else (
                                        x, 'sum')), non_unique.columns.tolist())))
            df_unique = non_unique.sort_values(by=['Productcode']).copy()
            if not df_unique.empty:
                df_unique['Type Fout'] = 'Non-unique'
            return df_unique
        except TypeError:
            df.to_csv('error.csv', index=False)
            return pd.DataFrame()


    def categories(self, df: pd.DataFrame) -> pd.DataFrame:
        """Checks if the categories of the dataframe are correct.

        Args:
            df (pd.DataFrame): The dataframe with all the parts.

        Returns:
            pd.DataFrame: A dataframe with all the category errors.
        """
        csvfile = helpers.resource_path('assets/categories.csv')
        df_categories = pd.read_csv(csvfile, header=None)
        categories = [x.lower() for x in df_categories[0].tolist()]
        df_category = df[~df['Categorie'].str.lower().isin(categories)]
        if not df_category.empty:
            df_category['Type Fout'] = 'Categorie'
        return df_category


    def comparisons(self, df: pd.DataFrame, schroef: bool=False, luchtdichting: bool=False) -> tuple[pd.DataFrame, list, list]:
        """Checks if there are duplicate shapes in the dataframe.

        Args:
            df (pd.DataFrame): The dataframe with all the parts.
            schroef (bool, optional): If screws need to be checked. Defaults to False.
            luchtdichting (bool, optional): If airtight materials need to be checked. Defaults to False.

        Returns:
            tuple[pd.DataFrame, list]: A dataframe with all the duplicate shapes, and two lists of shapes showing the parts with issues.
        """
        shapesA = []
        df_dub = pd.DataFrame()
        categories = sorted(df['Categorie'].unique())
        try:
            if not schroef:
                categories.remove('Schroeven en ankers')
        except ValueError:
            pass
        try:    
            if not luchtdichting:
                categories.remove('Luchtdichting')
        except ValueError:
            pass
        
        for category in categories:
            df_cat = df[df['Categorie'] == category]
            for a, b in itertools.combinations(df_cat['Shape'].tolist(), 2):
                bb1 = self.get_boundingbox(a)
                bb2 = self.get_boundingbox(b)
                if bb1 == bb2:
                    name = df.loc[df['Shape'] == a, 'Name'].iloc[0]
                    name1 = df.loc[df['Shape'] == b, 'Name'].iloc[0]
                    productcode = df.loc[df['Shape'] == a, 'Productcode'].iloc[0]
                    productcode1 = df.loc[df['Shape'] == b, 'Productcode'].iloc[0]
                    s = pd.DataFrame({'Name A': [name], 'Productcode A': [productcode],
                                    'Name B': [name1], 'Productcode B': [productcode1]})
                    df_dub = pd.concat([df_dub, s])
                    shapesA.append(a)
        
        if df_dub.empty:
            return df_dub, shapesA
        else:    
            df_dub = df_dub.groupby(df_dub.columns.tolist(), as_index=False).size()
            df_dub = df_dub.rename(columns={'size':'Hoeveel dubbelen'})
            return df_dub, shapesA
        

    def get_boundingbox(self, shape) -> tuple:
        """Gets the bounding box of a shape.

        Args:
            shape (Shape): The shape of the part.

        Returns:
            tuple: The coordinates of the bounding box.
        """
        bbox = Bnd_Box()
        brepbndlib.AddOptimal(shape, bbox, False)
        coordinates = bbox.Get()
        return coordinates


class App(QMainWindow, design.Ui_CSVgenerator):
    """Main application class.

    Args:
        QMainWindow (QMainWindow): Main window class from PyQt5.
        design (Ui_CSVgenerator): Generated design class from Qt Designer.
    """    
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon(helpers.resource_path("assets\\gewoonhout.ico")))

        # Weird tab bug fix
        self.tabs.setCurrentIndex(1)

        # Create ifc viewer
        load_backend("qt-pyqt5") #laptop
        # load_backend("pyqt5") #desktop/prod
        from OCC.Display.qtDisplay import qtViewer3d

        self.shapeTuples = []
        self.canva = qtViewer3d(self)
        self.preview_layout.addWidget(self.canva)
        self.canva.InitDriver()
        self.display = self.canva._display
        self.display.display_triedron()
        self.display.set_bg_gradient_color(
            [206, 215, 222], [128, 128, 128]
        )

        self.canva.menu_bar = QMenuBar(self.canva)
        self.ifcMenu = self.canva.menu_bar.addMenu('IFCs')

        # Create error box
        self.errorBox = QMessageBox(self)
        self.errorBox.setIcon(QMessageBox.Critical)
        self.errorBox.setWindowTitle("Error")

        # Connect buttons - CSV
        self.ifc_button.clicked.connect(self.get_ifc_csv)
        self.csv_button.clicked.connect(self.get_csv)
        self.prio_button.clicked.connect(self.get_prio)
        self.bulk_button.clicked.connect(self.get_bulk_csv)
        self.meterkast_button.clicked.connect(self.get_meterkast_csv)
        self.start_button.clicked.connect(self.generate_csv)
        self.reset_button.clicked.connect(self.reset_csv)
        self.exit_button.clicked.connect(self.exit_app)

        # Connect buttons - Report
        self.ifc_button2.clicked.connect(self.get_ifc_report)
        self.report_button.clicked.connect(self.get_report)

        self.start_button2.clicked.connect(self.generate_report)
        self.reset_button2.clicked.connect(self.reset_ifc)
        self.exit_button2.clicked.connect(self.exit_app)


    # Button functions
    def get_ifc_csv(self):
        """Gets the IFC directory for the CSV generation process.
        """        
        file = QFileDialog.getExistingDirectory(self, "Selecteer de map met IFCs.")
        self.ifc_path.setText(file)

    def get_csv(self):
        """Gets the CSV directory for the CSV generation process.
        """        
        file = QFileDialog.getExistingDirectory(self, "Selecteer de map voor de CSVs.")
        self.csv_path.setText(file)

    def get_prio(self):
        """Gets the priority CSV for the CSV generation process.
        """        
        file = QFileDialog.getOpenFileName(
            self, "Selecteer de CSV voor de prioriteit."
        )
        self.nesting_path.setText(file[0])

    def get_bulk_csv(self):
        """Gets the bulk CSV for the CSV generation process.
        """
        file = QFileDialog.getOpenFileName(
            self, "Selecteer de CSV voor de bulk."
        )
        self.bulk_path.setText(file[0])

    def get_meterkast_csv(self):
        """Gets the meterkast CSV for the CSV generation process.
        """
        file = QFileDialog.getOpenFileName(
            self, "Selecteer de CSV voor de meterkast."
        )
        self.meterkast_path.setText(file[0])

    def get_ifc_report(self):
        """Gets the IFC directory for the report generation process.
        """        
        file = QFileDialog.getExistingDirectory(self, "Selecteer de map met IFCs.")
        self.ifc_path2.setText(file)

    def get_report(self):
        """Gets the report directory for the report generation process.
        """        
        file = QFileDialog.getExistingDirectory(
            self, "Selecteer de locatie voor het rapport."
        )
        self.report_path.setText(file)

    def generate_csv(self):
        """Starts the CSV generation process.
        """        
        cassettes = False
        if self.ws_csv.isChecked():
            cassettes = True

        self.calc = CSVProcess(
            ifc_path=self.ifc_path.text(),
            csv_path=self.csv_path.text(),
            bulk_path=self.bulk_path.text(),
            meterkast_path=self.meterkast_path.text(),
            vh_nesting=self.nesting_path.text(),
            orderVH=self.vh_order.text(),
            orderBB=self.bb_order.text(),
            orderVMG=self.vmg_order.text(),
            bnormt=self.bnormt.isChecked(),
            bbChecked=self.bb_check.isChecked(),
            vhChecked=self.vh_check.isChecked(),
            vmgChecked=self.vmg_check.isChecked(),
            erpChecked=self.erp_check.isChecked(),
            cassettes=cassettes,
            ws198Checked=self.ws198_check.isChecked(),
        )

        self.calc.csvProgress.connect(self.updateCsvProgress)
        self.calc.lcdChanged.connect(self.updateLCD)
        self.calc.messageSignal.connect(self.csvSignal)
        self.calc.errorSignal.connect(self.errorSignal)
        self.calc.resetSignal.connect(self.resetSignal)
        self.calc.start()
        self.start_button.setEnabled(False)
        self.reset_button.setEnabled(False)

    def reset_csv(self):
        """Resets the CSV generation process.
        """        
        self.progressCSV.setValue(0)
        self.lcd.setProperty("value", 0)
        self.ifc_path.setText("")
        self.csv_path.setText("")
        self.bulk_path.setText("")
        self.meterkast_path.setText("")
        self.nesting_path.setText("")
        self.vh_order.setText("")
        self.bb_order.setText("")
        self.vmg_order.setText("")
        self.status_csv.setText("")
        self.start_button.setEnabled(True)

    def reset_ifc(self):
        """Resets the IFC quality check process.
        """        
        self.progressIFC.setValue(0)
        self.ifc_path2.setText("")
        self.report_path.setText("")
        self.status_qual.setText("")
        self.start_button2.setEnabled(True)

    def generate_report(self):
        """Starts the report generation process.
        """
        self.check = IFCProcess(
            ifc_path=self.ifc_path2.text(),
            report_loc=self.report_path.text(),
            schroef=self.screw_check.isChecked(),
            dichting=self.air_check.isChecked(),
        )

        self.check.ifcProgress.connect(self.updateIfcProgress)
        self.check.messageSignal.connect(self.ifcSignal)
        self.check.errorSignal.connect(self.errorSignal)
        self.check.displaySignal.connect(self.displaySignal)
        self.check.menuSignal.connect(self.addMenuItem)
        self.check.resetSignal.connect(self.checkResetSignal)
        self.check.start()
        self.start_button2.setEnabled(False)
        self.reset_button2.setEnabled(False)

    def exit_app(self):
        """Removes the TEMP folder and exits the application.
        """
        if os.path.isdir("TEMP"):
            for file in os.listdir("TEMP"):
                os.remove(f"TEMP/{file}")
            os.rmdir("TEMP")
        QCoreApplication.instance().quit()
        self.close()

    # Functions for updating the GUI
    def updateCsvProgress(self, value):
        """Updates the progress bar for the CSV generation process.

        Args:
            value (int): Value for the progress bar.
        """        
        self.progressCSV.setValue(value)
    
    def updateIfcProgress(self, value):
        """Updates the progress bar for the IFC quality check process.

        Args:
            value (int): Value for the progress bar.
        """
        self.progressIFC.setValue(value)

    def updateLCD(self, value):
        """Updates the LCD display for the CSV generation process.

        Args:
            value (int): LCD value.
        """        
        self.lcd.setProperty("value", value)

    def csvSignal(self, value):
        """Adds a message to the CSV status box.

        Args:
            value (str): Message to be added.
        """        
        self.status_csv.append(value)

    def resetSignal(self, value):
        """Resets the status box.

        Args:
            value (str): Message to be added.
        """        
        if value == "enable":
            self.reset_button.setEnabled(True)

        if value == "reset":
            self.reset_csv()

    def checkResetSignal(self, value):
        """Resets the status box.

        Args:
            value (str): Message to be added.
        """        
        if value == "enable":
            self.reset_button2.setEnabled(True)

        if value == "restart":
            self.reset_button2.setEnabled(True)
            self.start_button2.setEnabled(True)

        if value == "reset":
            self.reset_ifc()

    def ifcSignal(self, value):
        """Adds a message to the IFC status box.

        Args:
            value (str): Message to be added.
        """        
        self.status_qual.append(value)

    def errorSignal(self, value):
        """Shows an error message box.

        Args:
            value (str): Error message.
        """
        self.errorBox.setText(value)
        self.errorBox.exec_()

    def displaySignal(self, shapes, location, material, transparency, update, fit, screenshot, erasePrevious):
        """Displays the IFCs in the viewer.

        Args:
            shapes (list): List of shapes.
            location (str): Location of the screenshot.
            material (Graphic3d_NameOfMaterial): Material of the shapes.
            transparency (float): Transparency of the shapes.
            update (bool): Whether the viewer should update.
            fit (bool): Whether the viewer should fit the shapes.
            screenshot (bool): Whether the viewer should take a screenshot.
            erasePrevious (bool): Whether the viewer should erase the previous shapes.
        """        
        if erasePrevious:
            self.display.EraseAll()
        self.display.DisplayShape(shapes=shapes, material=material, transparency=transparency, update=update)
        if fit:
            self.display.FitAll()
        if screenshot:
            self.display.View.Dump(location)

    def addMenuItem(self, item, wholeModule, shapesA):
        """Adds an IFC to the menu.

        Args:
            item (str): Name of the IFC.
            shapes (list): List of shapes.
        """
        self.shapeTuples.append((item, wholeModule, shapesA))
        self.subMenu = self.ifcMenu.addMenu(item)
        self.subMenu.addAction(self.createAction('Show all', lambda: self.showWhole(item)))
        self.subMenu.addAction(self.createAction('Show part', lambda: self.showPart(item)))

    
    def createAction(self, name, callback):
        """Creates an action for the menu.

        Args:
            name (str): Name of the action.
            callback (function): Function to be called when the action is triggered.

        Returns:
            QAction: Action for the menu.
        """
        action = QAction(name, self)
        action.triggered.connect(callback)
        return action


    def showWhole(self, item):
        """Shows the selected IFC in the viewer.

        Args:
            item (str): Name of the IFC.

        """    
        for shape in self.shapeTuples:
            if shape[0] == item:
                self.display.EraseAll()
                self.display.DisplayShape(shapes=shape[1], material=Graphic3d_NOM_TRANSPARENT, transparency=0.95, update=False)
                self.display.DisplayShape(shapes=shape[2], color='RED', transparency=0.2, update=False)
                self.display.FitAll()
                # self.display.register_select_callback(lambda *args: print(args[0][0])) Kijken of callback kan?
                break


    def showPart(self, item):
        """Shows the selected IFC in the viewer.

        Args:
            item (str): Name of the IFC.

        """    
        for shape in self.shapeTuples:
            if shape[0] == item:
                self.display.EraseAll()
                self.display.DisplayShape(shapes=shape[2], material=Graphic3d_NOM_GOLD, transparency=0.4, update=False)
                self.display.FitAll()
                break

if __name__ == "__main__":
    pd.options.mode.chained_assignment = None
    freeze_support()
    appplication = QApplication([])
    window = App()
    window.show()
    sys.exit(appplication.exec_())