from __future__ import annotations

import logging
from typing import Any, Optional

from bayse_markets import BayseClient
from bot.config import settings

logger = logging.getLogger(__name__)


async def get_quote(client, *, event_id, market_id, outcome_id, side="BUY", amount, currency=None):
    currency = currency or settings.currency
    return await client.get_quote(
        event_id=event_id,
        market_id=market_id,
        side=side.upper(),
        outcome_id=outcome_id,
        amount=amount,
        currency=currency,
    )


async def buy(client, *, event_id, market_id, outcome_id, amount, price=None, order_type="MARKET", currency=None):
    currency = currency or settings.currency

    if settings.dry_run:
        logger.warning("[DRY-RUN] Would BUY %.2f %s of %s", amount, currency, outcome_id)
        return await get_quote(client, event_id=event_id, market_id=market_id,
                               outcome_id=outcome_id, side="BUY", amount=amount, currency=currency)

    return await client.buy(
        event_id=event_id,
        market_id=market_id,
        outcome_id=outcome_id,
        amount=amount,
        order_type=order_type,
        price=price,
        currency=currency,
    )


async def sell(client, *, outcome_id, shares, event_id=None, market_id=None, price=None, order_type="MARKET", currency=None):
    currency = currency or settings.currency

    if settings.dry_run:
        logger.warning("[DRY-RUN] Would SELL %.4f shares of %s", shares, outcome_id)
        return {"dry_run": True}

    kwargs = {
        "outcome_id": outcome_id,
        "shares": shares,
        "currency": currency,
        "order_type": order_type,
    }
    if event_id:
        kwargs["event_id"] = event_id
    if market_id:
        kwargs["market_id"] = market_id
    if price is not None:
        kwargs["price"] = price

    return await client.sell(**kwargs)