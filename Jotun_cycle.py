import matplotlib.pyplot as plt
import numpy as np
from numpy import pi as π
import pandas as pd

rho_ambient = 1.225 #kg/m3
R = .287 # kJ/kgK
LHV = 43000000/1e3 # kJ/kg Lower Heating Value of kerosene/paraffin
cp_300 = 1.0056   # kJ/kgK @ ~300 K air
cv_300 = .720     # kJ/kgK @ ~300 K air
gamma = 1.4 # @ 300K air
cp_1000 = 1.142 # kJ/kgK @ ~1000 K air
cv_1000 = .855  # kJ/kgK @ ~1000 K air
gamma_1000 = 1.336
N = 32000
ω = 2*π*N/(60)

c_avg = lambda c1, c2:(c1+c2)/2.0
to_rad = lambda degree: degree*π/180
to_deg = lambda radian: radian*180/π
T01 = 288 #k
P_AMBIENT = P01 = rho_ambient*R*T01 # Stagnasjonstrykk
rho_01 = rho_ambient
A_EXIT = 0
P_EXIT = 0
Ft = 1000 + (P_EXIT-P01)*A_EXIT #N
ve = 350 #m/s
v1 = 33 #m/s
d_1 = 0.3
A1 = (π/4)*(d_1)**2 # m^2
T1 = T01 - (v1**2)/(2*cp_300*1e3)


P1 = P01*(T1/T01)**(gamma/(gamma-1)) # Inlet pressure (pressure required to achieve correct mass flow)
rho_1 = P1/(R*T1)
mdot_air = rho_1*v1*A1

d_min = lambda area, d_max: np.sqrt(d_max**2-4*area/π)
d_max = lambda area, d_min: np.sqrt(d_min**2+4*area/π)

AREA = lambda d: 0.25*π*d**2
d = lambda A: np.sqrt(((4*A)/π))
dmm = lambda A: (np.sqrt(((4*A)/π)))*1e3

A_inlet = (π/4)*(d_1)**2
 
v_inlet = mdot_air/(rho_01*A_inlet)
v_eye = 129.11 #m/s


πc = 3

P02 = P01*πc
ΔP_combustor = .03
P03 = P02 * (1 - ΔP_combustor)
ws_C = ((gamma*R*T01)/(gamma-1))*((πc)**((gamma-1)/gamma)-1)

eta_c = .7

wC = ws_C/eta_c # required compressor work

d_2 = .195 #m
A2 = (π/4) * (d_2)**2

T02s = T01*(P02/P01)**((gamma-1)/gamma)

T02 = T01 + (T02s-T01)/eta_c
rho_02 = P02/(R*T02)
v2 = mdot_air/(rho_02*A2)
T2 = T02 - (v2**2)/(2*cp_300*1e3)
#P2 = P02 - (0.5*rho_02*v2**2)/1e3
P2 = P02*(T2/T02)**(gamma/(gamma-1))
rho_2 = P2/(R*T2)
mdot_02 = rho_02*v2*A2



T03 = T03s = 1000
Q_inn = c_avg(cp_300,cp_1000)*(T03-T02)
eta_b = .85  # Combustion efficiency
eta_m = .95 # Mechanical efficieny between turbine and compressor
WCdot = mdot_air*wC

mdot_fuel = (mdot_air*Q_inn)/(LHV*eta_b)
mdot_exhaust = mdot_air + mdot_fuel
rho_03 = P03/(R*T03)
v3 = 40
v3 = 200
v3 = 120
print(Q_inn)
# mdot_air = rho_02*v1*A1

#P3 = P03 - (0.5*rho_03*v3**2)/1e3
T3 = T03 - (v3**2)/(2*cp_1000*1e3)
P3 = P03*(T3/T03)**(gamma_1000/(gamma_1000-1))
f = (cp_1000*(T03-T02))
rho_3 = P3/(R*T3)
A3 =  mdot_exhaust/(rho_3*v3)

WTdot = WCdot / eta_m
M = lambda v,T: v / np.sqrt(gamma * R * 1000 * T)
q = lambda rho,v: 0.5*rho*v**2/1e3
eta_t = .75

T04 = T03 - WTdot/(mdot_exhaust*cp_1000)
T04s = T03 - (T03 - T04)/eta_t
P04 = P03 * (T04s/T03)**(gamma_1000/(gamma_1000 - 1))
rho_04 = P04/(R*T04)
ΔP_AB = 0.07
v4 = 80
v4 = 220

T4 = T04 - (v4**2)/(2*cp_1000*1e3) 
P4 = P04*(T4/T04)**(gamma_1000/(gamma_1000-1))
rho_4 = P4/(R*T4)
P05 = P04 * (1 - ΔP_AB)
A4 =  mdot_exhaust/(rho_4*v4)


T05 = T05s = 1300 #K Afterburner target stagTemp
eta_n = 0.90 # Nozzle efficency
rho_05 = P05/(R*T05)


eta_AB = 0.80  # afterburner combustion efficiency
Q_AB = cp_1000 * (T05 - T04)  # kJ/kg exhaust gas entering AB
mdot_fuel_AB = (mdot_exhaust * Q_AB) / (LHV * eta_AB)
mdot_exit = mdot_exhaust + mdot_fuel_AB
v5 = 200
T5 = T05 - (v5**2)/(2*cp_1000*1e3)
P5 = P05*(T5/T05)**(gamma_1000/(gamma_1000-1))

rho_5 = P5/(R*T5)

A5 = mdot_exit/(rho_5*v5)
#v5 = 


P6 = P01
T6s = T05*(P6/P05)**((gamma_1000-1)/gamma_1000)
T6 = T05 - eta_n * (T05 - T6s)
v6 = np.sqrt(2 * cp_1000 * 1000 * (T05 - T6))
rho_6 = P6 / (R * T6)
#T06 = T05 - eta_n*(T05 - T06s)

T06 = T05
P06 = P6 * (T06 / T6)**(gamma_1000/(gamma_1000-1))
rho_06 = P06/(R*T06)
T06s = T05 * (P06/P05)**((gamma_1000-1)/gamma_1000)







A6 = mdot_exit/(rho_6*v6)
T6 = T06 - (v6**2)/(2*cp_1000*1e3)


S1 = 0
Δs2_1 = S2 = cp_300*np.log(T02/T01) - R * np.log(P02/P1)
Δs3_2 = c_avg(cp_300,cp_1000)*np.log(T03/T02) - R * np.log(P03/P02)
S3 =  Δs3_2 + Δs2_1
Δs4_3 = cp_1000*np.log(T04/T03) - R*np.log(P04/P03)
S4 = Δs4_3+ S3
Δs5_4 = cp_1000*np.log(T05/T04) - R*np.log(P05/P04)
S5 = S4 + Δs5_4
S6 = cp_1000*np.log(T06/T05) - R * np.log(P06/P05)+ S5


S0_1 = S1
S0_2 = cp_300*np.log(T02s/T01) - R * np.log(P02/P1)
S0_3 = Δs3_2 + S0_2 
S0_4 = Δs3_2 + S0_2 


stagTemp = [T01, T02,T03, T04, T05, T06] # T01 -> ambient. T02 -> post compression. T03 -> post combustion. T04 -> Post turbine. T05 -> Post afterburner. T06 -> Post nozzle
stagPres = [P01, P02, P03, P04, P05, P06]   
Temp = [T1, T2,T3, T4, T5, T6]
Pres = [P1, P2, P3, P4, P5, P6]
# tempS = [T01, T2s,T3s, T4s,T05s,T6s]

entropy = [S1, S2, S3, S4, S5, S6]
entropyS = [S1, S0_2,S0_3]

plt.xlabel('Entropy [kJ/kgK]')
plt.ylabel('Temperature [K]')
plt.title('Jotun - Cycle Diagram')
plt.plot(entropy, stagTemp, color="c")#, label='Compression')
Δh02_01 = cp_300*(T02-T01)
Δh03_01 = c_avg(cp_300,cp_1000)*(T03-T02) + Δh02_01
Δh04_01 = cp_1000*(T04-T03) + Δh03_01
Δh05_01 = cp_1000*(T05-T04) + Δh04_01
Δh06_01 = cp_1000*(T06-T05) + Δh05_01
Hdot02 = Δh02_01*mdot_air
Hdot03 = Δh03_01*mdot_exhaust
Hdot04 = Δh04_01*mdot_exhaust
Hdot05 = Δh05_01*mdot_exit
Hdot06 = Δh06_01*mdot_exit

h01 = cp_300*T01
h02 = cp_300*T02
h03 = cp_1000*T03
h04 = cp_1000*T04
h05 = cp_1000*T05
h06 = cp_1000*T06
h1 = cp_300*T1
h2 = cp_300*T2
h3 = cp_1000*T3
h4 = cp_1000*T4
h5 = cp_1000*T5
h6 = cp_1000*T6
enthalpy = [h01, h02, h03, h04, h05, h06]

plt.text(.05,286, "1: Inlet",   fontsize=8)
plt.text(.12,425, "2: Compressor exit / plenum ",   fontsize=8)
plt.text(.9,1030, "3: Combustion exit",   fontsize=8)
plt.text(1,810, "4: Turbine exit",   fontsize=8)
plt.text(1.25,1250, "5: AB exit",   fontsize=8)
plt.text(1.5,1200, "6: Nozzle",   fontsize=8)
plt.scatter(S1,T01, label=f'T01 = {T01:.2f} K', color="g"),# s1 = {S1:.2f}kJ
plt.scatter(S2,T02, label=f'T02 = {T02:.2f} K', color="b") #, s2-s1 = {S2:.2f}kJ/kgK 
plt.scatter(S3,T03, label=f'T03 = {T03:.2f} K', color="c") #, s3-s2 = {S3:.2f}kJ/kgK 
plt.scatter(S4,T04, label=f'T04 = {T04:.2f} K', color="y") #, s4-s3 = {S4:.2f}kJ/kgK 
plt.scatter(S5,T05, label=f'T05 = {T05:.2f} K', color="r") #, s5-s4 = {S5:.2f}kJ/kgK 
plt.scatter(S6,T06, label=f'T06 = {T06:.2f} K', color="c") #, s6-s5 = {S6:.2f}kJ/kgK 
ve_calc = np.sqrt(2 * cp_1000 * 1000 * (T05 - T06))
ve_ideal = np.sqrt(2*cp_1000*1e3*T06*(1-(P_AMBIENT/P06)**((gamma_1000-1)/(gamma_1000))))
Δh02_01 = cp_300*(T02-T01)

plt.legend()
plt.grid()

def printboard():
    
    F_calc = mdot_exit*ve_calc
    print(f'eta_c = {eta_c:.2f}')
    print(f'WCdot = {WCdot:.2f} kW [kJ/s]')
    print(f'eta_m = {eta_m:.2f}')
    print(f'WTdot = {WTdot:.2f} kW [kJ/s]')
    print(f'P1 = {P1:.2f} kPa')
    print(f'P01 = {P01:.2f} kPa')
    print(f'P02 = {P02:.2f} kPa')
    print(f'P03 = {P03:.2f} kPa')
    print(f'P04 = {P04:.2f} kPa')
    print(f'P05 = {P05:.2f} kPa')
    print(f'P06 = {P06:.2f} kPa')
    print(f'P05/P06 = {P05/P06:.3f}')
    print(f'T05 = {T05:.2f} K')
    print(f'T06 = {T06:.2f} K')
    print(f'H2 = {Hdot02:.2f} kW')
    print(f'H3 = {Hdot03:.2f} kW')
    print(f'H4 = {Hdot04:.2f} kW')
    print(f'H5 = {Hdot05:.2f} kW')
    print(f'H6 = {Hdot06:.2f} kW')   
    print(f'mdot_air = {mdot_air:.3f} kg/s')
    print(f'mdot_fuel_main = {mdot_fuel:.4f} kg/s')
    print(f'mdot_fuel_AB = {mdot_fuel_AB:.4f} kg/s')
    print(f'mdot_exit = {mdot_exit:.3f} kg/s')
    print(f'H3-WTdot = {Hdot03-WTdot:.3f} kW')
    print(f'fuel-air ratio main = {mdot_fuel/mdot_air:.4f}')
    print(f'fuel-air ratio total = {(mdot_fuel + mdot_fuel_AB)/mdot_air:.4f}')
    print(f'Δh0 = {Δh02_01:.2f} kJ/kg')
    psi = .6
    U2 = np.sqrt(Δh02_01*1e3/psi)
    # Δh0 = psi*U2**2
    print(f'U2 = {U2:.2f}')



def call_engine_cycle():
    printboard()
    plt.show()

def tableRound(matrix, specifier = 2):
    new_matrix = []
    for i in matrix:
        new_matrix.append(round(i,specifier))
    return new_matrix
specific_stagEnthalpy = [h01, h02, h03, h04, h05, h06]
specific_Enthalpy = [h1, h2, h3, h4, h5, h6]
massFlow = [
    mdot_air,       # 1: inlet
    mdot_air,       # 2: compressor exit
    mdot_exhaust,   # 3: combustor exit
    mdot_exhaust,   # 4: turbine exit
    mdot_exit,      # 5: afterburner exit
    mdot_exit       # 6: nozzle exit
]
ρ0 = [rho_01,rho_02,rho_03,rho_04,rho_05,rho_06]
ρ = [rho_1,rho_2,rho_3,rho_4,rho_5,rho_6]

velocities = [v1,v2,v3,v4,v5,v6]
areas = [A1,A2,A3,A4,A5,A6]
diameters = [dmm(A1),dmm(A2),dmm(A3),dmm(A4),dmm(A5),dmm(A6)]

MACH = [M(v1,T1),M(v2,T2),M(v3,T3),M(v4,T4),M(v5,T5),M(v6,T6)]
dynamicPres = [q(rho_1,v1),q(rho_2,v2),q(rho_3,v3),q(rho_4,v4),q(rho_5,v5),q(rho_6,v6)]

F_momentum = mdot_exit*v6 - mdot_air*v1
F_momentum_static = mdot_exit*v6 
F_ideal = mdot_exit*ve_ideal
F_pressure = (P6-P_AMBIENT)*1000*A6
F_calc = F_momentum + F_pressure
F_calc_static = F_momentum_static + F_pressure
F_calc_static_ideal = F_ideal + F_pressure
thrust = ['','','','','',F_calc]
mdot_hydrocarbons = mdot_fuel + mdot_fuel_AB
TSFC = mdot_hydrocarbons/F_calc 
# print(f'\n                                                                             --- JOTUN CYCLE --- ')
engine_cycle_table = {
    "Station": ["1: Inlet", "2: Compressor exit", "3: Combustor exit", "4: Turbine exit", "5: Afterburner exit", "6: Nozzle exit"],
    "P0 [kPa]": tableRound(stagPres),
    "T0 [K]": tableRound(stagTemp),
    "P [kPa]": tableRound(Pres),
    "T [K]": tableRound(Temp),
    "Mdot [kg/s]": tableRound(massFlow,3),
    "ρ [kg/m^3]": tableRound(ρ,3),
    # "ρ0 [kg/m^3]": tableRound(ρ0,3),
    "h0 [kJ/kg]": tableRound(specific_stagEnthalpy),
    "h [kJ/kg]": tableRound(specific_Enthalpy),
    "v [m/s]": tableRound(velocities),
    "A [m^2]": tableRound(areas,5),
    "q [kPa]": tableRound(dynamicPres),
    "|": ['|','|','|','|','|','|'],
    "M": tableRound(MACH),
    "-": ['-','-','-','-','-','-'],
    "Thrust [N]": ['*','*',f'[P05/PA = {P05/P_AMBIENT:.2f}]',f' {round(F_calc,2)} (v1 = {v1} m/s)', f' {F_calc_static_ideal:.2f} (ideal)',f'{round(F_calc_static,2)} (static)']
    # "d [mm]": tableRound(diameters)
    }

df = pd.DataFrame(engine_cycle_table)
# print(tableRound(stagPres))
# call_engine_cycle();
print();print(df.to_string(index=False));print()
# print(f'TSFC = {TSFC}')
test_time = 60 #s
T = (WTdot*1e3)/ω
τmax = 400*1e6 #Pa
hub_D = ((16*T)/(π*τmax))**(1/3)
hub_D = 0.0800#m (80mm)

# print(f'P02 = {P2*(1+(.5*(gamma-1)*M(v2,T2)**2))**(gamma/(gamma-1)):.2f} kPa')
τmax = ((16*T)/(π*hub_D**3))/10e5 #Pa
# print(f'Fuel consumed: {(mdot_fuel+mdot_fuel_AB)*test_time:.2f} kg')
print(f'P_Turbin = {WTdot:.2f} kW')
print(f'P_Kompressor = {WCdot:.2f} kW')
# print(f'mdot = {mdot_air:.2f} kg/s')
# print(f'T = {T} Nm')
# print(f'shaft = {hub_D*1e3} mm')
# print(f'τmax = {τmax:.2f} MPa @ hub_D = {hub_D*1e3:.2f} mm')
print(f'Fuel consumed during static test: {(mdot_fuel+mdot_fuel_AB)*test_time:.2f} kg')
# print(f'P_Turbin = {WTdot:.2f} kW')
# print(f'P_Kompressor = {WCdot/mdot_air:.2f} kW')
# print(f'mdot = {mdot_air:.2f} kg/s')
# print(f'v6 = {v6:.2f} m/s')
# print(f'v6*mdot = {mdot_exit:.2f} N')
# print(f'T = {T} Nm')
# print(f'shaft = {hub_D*1e3} mm')
# print(f'τmax = {τmax:.2f} MPa @ hub_D = {hub_D*1e3:.2f} mm')

#print(d())
