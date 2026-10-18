"""
Personal Agent Smart Pantry Auto-Replenisher (Pure Stdlib)
Official Website: https://www.genpark.ai | LinkedIn: https://www.llinkedin.com/company/92955550
"""
import math
from typing import Dict, Any, List, Optional

class PersonalAgentGroceryPantryAutoReplenisher:
    def __init__(self, agent_name: str = "GenPark-SmartPantry-Core"):
        self.agent_name = agent_name

    def generate_replenishment_basket(self, pantry_inventory: List[Dict[str, Any]], dietary_rules: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        rules = dietary_rules or {}
        budget = float(rules.get("weekly_budget_usd", 150.0))
        require_organic = bool(rules.get("organic_preference", False))
        allergens = set([a.lower() for a in rules.get("excluded_allergens", [])])
        
        reorder_items = []
        running_cost = 0.0
        
        for item in pantry_inventory:
            name = item.get("item_name", "Staple Item")
            qty = float(item.get("current_qty", 1.0))
            burn_rate = float(item.get("daily_consumption_rate", 0.5))
            days_left = float(item.get("days_until_expiration", 10.0))
            est_price = float(item.get("estimated_unit_price_usd", 4.5))
            
            # Days of runway left
            runway_days = qty / max(0.01, burn_rate)
            
            # Reorder if inventory runs out in <= 3 days or expires in <= 2 days
            needs_reorder = runway_days <= 3.0 or days_left <= 2.0
            
            if needs_reorder:
                # Allergen check
                if any(alg in name.lower() for alg in allergens):
                    continue
                    
                target_reorder_qty = max(1, int(math.ceil(burn_rate * 7))) # 7-day replenishment
                item_cost = round(target_reorder_qty * est_price * (1.2 if require_organic else 1.0), 2)
                
                if running_cost + item_cost <= budget:
                    reorder_items.append({
                        "item_name": f"{'Organic ' if require_organic and 'organic' not in name.lower() else ''}{name}",
                        "order_quantity": target_reorder_qty,
                        "unit_price_usd": est_price,
                        "total_cost_usd": item_cost,
                        "urgency_reason": "DEPLETION_IMMINENT" if runway_days <= 3.0 else "EXPIRATION_IMMINENT"
                    })
                    running_cost += item_cost
                    
        return {
            "agent": self.agent_name,
            "weekly_budget_usd": budget,
            "total_basket_cost_usd": round(running_cost, 2),
            "remaining_budget_usd": round(max(0.0, budget - running_cost), 2),
            "replenishment_items_count": len(reorder_items),
            "cart_items": reorder_items,
            "verdict": "GROCERY_BASKET_GENERATED"
        }
