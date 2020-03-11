from django.http import JsonResponse
import math


def turbojet_solve(request):
    gamma = 1.4
    Ma = float(request.POST.get('Ma', 0.75))
    delH_CpTa = float(request.POST.get('delH_CpTa', 150))
    Tt4_Ta = float(request.POST.get('Tt4_Ta', 6))
    steps = float(request.POST.get('steps', 2.5))

    Tta_Ta = (1 + (gamma - 1) * Ma ** 2 / 2)
    Ta_Tta = 1 / Tta_Ta

    plot_x = []
    plot_f = []
    plot_t = []
    pi_c_min = float(request.POST.get('pi_c_min', 5))
    pi_c_max = float(request.POST.get('pi_c_max', 25))
    _pi_c_min = int(pi_c_min/steps)
    _pi_c_max = int(pi_c_max/steps)+1
    for _pi_c in range(_pi_c_min, _pi_c_max):
        pi_c = _pi_c * steps
        tau_c = pi_c ** ((gamma - 1) / gamma)
        F_ma = Ma * (math.sqrt(((Tta_Ta / (Tta_Ta - 1)) * (Tt4_Ta * Ta_Tta / tau_c) * (tau_c - 1)) + (Tt4_Ta / (Tta_Ta * tau_c))) - 1)
        TSFC = (Tt4_Ta - Tta_Ta * tau_c) / (delH_CpTa * F_ma)
        plot_x.append(pi_c)
        plot_f.append(F_ma)
        plot_t.append(TSFC)
    
    data = {'x': plot_x, 'f': plot_f, 't': plot_t}
    
    return JsonResponse(data)


def turbofan_solve(request):
    gamma = 1.4
    Ma = float(request.POST.get('Ma', 0.75))
    delH_CpTa = float(request.POST.get('delH_CpTa', 150))
    Tt4_Ta = float(request.POST.get('Tt4_Ta', 6))
    alpha = float(request.POST.get('alpha', 4))

    Tta_Ta = (1 + (gamma - 1) * Ma ** 2 / 2)
    Ta_Tta = 1 / Tta_Ta
    Ta_Tt4 = 1 / Tt4_Ta

    plot_x = []
    plot_y = []
    plot_f = []
    plot_t = []
    pi_c_min = float(request.POST.get('pi_c_min', 0))
    pi_c_max = float(request.POST.get('pi_c_max', 30))
    pi_f_min = float(request.POST.get('pi_f_min', 1))
    pi_f_max = float(request.POST.get('pi_f_max', 4))
    steps_c = (pi_c_max-pi_c_min)/100
    steps_f = (pi_f_max-pi_f_min)/100
    _pi_c_min = int(pi_c_min / steps_c)
    _pi_c_max = int(pi_c_max / steps_c) + 1
    _pi_f_min = int(pi_f_min / steps_f)
    _pi_f_max = int(pi_f_max / steps_f) + 1
    for _pi_c in range(_pi_c_min, _pi_c_max):
        f_row = []
        t_row = []
        pi_c = _pi_c * steps_c
        tau_c = pi_c ** ((gamma - 1) / gamma)
        plot_x.append(pi_c)
        for _pi_f in range(_pi_f_min, _pi_f_max):
            pi_f = _pi_f * steps_f
            tau_f = pi_f ** ((gamma - 1) / gamma)
            if len(plot_y) < _pi_f_max-_pi_f_min:
                plot_y.append(pi_f)
            try:
                F_ma = Ma * (math.sqrt(((Tt4_Ta * Ta_Tta) * (Tta_Ta * tau_c * (1 - (Tta_Ta * Ta_Tt4) * ((tau_c - 1) + alpha * (tau_f - 1))) - 1) / tau_c)/(Tta_Ta - 1)) - 1) + alpha * Ma * (math.sqrt((Tta_Ta * tau_f - 1)/(Tta_Ta - 1)) - 1)
                TSFC = ((Tt4_Ta - Tta_Ta * tau_c) / (delH_CpTa)) / F_ma
            except:
                # print(pi_c, pi_f)
                F_ma = None
                TSFC = None
            f_row.append(F_ma)
            t_row.append(TSFC)
        plot_f.append(f_row)
        plot_t.append(t_row)
    # print(plot_x)
    # print(plot_y)
    # print(len(plot_f)*len(plot_f[0]))
    data = {'x': plot_x, 'y': plot_y, 'f': plot_f, 't': plot_t}
    
    return JsonResponse(data)
