class Expense:
    def __init__(self):
        self.total_debit = 0
        self.total_credit = 0
        self.category_spendings = {}

    def get_category_spendings(self, category: str) -> int:
        return self.category_spendings.get(category, 0)
    
    def add_expense_to_category(self, options: list[str], text: str, category: str, amount: int):
        if any(option in text for option in options):
            self.category_spendings[category] = self.category_spendings.get(category, 0) + amount

