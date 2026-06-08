from fractions import Fraction


def parse_numeric_input(user_input: str) -> float:
    """Advanced numeric parser supporting standard floats, scientific notation,

    fractions (e.g., 1/3), and percentages (e.g., 25%).
    """
    clean_input = user_input.strip()

    match clean_input:
        # Case 1: Match percentages (e.g., 25% or 12.5%)
        case s if s.endswith("%"):
            return float(s[:-1]) / 100

        # Case 2: Match fractions (e.g., 1/3 or 5/2)
        case s if "/" in s:
            return float(Fraction(s))

        # Case 3: Standard integers, decimals, or scientific notation (e.g., 1e-3)
        case _:
            return float(clean_input)


def get_valid_float(prompt: str) -> float:
    """Ensures the user enters a valid numeric value, routing through the advanced parser."""
    while True:
        try:
            user_raw = input(prompt)
            return parse_numeric_input(user_raw)
        except (ValueError, ZeroDivisionError):
            print(
                "⚠️ Invalid input! Please enter a valid number (e.g., 5, 3.14, 1/3, or 20%)."
            )


def show_data_summary(data: dict[str, dict[str, float]]) -> None:
    """Displays a well-formatted data review panel in the console."""
    print("\n📊 --- Current Data Review Panel ---")
    print("-" * 55)
    for group, info in data.items():
        print(
            f"  {group} -> Freq(N): {info['frequency']:<6.2f} "
            f"Mean: {info['mean']:<6.4f} "
            f"Variance: {info['variance']:<6.4f}"
        )
    print("-" * 55)


def get_data() -> dict[str, dict[str, float]]:
    """Handles structured data entry and supports mid-stream dynamic corrections."""
    data: dict[str, dict[str, float]] = dict()
    group_number = 1

    # ---- Phase 1: Initial Data Entry ----
    while True:
        f_input = get_valid_float(f"Enter the frequency of group {group_number}: ")
        m_input = get_valid_float(f"Enter the mean of group {group_number}: ")
        v_input = get_valid_float(f"Enter the variance of group {group_number}: ")

        data[f"Group {group_number}"] = {
            "frequency": f_input,
            "mean": m_input,
            "variance": v_input,
        }

        while True:
            quit_status = input("Do you wish to quit? (Y/N): ").upper().strip()
            if quit_status in ["Y", "N"]:
                break
            print("⚠️ Invalid choice! Please type 'Y' to quit or 'N' to continue.")

        if quit_status == "Y":
            break

        group_number += 1

    # ---- Phase 2: Dynamic Data Modification ----
    while True:
        show_data_summary(data)
        modify_choice = input(
            "💡 Press [Enter] to calculate if everything is correct.\n"
            "   To fix an error, type the group number to modify (e.g., 1 or 2): "
        ).strip()

        if not modify_choice:
            break

        target_group = f"Group {modify_choice}"

        if target_group in data:
            print(f"\n🔄 Re-entering data for [{target_group}]:")
            data[target_group]["frequency"] = get_valid_float(
                f"Enter the new frequency for {target_group}: "
            )
            data[target_group]["mean"] = get_valid_float(
                f"Enter the new mean for {target_group}: "
            )
            data[target_group]["variance"] = get_valid_float(
                f"Enter the new variance for {target_group}: "
            )
            print(f"✅ {target_group} data successfully updated!")
        else:
            print(f"⚠️ [{target_group}] not found. Please check the group number.")

    return data


# =====================================================================
# Core Calculation Section
# =====================================================================
total_score = 0.0
total_frequency = 0.0
SS_total = 0.0

# Initialize data gathering workflow
Data = get_data()

# 1. Compute the global weighted population mean (x_bar)
for group_info in Data.values():
    total_score += group_info["frequency"] * group_info["mean"]
    total_frequency += group_info["frequency"]

x_bar = total_score / total_frequency

# 2. Compute the total sum of squares (SS_total) via an optimized single loop
for group_info in Data.values():
    n_i = group_info["frequency"]
    x_bar_i = group_info["mean"]
    s_i = group_info["variance"]

    # Formula Mapping: n_i * [ σ_i² + (x_bar_i - x_bar)² ]
    SS_total += n_i * (s_i + (x_bar_i - x_bar) ** 2)

# 3. Derive final population variance from total sum of squares
population_variance = SS_total / total_frequency

# =====================================================================
# Final Metrics Exhibition Panel
# =====================================================================
print("\n" + "=" * 45)
print("🎉 Final Calculation Metrics:")
print("=" * 45)
print(f"-> Population mean (x_bar) is      : {x_bar:.4f}")
print(f"-> Sum of Squares Total (SS_total) : {SS_total:.4f}")
print(f"-> Population variance (σ²) is      : {population_variance:.4f}")
print("=" * 45)