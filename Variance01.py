from typing import Any


def GetData() -> dict[Any, Any]:
    data = dict()
    group_number = 1

    while True:
        f_input = float(input(f"Enter the frequency of group {group_number}: "))
        m_input = float(input(f"Enter the mean of group {group_number}: "))
        v_input = float(input(f"Enter the variance of group {group_number}: "))

        data[f"Group {group_number}"] = {
            "frequency": f_input,
            "mean": m_input,
            "variance": v_input
        }

        quit_or_not_status = input("Do you wish to quit or not? (type Y/N): ")
        if quit_or_not_status.upper() == "Y":
            break

        group_number += 1

    return data

total_score = 0.0
total_frequency = 0
population_variance = 0.0
SS_total = 0.0


Data = GetData()

for group_info in Data.values():
    total_score += group_info["frequency"] * group_info["mean"]
    total_frequency += group_info["frequency"]

x_bar = total_score / total_frequency

for group_name, group_info in Data.items():
    n_i = group_info["frequency"]
    x_bar_i = group_info["mean"]
    s_i = group_info["variance"]
    SS_total += n_i * (s_i + (x_bar_i - x_bar) ** 2)

population_variance = SS_total / total_frequency
print(f"-> Population mean (x_bar) is: {x_bar:.2f}")
print(f"-> Population variance (x_bar_i) is: {population_variance:.4f}")
print(f"-> SS_total is: {SS_total:.4f}")


