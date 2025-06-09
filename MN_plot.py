
# To stop the iteration for asking values of parameters, type 0 in 'enter depth' input !

import matplotlib.pyplot as plt
import math
import pandas as pd

bar_width = 0.35
M_sandstone = (189-55.5)*0.01/(2.65-1)
N_sandstone = (1+0.035)/(2.65-1)

M_limestone = (189-47.5)*0.01/(2.71-1)
N_limestone = (1-0)/(2.71-1)

M_dolomite = (189-43.5)*0.01/(2.87-1)
N_dolomite = (1-0.02)/(2.87-1)

slope_l_s = (M_sandstone-M_limestone)/(N_sandstone-N_limestone)
intercept_l_s = M_limestone - N_limestone*slope_l_s

slope_d_s = (M_sandstone-M_dolomite)/(N_sandstone-N_dolomite)
intercept_d_s = M_dolomite - N_dolomite*slope_d_s

slope_l_d = (M_limestone-M_dolomite)/(N_limestone-N_dolomite)
intercept_l_d = M_limestone - N_limestone*slope_l_d

y_ld = [M_limestone, M_dolomite]
x_ld = [N_limestone, N_dolomite]
y_ls = [M_limestone, M_sandstone]
x_ls = [N_limestone, N_sandstone]
y_sd = [M_sandstone, M_dolomite]
x_sd = [N_sandstone, N_dolomite]



def dolomite_fraction(x,y):
    b = y - x*slope_l_s
    x = (intercept_l_d-b)/(slope_l_s-slope_l_d)
    y = slope_l_d*x + intercept_l_d
    #print(x,'--',y)
    distance = math.sqrt((y-M_dolomite)**2+(x-N_dolomite)**2)
    total_distance = math.sqrt((M_limestone-M_dolomite)**2+(N_limestone-N_dolomite)**2)
    fraction = 100-(distance/total_distance)*100
    fraction = round(fraction, 2)
    #dolomite_fractions.append(fraction)
    #return dolomite_fractions
    return fraction

def sandstone_fraction(x, y):
    b = y - x * slope_l_d
    x = (intercept_d_s - b) / (slope_l_d - slope_d_s)
    y = slope_d_s * x + intercept_d_s
    #print(x, '--', y)
    distance = math.sqrt((y - M_sandstone) ** 2 + (x - N_sandstone) ** 2)
    total_distance = math.sqrt((M_dolomite - M_sandstone) ** 2 + (N_dolomite - N_sandstone) ** 2)
    fraction = 100 - (distance / total_distance)*100
    fraction = round(fraction, 2)
    #sandstone_fractions.append(fraction)
    #return sandstone_fractions
    return fraction

def limestone_fraction(x, y):
    b = y - x * slope_d_s
    x = (intercept_l_s - b) / (slope_d_s - slope_l_s)
    y = slope_l_s* x + intercept_l_s
    #print(x, '--', y)
    distance = math.sqrt((y - M_limestone) ** 2 + (x - N_limestone) ** 2)
    total_distance = math.sqrt((M_sandstone - M_limestone) ** 2 + (N_sandstone - N_limestone) ** 2)
    fraction = 100 - (distance / total_distance)*100
    fraction = round(fraction, 2)
    #limestone_fractions.append(fraction)
    return fraction

def draw_barchart(df):
    df.plot(kind='barh',
                    stacked=True,
                    colormap='viridis',
                    figsize=(10, 6))
    plt.xlabel("Fractions (%)")
    plt.ylabel("Depth")
    plt.legend(["Dolomite", 'Sandstone', 'Limestone'],loc="upper left", ncol=3)
    plt.title("Fractions by depth")
    plt.tight_layout()
    plt.show()

def draw_graph(depths, M_values, N_values):
    plt.plot(x_ld, y_ld, label='LD')
    plt.plot(x_ls, y_ls, label='LS')
    plt.plot(x_sd, y_sd, label='SD')
    plt.xlabel('N')
    plt.ylabel('M')
    plt.annotate('Dolomite', (N_dolomite, M_dolomite))
    plt.annotate('Sandstone', (N_sandstone, M_sandstone))
    plt.annotate('Limestone', (N_limestone, M_limestone))

    plt.scatter(N_values, M_values, color='red')
    for i, txt in enumerate(depths):
        plt.annotate(txt, (N_values[i], M_values[i]))
    plt.legend()
    plt.show()

depths = []
M_values = []
N_values = []
dolomite_fractions = []
sandstone_fractions= []
limestone_fractions = []

while True:
    depth = input('Enter depth: ')
    if depth == '0':
        # M_values.pop()
        # N_values.pop()
        break
    rob, delta_t, porosity_N = map(float, input('Enter values for rob, delta_t and porosity_N : ').split())
    depths.append(depth)
    def m_n_values(delta_t, rob, porosity_N, tf=189, rof=1, porosity_Nf=1):
        porosity_N = porosity_N*0.01
        M = (tf-delta_t)*0.01/(rob-rof)
        N = (porosity_Nf-porosity_N)/(rob-rof)
        return M, N

    M, N = m_n_values(delta_t, rob, porosity_N, tf=189, rof=1, porosity_Nf=1)

    def values(M, N):
        M_values.append(M)
        N_values.append(N)
        return M_values, N_values

    M_values, N_values = values(M, N)


    # dolomite,sandstone,limestone mixture
    if slope_d_s*N+intercept_d_s<M and slope_l_d*N+intercept_l_d>M and slope_l_s*N+intercept_l_s>M:
        d = dolomite_fraction(N, M)
        dolomite_fractions.append(dolomite_fraction(N,M))
        s = sandstone_fraction(N, M)
        sandstone_fractions.append(sandstone_fraction(N,M))
        l = limestone_fraction(N, M)
        limestone_fractions.append(limestone_fraction(N,M))
        print('Dolomite: ',d,';','Sandstone: ',s,';', 'Limestone: ',l)
    # dolomite sandstone mixture
    elif slope_l_d*N+intercept_l_d>M and slope_d_s*N+intercept_d_s>M and slope_l_s*N+intercept_l_s>M:
        s = sandstone_fraction(N, M)
        sandstone_fractions.append(s)
        d = 100 - sandstone_fraction(N, M)
        dolomite_fractions.append(d)
        l = 0
        limestone_fractions.append(l)
        print('Dolomite: ',round(d,2), ';','Sandstone: ',s, ';','Limestone: ', l)
    # dolomite limestone mixture
    elif slope_d_s*N+intercept_d_s<M and slope_l_d*N+intercept_l_d<M and slope_l_s*N+intercept_l_s>M:
        s = 0
        sandstone_fractions.append(s)
        d = dolomite_fraction(N ,M)
        dolomite_fractions.append(d)
        l = 100 - dolomite_fraction(N, M)
        limestone_fractions.append(l)
        print('Dolomite: ',d, ';','Sandstone: ', s, ';','Limestone: ', round(l,2))
    # sandstone limestone mixture
    elif slope_l_d * N + intercept_l_d > M and slope_d_s * N + intercept_d_s < M and slope_l_s * N + intercept_l_s < M:
        s = 100 - limestone_fraction(N, M)
        sandstone_fractions.append(s)
        d = 0
        dolomite_fractions.append(d)
        l = limestone_fraction(N, M)
        limestone_fractions.append(l)
        print('Dolomite: ',d, ';','Sandstone: ', round(s,2), ';','Limestone: ', l)
    #100% dolomite
    elif slope_d_s*N+intercept_d_s>M and slope_l_d*N+intercept_l_d<M and N == N_dolomite and M == M_dolomite:
        s = 0
        sandstone_fractions.append(s)
        d = 100
        dolomite_fractions.append(d)
        l = 0
        limestone_fractions.append(l)
        print('Dolomite: ',d, ';','Sandstone: ',  s, ';','Limestone: ', l)
    elif slope_d_s*N+intercept_d_s>M and slope_l_d*N+intercept_l_d<M:
        s = 0
        sandstone_fractions.append(s)
        d = 100
        dolomite_fractions.append(d)
        l = 0
        limestone_fractions.append(l)
        print('Dolomite: ',d, ';','Sandstone: ',  s, ';','Limestone: ', l)
    #100% sandstone
    elif slope_d_s*N+intercept_d_s>M and slope_l_s*N+intercept_l_s<M and N == N_sandstone and M == M_sandstone:
        s = 100
        sandstone_fractions.append(s)
        d = 0
        dolomite_fractions.append(d)
        l = 0
        limestone_fractions.append(l)
        print('Dolomite: ',d, ';','Sandstone: ', s, ';','Limestone: ', l)
    elif slope_d_s*N+intercept_d_s>M and slope_l_s*N+intercept_l_s<M:
        s = 100
        sandstone_fractions.append(s)
        d = 0
        dolomite_fractions.append(d)
        l = 0
        limestone_fractions.append(l)
        print('Dolomite: ',d, ';','Sandstone: ', s, ';','Limestone: ', l)
    #100% limestone
    elif slope_l_d*N+intercept_l_d<M and slope_l_s*N+intercept_l_s<M and N == N_dolomite and M == M_limestone:
        s = 0
        sandstone_fractions.append(s)
        d = 0
        dolomite_fractions.append(d)
        l = 100
        limestone_fractions.append(l)
        print('Dolomite: ',d, ';','Sandstone: ', s, ';','Limestone: ', l)
    elif slope_l_d*N+intercept_l_d<M and slope_l_s*N+intercept_l_s<M:
        s=0
        sandstone_fractions.append(s)
        d = 0
        dolomite_fractions.append(d)
        l = 100
        limestone_fractions.append(l)
        print('Dolomite: ',d, ';','Sandstone: ', s, ';','Limestone: ', l)

draw_graph(depths, M_values, N_values)
# print(dolomite_fractions)
# print(sandstone_fractions)
data = {'Depths':depths, 'Dolomite (%)':dolomite_fractions,
        'Sandstone (%)':sandstone_fractions, 'Limestone (%)':limestone_fractions}

df = pd.DataFrame(data)
df.set_index('Depths',inplace=True)
df.to_csv('fractions.csv')
print(df)
# print(dolomite_fractions)
# print(sandstone_fractions)
# print(limestone_fractions)
draw_barchart(df)