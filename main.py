import asyncio
import argparse
import logging
from datetime import datetime

import aggregate
import plot


async def aggregate_chair_data():
    chair_data = await aggregate.get_chair_data()

    calendar_iso_date = datetime.now().strftime("%Y-%m-%d")
    with open(f"historic/{calendar_iso_date}-stef-fim.json", "w") as f:
        f.write(aggregate.chair_data_to_json(chair_data))

def plot_chair_data():
    plot.plot_by_chair()
    plot.plot_over_time()


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(levelname)s [%(filename)s %(lineno)d]: %(message)s"
    )

    parser = argparse.ArgumentParser("steffim")
    parser.add_argument(
        "mode", choices=["aggregate", "plot"], help="choose the mode to run", type=str
    )
    args = parser.parse_args()

    try:
        if args.mode == "aggregate":
            asyncio.run(aggregate_chair_data())
        elif args.mode == "plot":
            plot_chair_data()
    except Exception as e:
        logging.error(f"process failed: {e}")
        exit(1)
