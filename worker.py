worker_log={}
while True:
    print("\n--- Worker Log Menu ---")
    print("1. Add Worker")
    print("2. Add Work & Wage Entry")
    print("3. View Raw Data Log")
    print("4. View Clean Report")
    print("5. Delete Worker")
    print("6. Add Deduction")
    print("7. Remove Work Entry")
    print("8. Remove Deduction")
    print("9. Exit")

    choice = input("Choose an option (1-9): ")

    if choice == "1":
        name = input("Enter worker name: ").strip().title()
        if name in worker_log:
            print("Worker already exists.")
        else:
            try:
                age = int(input(f"Enter age for {name}: "))
            except ValueError:
                print("Please enter a valid age.")
                continue
            if age < 18:
                print("Worker must be at least 18 years old.")
                continue
            job = input(f"Enter occupation for {name}: ").strip()
            worker_log[name] = {"age": age, "occupation": job, "work_entries": [], "deductions": []}
            print(f"{name} added successfully.")

    elif choice == "2":
        name = input("Enter worker name: ").strip().title()
        if name not in worker_log:
            print("Worker not found.")
        else:
            shift = input("Enter shift name: ").strip()
            try:
                days = int(input("Enter number of days worked: "))
                hours = float(input("Enter average hours worked per day: "))
                wage = float(input("Enter hourly wage: $"))
            except ValueError:
                print("Please enter valid numeric values.")
                continue
            if days <= 0:
                print("Days worked must be greater than 0.")
                continue
            if hours <= 0 or hours > 24:
                print("Average hours worked per day must be between 0 and 24.")
                continue
            if wage < 0:
                print("Hourly wage cannot be negative.")
                continue
            worker_log[name]["work_entries"].append({"shift": shift, "days": days, "hours_per_day": hours, "hourly_wage": wage})
            print("Work entry added successfully.")

    elif choice == "3":
        print(worker_log)

    elif choice == "4":
        if not worker_log:
            print("No data available.")
        else:
            for name,data in worker_log.items():
                print("\n===============================================")
                print(f"Worker : {name}")
                print(f"Age    : {data['age']}")
                print(f"Job    : {data['occupation']}")
                print("===============================================")
                total_days=0; total_hours=0; gross=0
                if data["work_entries"]:
                    print(f"\n{'Shift':<15}{'Days':<8}{'Hours':<10}{'Wage/hr':<12}{'Earnings'}")
                    print("-"*60)
                    for e in data["work_entries"]:
                        hrs=e["days"]*e["hours_per_day"]
                        pay=hrs*e["hourly_wage"]
                        total_days+=e["days"]; total_hours+=hrs; gross+=pay
                        print(f"{e['shift']:<15}{e['days']:<8}{hrs:<10.1f}${e['hourly_wage']:<11.2f}${pay:.2f}")
                else:
                    print("No work entries.")
                deduct=0
                if data["deductions"]:
                    print("\nDeductions")
                    print(f"{'Reason':<20}{'Absent Days':<15}{'Amount'}")
                    print("-"*50)
                    for d in data["deductions"]:
                        deduct+=d["amount"]
                        print(f"{d['reason']:<20}{d['days_absent']:<15}${d['amount']:.2f}")
                print("\n---------------- SUMMARY ----------------")
                print(f"Total Days Worked : {total_days}")
                print(f"Total Hours       : {total_hours:.1f}")
                print(f"Gross Earnings    : ${gross:.2f}")
                print(f"Total Deductions  : ${deduct:.2f}")
                print(f"Final Payout      : ${gross-deduct:.2f}")
                print("-----------------------------------------")

    elif choice=="5":
        name=input("Enter worker name to delete: ").strip().title()
        if name in worker_log:
            del worker_log[name]
            print("Worker deleted.")
        else:
            print("Worker not found.")

    elif choice=="6":
        name=input("Enter worker name: ").strip().title()
        if name not in worker_log:
            print("Worker not found.")
        else:
            reason=input("Reason for deduction: ")
            try:
                absent=int(input("Days absent: "))
                amount=float(input("Deduction amount: $"))
            except ValueError:
                print("Please enter valid numbers.")
                continue
            if absent<0 or amount<0:
                print("Values cannot be negative.")
                continue
            worker_log[name]["deductions"].append({"reason":reason,"days_absent":absent,"amount":amount})
            print("Deduction added successfully.")

    elif choice=="7":
        name=input("Enter worker name: ").strip().title()
        if name not in worker_log:
            print("Worker not found.")
        elif not worker_log[name]["work_entries"]:
            print("No work entries.")
        else:
            for i,e in enumerate(worker_log[name]["work_entries"],1):
                print(f"{i}. {e['shift']} | {e['days']} days | {e['hours_per_day']} hrs/day | ${e['hourly_wage']}/hr")
            try:
                x=int(input("Entry number to remove: "))
                if 1<=x<=len(worker_log[name]["work_entries"]):
                    worker_log[name]["work_entries"].pop(x-1)
                    print("Work entry removed.")
                else:
                    print("Invalid entry.")
            except ValueError:
                print("Invalid input.")

    elif choice=="8":
        name=input("Enter worker name: ").strip().title()
        if name not in worker_log:
            print("Worker not found.")
        elif not worker_log[name]["deductions"]:
            print("No deductions.")
        else:
            for i,d in enumerate(worker_log[name]["deductions"],1):
                print(f"{i}. {d['reason']} | {d['days_absent']} absent | ${d['amount']}")
            try:
                x=int(input("Deduction number to remove: "))
                if 1<=x<=len(worker_log[name]["deductions"]):
                    worker_log[name]["deductions"].pop(x-1)
                    print("Deduction removed.")
                else:
                    print("Invalid entry.")
            except ValueError:
                print("Invalid input.")

    elif choice=="9":
        print("Goodbye!")
        break
    else:
        print("Invalid choice.")
