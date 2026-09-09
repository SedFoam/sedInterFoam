import numpy as np
import pandas as pd
import fluidfoam

from scipy.interpolate import griddata

from pylab import matplotlib, mpl, figure, subplot, savefig, show
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from matplotlib.lines import Line2D

# ============================================================
# Figure style
# ============================================================

matplotlib.rcParams.update({"font.size": 12})
mpl.rcParams["lines.linewidth"] = 2
mpl.rcParams["lines.markersize"] = 6

plt.rc("font", family="serif")

# ============================================================
# User parameters
# ============================================================

# Numerical simulation
folder = "../RAS/Grilli2017/2D_landslideWave"

# Horizontal shift used for the experimental profiles
Decalage = 0.35

# CFD times to read (includes shift of 0.12 to account for the gate opening time)
listTime = [0.14, 0.44, 0.74]

# Experimental times corresponding to the three panels
expTimeLabels = [0.02, 0.32, 0.62]

titles = [
    r"$t=0.02$ s",
    r"$t=0.32$ s",
    r"$t=0.62$ s",
]

# Experimental files
exp_shape_files = [
    "DATA/Grilli2017/Grilli_shape_t0.02.csv",
    "DATA/Grilli2017/Grilli_shape_t0.32.csv",
    "DATA/Grilli2017/Grilli_shape_t0.62.csv",
]

initial_shape_file = "DATA/Grilli2017/Grilli_shape_t0.csv"

# Solid contour used to define the landslide boundary
alphaThreshold = 0.4

# ============================================================
# Interpolation grid
# ============================================================

ngridx = 400
ngridy = 100

xinterpmin = 0.0
xinterpmax = 2.
yinterpmin = 0.0
yinterpmax = 0.5

xi = np.linspace(xinterpmin, xinterpmax, ngridx)
yi = np.linspace(yinterpmin, yinterpmax, ngridy)

xinterp, yinterp = np.meshgrid(xi, yi)

# ============================================================
# Functions
# ============================================================


def readOpenFoam(case_folder, times):
    X, Y, Z = fluidfoam.readmesh(case_folder)

    alpha = []
    alphaW = []

    for tread in times:

        print("Reading " + case_folder + " at t=" + str(tread))

        alpha0 = fluidfoam.readscalar(
            case_folder,
            str(tread),
            "alpha.solid"
        )

        alphaW0 = fluidfoam.readscalar(
            case_folder,
            str(tread),
            "alpha.water"
        )

        alpha_i = griddata(
            (X, Y),
            alpha0,
            (xinterp, yinterp),
            method="linear"
        )

        alphaW_i = griddata(
            (X, Y),
            alphaW0,
            (xinterp, yinterp),
            method="linear"
        )

        alpha.append(alpha_i)
        alphaW.append(alphaW_i)

    return alpha, alphaW

# Read experimental landslide profile from Grilli et al. (2017).


def readGrilliShape(filename, decalage):

    data = pd.read_csv(filename, header=0)
    data.columns = data.columns.str.strip()

    x_shape = data["x"].to_numpy() + decalage
    y_shape = data["y"].to_numpy()

    return x_shape, y_shape


# ============================================================
# Read numerical and experimental data
# ============================================================

alpha, alphaW = readOpenFoam(folder, listTime)

x_grilli_initial, y_grilli_initial = readGrilliShape(initial_shape_file, Decalage)

exp_shapes = []

for filename in exp_shape_files:
    exp_shapes.append(readGrilliShape(filename, Decalage))

# ============================================================
# Plot parameters
# ============================================================

# Water contour levels
levelsW = np.arange(0.4, 1.1, 0.65)

# Solid volume-fraction contour
levelsLandslide = [alphaThreshold]

# Bed slope
x_fill = np.linspace(0.5, 1.08, 100)
y_fill = -0.7 * x_fill + 0.756

# ============================================================
# Figure layout
# ============================================================

gs = gridspec.GridSpec(1, 3)
gs.update(
    left=0.065,
    right=0.985,
    top=0.92,
    bottom=0.18,
    wspace=0.12,
    hspace=0.2
)

figwidth = 9
figheight = 3.0

figure(
    num=1,
    figsize=(figwidth, figheight),
    dpi=200
)

axes = []

# ============================================================
# Shape comparison
# ============================================================

for i in range(3):

    ax = subplot(gs[0, i])
    axes.append(ax)

    # --------------------------------------------------------
    # Solid bottom
    # --------------------------------------------------------

    ax.fill_between(
        x_fill,
        y_fill,
        0,
        color="grey",
        alpha=0.5
    )

    # --------------------------------------------------------
    # Panel title
    # --------------------------------------------------------

    ax.text(
        0.40,
        0.94,
        titles[i],
        fontsize=12,
        color="black",
        transform=ax.transAxes,
        verticalalignment="top"
    )

    # --------------------------------------------------------
    # Initial experimental shape
    # --------------------------------------------------------

    if i == 0:

        ax.plot(
            x_grilli_initial,
            y_grilli_initial,
            color="black",
            linestyle="-",
            linewidth=1.5
        )

    # --------------------------------------------------------
    # Water region
    # --------------------------------------------------------

    ax.contourf(
        xi,
        yi,
        alphaW[i],
        cmap=plt.cm.Blues,
        levels=levelsW,
        alpha=0.3
    )

    # --------------------------------------------------------
    # Landslide contour
    # --------------------------------------------------------

    ax.contour(
        xi,
        yi,
        alpha[i],
        levels=levelsLandslide,
        colors="orange",
        linewidths=2.0,
        linestyles="-"
    )

    # --------------------------------------------------------
    # Experimental shape
    # --------------------------------------------------------

    x_exp, y_exp = exp_shapes[i]

    ax.plot(
        x_exp,
        y_exp,
        linestyle="None",
        marker="o",
        markerfacecolor="none",
        markeredgecolor="black",
        markeredgewidth=0.7,
        markersize=6
    )

    # --------------------------------------------------------
    # Axes formatting
    # --------------------------------------------------------

    ax.set_xlim([0.5, 1.2])
    ax.set_ylim([0.0, 0.4])

    ax.set_aspect(
        "equal",
        adjustable="box"
    )

    ax.grid(True)
    ax.set_xlabel(r"$x$ [m]")

axes[0].set_ylabel(r"$h$ [m]")

for ax in axes[1:]:
    ax.set_yticklabels([])

# ============================================================
# Legend
# ============================================================

legend_handles = [
    Line2D(
        [0],
        [0],
        color="black",
        linestyle="-",
        linewidth=1.5,
        label="Initial shape"
    ),
    Line2D(
        [0],
        [0],
        color="black",
        linestyle="None",
        marker="o",
        markerfacecolor="none",
        markeredgecolor="black",
        markersize=6,
        label="Grilli et al. (2017)"
    ),
    Line2D(
        [0],
        [0],
        color="orange",
        linestyle="-",
        linewidth=2.0,
        label="sedInterFoam"
    ),
]

axes[0].legend(
    handles=legend_handles,
    loc="lower right",
    fontsize=8.5,
    framealpha=0.9
)

# ============================================================
# Save figure
# ============================================================

savefig(
    "Figures/landslideWave_DepositShape.png",
    dpi=200,
    bbox_inches="tight"
)

show()
