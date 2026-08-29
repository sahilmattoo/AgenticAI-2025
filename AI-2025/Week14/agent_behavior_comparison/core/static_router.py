class StaticRouter:
    """
    Week 9: Legacy Rule-Based Routing.
    Logic is hardcoded and fragile.
    """
    
    @staticmethod
    def route_query(query: str) -> str:
        # Normalize
        q = query.lower()
        
        # Hardcoded Rules
        if "bill" in q or "invoice" in q or "charge" in q:
            return "BILLING"
        elif "error" in q or "bug" in q or "fail" in q:
            return "TECHNICAL"
        elif "feature" in q or "product" in q or "buy" in q:
            return "PRODUCT"
        else:
            return "GENERAL_SUPPORT"
