#!/usr/bin/env python
import asyncio
import os
import json
from devtools import pprint

from monarchmoney import MonarchMoney

_SESSION_FILE_ = ".mm/mm_session.pickle"

def dx(title, obj):
    print(f"============================= {title} ===================================")
    pprint(obj)

def d0(title, obj):
    dx(f"{title}[0]", obj[0])

def dk(title, obj):
    dx(f"{title}.keys()", obj.keys())


def main() -> None:
    # Use session file
    mm = MonarchMoney(session_file=_SESSION_FILE_)

    if False:
        asyncio.run(mm.interactive_login())
        mm.save_session()
    else:
        mm.load_session()

    # Subscription details
    subs = asyncio.run(mm.get_subscription_details())
    dk("subs", subs)
    dx("subs['subscription']", subs['subscription'])

    # Accounts
    accounts = asyncio.run(mm.get_accounts())
    dk("accounts", accounts)
    d0("accounts['accounts']", accounts['accounts'])
    dx("accounts['householdPreferences']", accounts['householdPreferences'])

    # Institutions
    institutions = asyncio.run(mm.get_institutions())
    dk("institutions", institutions)
    d0("institutions['credentials']", institutions["credentials"])
    d0("institutions['accounts']", institutions["accounts"])
    dx("institutions['subscription']", institutions["subscription"])

    # Budgets
    budgets = asyncio.run(mm.get_budgets())
    dk("budgets", budgets)
    dk("budgets['budgetData']", budgets["budgetData"])
    d0("budgets['categoryGroups']", budgets["categoryGroups"])
    d0("budgets['goalsV2']", budgets["goalsV2"])
    dx("budgets['budgetSystem']", budgets["budgetSystem"])


    zzz="""
    # Transactions summary
    transactions_summary = asyncio.run(mm.get_transactions_summary())
    with open("transactions_summary.json", "w") as outfile:
        json.dump(transactions_summary, outfile)

    # # Transaction categories
    categories = asyncio.run(mm.get_transaction_categories())
    with open("categories.json", "w") as outfile:
        json.dump(categories, outfile)

    income_categories = dict()
    for c in categories.get("categories"):
        if c.get("group").get("type") == "income":
            print(
                f'{c.get("group").get("type")} - {c.get("group").get("name")} - {c.get("name")}'
            )
            income_categories[c.get("name")] = 0

    expense_category_groups = dict()
    for c in categories.get("categories"):
        if c.get("group").get("type") == "expense":
            print(
                f'{c.get("group").get("type")} - {c.get("group").get("name")} - {c.get("name")}'
            )
            expense_category_groups[c.get("group").get("name")] = 0
    """
    # Transactions
    transactions = asyncio.run(mm.get_transactions(limit=10))
    dk("transactions", transactions)
    dk("transactions['allTransactions']", transactions['allTransactions'])
    d0("transactions['transactionRules']", transactions['transactionRules'])

    import sys;sys.exit(0)
    # Cashflow
    cashflow = asyncio.run(
        mm.get_cashflow(start_date="2023-10-01", end_date="2023-10-31")
    )
    with open("cashflow.json", "w") as outfile:
        json.dump(cashflow, outfile)

    for c in cashflow.get("summary"):
        print(
            f'Income: {c.get("summary").get("sumIncome")} '
            f'Expense: {c.get("summary").get("sumExpense")} '
            f'Savings: {c.get("summary").get("savings")} '
            f'({c.get("summary").get("savingsRate"):.0%})'
        )

    for c in cashflow.get("byCategory"):
        if c.get("groupBy").get("category").get("group").get("type") == "income":
            income_categories[c.get("groupBy").get("category").get("name")] += c.get(
                "summary"
            ).get("sum")

    print()
    for c in cashflow.get("byCategoryGroup"):
        if c.get("groupBy").get("categoryGroup").get("type") == "expense":
            expense_category_groups[
                c.get("groupBy").get("categoryGroup").get("name")
            ] += c.get("summary").get("sum")

    print(income_categories)
    print()
    print(expense_category_groups)


main()
