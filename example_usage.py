from client import PersonalAgentGroceryPantryAutoReplenisher

def main():
    agent = PersonalAgentGroceryPantryAutoReplenisher()
    pantry = [
        {"item_name": "Rolled Oats", "current_qty": 0.2, "daily_consumption_rate": 0.1, "days_until_expiration": 30, "estimated_unit_price_usd": 4.29},
        {"item_name": "Cold Brew Coffee", "current_qty": 0.3, "daily_consumption_rate": 0.3, "days_until_expiration": 4, "estimated_unit_price_usd": 6.99}
    ]
    res = agent.generate_replenishment_basket(pantry, {"weekly_budget_usd": 60.0, "organic_preference": False})
    print("--- Smart Pantry Auto-Replenishment ---")
    print(f"Total Cart: ${res['total_basket_cost_usd']} (Remaining: ${res['remaining_budget_usd']})")
    for it in res['cart_items']:
        print(f"* {it['item_name']} x{it['order_quantity']} (${it['total_cost_usd']}) - Reason: {it['urgency_reason']}")

if __name__ == "__main__":
    main()
