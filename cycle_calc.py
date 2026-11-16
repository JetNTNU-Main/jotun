import configparser
from pathlib import Path

from numpy import pi
import numpy as np

constants_parser = configparser.ConfigParser()
CONSTANTS_PATH = Path(__file__).with_name("constants.cfg")
constants_parser.read(CONSTANTS_PATH)

CONFIG_PATH = Path(__file__).with_name("config.cfg")
config = configparser.ConfigParser()
config.read(CONFIG_PATH)

stagTemp = np.zeros(6)
stagPres = np.zeros(6)
Temp = np.zeros(6)
Pres = np.zeros(6)
entropy = np.zeros(6)
entropyS = np.zeros(6)
specific_stagEnthalpy = np.zeros(6)
specific_Enthalpy = np.zeros(6)
massFlow = np.zeros(6)
stagDensity = np.zeros(6)
Density = np.zeros(6)
velocities = np.zeros(6)
areas = np.zeros(6)

rho_ambient = constants_parser.getfloat("air", "density")  # kg/m3
R = constants_parser.getfloat("air", "R")  # J/kgK
cp_300 = constants_parser.getfloat("air", "cp_300")  # J/kgK @ ~300 K air
cv_300 = constants_parser.getfloat("air", "cv_300")  # J/kgK @ ~300 K air
gamma_300 = cp_300 / cv_300  # @ 300K air
cp_1000 = constants_parser.getfloat("air", "cp_1000")  # J/kgK @ ~1000 K air
cv_1000 = constants_parser.getfloat("air", "cv_1000")  # J/kgK @ ~1000 K air
gamma_1000 = cp_1000 / cv_1000

LHV = constants_parser.getfloat("fuel", "kerosene_LHV")  # J/kg Lower Heating Value of kerosene/paraffin

N = config.getfloat("engine", "RPM")
stagTemp[0] = config.getfloat("temps", "ambient")  # K
velocities[0] = config.getfloat("flow", "v_1")  # m/s
d_1 = config.getfloat("engine", "inlet_diameter")  # m
pic = config.getfloat("compressor", "pressure_ratio")
ΔP_combustor = config.getfloat("combustor", "delta_p")
eta_c = config.getfloat("efficiencies", "compressor")  # Compressor efficiency
d_2 = config.getfloat("compressor", "diameter")  # m
stagTemp[2] = T03s = config.getfloat("temps", "combustor")
eta_b = config.getfloat("efficiencies", "combustor")  # Combustion efficiency
eta_m = config.getfloat("efficiencies", "mechanical")  # Mechanical efficieny between turbine and compressor
velocities[2] = config.getfloat("flow", "v_3")
eta_t = config.getfloat("efficiencies", "turbine")
ΔP_AB = config.getfloat("afterburner", "delta_p")
velocities[3] = config.getfloat("flow", "v_4")
stagTemp[4] = T05s = config.getfloat("temps", "afterburner")  # K Afterburner target stagTemp
eta_n = config.getfloat("efficiencies", "nozzle")  # Nozzle efficency
velocities[4] = config.getfloat("flow", "v_5")
eta_AB = config.getfloat("efficiencies", "afterburner")  # afterburner combustion efficiency

ω = 2 * pi * N / 60

c_avg = lambda c1, c2: (c1 + c2) / 2.0
to_rad = lambda degree: degree * pi / 180
to_deg = lambda radian: radian * 180 / pi
d_min = lambda area, d_max: np.sqrt(d_max**2 - 4 * area / pi)
d_max = lambda area, d_min: np.sqrt(d_min**2 + 4 * area / pi)
AREA = lambda d: 0.25 * pi * d**2
d = lambda A: np.sqrt(((4 * A) / pi))
dmm = lambda A: (np.sqrt(((4 * A) / pi))) * 1e3
M = lambda v, T: v / np.sqrt(gamma_300 * R * T)
q = lambda rho, v: 0.5 * rho * v**2

P_AMBIENT = rho_ambient * R * stagTemp[0]  # Stagnasjons trykk

areas[0] = (pi / 4) * (d_1)**2  # m^2
Temp[0] = stagTemp[0] - (velocities[0]**2) / (2 * cp_300)
stagPres[0] = P_AMBIENT
Pres[0] = stagPres[0] * (Temp[0] / stagTemp[0])**(gamma_300 / (gamma_300 - 1))  # Inlet pressure (pressure required to achieve correct mass flow)
stagDensity[0] = rho_ambient
Density[0] = Pres[0] / (R * Temp[0])

massFlow[0] = Density[0] * velocities[0] * areas[0]
v_inlet = massFlow[0] / (stagDensity[0] * areas[0])

stagPres[1] = stagPres[0] * pic
areas[1] = (pi / 4) * (d_2)**2
T02s = stagTemp[0] * (stagPres[1] / stagPres[0])**((gamma_300 - 1) / gamma_300)
stagTemp[1] = stagTemp[0] + (T02s - stagTemp[0]) / eta_c
stagDensity[1] = stagPres[1] / (R * stagTemp[1])
velocities[1] = massFlow[0] / (stagDensity[1] * areas[1])
Temp[1] = stagTemp[1] - (velocities[1]**2) / (2 * cp_300)
Pres[1] = stagPres[1] * (Temp[1] / stagTemp[1])**(gamma_300 / (gamma_300 - 1))
Density[1] = Pres[1] / (R * Temp[1])
massFlow[1] = stagDensity[1] * velocities[1] * areas[1]
ws_C = ((gamma_300 * R * stagTemp[0]) / (gamma_300 - 1)) * ((pic)**((gamma_300 - 1) / gamma_300) - 1)
wC = ws_C / eta_c  # required compressor work
WCdot = massFlow[0] * wC

stagPres[2] = stagPres[1] * (1 - ΔP_combustor)
stagDensity[2] = stagPres[2] / (R * stagTemp[2])
Q_inn = c_avg(cp_300, cp_1000) * (stagTemp[2] - stagTemp[1])
mdot_fuel = (massFlow[1] * Q_inn) / (LHV * eta_b)
massFlow[2] = massFlow[1] + mdot_fuel
Temp[2] = stagTemp[2] - (velocities[2]**2) / (2 * cp_1000)
Pres[2] = stagPres[2] * (Temp[2] / stagTemp[2])**(gamma_1000 / (gamma_1000 - 1))
Density[2] = Pres[2] / (R * Temp[2])
areas[2] = massFlow[2] / (Density[2] * velocities[2])

massFlow[3] = massFlow[2]
WTdot = WCdot / eta_m
stagTemp[3] = stagTemp[2] - WTdot / (massFlow[3] * cp_1000)
T04s = stagTemp[2] - (stagTemp[2] - stagTemp[3]) / eta_t
stagPres[3] = stagPres[2] * (T04s / stagTemp[2])**(gamma_1000 / (gamma_1000 - 1))
stagDensity[3] = stagPres[3] / (R * stagTemp[3])
Temp[3] = stagTemp[3] - (velocities[3]**2) / (2 * cp_1000)
Pres[3] = stagPres[3] * (Temp[3] / stagTemp[3])**(gamma_1000 / (gamma_1000 - 1))
Density[3] = Pres[3] / (R * Temp[3])
areas[3] = massFlow[3] / (Density[3] * velocities[3])

stagPres[4] = stagPres[3] * (1 - ΔP_AB)
stagDensity[4] = stagPres[4] / (R * stagTemp[4])
Temp[4] = stagTemp[4] - (velocities[4]**2) / (2 * cp_1000)
Pres[4] = stagPres[4] * (Temp[4] / stagTemp[4])**(gamma_1000 / (gamma_1000 - 1))
Density[4] = Pres[4] / (R * Temp[4])

Q_AB = cp_1000 * (stagTemp[4] - stagTemp[3])  # kJ/kg exhaust gas entering AB
mdot_fuel_AB = (massFlow[3] * Q_AB) / (LHV * eta_AB)
massFlow[4] = massFlow[3] + mdot_fuel_AB
areas[4] = massFlow[4] / (Density[4] * velocities[4])

Pres[5] = stagPres[0]
T6s = stagTemp[4] * (Pres[5] / stagPres[4])**((gamma_1000 - 1) / gamma_1000)
Temp[5] = stagTemp[4] - eta_n * (stagTemp[4] - T6s)
velocities[5] = np.sqrt(2 * cp_1000 * (stagTemp[4] - Temp[5]))
Density[5] = Pres[5] / (R * Temp[5])
stagTemp[5] = stagTemp[4]
stagPres[5] = Pres[5] * (stagTemp[5] / Temp[5])**(gamma_1000 / (gamma_1000 - 1))
stagDensity[5] = stagPres[5] / (R * stagTemp[5])
T06s = stagTemp[4] * (stagPres[5] / stagPres[4])**((gamma_1000 - 1) / gamma_1000)
Temp[5] = stagTemp[5] - (velocities[5]**2) / (2 * cp_1000)
massFlow[5] = massFlow[4]
areas[5] = massFlow[5] / (Density[5] * velocities[5])

Δs2_1 = entropy[1] = cp_300 * np.log(stagTemp[1] / stagTemp[0]) - R * np.log(stagPres[1] / Pres[0])
Δs3_2 = c_avg(cp_300, cp_1000) * np.log(stagTemp[2] / stagTemp[1]) - R * np.log(stagPres[2] / stagPres[1])
entropy[2] = Δs3_2 + Δs2_1
Δs4_3 = cp_1000 * np.log(stagTemp[3] / stagTemp[2]) - R * np.log(stagPres[3] / stagPres[2])
entropy[3] = Δs4_3 + entropy[2]
Δs5_4 = cp_1000 * np.log(stagTemp[4] / stagTemp[3]) - R * np.log(stagPres[4] / stagPres[3])
entropy[4] = entropy[3] + Δs5_4
entropy[5] = cp_1000 * np.log(stagTemp[5] / stagTemp[4]) - R * np.log(stagPres[5] / stagPres[4]) + entropy[4]

entropyS[1] = cp_300 * np.log(T02s / stagTemp[0]) - R * np.log(stagPres[1] / Pres[0])
entropyS[2] = Δs3_2 + entropyS[1]

Δh02_01 = cp_300 * (stagTemp[1] - stagTemp[0])
Δh03_01 = c_avg(cp_300, cp_1000) * (stagTemp[2] - stagTemp[1]) + Δh02_01
Δh04_01 = cp_1000 * (stagTemp[3] - stagTemp[2]) + Δh03_01
Δh05_01 = cp_1000 * (stagTemp[4] - stagTemp[3]) + Δh04_01
Δh06_01 = cp_1000 * (stagTemp[5] - stagTemp[4]) + Δh05_01
Hdot02 = Δh02_01 * massFlow[1]
Hdot03 = Δh03_01 * massFlow[2]
Hdot04 = Δh04_01 * massFlow[3]
Hdot05 = Δh05_01 * massFlow[4]
Hdot06 = Δh06_01 * massFlow[5]

specific_stagEnthalpy[0] = cp_300 * stagTemp[0]
specific_stagEnthalpy[1] = cp_300 * stagTemp[1]
specific_stagEnthalpy[2] = cp_1000 * stagTemp[2]
specific_stagEnthalpy[3] = cp_1000 * stagTemp[3]
specific_stagEnthalpy[4] = cp_1000 * stagTemp[4]
specific_stagEnthalpy[5] = cp_1000 * stagTemp[5]
specific_Enthalpy[0] = cp_300 * Temp[0]
specific_Enthalpy[1] = cp_300 * Temp[1]
specific_Enthalpy[2] = cp_1000 * Temp[2]
specific_Enthalpy[3] = cp_1000 * Temp[3]
specific_Enthalpy[4] = cp_1000 * Temp[4]
specific_Enthalpy[5] = cp_1000 * Temp[5]

ve_calc = np.sqrt(2 * cp_1000 * (stagTemp[4] - stagTemp[5]))
ve_ideal = np.sqrt(2 * cp_1000 * stagTemp[5] * (1 - (P_AMBIENT / stagPres[5])**((gamma_1000 - 1) / (gamma_1000))))

F_momentum = massFlow[5] * velocities[5] - massFlow[0] * velocities[0]
F_momentum_static = massFlow[5] * velocities[5]
F_ideal = massFlow[5] * ve_ideal
F_pressure = (Pres[5] - P_AMBIENT) * 1000 * areas[5]
F_calc = F_momentum + F_pressure
F_calc_static = F_momentum_static + F_pressure
F_calc_static_ideal = F_ideal + F_pressure
mdot_hydrocarbons = mdot_fuel + mdot_fuel_AB
TSFC = mdot_hydrocarbons / F_calc

# print(f'TSFC = {TSFC}')
test_time = 60 * 60  # s
T = (WTdot * 1e3) / ω
tau_max = 400 * 1e6  # Pa
hub_D = ((16 * T) / (pi * tau_max))**(1 / 3)
hub_D = 0.0800  # m (80mm)
# print(f'P02 = {P2*(1+(.5*(gamma-1)*M(v2,T2)**2))**(gamma/(gamma-1)):.2f} kPa')
tau_max = ((16 * T) / (pi * hub_D**3)) / 10e5  # Pa


# ------------ OUTPUT LISTS -------------------
MACH = [M(velocities[0], Temp[0]), M(velocities[1], Temp[1]), M(velocities[2], Temp[2]), M(velocities[3], Temp[3]), M(velocities[4], Temp[4]), M(velocities[5], Temp[5])]
dynamicPres = [q(Density[0], velocities[0]), q(Density[1], velocities[1]), q(Density[2], velocities[2]), q(Density[3], velocities[3]), q(Density[4], velocities[4]), q(Density[5], velocities[5])]
