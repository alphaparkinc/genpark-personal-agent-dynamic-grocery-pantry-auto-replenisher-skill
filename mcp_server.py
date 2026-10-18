#!/usr/bin/env python3
import json
import sys
from client import PersonalAgentGroceryPantryAutoReplenisher

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        agent = PersonalAgentGroceryPantryAutoReplenisher()
        pantry = [
            {"item_name": "Almond Milk", "current_qty": 0.5, "daily_consumption_rate": 0.4, "days_until_expiration": 5, "estimated_unit_price_usd": 3.99},
            {"item_name": "Greek Yogurt", "current_qty": 3.0, "daily_consumption_rate": 0.2, "days_until_expiration": 12, "estimated_unit_price_usd": 5.49}
        ]
        res = agent.generate_replenishment_basket(pantry, {"weekly_budget_usd": 100.0, "organic_preference": True})
        assert res["replenishment_items_count"] == 1
        assert "Almond Milk" in res["cart_items"][0]["item_name"]
        print(f"[TEST PASS] Smart Pantry Cart: {res['replenishment_items_count']} items, Total: ${res['total_basket_cost_usd']}")
        sys.exit(0)

    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            if method == "initialize":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"serverInfo": {"name": "genpark-smart-pantry-replenisher", "version": "1.0.0"}}}))
            elif method == "tools/list":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": [{"name": "generate_replenishment_basket", "description": "Generate dietary-aligned grocery replenishment basket"}]}}))
            elif method == "tools/call":
                args = req.get("params", {}).get("arguments", {})
                agent = PersonalAgentGroceryPantryAutoReplenisher()
                out = agent.generate_replenishment_basket(args.get("pantry_inventory", []), args.get("dietary_rules"))
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(out)}]}}))
            else:
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}))
            sys.stdout.flush()

if __name__ == "__main__":
    main()
