import aggregate
from datetime import datetime
import plot
import logging
import os

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)s [%(filename)s %(lineno)d]: %(message)s')

    try:
        chair_data = aggregate.get_chair_data()

        with open(f'historic/{datetime.now().isoformat()}-stef-fim.json', 'w') as f:
            f.write(aggregate.chair_data_to_json(chair_data))

        plot.plot_by_chair(chair_data)
        plot.plot_over_time()
    except Exception as e:
        logging.error(f'Failed to generate plots: {e}')
        os._exit(1)
