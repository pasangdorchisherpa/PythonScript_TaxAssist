
# Income Entry Section


Income_Number = int(input("\nEnter the number of income sources you had this year: "))
Income_Data_By_Source = {}
valid_slips = ["T4", "T4A", "T5", "T3", "None"]

for i in range(Income_Number):
    print(f"\n--- Income Source {i + 1} ---")
    source = input("Enter the income source name (e.g., Employment, Scholarship, Rental, Investment): ")

    while True:
        try:
            amount = float(input(f"Enter the amount for {source} (CAD): "))
            break
        except ValueError:
            print("Please enter a valid number.")

    taxable_input = input(f"Is {source} taxable? (yes/no): ").strip().lower()
    taxable = taxable_input in ["yes", "y"]

    print(f"Choose slip type for {source} from: {', '.join(valid_slips)}")
    slip = input("Slip type: ").strip()
    if slip not in valid_slips:
        slip = "None"

    notes = ""
    if source.lower() == "scholarship":
        if taxable:
            notes = "Scholarship is taxable under CRA rules."
        else:
            notes = "Scholarship exempt — full-time program or qualifying award."
    elif source.lower() == "employment":
        notes = "T4 wages from employment in Canada."
    elif source.lower() == "rental":
        notes = "Rental income — expenses may be deductible."

    Income_Data_By_Source[source] = {
        "amount": amount,
        "taxable": taxable,
        "slip": slip,
        "notes": notes
    }

if source.lower() == "investment":
    print("Enter the breakdown of your investment income:")

    while True:
        try:
            cap_gains = float(input("  Capital Gains (CAD): "))
            break
        except ValueError:
            print("Please enter a valid number.")

    while True:
        try:
            dividends = float(input("  Dividends (CAD): "))
            break
        except ValueError:
            print("Please enter a valid number.")

    while True:
        try:
            interest = float(input("  Interest Income (CAD): "))
            break
        except ValueError:
            print("Please enter a valid number.")


    taxable_cap_gains = cap_gains * 0.5 # Capital gains are 50% taxable
    taxable_interest = interest  # fully taxable
    taxable_dividends = dividends  # keep it simple for now, can add gross-up later

    Income_Data_By_Source[source] = {
        "amount": cap_gains + dividends + interest,
        "taxable": True,
        "slip": slip,
        "notes": f"Capital Gains: ${cap_gains}, Dividends: ${dividends}, Interest: ${interest}",
        "taxable_breakdown": {
            "capital_gains": taxable_cap_gains,
            "dividends": taxable_dividends,
            "interest": taxable_interest
        }
    }



# Deduction Inputs


print("\n===== ENTER DEDUCTIONS & CREDITS =====")
rrsp = float(input("Enter RRSP contributions (CAD): "))
union_dues = float(input("Enter union/professional dues (CAD): "))
childcare = float(input("Enter childcare expenses (CAD): "))
tuition = float(input("Enter tuition paid (CAD): "))
medical = float(input("Enter eligible medical expenses (CAD): "))
donations = float(input("Enter charitable donations (CAD): "))


# Tax Calculation Function


def calculate_tax(incomes, rrsp=0, union_dues=0, childcare=0, tuition=0, medical=0, donations=0, tax_year=2025, province="Saskatchewan"):
    # --- 2025 Federal Rates ---
    federal_brackets = [
        (55867, 0.145),
        (111733, 0.205),
        (173205, 0.26),
        (246752, 0.29),
        (float("inf"), 0.33)
    ]
    federal_bpa = 15805  # Basic Personal Amount

    # 2025 Saskatchewan Rates
    sk_brackets = [
        (52281, 0.105),
        (149865, 0.125),
        (float("inf"), 0.145)
    ]
    sk_bpa = 19491  # Basic Personal Amount SK

    # CPP & EI (2025)
    cpp_rate = 0.0595
    cpp_max_earnings = 71300
    cpp_basic_exemption = 3500
    cpp_max_contribution = 4034.10

    ei_rate = 0.0164
    ei_max_earnings = 65700
    ei_max_contribution = 1077.48

    # Step 1: Total incomes
    gross_income = sum(v["amount"] for v in incomes.values())
    taxable_income = 0
    for v in incomes.values():
        if v["taxable"]:
            if "taxable_breakdown" in v:
                # Investment income with breakdown
                taxable_income += sum(v["taxable_breakdown"].values())
            else:
                taxable_income += v["amount"]

    # Step 2: Apply deductions to taxable income
    taxable_income -= (rrsp + union_dues + childcare)
    taxable_income = max(taxable_income, 0)

    # Step 3: Federal tax
    federal_tax = 0
    remaining = taxable_income
    prev_limit = 0
    for limit, rate in federal_brackets:
        if taxable_income > prev_limit:
            taxed_amount = min(limit - prev_limit, remaining)
            federal_tax += taxed_amount * rate
            remaining -= taxed_amount
            prev_limit = limit
        else:
            break
    # Basic personal amount credit
    federal_tax -= federal_bpa * federal_brackets[0][1]

    # Step 4: Provincial tax (Saskatchewan)
    provincial_tax = 0
    remaining = taxable_income
    prev_limit = 0
    for limit, rate in sk_brackets:
        if taxable_income > prev_limit:
            taxed_amount = min(limit - prev_limit, remaining)
            provincial_tax += taxed_amount * rate
            remaining -= taxed_amount
            prev_limit = limit
        else:
            break
    provincial_tax -= sk_bpa * sk_brackets[0][1]

    # Step 5: CPP & EI
    cpp_contribution = 0
    if taxable_income > cpp_basic_exemption:
        cpp_contribution = min((taxable_income - cpp_basic_exemption) * cpp_rate, cpp_max_contribution)

    ei_contribution = min(taxable_income * ei_rate, ei_max_contribution)

    # Step 6: Non-refundable tax credits
    # Tuition/education
    federal_tax -= tuition * 0.15
    provincial_tax -= tuition * 0.10

    # Medical expenses (only exceeding 3% of net income)
    medical_deduction = max(0, medical - 0.03 * taxable_income)
    federal_tax -= medical_deduction * 0.15
    provincial_tax -= medical_deduction * 0.10

    # Charitable donations (tiered federal, flat provincial)
    federal_tax -= min(donations, 200) * 0.15 + max(0, donations - 200) * 0.29
    provincial_tax -= donations * 0.11

    # Step 7: Total tax & net income
    total_tax = max(federal_tax, 0) + max(provincial_tax, 0) + cpp_contribution + ei_contribution
    net_income = gross_income - total_tax

    # Output
    print("\n===== TAX CALCULATION SUMMARY =====")
    print(f"Gross Income: ${gross_income:,.2f}")
    print(f"Taxable Income (after deductions): ${taxable_income:,.2f}")
    print(f"Federal Tax (after credits): ${max(federal_tax, 0):,.2f}")
    print(f"Provincial Tax (after credits): ${max(provincial_tax, 0):,.2f}")
    print(f"CPP Contribution: ${cpp_contribution:,.2f}")
    print(f"EI Contribution: ${ei_contribution:,.2f}")
    print(f"Total Tax Payable: ${total_tax:,.2f}")
    print(f"Net (After-Tax) Income: ${net_income:,.2f}")
    tax_percentage = total_tax / gross_income * 100 if gross_income > 0 else 0
    print(f"Effective Tax Rate: {tax_percentage:.2f}%")


# Run the tax calculation

calculate_tax(
    Income_Data_By_Source,
    rrsp = rrsp,
    union_dues = union_dues,
    childcare = childcare,
    tuition = tuition,
    medical = medical,
    donations = donations
)

