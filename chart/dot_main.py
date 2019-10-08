# -*- coding: utf-8 -*-

from typing import Any, Dict

import numpy as np
import pandas as pd

from fun.chart.dot import DotScatter


def plot_chart(df, column, settings):

    data = []

    try:
        vs = df["{}-1".format(column)].values
        vs = vs[np.logical_not(np.isnan(vs))]
        data.append(vs)

        vs = df["{}-2".format(column)].values
        vs = vs[np.logical_not(np.isnan(vs))]
        data.append(vs)

        vs = df["{}-3".format(column)].values
        vs = vs[np.logical_not(np.isnan(vs))]
        data.append(vs)

    except KeyError:
        pass

    p = DotScatter(
        data,
        data_round=settings.get("data_round", True),
        data_ndigits=settings.get("data_ndigits", 0),
        title=settings.get("title", "{} Change".format(column.replace("-", " "))),
        xlabel=settings.get("xlabel", ""),
        ylabel=settings.get("ylabel", column.replace("-", " ")),
        text=settings.get("text", ""),
        title_font_size=settings.get("title_font_size", 14),
        label_font_size=settings.get("label_font_size", 10),
        tick_font_size=settings.get("tick_font_size", 8),
        text_font_size=settings.get("text_font_size", 8),
        group_width=settings.get("group_width", 1),
        ymargin=settings.get("ymargin", 1),
        point_size=settings.get("point_size", 20),
        # point_size=settings.get("point_size", 0.05),
        point_padding=settings.get("point_padding", 0.07),
        # point_padding=settings.get("point_padding", 1.25),
        point_colors=settings.get("point_colors", ["#ff0000", "#00ff48", "#0088ff"]),
        point_alpha=settings.get("point_alpha", 1),
        xticklabels=settings.get("xticklabels", ["Base", "6W", "12W"]),
        line_colors=settings.get("line_colors", ["#000000", "#000000", "#000000"]),
        line_alpha=settings.get("line_alpha", 1),
        line_width=settings.get("line_width", 2),
        line_length=settings.get("line_length", 7),
        line_style=settings.get("line_style", "-."),
        legend=settings.get("legend", False),
        calc=settings.get("calc", "mean"),
        dpi=settings.get("dpi", 500),
        output=settings.get("output", "{}.png".format(column).replace("/", "_")),
    )

    p.plot()


if __name__ == "__main__":
    labels = [
        "Weight",
        "BMI",
        "HAMD",
        "BDI",
        "STAI-State",
        "STAI-Trait",
        "ステージ-STAI-State",
        "ステージ-STAI-Trait",
        "PSQI",
        "GSRS-酸逆流",
        "GSRS-腹痛",
        "GSRS-消化不良",
        "GSRS-下痢",
        "GSRS-便秘",
        "GSRS-全体スコア",
        "Lactulose-%Recovery",
        "Mannnitol",
        "Lactulose/Mannitol-Ratio",
        "MRI_Neutral",
        "酢酸",
        "プロピオン酸",
        "n酪酸",
        "CTACK",
        "Eotaxin",
        "G-CSF",
        "GM-CSF",
        "GROa",
        "HGF",
        "IFN-a2",
        "IL-1a",
        "IL-1b",
        "IL-1ra",
        "IL-2",
        "IL-4",
        "IL-5",
        "IL-6",
        "IL-7",
        "IL-8",
        "IL-9",
        "IL-10",
        "IL-12(p70)",
        "IL-13",
        "IL-15",
        "IL-16",
        "IL-18",
        "IP-10",
        "LIF",
        "MCP-1",
        "M-CSF",
        "MIF",
        "MIG",
        "MIP-1a",
        "MIP-1b",
        "b-NGF",
        "PDGF-bb",
        "RANTES",
        "SCF",
        "SCGF-b",
        "SDF-1a",
        "TNF-a",
        "TNF-b",
        "TRAIL",
        "VEGF",
        "Total-bacteria",
        "C.coccoides-g.",
        "C.leptum-sg.",
        "B.fragilis-g.",
        "Bifidobacterium",
        "Atopobium-cluster",
        "Prevotella",
        "C.difficile",
        "C.perfringens",
        "Total-Lactobacillus",
        "L.brevis",
        "L.casei-sg.",
        "L.fermentum",
        "L.gasseri-sg.",
        "L.plantarum-sg.",
        "L.reuteri-sg.",
        "L.ruminis-sg.",
        "L.sakei-sg.",
        "Enterobacteriaceae",
        "Enterococcus",
        "Staphylococcus",
    ]

    ###########################################################################

    settings: Dict[str, Any] = {label: {} for label in labels}

    ###########################################################################
    # YOUR JOB
    # your csv file for y labels and p values

    df = pd.read_csv("/home/neko/Downloads/YlableP - in ncnp.csv")

    ###########################################################################

    for label in labels:
        ylabel = df[label][0]
        if type(ylabel) != str:
            ylabel = ""

        p = float(df[label][1])

        settings[label]["ylabel"] = "{} {}".format(label, ylabel)

        if p < 0.05:
            settings[label]["text"] = "P={}".format(round(p, 3))
        else:
            settings[label]["text"] = "P={}".format(round(p, 2))

    ###########################################################################
    # YOUR JOB

    settings["ステージ-STAI-State"]["title"] = "STAI State Stage"
    settings["ステージ-STAI-State"]["ylabel"] = "Stage Level"

    settings["ステージ-STAI-Trait"]["title"] = "STAI Trait Stage"
    settings["ステージ-STAI-Trait"]["ylabel"] = "Stage Level"

    settings["GSRS-酸逆流"]["title"] = "GSRS Reflux"
    settings["GSRS-酸逆流"]["ylabel"] = "GSRS Reflux Score"

    settings["GSRS-腹痛"]["title"] = "GSRS Abdominal Pain"
    settings["GSRS-腹痛"]["ylabel"] = "GSRS Abdominal Pain Score"

    settings["GSRS-消化不良"]["title"] = "GSRS Indigestion"
    settings["GSRS-消化不良"]["ylabel"] = "GSRS Indigestion Score"

    settings["GSRS-下痢"]["title"] = "GSRS Aiarrhoea"
    settings["GSRS-下痢"]["ylabel"] = "GSRS Aiarrhoea Score"

    settings["GSRS-便秘"]["title"] = "GSRS Constipation"
    settings["GSRS-便秘"]["ylabel"] = "GSRS Constipation Score"

    settings["GSRS-全体スコア"]["title"] = "GSRS Total"
    settings["GSRS-全体スコア"]["ylabel"] = "GSRS Total Score"

    settings["Lactulose-%Recovery"]["ymargin"] = 0.05
    settings["Lactulose-%Recovery"]["data_ndigits"] = 3

    settings["Lactulose/Mannitol-Ratio"]["ymargin"] = 0.05
    settings["Lactulose/Mannitol-Ratio"]["data_ndigits"] = 3

    settings["MRI_Neutral"]["xticklabels"] = ["base", "12W"]
    settings["MRI_Neutral"]["point_colors"] = ["#ff0000", "#0088ff"]
    settings["MRI_Neutral"]["ymargin"] = 0.05
    settings["MRI_Neutral"]["data_ndigits"] = 3
    settings["MRI_Neutral"]["title"] = "MRI Neutral Change"
    settings["MRI_Neutral"]["ylabel"] = "MRI Neutral Score"

    settings["酢酸"]["title"] = "Acetic Acid"
    settings["酢酸"]["ylabel"] = "Acetic Acid(μmol/L plasma)"

    settings["プロピオン酸"]["title"] = "Propionic Acid"
    settings["プロピオン酸"]["ylabel"] = "Propionic Acid(μmol/L plasma)"

    settings["n酪酸"]["title"] = "N-butyric Acid"
    settings["n酪酸"]["ylabel"] = "N-butyric Acid(μmol/L plasma)"
    settings["n酪酸"]["ymargin"] = 0.05
    settings["n酪酸"]["data_ndigits"] = 3

    settings["GM-CSF"]["ymargin"] = 0.05
    settings["GM-CSF"]["data_ndigits"] = 3

    settings["IFN-a2"]["ymargin"] = 0.05
    settings["IFN-a2"]["data_ndigits"] = 3

    settings["IL-1b"]["ymargin"] = 0.05
    settings["IL-1b"]["data_ndigits"] = 3

    settings["IL-2"]["ymargin"] = 0.05
    settings["IL-2"]["data_ndigits"] = 3

    settings["IL-4"]["ymargin"] = 0.05
    settings["IL-4"]["data_ndigits"] = 3

    settings["IL-6"]["ymargin"] = 0.05
    settings["IL-6"]["data_ndigits"] = 3

    settings["IL-7"]["ymargin"] = 0.05
    settings["IL-7"]["data_ndigits"] = 3

    settings["IL-8"]["ymargin"] = 0.05
    settings["IL-8"]["data_ndigits"] = 3

    settings["IL-10"]["ymargin"] = 0.05
    settings["IL-10"]["data_ndigits"] = 3

    settings["IL-12(p70)"]["ymargin"] = 0.05
    settings["IL-12(p70)"]["data_ndigits"] = 3

    settings["IL-13"]["ymargin"] = 0.05
    settings["IL-13"]["data_ndigits"] = 3

    settings["MIP-1a"]["ymargin"] = 0.05
    settings["MIP-1a"]["data_ndigits"] = 3

    settings["b-NGF"]["ymargin"] = 0.05
    settings["b-NGF"]["data_ndigits"] = 3

    settings["Total-bacteria"]["ymargin"] = 0.05
    settings["Total-bacteria"]["data_ndigits"] = 3

    settings["C.coccoides-g."]["ymargin"] = 0.05
    settings["C.coccoides-g."]["data_ndigits"] = 3

    settings["C.leptum-sg."]["ymargin"] = 0.05
    settings["C.leptum-sg."]["data_ndigits"] = 3

    settings["B.fragilis-g."]["ymargin"] = 0.05
    settings["B.fragilis-g."]["data_ndigits"] = 3

    settings["Bifidobacterium"]["ymargin"] = 0.05
    settings["Bifidobacterium"]["data_ndigits"] = 3

    settings["Atopobium-cluster"]["ymargin"] = 0.05
    settings["Atopobium-cluster"]["data_ndigits"] = 3

    settings["Prevotella"]["ymargin"] = 0.05
    settings["Prevotella"]["data_ndigits"] = 3

    settings["C.difficile"]["ymargin"] = 0.05
    settings["C.difficile"]["data_ndigits"] = 3
    settings["C.difficile"]["group_width"] = 2
    settings["C.difficile"]["point_padding"] = 0.1

    settings["C.perfringens"]["ymargin"] = 0.05
    settings["C.perfringens"]["data_ndigits"] = 3
    settings["C.perfringens"]["group_width"] = 2
    settings["C.perfringens"]["point_padding"] = 0.1

    settings["Total-Lactobacillus"]["ymargin"] = 0.05
    settings["Total-Lactobacillus"]["data_ndigits"] = 3

    settings["L.brevis"]["ymargin"] = 0.05
    settings["L.brevis"]["data_ndigits"] = 3
    settings["L.brevis"]["group_width"] = 2
    settings["L.brevis"]["point_padding"] = 0.1

    settings["L.casei-sg."]["ymargin"] = 0.05
    settings["L.casei-sg."]["data_ndigits"] = 3

    settings["L.fermentum"]["ymargin"] = 0.05
    settings["L.fermentum"]["data_ndigits"] = 3

    settings["L.gasseri-sg."]["ymargin"] = 0.05
    settings["L.gasseri-sg."]["data_ndigits"] = 3

    settings["L.plantarum-sg."]["ymargin"] = 0.05
    settings["L.plantarum-sg."]["data_ndigits"] = 3

    settings["L.reuteri-sg."]["ymargin"] = 0.05
    settings["L.reuteri-sg."]["data_ndigits"] = 3

    settings["L.ruminis-sg."]["ymargin"] = 0.05
    settings["L.ruminis-sg."]["data_ndigits"] = 3

    settings["L.sakei-sg."]["ymargin"] = 0.05
    settings["L.sakei-sg."]["data_ndigits"] = 3

    settings["Enterobacteriaceae"]["ymargin"] = 0.05
    settings["Enterobacteriaceae"]["data_ndigits"] = 3

    settings["Enterococcus"]["ymargin"] = 0.05
    settings["Enterococcus"]["data_ndigits"] = 3

    settings["Staphylococcus"]["ymargin"] = 0.05
    settings["Staphylococcus"]["data_ndigits"] = 3

    settings["n酪酸"]["ymargin"] = 0.05
    settings["n酪酸"]["data_ndigits"] = 3

    ###########################################################################

    ###########################################################################
    # YOUR JOB
    # your data csv file

    df = pd.read_csv("/home/neko/Downloads/data横.csv")

    ##########################################################################

    for column, setting in settings.items():
        plot_chart(df, column, setting)
