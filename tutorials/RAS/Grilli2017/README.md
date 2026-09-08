# Grilli et al. (2017) submerged landslide-wave benchmark

This tutorial reproduces the submerged granular landslide-wave benchmark of
Grilli et al. (2017), Test 17, with `sedInterFoam`.

The case consists of a dense granular wedge released on a 35° submerged slope.
The landslide deforms downslope and generates a free-surface wave recorded at
several wave gauges. 

This benchmark was used in:

> Montellà, E. P., Romano, A., Barajas, G., Lozano, J. A., Vázquez, J. T.,
> Lara, J. L., & Fraile-Nuez, E. (2026). *Submarine flank collapses at Tagoro
> volcano: Insights from bathymetric surveys and 3D multiphase simulations*.
> Journal of Geophysical Research: Oceans, 131, e2025JC023976.  
> <https://doi.org/10.1029/2025JC023976>

## Tutorial structure

```text
tutorials/RAS/Grilli2017/
├── 1D_sedimentation
└── 2D_landslideWave
```

Post-processing scripts are located in the Python tutorial folder:

```text
tutorials//Py/
```

## Running the tutorial

The tutorial must be run in two steps.

### Step 1: 1D sedimentation

First, run the 1D sedimentation case:

```bash
cd 1D_sedimentation
./Allrun
```

This step prepares the initial dense granular state. It is used to establish a
consistent sediment volume fraction and pressure state before initializing the
2D landslide-wave case.

### Step 2: 2D landslide-wave simulation

After the 1D case has finished, run the 2D landslide-wave case:

```bash
cd ../2D_landslideWave
./Allrun
```

The 2D case generates the mesh, initializes the granular wedge, maps the
sedimentation result from `../1D_sedimentation`, and then runs the submerged
landslide-wave simulation.

## Benchmark reference

The physical benchmark corresponds to Test 17 of Grilli et al. (2017). The main
experimental parameters are:

| Quantity | Value |
|---|---:|
| Solid density | 2500 kg/m³ |
| Water density | 1000 kg/m³ |
| Water depth | 0.33 m |
| Particle diameter | 4 mm |
| Initial solid volume fraction | 0.61 |
| Slope angle | 35° |
| Initial granular height | 0.084 m |
| Initial granular length | 0.28 m |
| Tank length | 6 m |

Reference:

> Grilli, S. T., Shelby, M., Kimmoun, O., Dupont, G., Nicolsky, D., Ma, G.,
> Kirby, J. T., & Shi, F. (2017). *Modeling coastal tsunami hazard from
> submarine mass failures: Effect of slide rheology, experimental validation,
> and case studies off the US East Coast*. Natural Hazards, 86, 353-391.  
> <https://doi.org/10.1007/s11069-016-2692-3>

## Post-processing

Post-processing is done from the common Python tutorial folder:

```bash
cd ../../Py
```

The following scripts are provided for comparison with the experimental data:

```bash
python plot_tuto2DlandslideWave_DepositShape.py
python plot_tuto2DlandslideWave_WG.py
```

`plot_tuto2DlandslideWave_DepositShape.py` compares the simulated landslide shape with the
experimental deposit profiles.

`plot_tuto2DlandslideWave_WG.py` compares the simulated free-surface elevation with the
experimental wave-gauge records.

## Note on mesh resolution

This repository tutorial is intentionally coarser than the simulations
used in Montellà et al. (2026). The article used a refined 2D numerical wave tank
with approximately 1.1 million cells, including strong refinement near the free
surface and along the slope and toe region.

