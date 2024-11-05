from datetime import datetime
import matplotlib.pyplot as plt
from typing import List
import time

class Expense:
    def __init__(self, date: str, amount: float, category: str, description: str):
        self.date = datetime.strptime(date, "%Y-%m-%d")
        self.amount = amount
        self.category = category
        self.description = description

class ExpenseTracker:
    def __init__(self):
        self.expenses: List[Expense] = []
        
    def add_expense(self, date: str, amount: float, category: str, description: str) -> None:
        """
        Add expense using insertion sort to maintain sorted order by date
        Time Complexity: O(n)
        """
        try:
            new_expense = Expense(date, amount, category, description)
            
            # Insertion sort by date
            i = len(self.expenses)
            self.expenses.append(new_expense)
            
            while i > 0 and self.expenses[i-1].date > self.expenses[i].date:
                self.expenses[i-1], self.expenses[i] = self.expenses[i], self.expenses[i-1]
                i -= 1
                
            print("Expense added successfully!")
            
        except ValueError as e:
            print(f"Error: {e}")

    def merge_sort_by_amount(self, expenses: List[Expense]) -> List[Expense]:
        """
        Merge sort implementation for sorting expenses by amount
        Time Complexity: O(n log n)
        """
        if len(expenses) <= 1:
            return expenses
            
        mid = len(expenses) // 2
        left = self.merge_sort_by_amount(expenses[:mid])
        right = self.merge_sort_by_amount(expenses[mid:])
        
        return self.merge(left, right)
    
    def merge(self, left: List[Expense], right: List[Expense]) -> List[Expense]:
        """Helper function for merge sort"""
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if left[i].amount <= right[j].amount:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def binary_search_by_date(self, target_date: str) -> List[Expense]:
        """
        Binary search implementation for finding expenses by date
        Time Complexity: O(log n)
        """
        target = datetime.strptime(target_date, "%Y-%m-%d")
        left, right = 0, len(self.expenses) - 1
        results = []
        
        while left <= right:
            mid = (left + right) // 2
            if self.expenses[mid].date == target:
                # Find all expenses with the same date
                results.append(self.expenses[mid])
                # Check left side
                i = mid - 1
                while i >= 0 and self.expenses[i].date == target:
                    results.append(self.expenses[i])
                    i -= 1
                # Check right side
                i = mid + 1
                while i < len(self.expenses) and self.expenses[i].date == target:
                    results.append(self.expenses[i])
                    i += 1
                return results
            elif self.expenses[mid].date < target:
                left = mid + 1
            else:
                right = mid - 1
        
        return results

    def view_expenses(self, sort_by_amount=False):
        """Display expenses with option to sort by amount"""
        if not self.expenses:
            print("No expenses recorded yet.")
            return
            
        display_expenses = self.merge_sort_by_amount(self.expenses.copy()) if sort_by_amount else self.expenses
        
        print("\nExpense List:")
        print("-" * 80)
        print(f"{'Date':<12} {'Amount':>10} {'Category':<15} {'Description':<30}")
        print("-" * 80)
        
        for expense in display_expenses:
            print(f"{expense.date.strftime('%Y-%m-%d'):<12} "
                  f"${expense.amount:>9.2f} "
                  f"{expense.category:<15} "
                  f"{expense.description:<30}")
        print("-" * 80)

    def analyze_expenses(self):
        """
        Analyze and visualize expense data
        """
        if not self.expenses:
            print("No expenses to analyze.")
            return
            
        # Category-wise analysis
        category_totals = {}
        for expense in self.expenses:
            category_totals[expense.category] = category_totals.get(expense.category, 0) + expense.amount
            
        # Create pie chart
        plt.figure(figsize=(10, 6))
        plt.pie(category_totals.values(), labels=category_totals.keys(), autopct='%1.1f%%')
        plt.title('Expense Distribution by Category')
        plt.axis('equal')
        plt.show()

def main():
    tracker = ExpenseTracker()
    
    while True:
        print("\nPersonal Expense Tracker")
        print("1. Add Expense")
        print("2. View Expenses (Sort by Date)")
        print("3. View Expenses (Sort by Amount)")
        print("4. Search Expenses by Date")
        print("5. Analyze Expenses")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == '1':
            date = input("Enter date (YYYY-MM-DD): ")
            try:
                amount = float(input("Enter amount: "))
                category = input("Enter category: ")
                description = input("Enter description: ")
                tracker.add_expense(date, amount, category, description)
            except ValueError:
                print("Invalid amount! Please enter a number.")
                
        elif choice == '2':
            tracker.view_expenses(sort_by_amount=False)
            
        elif choice == '3':
            tracker.view_expenses(sort_by_amount=True)
            
        elif choice == '4':
            date = input("Enter date to search (YYYY-MM-DD): ")
            try:
                results = tracker.binary_search_by_date(date)
                if results:
                    print("\nFound Expenses:")
                    print("-" * 80)
                    print(f"{'Date':<12} {'Amount':>10} {'Category':<15} {'Description':<30}")
                    print("-" * 80)
                    for expense in results:
                        print(f"{expense.date.strftime('%Y-%m-%dd'):<12} "
                              f"${expense.amount:>9.2f} "
                              f"{expense.category:<15} "
                              f"{expense.description:<30}")
                    print("-" * 80)
                else:
                    print("No expenses found for this date.")
            except ValueError:
                print("Invalid date format!")
                
        elif choice == '5':
            tracker.analyze_expenses()
            
        elif choice == '6':
            print("Thank you for using the Expense Tracker!")
            break
            
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
