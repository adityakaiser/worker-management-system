import json
import os

FILE="worker_log.json"

if os.path.exists(FILE):
    with open(FILE,"r") as f:
        try:
            worker_log=json.load(f)
        except:
            worker_log={}
else:
    worker_log={}

def save():
    with open(FILE,"w") as f:
        json.dump(worker_log,f,indent=4)

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

    c=input("Choose an option (1-9): ")

    if c=="1":
        n=input("Enter worker name: ").strip().title()
        if n in worker_log:
            print("Worker already exists.")
            continue
        try:
            age=int(input("Enter age: "))
        except:
            print("Invalid age."); continue
        if age<18:
            print("Worker must be at least 18."); continue
        job=input("Enter occupation: ")
        worker_log[n]={"age":age,"occupation":job,"work_entries":[],"deductions":[]}
        save()
        print("Worker added.")

    elif c=="2":
        n=input("Enter worker name: ").strip().title()
        if n not in worker_log:
            print("Worker not found."); continue
        shift=input("Shift: ")
        try:
            d=int(input("Days worked: "))
            h=float(input("Hours/day: "))
            w=float(input("Hourly wage: "))
        except:
            print("Invalid input."); continue
        if d<=0 or h<=0 or h>24 or w<0:
            print("Invalid values."); continue
        worker_log[n]["work_entries"].append({"shift":shift,"days":d,"hours_per_day":h,"hourly_wage":w})
        save()
        print("Work entry added.")

    elif c=="3":
        print(worker_log)

    elif c=="4":
        if not worker_log:
            print("No data.")
        for n,data in worker_log.items():
            print("\n"+"="*45)
            print("Worker:",n)
            print("Age:",data["age"])
            print("Job:",data["occupation"])
            gross=hours=days=0
            if data["work_entries"]:
                print(f"\n{'Shift':<15}{'Days':<8}{'Hours':<10}{'Pay'}")
                for e in data["work_entries"]:
                    hrs=e["days"]*e["hours_per_day"]
                    pay=hrs*e["hourly_wage"]
                    days+=e["days"]; hours+=hrs; gross+=pay
                    print(f"{e['shift']:<15}{e['days']:<8}{hrs:<10.1f}${pay:.2f}")
            ded=0
            if data["deductions"]:
                print("\nDeductions")
                for x in data["deductions"]:
                    ded+=x["amount"]
                    print(f"{x['reason']} - ₹{x['amount']:.2f}")
            print(f"\nTotal Days: {days}")
            print(f"Total Hours: {hours:.1f}")
            print(f"Gross: ₹{gross:.2f}")
            print(f"Deductions: ₹{ded:.2f}")
            print(f"Final: ₹{gross-ded:.2f}")

    elif c=="5":
        n=input("Worker name: ").strip().title()
        if n in worker_log:
            del worker_log[n]
            save()
            print("Deleted.")
        else:
            print("Worker not found.")

    elif c=="6":
        n=input("Worker name: ").strip().title()
        if n not in worker_log:
            print("Worker not found."); continue
        reason=input("Reason: ")
        try:
            a=int(input("Absent days: "))
            amt=float(input("Amount: "))
        except:
            print("Invalid."); continue
        if a<0 or amt<0:
            print("Invalid."); continue
        worker_log[n]["deductions"].append({"reason":reason,"days_absent":a,"amount":amt})
        save()
        print("Deduction added.")

    elif c=="7":
        n=input("Worker name: ").strip().title()
        if n not in worker_log or not worker_log[n]["work_entries"]:
            print("No work entries."); continue
        for i,e in enumerate(worker_log[n]["work_entries"],1):
            print(f"{i}. {e['shift']} ({e['days']} days)")
        try:
            i=int(input("Remove entry #: "))
            worker_log[n]["work_entries"].pop(i-1)
            save()
            print("Removed.")
        except:
            print("Invalid.")

    elif c=="8":
        n=input("Worker name: ").strip().title()
        if n not in worker_log or not worker_log[n]["deductions"]:
            print("No deductions."); continue
        for i,d in enumerate(worker_log[n]["deductions"],1):
            print(f"{i}. {d['reason']} - ₹{d['amount']}")
        try:
            i=int(input("Remove deduction #: "))
            worker_log[n]["deductions"].pop(i-1)
            save()
            print("Removed.")
        except:
            print("Invalid.")

    elif c=="9":
        save()
        print("Data saved. Goodbye!")
        break
    else:
        print("Invalid choice.")