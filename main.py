
from expense_manager import ExpenseManager, money_to_paise, format_money
from settlement import SettlementEngine
from reports import export_report


def main():
    app = ExpenseManager()
    latest_settlements = None

    print("=" * 42)
    print("       NET-SETTLE")
    print(" Smart Group Expense & Debt Minimiser")
    print("=" * 42)

    while True:
        print("\n1. Add group member")
        print("2. Record a shared expense")
        print("3. View expense history")
        print("4. View net balances")
        print("5. Calculate settlements")
        print("6. Export CSV report")
        print("7. Exit")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                name = input("Member name: ")
                app.add_member(name)
                latest_settlements = None
                print(f"{name.strip()} added successfully.")

            elif choice == "2":
                if len(app.members) < 2:
                    print("Add at least two members first.")
                    continue

                payer = input("Who paid? ").strip()

                if payer not in app.members:
                    print("That payer is not registered.")
                    continue

                amount = money_to_paise(
                    input("Total expense in Rs.: ")
                )

                description = input("Expense description: ").strip()
                category = input(
                    "Category (food, travel, rent, etc.): "
                ).strip()

                print("Registered members:", ", ".join(
                    sorted(app.members)
                ))

                names = input(
                    "Who shared this expense? "
                    "Enter names separated by commas: "
                )

                participants = [
                    name.strip()
                    for name in names.split(",")
                    if name.strip()
                ]

                app.add_expense(
                    payer,
                    amount,
                    description,
                    category,
                    participants
                )

                latest_settlements = None
                print("Expense recorded successfully!")

            elif choice == "3":
                app.show_expenses()

            elif choice == "4":
                app.show_balances()

            elif choice == "5":
                engine = SettlementEngine(app.balances)
                latest_settlements = engine.minimise_transfers()

                print("\n--- Recommended Settlements ---")

                if not latest_settlements:
                    print("Everyone is already settled.")
                else:
                    for payment in latest_settlements:
                        print(
                            f"{payment['from']} pays "
                            f"{payment['to']}: "
                            f"{format_money(payment['amount'])}"
                        )

                fee_input = input(
                    "Estimated fee per transfer in Rs. "
                    "(press Enter for 0): "
                ).strip()

                if fee_input:
                    fee = money_to_paise(fee_input)
                else:
                    fee = 0

                total_fees = engine.estimate_fees(
                    latest_settlements, fee
                )

                print(
                    f"Total transfers: {len(latest_settlements)}"
                )
                print(
                    f"Estimated total fees: {format_money(total_fees)}"
                )
                print(
                    f"Total recorded expenses: "
                    f"{format_money(app.total_expense())}"
                )

            elif choice == "6":
                if latest_settlements is None:
                    latest_settlements = (
                        SettlementEngine(
                            app.balances
                        ).minimise_transfers()
                    )

                export_report(app, latest_settlements)

            elif choice == "7":
                print("Thank you for using Net-Settle!")
                break

            else:
                print("Please select a number from 1 to 7.")

        except ValueError as error:
            print("Could not complete that action:", error)

        except OSError as error:
            print("Could not save the report:", error)


if __name__ == "__main__":
    main()
