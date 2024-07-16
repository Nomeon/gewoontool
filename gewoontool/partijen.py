import pandas as pd
import numpy as np
import helpers

def BB(df: pd.DataFrame, ordernummer: str, path: str, prio_dict: dict, bulk_file: list, bulk: bool, cassettes: bool, cass_global: bool) -> None:
    """Gets the BB parts from the dataframe and saves it to a CSV file.

    Args:
        df (pd.DataFrame): The dataframe with all the parts.
        ordernummer (str): The ordernumber of the project.
        path (str): The path to save the CSV file.
        prio_dict (dict): The dictionary with the priority of the modules.
        bulk (list): The dataframe with all the parts for the bulk CSV.
    """
    project, bouwnummer = df["Projectnummer"].iloc[0], df["Bouwnummer"].iloc[0]

    df = df[~df["Productcode"].apply(helpers.delete_productcode)]
    df = df[df["Name"].str.contains("LVLQ 90|LVLQ 100|LVLQ 144|LVLQ 69") | ((df["Name"].str.contains("LVLS 45")) & (df["Lengte"] > 3360)) | ((df["Name"].str.contains("SPANO 18")) & (df["Lengte"] > 2700)) | df["Materiaal"].str.contains("BAUB")]

    if df.empty:
        return

    df = df.astype({"Aantal": "int"})
    df = df.groupby(df.columns.tolist(), as_index=False).size()
    df["Aantal"] = (df["Aantal"] * df["size"]).astype(int)
    df = df.drop("size", axis=1)

    df["Nesting Prioriteit"] = df["Moduletype"]
    modules = sorted(df["Moduletype"].unique())
    prioriteit = dict(zip(modules, [x for x in range(len(modules), 0, -1)]))
    df = df.replace({"Nesting Prioriteit": prioriteit})

    df[["CNC Bewerking", "InkooporderNr"]] = "", ordernummer
    df["Dikte"] = df["Name"].apply(lambda x: helpers.get_dikte(x)).astype(int)

    df["Prio"] = df["Modulenaam"] + "-" + df["Station"]
    for key, value in prio_dict.items():
        df.loc[df["Prio"].str.contains(key), "Nesting Prioriteit"] = value

    df = df[
        [
            "Materiaal",
            "Productcode",
            "Name",
            "Dikte",
            "Aantal",
            "CNC Bewerking",
            "Modulenaam",
            "InkooporderNr",
            "Nesting Prioriteit",
            "Station",
        ]
    ]
    df = df.rename(
        columns={
            "Materiaal": "Materiaal BB",
            "Name": "OnderdeelNaam",
            "Dikte": "Dikte BB",
            "Aantal": "Aantal BB",
        }
    )
    df = df.sort_values(by=["OnderdeelNaam", "Modulenaam"])

    # Normaal-Normaal, bulk = False and casettes = False, BN
    if not bulk and not cassettes:
        df = df[~df["Productcode"].isin(bulk_file)]
        if cass_global:
            df = df[~df["Station"].isin(["WS101", "WS102", "WS103"])]
        df.to_csv(f"{path}/{ordernummer}-{project}-{bouwnummer}-BB.csv", index=False, sep=";")

    # Normaal-Bulk, bulk = True and casettes = False, BATCH
    elif bulk and not cassettes:
        df_bulk = df[df["Productcode"].isin(bulk_file)]
        if cass_global:
            df_bulk = df_bulk[~df_bulk["Station"].isin(["WS101", "WS102", "WS103"])]
        if not df_bulk.empty:
            df_bulk.to_csv(f"{path}/{ordernummer}-{project}-BB-BULK.csv", index=False, sep=";")

    # Cas-Normaal, bulk = False and casettes = True, BN
    elif not bulk and cassettes:
        df = df[~df["Productcode"].isin(bulk_file)]
        df = df[df["Station"].isin(["WS101", "WS102", "WS103"])]
        df.to_csv(f"{path}/{ordernummer}-{project}-{bouwnummer}-BB-CASSETTES.csv", index=False, sep=";")
  
    # Cas-Bulk, bulk = True and casettes = True, BATCH
    elif bulk and cassettes:
        df_bulk = df[df["Productcode"].isin(bulk_file)]
        df_bulk = df_bulk[df_bulk["Station"].isin(["WS101", "WS102", "WS103"])]
        if not df_bulk.empty:
            df_bulk.to_csv(f"{path}/{ordernummer}-{project}-BB-BULK-CASSETTES.csv", index=False, sep=";")


def VH(df: pd.DataFrame, ordernummer: str, path: str, prio_dict: dict, bulk_file: list,  meterkast_file: list, bulk: bool, cassettes: bool, cass_global: bool, meterkast: bool=False) -> None:
    """Gets the Van Hulst parts from the dataframe and saves it to a CSV file.

    Args:
        df (pd.DataFrame): The dataframe with all the parts.
        ordernummer (str): The ordernumber of the project.
        path (str): The path to save the CSV file.
        prio_dict (dict): The dictionary with the priority of the modules.
    """
    project, bouwnummer = df["Projectnummer"].iloc[0], df["Bouwnummer"].iloc[0]

    #! Implement bouwnummer voor verschill tussen H5-01 en BN35 (H5-01 altijd helemaal)
    bouwnummer = df["Bouwnummer"].iloc[0]
    bouwnummer_kort = bouwnummer
    if bouwnummer.startswith("BN"):
        bouwnummer_kort = bouwnummer.replace("BN", "")
   
    df = df[~df["Productcode"].apply(helpers.delete_productcode)]
    df = df[~(df["Name"].str.contains("LVLQ 90|LVLQ 100|LVLQ 144|LVLQ 69") | ((df["Name"].str.contains("LVLS 45")) & (df["Lengte"] > 3360)) | ((df["Name"].str.contains("SPANO 18")) & (df["Lengte"] > 2700)) | df["Materiaal"].str.contains("BAUB"))]
    df = df[~df["Materiaal"].str.contains("PRO")]

    if df.empty:
        return

    df["Dikte"] = df["Name"].apply(lambda x: helpers.get_dikte(x)).astype(int)
    df["InkooporderNr"] = f"{ordernummer}-{bouwnummer_kort}"
    df["Klant"] = f"geWOONhout {project} {bouwnummer}"
    df["Order"] = (
        str(project)
        + " "
        + str(bouwnummer)
        + " "
        + df["Materiaal"]
        + " "
        + df["Dikte"].astype(int).astype(str)
    )
    df["Bestand"] = (
        "P:\\"
        + str(project)
        + "\\DWG\\"
        + df["Materiaal"]
        + " "
        + df["Dikte"].astype(int).astype(str)
        + "\\"
        + df["Productcode"]
        + ".DWG"
    )
    df[
        [
            "Configuratie",
            "Setup",
            "Nesten",
            "Nest Rotatie Methode",
            "Nest Rotatie",
            "Nest Setnr",
        ]
    ] = ("", "", 1, 0, 180, 1)
    df["Index.1"] = df.index
    df = df.astype({"Aantal": int, "Dikte": int})
    df["Nesting Prioriteit"] = df["Moduletype"]
    # Barcode met cijfers, WS weghalen
    df["Barcode"] = (
        df["Productcode"]
        + "-"
        + df["Station"].str[-2:]
        + "-"
        + df["Moduletype"].str[-2:]
    )
    df = df.groupby(["Barcode"], as_index=False).agg(
        dict(
            map(
                (lambda x: (x, "sum") if x == "Aantal" else (x, "first")),
                df.columns.tolist(),
            )
        )
    )

    df["Prio"] = df["Modulenaam"] + "-" + df["Station"]
    for key, value in prio_dict.items():
        df.loc[df["Prio"].str.contains(key), "Nesting Prioriteit"] = value

    df = df[
        [
            "Klant",
            "Order",
            "InkooporderNr",
            "Configuratie",
            "Setup",
            "Materiaal",
            "Dikte",
            "Bestand",
            "Name",
            "Aantal",
            "Nesten",
            "Nest Rotatie Methode",
            "Nest Rotatie",
            "Nesting Prioriteit",
            "Nest Setnr",
            "Station",
            "Productcode",
            "Modulenaam",
            "Barcode",
        ]
    ]

    df = df.rename(
        columns={
            "Klant": "KlantvH",
            "Materiaal": "Materiaal vH",
            "Dikte": "Dikte vH",
            "Aantal": "AantalvH",
            "Name": "OnderdeelNaam",
        }
    )

    # Add -BW to the order number for binnenwanden, checken of dit mag voor alles.
    mask = (
        (df["Materiaal vH"] == "LVLS")
        & (df["Dikte vH"] == 45)
        & df["Station"].isin(["WS05", "WS114"])
    )

    df_rest = df[~mask]
    df_binnenwand = df[mask]
    df_binnenwand["Order"] += "-BW"
    df = pd.concat([df_rest, df_binnenwand], ignore_index=True, sort=False)

    # Convert modulenaam to string:
    df['Modulenaam'] = df['Modulenaam'].astype(str)

    # Meterkast CSV
    #! CHECK IF THIS HAS TO BE PER BOUWNUMMER OR PER PROJECT   
    df_meterkast = df[df["Productcode"].isin(meterkast_file)]
    df = df[~df["Productcode"].isin(meterkast_file)]
    if not df_meterkast.empty and meterkast:
        df_meterkast.to_csv(f"{path}/{ordernummer}-{project}-VH-METERKAST.csv", index=False, sep=";")

    # Normaal-Normaal, bulk = False and casettes = False, BN
    if not bulk and not cassettes:
        df = df[~df["Productcode"].isin(bulk_file)]
        if cass_global:
            df = df[~df["Station"].isin(["WS101", "WS102", "WS103"])]
        df.to_csv(f"{path}/{ordernummer}-{project}-{bouwnummer_kort}-VH.csv", index=False, sep=";")

    # Normaal-Bulk, bulk = True and casettes = False, BATCH
    elif bulk and not cassettes:
        df_bulk = df[df["Productcode"].isin(bulk_file)]
        df_bulk['Modulenaam'] = str(project) + "-BULK"
        if cass_global:
            df = df[~df["Station"].isin(["WS101", "WS102", "WS103"])]
        if not df_bulk.empty:
            df_bulk.to_csv(f"{path}/{ordernummer}-{project}-VH-BULK.csv", index=False, sep=";")

    # Cas-Normaal, bulk = False and casettes = True, BN
    elif not bulk and cassettes:
        df = df[~df["Productcode"].isin(bulk_file)]
        df = df[df["Station"].isin(["WS101", "WS102", "WS103"])]
        df.to_csv(f"{path}/{ordernummer}-{project}-{bouwnummer_kort}-VH-CASSETTES.csv", index=False, sep=";")

    # Cas-Bulk, bulk = True and casettes = True, BATCH
    elif bulk and cassettes:
        df_bulk = df[df["Productcode"].isin(bulk_file)]
        df_bulk = df_bulk[df_bulk["Station"].isin(["WS101", "WS102", "WS103"])]
        if not df_bulk.empty:
            df_bulk['Modulenaam'] = str(project) + "-BULK"
            df_bulk.to_csv(f"{path}/{ordernummer}-{project}-VH-BULK-CASSETTES.csv", index=False, sep=";")


def VMG(df: pd.DataFrame, ordernummer: str, path: str, prio_dict: dict, bulk_file: list, bulk: bool, cassettes: bool, cass_global: bool) -> None:
    """Gets the VMG parts from the dataframe and saves it to a CSV file.

    Args:
        df (pd.DataFrame): The dataframe with all the parts.
        ordernummer (str): The ordernumber of the project.
        path (str): The path to save the CSV file.
        prio_dict (dict): The dictionary with the priority of the modules.
    """
    project, bouwnummer = df["Projectnummer"].iloc[0], df["Bouwnummer"].iloc[0]
    df = df[df["Materiaal"].str.contains("PRO")]

    if df.empty:
        return
    
    df["Nesting Prioriteit"] = df["Moduletype"]
    df["Prio"] = df["Modulenaam"] + "-" + df["Station"]
    for key, value in prio_dict.items():
        df.loc[df["Prio"].str.contains(key), "Nesting Prioriteit"] = value
    

    if not 'BuildingStep' in df.columns:
        df['Bouwlaag promat'] = ''
    else:
        df['Bouwlaag promat'] = df['BuildingStep'].str.split('_').str[1]
        # Drop the BuildingStep column
        df.drop('BuildingStep', axis=1, inplace=True)
        bouwlaag_dict = helpers.bouwlaag_translation()
        df['Bouwlaag promat'] = df['Bouwlaag promat'].replace(bouwlaag_dict)

    df["Order"] = ordernummer
    df["Dikte"] = df["Name"].apply(lambda x: helpers.get_dikte(x)).astype(int)
    df["Materiaal"] = df["Materiaal"] + " " + df["Dikte"].astype(str)
    df = df[
        [
            "Order",
            "Modulenaam",
            "Station",
            "Name",
            "Materiaal",
            "Productcode",
            "Lengte",
            "Breedte",
            "Dikte",
            "Aantal",
            "Bouwlaag promat",
            "Nesting Prioriteit",
        ]
    ]
    df = df.rename(columns={"Name": "Naam"})

    df = df.astype({"Aantal": "int"})
    df = df.groupby(df.columns.tolist(), as_index=False).size()
    df["Aantal"] = (df["Aantal"] * df["size"]).astype(int)
    df = df.drop("size", axis=1)

    # Normaal-Normaal, bulk = False and casettes = False, BN
    if not bulk and not cassettes:
        df = df[~df["Productcode"].isin(bulk_file)]
        if cass_global:
            df = df[~df["Station"].isin(["WS101", "WS102", "WS103"])]
        df.to_csv(f"{path}/{ordernummer}-{project}-{bouwnummer}-VMG.csv", index=False, sep=";")

    # Normaal-Bulk, bulk = True and casettes = False, BATCH
    elif bulk and not cassettes:
        df_bulk = df[df["Productcode"].isin(bulk_file)]
        if cass_global:
            df_bulk = df_bulk[~df_bulk["Station"].isin(["WS101", "WS102", "WS103"])]
        if not df_bulk.empty:
            df_bulk.to_csv(f"{path}/{ordernummer}-{project}-VMG-BULK.csv", index=False, sep=";")

    # Cas-Normaal, bulk = False and casettes = True, BN
    elif not bulk and cassettes:
        df = df[~df["Productcode"].isin(bulk_file)]
        df = df[df["Station"].isin(["WS101", "WS102", "WS103"])]
        df.to_csv(f"{path}/{ordernummer}-{project}-{bouwnummer}-VMG-CASSETTES.csv", index=False, sep=";")

    # Cas-Bulk, bulk = True and casettes = True, BATCH
    elif bulk and cassettes:
        df_bulk = df[df["Productcode"].isin(bulk_file)]
        df_bulk = df_bulk[df_bulk["Station"].isin(["WS101", "WS102", "WS103"])]
        if not df_bulk.empty:
            df_bulk.to_csv(f"{path}/{ordernummer}-{project}-VMG-CASSETTES-BULK.csv", index=False, sep=";")


def ERP(df: pd.DataFrame, path: str, bnormt: bool) -> None:
    """Gets the ERP parts from the dataframe and saves it to a CSV file.

    Args:
        df (pd.DataFrame): The dataframe with all the parts.
        path (str): The path to save the CSV file.
        bnormt (bool): If the project is a Bnormt project.
    """
    project, bouwnummer = df["Projectnummer"].iloc[0], df["Bouwnummer"].iloc[0]

    df["Voorraad"] = df["Productcode"].apply(lambda x: helpers.delete_productcode(x))
    df["Voorraad"] = np.where(df["Voorraad"], "Ja", "Nee")

    df_unit = df[df["Eenheid"] == "unit"]
    df_metric = df[df["Eenheid"] != "unit"]

    # Compression on units
    df_unit = df_unit.sort_values(by=["Name", "Station", "Dikte", "Breedte", "Lengte"])
    df_unit = df_unit.groupby(
        ["Productcode", "Name", "Moduletype", "Materiaal", "Station", "Eenheid"],
        as_index=False,
    ).agg(
        dict(
            map(
                (lambda x: (x, "first") if x != "Aantal" else (x, "sum")),
                df_unit.columns.tolist(),
            )
        )
    )

    # Compression on m1, m2
    df_metric = df_metric.sort_values(
        by=["Name", "Station", "Dikte", "Breedte", "Lengte"]
    )
    df_metric = df_metric.groupby(
        ["Productcode", "Name", "Moduletype", "Materiaal", "Station", "Eenheid"],
        as_index=False,
    ).agg(
        dict(
            map(
                (
                    lambda x: (x, "sum")
                    if x == "Aantal"
                    else ((x, "sum") if x == "Gewicht" else (x, "first"))
                ),
                df_metric.columns.tolist(),
            )
        )
    )

    df_merged = pd.concat([df_unit, df_metric], ignore_index=True)
    df_merged["Name"] = df_merged["Name"].astype("string")
    df_merged = df_merged.sort_values(by=["Name", "Moduletype"])
    df_merged = df_merged.round({"Aantal": 2, "Gewicht": 3})
    df_merged = df_merged.rename(
        columns={
            "Categorie": "Artikelcategorie",
            "Name": "Productnaam",
            "IFC bestand": "IFC-bestand",
        }
    )

    df_merged["IFC-bestand"] = df_merged["IFC-bestand"].str.replace(" ", "_")
    
    if 'BuildingStep' in df.columns:
        # Remove the BuildingStep column
        df_merged.drop('BuildingStep', axis=1, inplace=True)
    
    if bnormt:
        df_merged.to_csv(f"{path}/{project}-{bouwnummer}-ERP.csv", index=False, sep=";")
    else:
        modules = df_merged["Moduletype"].unique()
        for mod_label in modules:
            df_mod = df_merged[df_merged["Moduletype"] == mod_label]
            df_mod.to_csv(
                f"{path}/{project}-{bouwnummer}-{mod_label}.csv", index=False, sep=";"
            )

def WS198(df: pd.DataFrame, path: str) -> None:
    project, bouwnummer = df["Projectnummer"].iloc[0], df["Bouwnummer"].iloc[0]

    # Get all products where "Station" is WS198
    df = df[df["Station"] == "WS198"]
    if df.empty:
        return
    
    df_unit = df[df["Eenheid"] == "unit"]
    df_metric = df[df["Eenheid"] != "unit"]

    # Compression on units
    df_unit = df_unit.sort_values(by=["Name", "Station", "Dikte", "Breedte", "Lengte"])
    df_unit = df_unit.groupby(
        ["Productcode", "Name", "Moduletype", "Materiaal", "Station", "Eenheid"],
        as_index=False,
    ).agg(
        dict(
            map(
                (lambda x: (x, "first") if x != "Aantal" else (x, "sum")),
                df_unit.columns.tolist(),
            )
        )
    )

    # Compression on m1, m2
    df_metric = df_metric.sort_values(
        by=["Name", "Station", "Dikte", "Breedte", "Lengte"]
    )
    df_metric = df_metric.groupby(
        ["Productcode", "Name", "Moduletype", "Materiaal", "Station", "Eenheid"],
        as_index=False,
    ).agg(
        dict(
            map(
                (
                    lambda x: (x, "sum")
                    if x == "Aantal"
                    else ((x, "sum") if x == "Gewicht" else (x, "first"))
                ),
                df_metric.columns.tolist(),
            )
        )
    )

    df_merged = pd.concat([df_unit, df_metric], ignore_index=True)
    df_merged["Name"] = df_merged["Name"].astype("string")
    df_merged = df_merged.sort_values(by=["Productcode"])
    df_merged = df_merged.round({"Aantal": 2})

    df_ws198 = df_merged[
        [
            "Name",
            "Productcode",
            "Aantal",
            "Eenheid",
            "Modulenaam",
            "Breedte",
            "Lengte",
            "Dikte",
        ]
    ]

    df_ws198.to_excel(f"{path}/{project}-{bouwnummer}-WS198.xlsx", index=False)