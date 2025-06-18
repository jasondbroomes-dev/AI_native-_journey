# budget_calculator.py
# A simple budget calculator that shows how much money is left after spending

def get_expense(item_name):
    """
    Ask the user how much they spent on a specific item.
    """
    amount = float(input(f"How much did you spend on {item_name}? $"))
    return amount

# --- Main Program ---

print("🧮 Welcome to the Budget Calculator!")

# Ask for starting budget
starting_money = float(input("How much money do you have to spend today? $"))

# Ask for spending on different categories
food = get_expense("food")
clothes = get_expense("clothes")
games = get_expense("games")

# Calculate total spent and what's left
total_spent = food + clothes + games
remaining = starting_money - total_spent

# Display results
print("\n----- Summary -----")
print(f"Total spent: ${total_spent:.2f}")
print(f"Money left: ${remaining:.2f}")

# Conditional feedback
if remaining > 0:
    print("✅ You're within your budget. Great job!")
elif remaining == 0:
    print("⚠️ You've spent exactly your budget. Be careful!")
else:
    print("❌ You went over your budget! Time to save next time.")
