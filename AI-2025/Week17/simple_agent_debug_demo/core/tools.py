"""
Industrial tools for the IT Support Agent.
"""

import random

def check_service_status(service_name: str) -> str:
    """Checks the operational status of a given IT service."""
    services = {
        "payment": "Degraded - High Latency",
        "inventory": "Operational",
        "auth": "Operational",
        "shipping": "Down - Connection Timeout"
    }
    status = services.get(service_name.lower(), "Unknown Service")
    return f"Service '{service_name}' status: {status}"

def analyze_logs(service_name: str) -> str:
    """Retrieves and analyzes recent log entries for a service."""
    mock_logs = {
        "payment": [
            "2025-12-22 08:10:01 | ERROR | Connection pool exhausted",
            "2025-12-22 08:10:05 | WARN  | Latency exceeded 500ms",
            "2025-12-22 08:11:12 | ERROR | Failed to reach Database"
        ],
        "shipping": [
            "2025-12-22 08:05:22 | CRITICAL | 503 Service Unavailable",
            "2025-12-22 08:06:45 | ERROR | Dependency 'PartnerAPI' unreachable"
        ]
    }
    
    logs = mock_logs.get(service_name.lower(), ["No recent logs found for this service."])
    return f"Logs for {service_name}:\n" + "\n".join(logs)

def create_support_ticket(description: str, priority: str = "Medium") -> str:
    """Creates a support ticket in the internal tracking system."""
    ticket_id = f"TIC-{random.randint(1000, 9999)}"
    return f"Ticket {ticket_id} created successfully. Priority: {priority}. Description: {description}"
