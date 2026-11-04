import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from cycle_calc import (
    Hdot03,
    Pres,
    gamma_300,
    stagPres,
    Temp,
    stagTemp,
    massFlow,
    Density,
    specific_stagEnthalpy,
    specific_Enthalpy,
    velocities,
    areas,
    dynamicPres,
    MACH,
    F_calc,
    F_calc_static,
    F_calc_static_ideal,
    ve_calc,
    eta_c,
    eta_m,
    WCdot,
    WTdot,
    Hdot02,
    Hdot03,
    Hdot04,
    Hdot05,
    Hdot06,    
    mdot_fuel,
    mdot_fuel_AB,
    Δh02_01,
    entropy,
    test_time
)


def tableRound(matrix, specifier=2):
    new_matrix = []
    for i in matrix:
        new_matrix.append(round(i, specifier))
    return new_matrix

def build_cycle_table():
    engine_cycle_table = {
        "Station": ["1: Inlet", "2: Compressor exit", "3: Combustor exit", "4: Turbine exit", "5: Afterburner exit", "6: Nozzle exit"],
        "P0 [kPa]": tableRound(np.divide(stagPres, 1000)),
        "T0 [K]": tableRound(stagTemp),
        "P [kPa]": tableRound(np.divide(Pres, 1000)),
        "T [K]": tableRound(Temp),
        "Mdot [kg/s]": tableRound(massFlow, 3),
        "rho [kg/m^3]": tableRound(Density, 3),
        "h0 [kJ/kg]": tableRound(np.divide(specific_stagEnthalpy, 1000)),
        "h [kJ/kg]": tableRound(np.divide(specific_Enthalpy, 1000)),
        "v [m/s]": tableRound(velocities),
        "A [m^2]": tableRound(areas, 5),
        "q [kPa]": tableRound(np.divide(dynamicPres, 1000)),
        "|": ['|', '|', '|', '|', '|', '|'],
        "M": tableRound(MACH),
        "-": ['-', '-', '-', '-', '-', '-'],
        "Thrust [N]": ['*', '*', f'[P05/PA = {stagPres[4] / stagPres[0]:.2f}]', f' {round(F_calc, 2)} (v1 = {velocities[0]} m/s)', f' {F_calc_static_ideal:.2f} (ideal)', f'{round(F_calc_static, 2)} (static)']
    }
    return pd.DataFrame(engine_cycle_table)


def printboard():
    F_calc_local = massFlow[5] * ve_calc
    print(f'eta_c = {eta_c:.2f}')
    print(f'WCdot = {WCdot:.2f} kW [kJ/s]')
    print(f'eta_m = {eta_m:.2f}')
    print(f'WTdot = {WTdot:.2f} kW [kJ/s]')
    print(f'P1 = {Pres[0]/1000:.2f} kPa')
    print(f'P01 = {stagPres[0]/1000:.2f} kPa')
    print(f'P02 = {stagPres[1]/1000:.2f} kPa')
    print(f'P03 = {stagPres[2]/1000:.2f} kPa')
    print(f'P04 = {stagPres[3]/1000:.2f} kPa')
    print(f'P05 = {stagPres[4]/1000:.2f} kPa')
    print(f'P06 = {stagPres[5]/1000:.2f} kPa')
    print(f'P05/P06 = {stagPres[4] / stagPres[5]:.3f}')
    print(f'T05 = {stagTemp[4]:.2f} K')
    print(f'T06 = {stagTemp[5]:.2f} K')
    print(f'H2 = {Hdot02/1000:.2f} kW')
    print(f'H3 = {Hdot03/1000:.2f} kW')
    print(f'H4 = {Hdot04/1000:.2f} kW')
    print(f'H5 = {Hdot05/1000:.2f} kW')
    print(f'H6 = {Hdot06/1000:.2f} kW')
    print(f'mdot_air = {massFlow[0]:.3f} kg/s')
    print(f'mdot_fuel_main = {mdot_fuel:.4f} kg/s')
    print(f'mdot_fuel_AB = {mdot_fuel_AB:.4f} kg/s')
    print(f'mdot_exit = {massFlow[5]:.3f} kg/s')
    print(f'H3-WTdot = {Hdot03/1000 - WTdot/1000:.3f} kW')
    print(f'fuel-air ratio main = {mdot_fuel / massFlow[0]:.4f}')
    print(f'fuel-air ratio total = {(mdot_fuel + mdot_fuel_AB) / massFlow[0]:.4f}')
    print(f'dh0 = {Δh02_01/1000:.2f} kJ/kg')
    psi = .6
    U2 = __import__('numpy').sqrt(Δh02_01 * 1e3 / psi)
    print(f'U2 = {U2:.2f}')


def plot_cycle():
    plt.xlabel('Entropy [kJ/kgK]')
    plt.ylabel('Temperature [K]')
    plt.title('Jotun - Cycle Diagram')
    plt.plot(entropy, stagTemp, color="c")
    plt.text(.05, 286, "1: Inlet", fontsize=8)
    plt.text(.12, 425, "2: Compressor exit / plenum ", fontsize=8)
    plt.text(.9, 1030, "3: Combustion exit", fontsize=8)
    plt.text(1, 810, "4: Turbine exit", fontsize=8)
    plt.text(1.25, 1250, "5: AB exit", fontsize=8)
    plt.text(1.5, 1200, "6: Nozzle", fontsize=8)
    plt.scatter(entropy[0], stagTemp[0], label=f'T01 = {stagTemp[0]:.2f} K', color="g")
    plt.scatter(entropy[1], stagTemp[1], label=f'T02 = {stagTemp[1]:.2f} K', color="b")
    plt.scatter(entropy[2], stagTemp[2], label=f'T03 = {stagTemp[2]:.2f} K', color="c")
    plt.scatter(entropy[3], stagTemp[3], label=f'T04 = {stagTemp[3]:.2f} K', color="y")
    plt.scatter(entropy[4], stagTemp[4], label=f'T05 = {stagTemp[4]:.2f} K', color="r")
    plt.scatter(entropy[5], stagTemp[5], label=f'T06 = {stagTemp[5]:.2f} K', color="c")
    plt.legend()
    plt.grid()


def call_engine_cycle():
    # printboard()
    print(); print(build_cycle_table().to_string(index=False)); print()
    print(f'Fuel consumed: {(mdot_fuel + mdot_fuel_AB) * test_time:.2f} kg')
    print(f'P_Turbin = {WTdot/1000:.2f} kW')
    print(f'P_Kompressor = {WCdot/1000:.2f} kW')
    print(f'mdot = {massFlow[0]:.2f} kg/s')
    # plot_cycle()
    # plt.show()


if __name__ == "__main__":
    call_engine_cycle()
