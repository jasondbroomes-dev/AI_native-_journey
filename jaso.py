# Starting amounts
joe = 5
sam = 7

# Ask how much Sam wants to give to Joe
amount = float(input("How much money does Sam want to give to Joe? $"))

# Check if Sam has enough money
if amount <= sam:
    sam = sam - amount
    joe = joe + amount
    print("Joe now has $" + str(joe))
    print("Sam now has $" + str(sam))
else:
    print("Sam doesn’t have enough money to give.")
