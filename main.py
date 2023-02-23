import aggregate
import plot

if __name__ == '__main__':
    chair_data = aggregate.get_chair_data()
    
    with open('data.json', 'w') as f:
        f.write(aggregate.chair_data_to_json(chair_data))

    plot.plot_by_chair(chair_data)
