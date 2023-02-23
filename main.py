import aggregate
import plot

if __name__ == '__main__':
    chair_data = aggregate.get_chair_data()
    plot.plot_by_chair(chair_data)
