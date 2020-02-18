voltage_V = 24  # Напряжение питания, В
power_W = 15  # Мощность потребителей,Вт
current_i = 0  # Ток нагрузки,А
length_L = 1000  # Длина участка цепи,м.
cable_section_S = 0  # Сечение кабеля,мм²
resistivity_dc = 0  # Удельное сопротивление провода постоянному току,Ом·мм²/м
conductor = "Cu"  # Проводник
temperature = 20  # Температура эксплуатации,°C

input_data = {}

#
# обработка данных

# Находим ТОК или МОЩНОСТЬ

if power_W == 0 == current_i:
    print("Необходимо ввести мощность или ток")
elif power_W == 0:
    power_W = voltage_V * current_i
else:
    current_i = power_W / voltage_V

# Вычисляем удельное сопротивление провода постоянному току

if resistivity_dc == 0:
    if conductor == "Cu":
        resistivity_dc = 0.0181
    elif conductor == "Al":
        resistivity_dc = 0.0181  # TODO нужно уточнить Удельное сопротивление провода постоянному току для алюминия
    else:
        print("Введенные значения превышают возможности программы")

output_data = {"Проводник": conductor, "Температура,°C": temperature,
               "Удельное сопротивление постоянному току, Ом·мм²/м": resistivity_dc}
# Находим СЕЧЕНИЕ

if cable_section_S == 0:
    cable_section_S = 0.5
    while ((((resistivity_dc * length_L) / cable_section_S) * 2) * current_i / voltage_V) > 0.1:
        cable_section_S += 0.25
        if cable_section_S == 1:
            break
    while ((((resistivity_dc * length_L) / cable_section_S) * 2) * current_i / voltage_V) > 0.1:
        cable_section_S += 0.5
        if cable_section_S == 3:
            break
    while ((((resistivity_dc * length_L) / cable_section_S) * 2) * current_i / voltage_V) > 0.1:
        cable_section_S += 1
        if cable_section_S == 25:
            print("Введенные значения превышают возможности программы")
            break
elif 0 == cable_section_S > 25:
    print("Введенные значения превышают возможности программы")

# Подбираем АВТОМАТ,ПРЕДОХРАНИТЕЛЬ и подгоняем сечение

breaker = 0  # Автоматический выключатель,А
if 0.5 <= cable_section_S <= 1.5:
    breaker = 6
if 1.5 <= cable_section_S <= 2.5:
    breaker = 10
if 2.5 <= cable_section_S <= 4:
    breaker = 16
elif cable_section_S == 4:
    breaker = 20
elif cable_section_S == 5:
    breaker = 25
elif cable_section_S == 6:
    breaker = 32
elif 7 <= cable_section_S <= 8:
    cable_section_S = 8
    breaker = 32
elif 9 <= cable_section_S <= 10:
    cable_section_S = 10
    breaker = 40
elif 10 < cable_section_S <= 16:
    cable_section_S = 16
    breaker = 40
elif 16 < cable_section_S <= 25:
    cable_section_S = 25
    breaker = 50
fuse = cable_section_S * 10  # Плавкий предохранитель,А

output_data['Плавкий предохранитель, А'] = fuse  # TODO уточнить!
output_data['Автоматический выключатель, А'] = breaker

"""
ПУЭ 7 т1.3.4 
Допустимый длительный ток для проводов и шнуров с резиновой и поливинилхлоридной изоляцией с медными жилами
"""

current_max = 0  # Максимальный ток для данного сечения
if cable_section_S < 1:
    current_max = "--"
elif cable_section_S == 1:
    current_max = 16
elif cable_section_S == 1.5:
    current_max = 19
elif cable_section_S == 2:
    current_max = 24
elif cable_section_S == 2.5:
    current_max = 27
elif cable_section_S == 3:
    current_max = 32
elif cable_section_S == 4:
    current_max = 38
elif cable_section_S == 5:
    current_max = 42
elif cable_section_S == 6:
    current_max = 46
elif cable_section_S == 8:
    current_max = 54
elif cable_section_S == 10:
    current_max = 70
elif cable_section_S == 16:
    current_max = 85
elif cable_section_S == 25:
    current_max = 115
elif cable_section_S > 25:
    print("Введенные значения превышают возможности программы")
    current_max = "--"
output_data['Максимальный ток, А'] = current_max
#
# РАСЧЁТ
#
"""
Сопротивление провода зависит от удельного сопротивления ρ, которое измеряется в Ом·мм²/м.					

R₁ = ρ*L/S					

R₁ – Сопротивление одного проводника, Ом					
ρ – удельное сопротивление провода, Ом·мм²/м					
L – длина провода, м					
S – площадь поперечного сечения, мм²
"""
resistance = (resistivity_dc * length_L) / cable_section_S  # Сопротивление один проводник, Ом
"""
По формуле рассчитаем падение напряжения на проводе:

∆U₁ = (ρ*L/S)*i					

∆U₁ – Падение напряжения на проводе, В					
i – Ток нагрузки, А	
"""
U1 = resistance * current_i  # Падение один проводник, В
"""
А так как электроснабжение осуществляется по двум проводникам, то для этого необходимо расчитать падение напряжения 
на конце участка цепи ∆U₁*2					

∆U= ∆U₁*2					
"""
output_data['Падение напряжение на, В'] = resistance_total = U1 * 2  # Падение на два проводника, В
"""
Далее вычисляем падение напряжения в процентах и напряжение, которое будет на конце данного участка цепи:					

Uend = U-∆U
∆U = (∆U2/U)*100

"""
output_data['Напряжение на конце участка цепи, В'] = Uend = voltage_V - resistance_total
output_data['Падение напряжения на, %'] = Up = round((U1 * 2 / voltage_V) * 100, 2)  # Падение U в %

"""
output_data['Падение напряжение на, В'] = U2 = current_i * resistance_total  # Напряжение на участке уменьшается на, В
output_data['Падение напряжения на, %'] = Up = round((U2 / voltage_V) * 100, 2)  # Падение U в %
output_data['Напряжение на конце участка цепи, В'] = Uend = voltage_V - U2  # Напряжение на конце участка, В
"""

# ВЫВОД ДАННЫХ
print(output_data)
