# greeting_by_time.py
# A simple script that gives a greeting based on the time of day.

time = input("What time is it? (morning, afternoon, or evening): ").lower()

if time == "morning":
    print("Good morning! Hope you have a great start to your day.")
elif time == "afternoon":
    print("Good afternoon! Keep going strong.")
elif time == "evening":
    print("Good evening! Time to relax and unwind.")
else:
    print("I don't recognize that time, but I hope you're doing well!")
