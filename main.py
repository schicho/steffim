import aggregate
from datetime import datetime
import plot

if __name__ == '__main__':
    chair_data = aggregate.get_chair_data()

    with open(f'{datetime.now().isoformat()}-stef-chair.json', 'w') as f:
        f.write(aggregate.chair_data_to_json(chair_data))

    plot.plot_by_chair(chair_data)
