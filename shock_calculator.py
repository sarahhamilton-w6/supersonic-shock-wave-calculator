import numpy as np

# Air properties
GAMMA = 1.4
R = 287.05  # Specific gas constant for air (J/kg/K)


# Calculate the speed of sound
def speed_of_sound(temperature):
    return np.sqrt(GAMMA * R * temperature)


# Calculate Mach number from velocity and temperature
def calculate_mach(velocity, temperature):
    return velocity / speed_of_sound(temperature)


# Calculate isentropic compressible-flow properties
def isentropic_flow(mach):
    pressure_ratio = (1 + (GAMMA - 1) / 2 * mach**2) ** (
        -GAMMA / (GAMMA - 1)
    )

    temperature_ratio = 1 / (
        1 + (GAMMA - 1) / 2 * mach**2
    )

    density_ratio = (1 + (GAMMA - 1) / 2 * mach**2) ** (
        -1 / (GAMMA - 1)
    )

    return pressure_ratio, temperature_ratio, density_ratio


# Calculate flow properties across a normal shock
def normal_shock(mach):
    if not np.isfinite(mach) or mach <= 1:
        raise ValueError("Upstream Mach number must be a finite number greater than 1.")
        

    # Pressure ratio across shock
    pressure_ratio = 1 + (
        2 * GAMMA / (GAMMA + 1)
    ) * (mach**2 - 1)

    # Density ratio across shock
    density_ratio = (
        (GAMMA + 1) * mach**2
    ) / (
        (GAMMA - 1) * mach**2 + 2
    )

    # Temperature ratio across shock
    temperature_ratio = pressure_ratio / density_ratio

    # Mach number after shock
    mach_after = np.sqrt(
        (1 + (GAMMA - 1) / 2 * mach**2)
        / (GAMMA * mach**2 - (GAMMA - 1) / 2)
    )

    return pressure_ratio, temperature_ratio, density_ratio, mach_after


# Calculate and display results for given conditions
def analyze_flow(mach, pressure, temperature):

    # Conditions before the shock
    sound_speed = speed_of_sound(temperature)
    velocity = mach * sound_speed

    # Calculate shock properties
    p_ratio, t_ratio, rho_ratio, mach_after = normal_shock(mach)

    # Conditions after the shock
    pressure_after = pressure * p_ratio
    temperature_after = temperature * t_ratio
    density_before = pressure / (R * temperature)
    density_after = density_before * rho_ratio
    velocity_after = mach_after * speed_of_sound(temperature_after)

    # Display results
    print("\n========== FLOW ANALYSIS ==========")

    print(f"Upstream Mach Number: {mach:.2f}")
    print(f"Upstream Velocity: {velocity:.2f} m/s")
    print(f"Upstream Pressure: {pressure:.2f} Pa")
    print(f"Upstream Temperature: {temperature:.2f} K")

    print("\n---------- NORMAL SHOCK ----------")

    print(f"Pressure Ratio (P2/P1): {p_ratio:.4f}")
    print(f"Temperature Ratio (T2/T1): {t_ratio:.4f}")
    print(f"Density Ratio (rho2/rho1): {rho_ratio:.4f}")

    print("\n---------- AFTER SHOCK ----------")

    print(f"Downstream Mach Number: {mach_after:.4f}")
    print(f"Downstream Velocity: {velocity_after:.2f} m/s")
    print(f"Downstream Pressure: {pressure_after:.2f} Pa")
    print(f"Downstream Temperature: {temperature_after:.2f} K")
    print(f"Downstream Density: {density_after:.4f} kg/m^3")

    print("===================================\n")


# Run the calculator
if __name__ == "__main__":

    print("SUPERSONIC FLOW & SHOCK WAVE CALCULATOR")

    # Ask the user for flow conditions
    try:
        mach = float(input("Enter upstream Mach number (>1): "))
        pressure = float(input("Enter upstream pressure (Pa): "))
        temperature = float(input("Enter upstream temperature (K): "))

        if not np.isfinite(pressure) or not np.isfinite(temperature):
            raise ValueError("Pressure and temperature must be finite numbers.")
        
        if pressure <= 0 or temperature <= 0:
            raise ValueError("Pressure and temperature must be positive.")

        analyze_flow(mach, pressure, temperature)

    except ValueError as error:
        print(f"Invalid input: {error}")

    # Test the calculator at different Mach numbers
    print("\n========== MACH NUMBER TESTS ==========")

    test_mach_numbers = [2, 3, 5, 8]

    for m in test_mach_numbers:
        p, t, rho, m_after = normal_shock(m)

        print(
            f"Mach {m}: "
            f"P2/P1 = {p:.3f}, "
            f"T2/T1 = {t:.3f}, "
            f"rho2/rho1 = {rho:.3f}, "
            f"M2 = {m_after:.3f}"
        )

    print("=======================================")
