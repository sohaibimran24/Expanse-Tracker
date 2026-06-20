# ============================================
# Expense Tracker
# Author: Muhammad Sohaib Imran
# FAST-NUCES, Lahore | FinTech
# ============================================

import json
import os
from datetime import datetime


DATA_FILE = "expenses.json"

CATEGORIES = [
    "Food & Dining",
    "Transport",
    "Shopping",
    "Education",
    "Health",
    "Entertainment",
    "Utilities",
    "Other"
]


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    print("\n" + "=" * 45)
    print("           📊 EXPENSE TRACKER")
    print("           Muhammad Sohaib Imran")
    print("           FAST-NUCES, Lahore")
    print("=" * 45)


def load_expenses():
    """Load expenses from file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"expenses": [], "budget": 0}


def save_expenses(data):
    """Save expenses to file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def add_expense(data):
    """Add a new expense."""
    print("\n  ➕ ADD NEW EXPENSE")
    print("  " + "-" * 30)

    # Description
    description = input("  Description: ").strip()
    if not description:
        print("  ❌ Description cannot be empty!")
        return

    # Amount
    while True:
        try:
            amount = float(input("  Amount (Rs.): "))
            if amount <= 0:
                print("  ❌ Amount must be greater than 0!")
                continue
            break
        except ValueError:
            print("  ❌ Please enter a valid amount!")

    # Category
    print("\n  Select Category:")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"  {i}. {cat}")

    while True:
        try:
            cat_choice = int(input("\n  Enter category number: "))
            if 1 <= cat_choice <= len(CATEGORIES):
                category = CATEGORIES[cat_choice - 1]
                break
            else:
                print(f"  ❌ Enter a number between 1 and {len(CATEGORIES)}")
        except ValueError:
            print("  ❌ Please enter a valid number!")

    # Date
    date_str = datetime.now().strftime("%Y-%m-%d")

    expense = {
        "id": len(data["expenses"]) + 1,
        "description": description,
        "amount": amount,
        "category": category,
        "date": date_str
    }

    data["expenses"].append(expense)
    save_expenses(data)
    print(f"\n  ✅ Expense added! Rs.{amount:.2f} — {description} ({category})")


def view_expenses(data):
    """View all expenses."""
    if not data["expenses"]:
        print("\n  📭 No expenses recorded yet!")
        return

    print("\n  📋 ALL EXPENSES")
    print("  " + "=" * 65)
    print(f"  {'ID':<5} {'Date':<12} {'Description':<20} {'Category':<18} {'Amount':>10}")
    print("  " + "-" * 65)

    total = 0
    for e in data["expenses"]:
        print(f"  {e['id']:<5} {e['date']:<12} {e['description'][:18]:<20} {e['category'][:16]:<18} Rs.{e['amount']:>8.2f}")
        total += e['amount']

    print("  " + "=" * 65)
    print(f"  {'TOTAL':<57} Rs.{total:>8.2f}")
    print("  " + "=" * 65)

    # Budget check
    if data["budget"] > 0:
        remaining = data["budget"] - total
        if remaining < 0:
            print(f"\n  🚨 OVER BUDGET by Rs.{abs(remaining):.2f}!")
        else:
            print(f"\n  💰 Budget Remaining: Rs.{remaining:.2f} / Rs.{data['budget']:.2f}")


def delete_expense(data):
    """Delete an expense by ID."""
    if not data["expenses"]:
        print("\n  📭 No expenses to delete!")
        return

    view_expenses(data)

    while True:
        try:
            exp_id = int(input("\n  Enter expense ID to delete: "))
            expense = next((e for e in data["expenses"] if e["id"] == exp_id), None)
            if expense:
                data["expenses"].remove(expense)
                save_expenses(data)
                print(f"\n  ✅ Deleted: {expense['description']} — Rs.{expense['amount']:.2f}")
                break
            else:
                print(f"  ❌ No expense found with ID {exp_id}!")
        except ValueError:
            print("  ❌ Please enter a valid ID!")


def category_summary(data):
    """Show spending summary by category."""
    if not data["expenses"]:
        print("\n  📭 No expenses recorded yet!")
        return

    summary = {}
    for e in data["expenses"]:
        cat = e["category"]
        summary[cat] = summary.get(cat, 0) + e["amount"]

    total = sum(summary.values())

    print("\n  📊 SPENDING BY CATEGORY")
    print("  " + "=" * 45)

    sorted_summary = sorted(summary.items(), key=lambda x: x[1], reverse=True)

    for cat, amount in sorted_summary:
        percentage = (amount / total) * 100
        bar_length = int(percentage / 5)
        bar = "█" * bar_length
        print(f"  {cat:<18} Rs.{amount:>8.2f}  {percentage:>5.1f}% {bar}")

    print("  " + "=" * 45)
    print(f"  {'TOTAL':<18} Rs.{total:>8.2f}")
    print("  " + "=" * 45)

    # Most spent category
    top_cat = sorted_summary[0]
    print(f"\n  🏆 Most spent on: {top_cat[0]} (Rs.{top_cat[1]:.2f})")


def monthly_summary(data):
    """Show monthly spending summary."""
    if not data["expenses"]:
        print("\n  📭 No expenses recorded yet!")
        return

    monthly = {}
    for e in data["expenses"]:
        month = e["date"][:7]  # YYYY-MM
        monthly[month] = monthly.get(month, 0) + e["amount"]

    print("\n  📅 MONTHLY SUMMARY")
    print("  " + "=" * 35)

    for month, amount in sorted(monthly.items()):
        print(f"  {month}    Rs.{amount:>10.2f}")

    print("  " + "=" * 35)
    print(f"  TOTAL      Rs.{sum(monthly.values()):>10.2f}")


def set_budget(data):
    """Set a monthly budget."""
    print(f"\n  💰 Current Budget: Rs.{data['budget']:.2f}" if data['budget'] > 0 else "\n  💰 No budget set.")

    while True:
        try:
            budget = float(input("  Set new budget (Rs.): "))
            if budget < 0:
                print("  ❌ Budget cannot be negative!")
                continue
            data["budget"] = budget
            save_expenses(data)
            print(f"\n  ✅ Budget set to Rs.{budget:.2f}")
            break
        except ValueError:
            print("  ❌ Please enter a valid amount!")


def quick_stats(data):
    """Show quick statistics."""
    if not data["expenses"]:
        print("\n  📭 No expenses recorded yet!")
        return

    amounts = [e["amount"] for e in data["expenses"]]
    total = sum(amounts)
    average = total / len(amounts)
    highest = max(data["expenses"], key=lambda x: x["amount"])
    lowest = min(data["expenses"], key=lambda x: x["amount"])

    print("\n  ⚡ QUICK STATS")
    print("  " + "=" * 40)
    print(f"  Total Expenses   : {len(amounts)}")
    print(f"  Total Spent      : Rs.{total:.2f}")
    print(f"  Average Expense  : Rs.{average:.2f}")
    print(f"  Highest Expense  : Rs.{highest['amount']:.2f} ({highest['description']})")
    print(f"  Lowest Expense   : Rs.{lowest['amount']:.2f} ({lowest['description']})")
    if data["budget"] > 0:
        used_pct = (total / data["budget"]) * 100
        print(f"  Budget Used      : {used_pct:.1f}%")
        if used_pct >= 100:
            print(f"  Status           : 🚨 OVER BUDGET!")
        elif used_pct >= 80:
            print(f"  Status           : ⚠️  Almost at limit!")
        else:
            print(f"  Status           : ✅ Within budget")
    print("  " + "=" * 40)


def main_menu():
    print("\n  MENU")
    print("  " + "-" * 30)
    print("  1. ➕ Add Expense")
    print("  2. 📋 View All Expenses")
    print("  3. 🗑️  Delete Expense")
    print("  4. 📊 Category Summary")
    print("  5. 📅 Monthly Summary")
    print("  6. ⚡ Quick Stats")
    print("  7. 💰 Set Budget")
    print("  0. 🚪 Exit")
    print("  " + "-" * 30)


def main():
    data = load_expenses()

    clear_screen()
    print_header()
    print("\n  Track your expenses and stay on budget!\n")

    while True:
        main_menu()
        choice = input("\n  Enter choice: ").strip()

        if choice == "1":
            add_expense(data)
        elif choice == "2":
            view_expenses(data)
        elif choice == "3":
            delete_expense(data)
        elif choice == "4":
            category_summary(data)
        elif choice == "5":
            monthly_summary(data)
        elif choice == "6":
            quick_stats(data)
        elif choice == "7":
            set_budget(data)
        elif choice == "0":
            print("\n  💰 Keep tracking your expenses!")
            print("  — Muhammad Sohaib Imran | FAST-NUCES\n")
            break
        else:
            print("\n  ❌ Invalid choice!")

        input("\n  Press Enter to continue...")
        clear_screen()
        print_header()


if __name__ == "__main__":
    main()
