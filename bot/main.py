from __future__ import annotations

import asyncio
import logging
import sys

from bot.client import get_client
from bot.config import settings
from bot.portfolio import print_portfolio
from bot.strategies import ExampleScannerStrategy


def setup_logging() -> None:
    logging.basicConfig(
        level=getattr(logging, settings.log_level, logging.INFO),
        format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%H:%M:%S",
    )


async def main() -> None:
    setup_logging()
    log = logging.getLogger("bot")

    log.info("Starting Bayse Prediction Bot v0.1.0")
    log.info("Currency: %s | Dry-run: %s", settings.currency, settings.dry_run)

    if settings.dry_run:
        log.warning("DRY-RUN mode is ON – no real orders will be placed.")

    async with get_client() as client:
        await print_portfolio(client)
        strategy = ExampleScannerStrategy(client)
        await strategy.run()
        log.info("Done.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
        sys.exit(0)
    except Exception as e:
        logging.getLogger("bot").exception("Fatal error: %s", e)
        sys.exit(1)