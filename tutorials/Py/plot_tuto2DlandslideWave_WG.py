import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pylab import matplotlib, mpl, figure, subplot, savefig, show
import matplotlib.gridspec as gridspec

# ============================================================
# Plot settings
# ============================================================

matplotlib.rcParams.update({"font.size": 12})
mpl.rcParams["lines.linewidth"] = 1.5
mpl.rcParams["lines.markersize"] = 5
mpl.rcParams["lines.markeredgewidth"] = 0.7

plt.rc("font", family="serif")

# ============================================================
# Numerical simulation folder
# ============================================================

folder = "../RAS/Grilli2017/2D_landslideWave"

# ============================================================
# Wave-gauge parameters
# ============================================================

totalL = 0.33
alphaThreshold = 0.5

# Time shift between numerical and experimental data
decal = 0.3

number_of_gauges = 4

# ============================================================
# Figure size and layout
# ============================================================

figwidth = 6
figheight = 3

gs = gridspec.GridSpec(4, 1)
gs.update(
    left=0.08,
    right=0.97,
    top=0.97,
    bottom=0.11,
    wspace=0.10,
    hspace=0.12
)

# ============================================================
# Functions
# ============================================================
# Read available sampleSet times from the postProcessing folder.


def get_sample_times(case_folder):

    sample_dir = os.path.join(
        case_folder,
        "postProcessing",
        "sampleSets"
    )

    if not os.path.isdir(sample_dir):
        print("Cannot find sampleSet directory:")
        print(sample_dir)
        sys.exit(0)

    time_names = []

    for name in os.listdir(sample_dir):

        try:
            float(name)
            time_names.append(name)

        except ValueError:
            pass

    time_names = sorted(
        time_names,
        key=lambda x: float(x)
    )

    print("Number of available sample times:", len(time_names))

    return time_names

# Read the water elevation at the four wave gauges.


def read_wave_gauges(case_folder):

    formatted_listTime = get_sample_times(case_folder)

    gauge_times = {}
    gauge_heights = {}

    for gauge_number in range(1, number_of_gauges + 1):

        gauge_times[gauge_number] = []
        gauge_heights[gauge_number] = []

    missing_files = 0

    for time_name in formatted_listTime:

        print("Reading time:", time_name)

        for gauge_number in range(1, number_of_gauges + 1):

            input_file = os.path.join(
                case_folder,
                "postProcessing",
                "sampleSets",
                time_name,
                "gauge_" + str(gauge_number) + "_alpha.water.xy"
            )

            if not os.path.isfile(input_file):

                missing_files += 1
                continue

            data = pd.read_csv(
                input_file,
                sep=r"\s+",
                header=None
            )

            if data.empty or data.shape[1] < 2:

                print("Skipping empty or invalid file:", input_file)
                continue

            found_interface = False

            for k in range(len(data[1])):

                if data[1][k] < alphaThreshold:

                    water_elevation = -totalL + data[0][k]
                    shifted_time = float(time_name) + decal

                    gauge_heights[gauge_number].append(water_elevation)
                    gauge_times[gauge_number].append(shifted_time)

                    found_interface = True
                    break

            if not found_interface:

                print("No water interface found in:", input_file)

    print("Finished reading case:", case_folder)

    return gauge_times, gauge_heights


def read_experimental_gauge(filename):
    """
    Read one experimental wave-gauge CSV file.
    Experimental elevations are converted from mm to m.
    """

    data = pd.read_csv(
        filename,
        header=0
    )

    data.columns = data.columns.str.strip()

    experimental_time = data["x"].to_numpy()
    experimental_height = data["y"].to_numpy() / 1000.0

    return experimental_time, experimental_height


# ============================================================
# Read numerical results
# ============================================================

times, heights = read_wave_gauges(folder)

# ============================================================
# Read experimental wave-gauge data
# ============================================================

experimental_times = {}
experimental_heights = {}

for gauge_number in range(1, number_of_gauges + 1):

    filename = (
        "DATA/Grilli2017/Grilli2017_WG"
        + str(gauge_number)
        + ".csv"
    )

    experimental_times[gauge_number], experimental_heights[gauge_number] = \
        read_experimental_gauge(filename)

# ============================================================
# Plot wave elevations
# ============================================================

figure(
    num=1,
    figsize=(figwidth, figheight),
    dpi=300,
    facecolor="w",
    edgecolor="w"
)

axes = []

for gauge_number in range(1, number_of_gauges + 1):

    ax = subplot(gs[gauge_number - 1, 0])
    axes.append(ax)

    # Experimental data
    ax.plot(
        experimental_times[gauge_number],
        experimental_heights[gauge_number],
        label="Grilli et al. (2017)",
        color="black",
        linestyle="None",
        marker="o",
        markerfacecolor="none",
        markeredgecolor="black",
        markersize=5
    )

    # Numerical simulation
    ax.plot(
        np.array(times[gauge_number]),
        np.array(heights[gauge_number]),
        label="sedInterFoam",
        color="orange",
        linestyle="-",
        linewidth=1.5
    )

    ax.set_ylabel(r"$\eta$ [m]")

    ax.set_ylim([
        -0.011,
        0.011
    ])

    ax.set_xlim([
        -0.01,
        8.0
    ])

    ax.grid(True)

    ax.text(
        0.985,
        0.88,
        "WG" + str(gauge_number),
        transform=ax.transAxes,
        horizontalalignment="right",
        verticalalignment="top"
    )

    if gauge_number < number_of_gauges:

        ax.set_xticklabels([])

axes[-1].set_xlabel("Time [s]")

axes[-1].legend(
    loc="lower left",
    framealpha=1
)

# ============================================================
# Save figure
# ============================================================

if not os.path.isdir("Figures"):

    os.makedirs("Figures")

savefig(
    "Figures/Grilli_comparison_WaveElevation.png",
    dpi=200,
    bbox_inches="tight"
)

show()
