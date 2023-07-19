import pandas as pd
import numpy as np
import helpers

def BB(df: pd.DataFrame, ordernummer: str, path: str, prio_dict: dict, productcodes: list) -> None:
    """Gets the BB parts from the dataframe and saves it to a CSV file.

    Args:
        df (pd.DataFrame): The dataframe with all the parts.
        ordernummer (str): The ordernumber of the project.
        path (str): The path to save the CSV file.
        prio_dict (dict): The dictionary with the priority of the modules.
    """
    project = df["Projectnummer"].iloc[0]

    df = df[~df["Productcode"].apply(helpers.delete_productcode)]
    df = df[df["Name"].str.contains("LVLQ 90|LVLQ 100|LVLQ 144") | df["Productcode"].isin(productcodes)]

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
    df.to_csv(f"{path}/{project}-BB.csv", index=False, sep=",")


def VH(df: pd.DataFrame, ordernummer: str, path: str, prio_dict: dict, productcodes: list) -> None:
    """Gets the Van Hulst parts from the dataframe and saves it to a CSV file.

    Args:
        df (pd.DataFrame): The dataframe with all the parts.
        ordernummer (str): The ordernumber of the project.
        path (str): The path to save the CSV file.
        prio_dict (dict): The dictionary with the priority of the modules.
    """
    project, bouwnummer = df["Projectnummer"].iloc[0], df["Bouwnummer"].iloc[0]
    
    df = df[~df["Productcode"].apply(helpers.delete_productcode)]
    df = df[(~df["Name"].str.contains("LVLQ 90|LVLQ 100|LVLQ 144")) & (~df["Productcode"].isin(productcodes))]

    if df.empty:
        return

    df["Dikte"] = df["Name"].apply(lambda x: helpers.get_dikte(x)).astype(int)
    df["InkooporderNr"] = f"{ordernummer}-{bouwnummer[-2:]}"
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
        + "\\"
        + bouwnummer
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

    binnenwand = True
    if binnenwand:
        mask = (
            (df["Materiaal vH"] == "LVLS")
            & (df["Dikte vH"] == 45)
            & (df["Station"] == "WS05")
        )
        df_rest = df[~mask]
        df_binnenwand = df[mask]
        df_binnenwand["InkooporderNr"] = df_binnenwand["InkooporderNr"] + "-BW"
        df_binnenwand.to_csv(
            f"{path}/{ordernummer}-{bouwnummer[-2:]}-BW-{project}-{bouwnummer}-VH.csv",
            index=False,
            sep=";",
        )
        df_rest.to_csv(
            f"{path}/{ordernummer}-{bouwnummer[-2:]}-{project}-{bouwnummer}-VH.csv",
            index=False,
            sep=";",
        )
    else:
        df.to_csv(
            f"{path}/{ordernummer}-{bouwnummer[-2:]}-{project}-{bouwnummer}-VH.csv",
            index=False,
            sep=";",
        )


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

    if bnormt:
        df_merged.to_csv(f"{path}/{project}-{bouwnummer}-ERP.csv", index=False, sep=";")
    else:
        modules = df_merged["Moduletype"].unique()
        for mod_label in modules:
            df_mod = df_merged[df_merged["Moduletype"] == mod_label]
            df_mod.to_csv(
                f"{path}/{project}-{bouwnummer}-{mod_label}.csv", index=False, sep=";"
            )

def VMG(df: pd.DataFrame, ordernummer: str, path: str) -> None:
    """Gets the VMG parts from the dataframe and saves it to a CSV file.

    Args:
        df (pd.DataFrame): The dataframe with all the parts.
        ordernummer (str): The ordernumber of the project.
        path (str): The path to save the CSV file.
    """
    project = df["Projectnummer"].iloc[0]
    df = df[df["Materiaal"] == "PRO"]

    if df.empty:
        return

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
            "Aantal",
        ]
    ]
    df = df.rename(columns={"Name": "Naam"})

    df = df.astype({"Aantal": "int"})
    df = df.groupby(df.columns.tolist(), as_index=False).size()
    df["Aantal"] = (df["Aantal"] * df["size"]).astype(int)
    df = df.drop("size", axis=1)

    df.to_csv(f"{path}/{project}-VMG.csv", index=False)