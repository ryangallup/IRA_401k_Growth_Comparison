import matplotlib.pyplot as plt

# Function to clean and convert input to float
def clean_input(input_value):
    # Remove the dollar sign and commas, then convert to float
    return float(input_value.replace('$', '').replace(',', ''))

# Constants
EXPECTED_GROWTH_RATE = 0.07  # 7% annual growth rate
PENALTY_RATE = 10  # 10% penalty for early Roth IRA withdrawal

# Get inputs from the user
ira_balance = clean_input(input("Enter your current Roth IRA balance: $"))
roth_401k_balance = clean_input(input("Enter your current Roth 401(k) balance: $"))
current_age = int(input("Enter your current age: "))
target_retirement_age = int(input("Enter your target retirement age: "))
taxable_income = clean_input(input("Enter your taxable income: $"))

# Calculate the number of years until retirement
years_to_retirement = target_retirement_age - current_age

# Federal tax brackets (for simplicity, we can apply the tax rate directly based on taxable income)
if taxable_income <= 11000:
    federal_tax_rate = 0.10
elif taxable_income <= 44725:
    federal_tax_rate = 0.12
elif taxable_income <= 95375:
    federal_tax_rate = 0.22
elif taxable_income <= 182100:
    federal_tax_rate = 0.24
elif taxable_income <= 231250:
    federal_tax_rate = 0.32
elif taxable_income <= 578125:
    federal_tax_rate = 0.35
else:
    federal_tax_rate = 0.37

# Calculate penalty for early withdrawal (set to 10%)
penalty_amount = ira_balance * (PENALTY_RATE / 100)

# Calculate the amount after penalty
amount_after_penalties = ira_balance - penalty_amount

# Calculate the federal tax on the withdrawal
federal_tax_on_withdrawal = amount_after_penalties * (federal_tax_rate / 100)

# Final amount rolled into Roth 401(k)
final_ira_rollover = amount_after_penalties - federal_tax_on_withdrawal

# New Roth 401(k) balance after rollover
new_roth_401k_balance = roth_401k_balance + final_ira_rollover

# Calculate future value of Roth IRA and Roth 401(k) accounts separately over time
years = list(range(current_age, target_retirement_age + 1))

# Calculate the growth of Roth IRA and Roth 401(k) separately over time
roth_ira_values = [ira_balance * (1 + EXPECTED_GROWTH_RATE) ** (year - current_age) for year in years]
roth_401k_values = [roth_401k_balance * (1 + EXPECTED_GROWTH_RATE) ** (year - current_age) for year in years]

# Calculate total value if accounts are kept separate
total_separate_values = [roth_ira + roth_401k for roth_ira, roth_401k in zip(roth_ira_values, roth_401k_values)]

# Calculate future value of Roth 401(k) with IRA rollover immediately
combined_roth_401k_values_immediate = [new_roth_401k_balance * (1 + EXPECTED_GROWTH_RATE) ** (year - current_age) for year in years]

# Results
print("\n--- Detailed Breakdown ---")
print(f"Federal tax rate applied: {federal_tax_rate * 100}%")
print(f"Roth IRA balance: ${ira_balance:,.2f}")
print(f"Penalty for early withdrawal: ${penalty_amount:,.2f}")
print(f"Amount after penalties: ${amount_after_penalties:,.2f}")
print(f"Federal tax on withdrawal: ${federal_tax_on_withdrawal:,.2f}")
print(f"Final amount rolled into Roth 401(k): ${final_ira_rollover:,.2f}")
print(f"New Roth 401(k) balance after rollover: ${new_roth_401k_balance:,.2f}")

print("\n--- Future Value Calculations ---")
print(f"Future value of Roth IRA at retirement (kept separate): ${roth_ira_values[-1]:,.2f}")
print(f"Future value of Roth 401(k) at retirement (kept separate): ${roth_401k_values[-1]:,.2f}")
print(f"Future value of Roth 401(k) and Roth IRA at retirement (total): ${total_separate_values[-1]:,.2f}")
print(f"Future value of Roth 401(k) with IRA rollover immediately (total): ${combined_roth_401k_values_immediate[-1]:,.2f}")

# Display total balance if accounts are kept separate
total_separate_balance = total_separate_values[-1]
print(f"\nTotal balance if kept separate: ${total_separate_balance:,.2f}")

# Display total balance if accounts are combined
total_combined_balance = combined_roth_401k_values_immediate[-1]
print(f"Total balance if combined: ${total_combined_balance:,.2f}")

# Conclusion on whether to combine or keep separate
if total_combined_balance > total_separate_balance:
    print("\nIt is better to combine the accounts, as it results in a higher total balance at retirement.")
else:
    print("\nIt is better to keep the accounts separate, as it results in a higher total balance at retirement.")

# Plotting the data (showing growth of both combined and separate scenarios)
plt.figure(figsize=(10, 6))

# Plot only the two lines
plt.plot(years, combined_roth_401k_values_immediate, label="Combined Roth 401(k) (immediate rollover)", color='r', linestyle='--')
plt.plot(years, total_separate_values, label="Total (separate accounts)", color='purple', linestyle='-.')

# Adding labels and title
plt.title('Growth of Combined Roth 401(k) vs. Separate Accounts Over Time')
plt.xlabel('Age')
plt.ylabel('Account Balance ($)')
plt.legend(loc='upper left')
plt.grid(True)

# Show the chart
plt.tight_layout()
plt.show()
