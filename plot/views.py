from django.http import JsonResponse
import math


gamma = 1.4
Ma = 0.75
delH_CpTa = 150
Tt4_Ta = 6
alpha = 4

Tta_Ta = (1+(gamma-1)*Ma**2/2)
Ta_Tta = 1/Tta_Ta
Ta_Tt4 = 1/Tt4_Ta


def turbojet_solve(request):
    plot_x = []
    plot_f = []
    plot_t = []
    pi_c_min = 5
    pi_c_max = 25
    steps = 2.5
    _pi_c_min = int(pi_c_min/steps)
    _pi_c_max = int(pi_c_max/steps)+1
    for _pi_c in range(_pi_c_min, _pi_c_max):
        pi_c = _pi_c * steps
        tau_c = pi_c ** ((gamma - 1) / gamma)
        F_ma = Ma * (math.sqrt(((Tta_Ta / (Tta_Ta - 1)) * (Tt4_Ta * Ta_Tta / tau_c) * (tau_c - 1)) + (Tt4_Ta / (Tta_Ta * tau_c))) - 1)
        TSFC = ((Tt4_Ta - Tta_Ta * tau_c) / (delH_CpTa * Ma)) / F_ma
        plot_x.append(pi_c)
        plot_f.append(F_ma)
        plot_t.append(TSFC)
    
    data = {'x': plot_x, 'f': plot_f, 't': plot_t}
    
    return JsonResponse(data)


def turbof(x):
    return Ma * (math.sqrt(x/(Tta_Ta - 1)) - 1)


def turbofan_solve(request):
    # plot_x = []
    plot_f = []
    plot_t = []
    pi_c_min = 0
    pi_c_max = 30
    pi_f_min = 1
    pi_f_max = 4
    steps = 1
    _pi_c_min = int(pi_c_min / steps)
    _pi_c_max = int(pi_c_max / steps) + 1
    _pi_f_min = int(pi_f_min / steps)
    _pi_f_max = int(pi_f_max / steps) + 1
    for _pi_c in range(_pi_c_min, _pi_c_max):
        f_row = []
        t_row = []
        for _pi_f in range(_pi_f_min, _pi_f_max):
            pi_c = _pi_c * steps
            pi_f = _pi_f * steps
            tau_c = pi_c ** ((gamma - 1) / gamma)
            tau_f = pi_f ** ((gamma - 1) / gamma)
            try:
                F_ma = turbof((Tt4_Ta * Ta_Tta) * (Tta_Ta * tau_c * (1 - (Tta_Ta * Ta_Tt4) * ((tau_c - 1) + alpha * (tau_f - 1))) - 1) / tau_c) + alpha * turbof(Tta_Ta * tau_f - 1)
                TSFC = ((Tt4_Ta - Tta_Ta * tau_c) / (delH_CpTa)) / F_ma
            except:
                print(pi_c, pi_f)
                F_ma = 0
                TSFC = 0
            f_row.append(F_ma)
            t_row.append(TSFC)
        plot_f.append(f_row)
        plot_t.append(t_row)
    
    data = {'f': plot_f, 't': plot_t}
    
    return JsonResponse(data)
