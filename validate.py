
import numpy as np
from shock_calculator import normal_shock

# Reference values calculated from NASA's normal shock equations
# for air with gamma = 1.4
reference_values = {
    2: (4.5000, 1.6875, 2.6667, 0.5774),
    3: (10.3333, 2.6790, 3.8571, 0.4752),
    5: (29.0000, 5.8000, 5.0000, 0.4152),
    8: (74.5000, 13.3867, 5.5652, 0.3929)
}

print("NORMAL SHOCK VALIDATION")
print("-----------------------")

for mach, expected in reference_values.items():
    calculated = normal_shock(mach)

    passed = np.allclose(
        calculated,
        expected,
        rtol=0,
        atol=0.0001
    )

    status = "PASS" if passed else "FAIL"
    print(f"Mach {mach}: {status}")

    if not passed:
        print(f"  Calculated: {calculated}")
        print(f"  Reference:  {expected}")

print("-----------------------")