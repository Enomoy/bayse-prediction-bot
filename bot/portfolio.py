from __future__ import annotations

import logging
from bayse_markets import BayseClient

logger = logging.getLogger(__name__)


async def print_portfolio(client: BayseClient) -> None:
    try:
        port = await client.get_portfolio()
        data = port.data

        print("\n" + "="*60)
        print("Portfolio".center(60))
        print("="*60)

        value = getattr(data, "portfolio_current_value", None) or getattr(data, "current_value", "?")
        print(f"Current value: {value}")

        balances = (
            getattr(data, "outcome_balances", None)
            or getattr(data, "positions", None)
            or getattr(data, "balances", [])
            or []
        )

        if not balances:
            print("No open positions.")
            return

        for bal in balances:
            title = getattr(getattr(bal, "market", None), "title", None) or getattr(bal, "title", "?")
            outcome = getattr(bal, "outcome", None) or getattr(bal, "outcome_label", "?")
            qty = getattr(bal, "balance", None) or getattr(bal, "shares", None) or getattr(bal, "quantity", "?")
            print(f"  • {title} [{outcome}]  qty={qty}")

    except Exception as e:
        print(f"Could not load portfolio: {e}")