
import heapq


class SettlementEngine:
    def __init__(self, balances):
        # Work on a copy so the original balances are unchanged.
        self.balances = balances.copy()

    def minimise_transfers(self):
        debtors = []
        creditors = []

        for name, balance in self.balances.items():
            if balance < 0:
                # Negative balance acts as a max-heap key.
                heapq.heappush(
                    debtors, (balance, name)
                )

            elif balance > 0:
                heapq.heappush(
                    creditors, (-balance, name)
                )

        total_balance = sum(self.balances.values())

        if total_balance != 0:
            raise ValueError(
                "Balances do not add up to zero. "
                "Check the expense records."
            )

        settlements = []

        while debtors and creditors:
            debt_balance, debtor = heapq.heappop(debtors)
            credit_balance, creditor = heapq.heappop(creditors)

            debt_amount = -debt_balance
            credit_amount = -credit_balance

            # Transfer the smaller outstanding amount.
            amount = min(debt_amount, credit_amount)

            settlements.append({
                "from": debtor,
                "to": creditor,
                "amount": amount
            })

            debt_amount -= amount
            credit_amount -= amount

            if debt_amount > 0:
                heapq.heappush(
                    debtors, (-debt_amount, debtor)
                )

            if credit_amount > 0:
                heapq.heappush(
                    creditors, (-credit_amount, creditor)
                )

        return settlements

    @staticmethod
    def estimate_fees(settlements, fee_per_transfer_paise):
        if fee_per_transfer_paise < 0:
            raise ValueError("Transaction fee cannot be negative.")

        return (
            len(settlements) * fee_per_transfer_paise
        )
