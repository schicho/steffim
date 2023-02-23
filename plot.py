import matplotlib.pyplot as plt

def plot_by_chair(chair_data):
    # leave out chairs with no stef
    chair_data = [chair for chair in chair_data if chair.stef_stats()[1] > 0]

    # get the names and number of stef
    names = [chair.stef_stats()[0]  for chair in chair_data]
    stef = [chair.stef_stats()[1] for chair in chair_data]

    # plot the data
    plt.bar(names, stef)
    plt.show()
