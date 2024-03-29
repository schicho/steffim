import json
import os
from datetime import datetime

import matplotlib.pyplot as plt

STEFFIM_PLOT_STYLE = "seaborn-v0_8-darkgrid"


def plot_by_chair(chair_data):
    with plt.style.context(STEFFIM_PLOT_STYLE):
        _plot_by_chair(chair_data)


def _plot_by_chair(chair_data):
    fig, ax = plt.subplots(figsize=(10, 10), constrained_layout=True)
    fig.set_figwidth(8)
    fig.set_figheight(5)

    plt.xticks(rotation=90)

    ax.set_title("Stef by Chair")

    # force integer y-axis
    ax.yaxis.get_major_locator().set_params(integer=True)
    ax.xaxis.get_major_locator().set_params(integer=True)

    # leave out empty chairs
    chair_data = [chair for chair in chair_data if len(chair._stef) > 0]

    # list of tuples (chair_name, stef_count)
    chair_and_stef_count = [(chair.name, len(chair._stef)) for chair in chair_data]

    # sort by stef count and then by name
    chair_names, stef_counts = zip(
        *sorted(chair_and_stef_count, key=lambda x: (x[1], x[0]))
    )

    rects = ax.bar(chair_names, stef_counts)
    ax.bar_label(
        rects, [f"{count}" for count in stef_counts], padding=-32, fontweight="bold"
    )

    fig.savefig("generated/stef_by_chair.svg")


def plot_over_time():
    with plt.style.context(STEFFIM_PLOT_STYLE):
        _plot_over_time()


def _plot_over_time():
    fig, ax = plt.subplots(figsize=(10, 10), constrained_layout=True)
    fig.set_figwidth(8)
    fig.set_figheight(5)

    plt.xticks(rotation=90)

    ax.set_title("#Stef Over Time")

    # force integer axis
    ax.yaxis.get_major_locator().set_params(integer=True)

    # get list of historic files
    historic_files = [f for f in os.listdir("historic") if f.endswith(".json")]
    historic_files.sort()

    # get data from historic files
    historic_data = []
    for historic_file in historic_files:
        with open(f"historic/{historic_file}", "r") as f:
            historic_data.append(json.load(f))

    xData = []
    yData = []

    for historic in historic_data:
        # convert timestamp to datetime YYYY-MM-DD
        timestamp = datetime.fromtimestamp(float(historic["timestamp"]))

        xData.append(timestamp.strftime("%Y-%m-%d"))

        # summarize stef count over all chairs
        stef_count = 0
        for chair in historic["data"]:
            stef_count += len(chair["stef_list"])

        yData.append(stef_count)

    ax.plot(xData, yData)
    fig.savefig("generated/stef_over_time.svg")
