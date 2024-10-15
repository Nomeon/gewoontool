import re
import os
import sys
import glob
import pdfkit
import base64
import datetime
import pandas as pd
import ifcopenshell
from itertools import product
from ifcopenshell import geom
from jinja2 import Environment, FileSystemLoader


def resource_path(path: str) -> str:
    """Convert relative path to absolute path

    Args:
        path (str): Relative path

    Returns:
        str: Absolute path
    """    
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    complete_path = os.path.join(base_path, path)
    return complete_path


def get_ifc_list(path: str) -> list:
    """Gets all the IFC files from a directory.

    Args:
        path (str): The path to the directory.

    Returns:
        list: A list with all the IFC files.
    """
    return [ifc for ifc in glob.glob(f"{path}/*ifc")]


def ifc_to_df(file: str, shape: bool=False, schroef: bool=True, lucht: bool=True) -> pd.DataFrame:
    """Converts an IFC file to a dataframe.

    Args:
        file (str): The path to the IFC file.
        shape (bool, optional): If a geometric shape should be created of the part. Defaults to False due to expensive computations.
        schroef (bool, optional): If the screws should be included. Defaults to True.
        lucht (bool, optional): If the air should be included. Defaults to True.

    Returns:
        pd.DataFrame: The dataframe with all the parts.
    """
    rows = []
    ifc = ifcopenshell.open(file)
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_PYTHON_OPENCASCADE, True)
    for element in ifc.by_type('IfcElement'):
        if ('IfcFastener' in str(element) or 'IfcMechanicalFastener' in str(element)) and (not schroef or not lucht):
            continue

        if 'IfcElementAssembly' not in str(element):
            try:                
                shape = geom.create_shape(settings, element).geometry if shape else None
                elements = ifcopenshell.util.element.get_psets(element)
                if 'kozijn' in file or 'gevel' in file:
                    name = elements['Identity Data']['Type Mark']
                else:
                    name = element.get_info()['Name']
                row = {'Shape': shape, 'Name': name}
                if ifc.schema == 'IFC2X3':
                    for v in elements.values():
                        if 'Klant' in v.keys():
                            row |= v
                elif ifc.schema == 'IFC4':
                    row |= elements['S']
                if 'Klant' not in row.keys():
                    continue
                rows.append(row)
            except KeyError:
                print(f'KeyError: {element}')
                continue

    df = pd.DataFrame(rows)
    
    if not 'BuildingStep' in df.columns:
        df['BuildingStep'] = ''

    columns_to_keep = ['Klant', 'Projectnummer', 'Bouwnummer', 'Moduletype',
            'Modulenaam', 'IFC bestand', 'Productcode', 'Name',
            'Categorie', 'Dikte', 'Breedte', 'Lengte', 'Gewicht',
            'Materiaal', 'Station', 'Aantal', 'Eenheid',
            'Shape', 'BuildingStep']

    df = df[columns_to_keep]
    df[["Projectnummer", "Dikte", "Breedte", "Lengte", "Gewicht", "Aantal"]] = df[["Projectnummer", "Dikte", "Breedte", "Lengte", "Gewicht", "Aantal"]].apply(pd.to_numeric)
    df = df.round({"Dikte": 1, "Lengte": 1, "Breedte": 1})
    df = df[~df['Station'].isin(['WS99', 'WS199'])]
    return df

def combine_dfs(df_list: list) -> pd.DataFrame:
    """Combines a list of dataframes to one dataframe.

    Args:
        df_list (list): A list with dataframes.

    Returns:
        pd.DataFrame: The combined dataframe.
    """
    df = pd.DataFrame()
    for dataframe in df_list:
        df = pd.concat([df, dataframe], ignore_index=True)

    df[["Projectnummer", "Dikte", "Breedte", "Lengte", "Gewicht", "Aantal"]] = df[
        ["Projectnummer", "Dikte", "Breedte", "Lengte", "Gewicht", "Aantal"]
    ].apply(pd.to_numeric)
    df = df.round({"Dikte": 1, "Lengte": 1, "Breedte": 1})
    df = df[~df['Station'].isin(['WS99', 'WS199'])]
    df = df.drop(["Shape"], axis=1)
    return df

def delete_productcode(column: str) -> bool:
    """Checks if the column is a voorraadproduct.

    Args:
        column (str): The column.

    Returns:
        bool: True if the column is a voorraadproduct.
    """
    included = (
        "EP" in column
        or "SP" in column
        or not re.match(r"[A-Z]{2}-\d{6}-\d{4}", column)
    )
    return included


def get_dikte(column: str) -> int:
    """Gets the dikte from the column.

    Args:
        column (str): The column.

    Returns:
        int: The dikte.
    """
    value = int(re.search(r"\d+", column).group())
    return value


def create_nesting(    
    combined_df: pd.DataFrame, prioriteit: pd.DataFrame
) -> dict:
    """Creates a dictionary with the nesting priority.

    Args:
        combined_df (pd.DataFrame): The dataframe with all the parts.
        prioriteit (pd.DataFrame): The dataframe with the priority of the modules.
        extended_prio (bool, optional): If the priority is extended. Defaults to False.

    Returns:
        dict: A dictionary with the nesting priority.
    """
    project = combined_df["Projectnummer"].iloc[0]
    bouwnummers = combined_df["Bouwnummer"].unique()
    mods = sorted(combined_df["Moduletype"].unique())
    sorted_werkstations = sorted(combined_df["Station"].unique())
    sorted_werkstations.reverse()
    mods.reverse()

    try:
        sorted_werkstations.append(
            sorted_werkstations.pop(sorted_werkstations.index("WS07"))
        )
    except:
        pass

    data, row = [], ""

    if prioriteit.empty:
        for bn, mt, ws in product(sorted(bouwnummers), mods, sorted_werkstations):
            row = f"{project}-{bn}-{mt}-{ws}"
            data.append({"Naam": row})
        
        for i in range(len(data)):
            data[i]["Prio"] = i
        df_prio = pd.DataFrame(data)
        prio_dict = dict(zip(df_prio.Naam, df_prio.Prio))
        return prio_dict

    modules = prioriteit.Condition.tolist()
    prioriteit["Value"] = pd.to_numeric(prioriteit["Value"])
    prio = dict(zip(prioriteit.Condition, prioriteit.Value))

    for bn, mt, ws in product(sorted(bouwnummers), modules, sorted_werkstations):
        row = f"{project}-{bn}-{mt}-{ws}"
        data.append({"Naam": row})

    df_prio = pd.DataFrame(data)
    df_prio["Prio"] = 0

    for index, row in df_prio.iterrows():
        for key, value in prio.items():
            for item in sorted_werkstations:
                key_ws = key + "-" + item
                ws_index = sorted_werkstations.index(item)
                if key_ws in row["Naam"]:
                    df_prio.loc[index, "Prio"] = (
                        (value - 1) + (ws_index * len(modules)) + 1
                    )

    prio_dict = dict(zip(df_prio.Naam, df_prio.Prio))
    return prio_dict


def encode_image(file: str) -> str:
    """Encodes an image to base64.

    Args:
        file (str): The path to the image.

    Returns:
        str: The encoded image.
    """

    with open(file, 'rb') as image_file:
        base64file = base64.b64encode(image_file.read()).decode()
        return base64file


def create_html(errors: pd.DataFrame, duplicates: pd.DataFrame, ifc: str) -> None:
    """Creates an HTML file with the errors and duplicates.

    Args:
        errors (pd.DataFrame): Dataframe with all the errors.
        duplicates (pd.DataFrame): Dataframe with all the duplicates.
        ifc (str): The path to the IFC file.
    """    
    tables, images = [], []
    try:
        ifc_name = ifc.split('.')[-2].split('\\')[-1]
    except ValueError:
        ifc_name = ifc.split('.')[-2]

    for filename in glob.glob('TEMP/*.png'):
        with open(os.path.join(os.getcwd(), filename), 'r'):
            files = filename.split('\\')[1].split('.')[0]
            if ifc_name in files:
                images.append((filename, files, encode_image(filename)))

    if not errors.empty:
        tables.append(errors)
    if not duplicates.empty:
        tables.append(duplicates)
    
    env = Environment(loader=FileSystemLoader(searchpath=resource_path('assets')))
    template = env.get_template('template.html')
    if len(tables) != 0 or len(images) != 0:
        html = template.render(tables=tables, images=images, ifc=ifc_name)
        with open(f'TEMP/{ifc_name} report.html', 'w') as f:
            f.write(html)


def create_empty_html(ifc_string: str, data: list) -> None:
    """Creates an empty HTML file with the IFC string.
    
    Args:
        ifc_string (str): The IFC string.
        data (list): The data for the HTML file.
    """
    env = Environment(loader=FileSystemLoader(searchpath=resource_path('assets')))
    template = env.get_template('empty.html')
    html = template.render(ifc_string=ifc_string, data=data)
    with open('TEMP/empty.html', 'w') as f:
        f.write(html)


def html_to_pdf(path: str, werknr: str) -> None:
    """Converts the HTML file to a PDF file.

    Args:
        path (str): The path to save the PDF file.
    """
    current_date = datetime.datetime.now()
    date = current_date.strftime("%d-%m-%Y")
    WKHTML_PATH = 'I:/GHO/00 Algemeen/ICT/Applicaties/IFC Tools/Installatiebestanden/wkhtmltopdf/bin/wkhtmltopdf.exe'
    # WKHTML_PATH = 'C:/Users/nomeon/Desktop/Projects/wkhtmltopdf/bin/wkhtmltopdf.exe'
    options = {
        'page-size' : 'A4',
        'dpi' : 400,
        'encoding' : 'UTF-8',
        'enable-local-file-access' : None,
        'footer-center' : f'Pagina [page]/[topage], gegenereerd op [date]',
        'footer-font-size' : 8,
    }
    path_wkhtmltopdf = r"{}".format(WKHTML_PATH)
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    for filename in glob.glob('TEMP/combined.html'):
        with open(os.path.join(os.getcwd(), filename), 'r'):
            output = f'{path}/{werknr}-{date}-report.pdf'
            cssfile = resource_path('assets\\template.css')
            pdfkit.from_file(filename, output, options=options, configuration=config, css=cssfile)


def combine_html() -> None:
    """Combines all the HTML files to one HTML file.
    """
    with open(os.path.join(os.getcwd(), 'TEMP/empty.html'), 'r') as e:
        empty_html = e.read()
    
    for file in glob.glob('TEMP/*.html'):
        if 'empty.html' not in file:
            with open(os.path.join(os.getcwd(), file), 'r') as f:
                html = f.read()
                empty_html = empty_html.replace('</body></html>', html + '<p style="page-break-before: always;"></p></body></html>')
    combined_html = empty_html.replace('<p style="page-break-before: always;"></p></body></html>', '</body></html>')
    
    with open('TEMP/combined.html', 'w') as f:
        f.write(combined_html)

def bouwlaag_translation() -> dict:
    """Gives the dictionary to shorten the description of bouwlaag.

    Returns:
        dict: A dictionary with the translations.
    """
    bouwlaag_dict = {
        "Binnenwand - Beplating - Zijde 1": "BW - 1",
        "Gevel - Afwerking - Binnenzijde en Dagkant": "G - Dagkant",
        "Gevel - Beplating - Binnenzijde": "G - Binnenzijde",
        "Gevel - Installaties, Luchtdichting en Brandwerende Voorzieningen": "G - Inst, LD, BV",
        "Overig - Op Locatie": "O - Op locatie",
        "Plafond - Hoofdbalk Gevel 1e laag": "PL - HBG - 1",
        "Plafond - Hoofdbalk Gevel 2e laag": "PL - HBG - 2",
        "Plafond - Hoofdbalk Gevel 3e laag": "PL - HBG - 3",
        "Plafond - Hoofdbalk Woningscheiding 1e laag": "PL - HBW - 1",
        "Plafond - Hoofdbalk Woningscheiding 2e laag": "PL - HBW - 2",
        "Plafond - Hoofdbalk Woningscheiding 3e laag": "PL - HBW - 3",
        "Plafond - Randbalk Connectie 1e laag": "PL - RBC - 1",
        "Plafond - Randbalk Connectie 2e laag": "PL - RBC - 2",
        "Plafond - Randbalk Connectie 3e laag": "PL - RBC - 3",
        "Plafond - Randbalk Gevel 1e laag": "PL - RBG - 1",
        "Plafond - Randbalk Gevel 2e laag": "PL - RBG - 2",
        "Plafond - Randbalk Gevel 3e laag": "PL - RBG - 3",
        "Plafond - Randbalk Woningscheiding 1e laag": "PL - RBW - 1",
        "Plafond - Randbalk Woningscheiding 2e laag": "PL - RBW - 2",
        "Plafond en Plat Dak - Installaties en Brandwerende Voorzieningen": "PL + DAK - Inst",
        "Vloer - Beplating - Onderzijde": "VL - Onderzijde",
        "Vloer - Hoofdliggers en Subliggers en Elementen voor koppelen fundering": "VL - HL + SL",
        "Vloer - Installaties en Brandwerende Voorzieningen": "VL - Inst",
        "Vloer - Randbalk Connectie 1e laag": "VL - RBC - 1",
        "Vloer - Randbalk Connectie 2e laag": "VL - RBC - 2",
        "Vloer - Randbalk Gevel 1e laag": "VL - RBG - 1",
        "Vloer - Randbalk Gevel 2e laag": "VL - RBG - 2",
        "Vloer - Randbalk Gevel 3e laag": "VL - RBG - 3",
        "Woningscheidende wand - Installaties en Brandwerende Voorzieningen": "WSW - Inst",
    }
    return bouwlaag_dict


def custom_groupby(df, groupby_cols, sum_cols):
    """Custom groupby function for pandas.

    Args:
        df (pd.DataFrame): The dataframe.
        groupby_cols (list): The columns to group by.
        sum_cols (list): The columns to sum.

    Returns:
        pd.DataFrame: The grouped dataframe.
    """
    # Save original order of columns
    columns = df.columns.tolist()
    agg_dict = {}

    for col in sum_cols:
        agg_dict[col] = 'sum'

    for col in df.columns:
        if col not in sum_cols and col not in groupby_cols:
            agg_dict[col] = 'first'

    df_grouped = df.groupby(groupby_cols, as_index=False).agg(agg_dict)
    df_grouped = df_grouped[columns]

    return df_grouped