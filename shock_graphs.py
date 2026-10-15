import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Import the physics equations from Day 1
from shock_calculator import normal_shock, isentropic_flow

# Create a folder to save our graphs
output_folder = Path(__file__).resolve().parent / "figures"
output_folder.mkdir(exist_ok=True)

# Generate 300 Mach numbers between 1.01 and 10
mach_numbers = np.linspace(1.01, 10, 300)

# Calculate normal shock properties for each Mach number
pressure = []
temperature = []
density = []
mach_after = []

for mach in mach_numbers:
    p, t, rho, m2 = normal_shock(mach)

    pressure.append(p)
    temperature.append(t)
    density.append(rho)
    mach_after.append(m2)


# Function to create and save a graph
def make_graph(x, y, title, ylabel, filename):

    plt.figure(figsize=(8, 5))
    plt.plot(x, y, linewidth=2)

    plt.xlabel("Upstream Mach Number (M1)")
    plt.ylabel(ylabel)
    plt.title(title)

    plt.grid(True)
    plt.tight_layout()

    plt.savefig(output_folder / filename, dpi=300)
    plt.close()


# Graph 1: Pressure ratio
make_graph(
    mach_numbers,
    pressure,
    "Pressure Ratio Across a Normal Shock",
    "Pressure Ratio (P2/P1)",
    "pressure_ratio.png"
)

# Graph 2: Temperature ratio
make_graph(
    mach_numbers,
    temperature,
    "Temperature Ratio Across a Normal Shock",
    "Temperature Ratio (T2/T1)",
    "temperature_ratio.png"
)

# Graph 3: Density ratio
make_graph(
    mach_numbers,
    density,
    "Density Ratio Across a Normal Shock",
    "Density Ratio (rho2/rho1)",
    "density_ratio.png"
)

# Graph 4: Downstream Mach number
make_graph(
    mach_numbers,
    mach_after,
    "Downstream Mach Number Across a Normal Shock",
    "Downstream Mach Number (M2)",
    "downstream_mach.png"
)


# Graph 5: Compare Mach 2, 5, and 8
test_mach = [2, 5, 8]

test_pressure = []
test_temperature = []
test_density = []

for mach in test_mach:
    p, t, rho, m2 = normal_shock(mach)

    test_pressure.append(p)
    test_temperature.append(t)
    test_density.append(rho)

x = np.arange(len(test_mach))
width = 0.25

plt.figure(figsize=(9, 5))

plt.bar(x - width, test_pressure, width, label="Pressure")
plt.bar(x, test_temperature, width, label="Temperature")
plt.bar(x + width, test_density, width, label="Density")

plt.xticks(x, ["Mach 2", "Mach 5", "Mach 8"])
plt.ylabel("Downstream / Upstream Ratio")
plt.title("Normal Shock Comparison at Different Mach Numbers")
plt.legend()
plt.grid(axis="y")

plt.tight_layout()
plt.savefig(output_folder / "mach_comparison.png", dpi=300)
plt.close()


# Graph 6: Isentropic flow comparison
# These are static-to-stagnation ratios, not shock ratios
isentropic_pressure = []
isentropic_temperature = []
isentropic_density = []

for mach in mach_numbers:
    p, t, rho = isentropic_flow(mach)

    isentropic_pressure.append(p)
    isentropic_temperature.append(t)
    isentropic_density.append(rho)

plt.figure(figsize=(8, 5))

plt.plot(mach_numbers, isentropic_pressure, label="P/P0")
plt.plot(mach_numbers, isentropic_temperature, label="T/T0")
plt.plot(mach_numbers, isentropic_density, label="rho/rho0")

plt.xlabel("Mach Number")
plt.ylabel("Static / Stagnation Ratio")
plt.title("Isentropic Compressible Flow")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig(output_folder / "isentropic_flow.png", dpi=300)
plt.close()

print("All 6 graphs generated successfully!")
print(f"Saved to: {output_folder}")