class PREducator:
    """Comparing two Purchase Requests contextually."""

    @staticmethod
    def compare_prs(pr1: dict, pr2: dict) -> dict:
        """
        Compares two PR dictionaries and returns a comparison report.
        """
        report = {
            "pr1_id": pr1.get("pr_id"),
            "pr2_id": pr2.get("pr_id"),
            "vendor1": pr1.get("vendor_name"),
            "vendor2": pr2.get("vendor_name"),
            "item_comparison": [],
            "total_diff": 0,
            "cheaper_option": None
        }

        # Normalize items for comparison (simple name matching for now)
        items1 = {item['name'].lower(): item for item in pr1.get('items', [])}
        items2 = {item['name'].lower(): item for item in pr2.get('items', [])}
        
        all_items = set(items1.keys()) | set(items2.keys())
        
        for item_name in all_items:
            i1 = items1.get(item_name)
            i2 = items2.get(item_name)
            
            comp = {
                "name": item_name,
                "in_pr1": i1 is not None,
                "in_pr2": i2 is not None,
                "price1": i1['unit_price'] if i1 else None,
                "price2": i2['unit_price'] if i2 else None,
                "diff": None,
                "status": "match"
            }
            
            if i1 and i2:
                diff = i2['unit_price'] - i1['unit_price']
                comp['diff'] = diff
                if diff < 0:
                    comp['status'] = "pr2_cheaper"
                elif diff > 0:
                    comp['status'] = "pr1_cheaper"
                else:
                    comp['status'] = "equal"
            
            report["item_comparison"].append(comp)

        total1 = pr1.get("grand_total", 0)
        total2 = pr2.get("grand_total", 0)
        report["total_diff"] = total2 - total1
        
        if total1 < total2:
            report["cheaper_option"] = pr1.get("vendor_name")
        elif total2 < total1:
            report["cheaper_option"] = pr2.get("vendor_name")
        else:
            report["cheaper_option"] = "Equal"

        return report
