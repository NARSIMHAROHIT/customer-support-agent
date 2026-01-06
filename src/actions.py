import uuid
from datetime import datetime


def create_support_ticket(user_issue: str) -> dict:
    """
    Create a mock support ticket.
    Returns ticket details.
    """

    ticket = {
        "ticket_id": str(uuid.uuid4()),
        "created_at": datetime.utcnow().isoformat(),
        "issue": user_issue,
        "status": "OPEN"
    }

    # For now, we just print it
    print("\nSupport Ticket Created")
    print(f"ID: {ticket['ticket_id']}")
    print(f"Issue: {ticket['issue']}")
    print(f"Status: {ticket['status']}\n")

    return ticket
