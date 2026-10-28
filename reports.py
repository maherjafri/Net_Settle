
import csv
from expense_manager import format_money


def export_report(manager, settlements, filename="settlement_report.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(["NET-SETTLE REPORT"])
        writer.writerow([])

        writer.writerow(["GROUP BALANCES"])
        writer.writerow(["Member", "Balance", "Status"])

        for name in sorted(manager.members):
            balance = manager.balances[name]

            if balance < 0:
                status = "Needs to pay"
            elif balance > 0:
                status = "Should receive"
            else:
                status = "Settled"

            writer.writerow([
                name,
                format_money(balance),
                status
            ])

        writer.writerow([])
        writer.writerow(["RECOMMENDED SETTLEMENTS"])
        writer.writerow(["From", "To", "Amount"])

        for payment in settlements:
            writer.writerow([
                payment["from"],
                payment["to"],
                format_money(payment["amount"])
            ])

        writer.writerow([])
        writer.writerow(["EXPENSE HISTORY"])
        writer.writerow([
            "Description", "Category", "Payer",
            "Amount", "Participants"
        ])

        for expense in manager.expenses:
            writer.writerow([
                expense["description"],
                expense["category"],
                expense["payer"],
                format_money(expense["amount"]),
                ", ".join(expense["participants"])
            ])

    print(f"\nReport saved as: {filename}")
