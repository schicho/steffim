import matplotlib.pyplot as plt

def plot_by_chair(chair_data):
    _plot_by_chair(chair_data)


def _plot_by_chair(chair_data):
    fig, ax = plt.subplots(figsize=(10, 10), constrained_layout=True)

    plt.xticks(rotation=90)

    ax.set_title('Stef by Chair')
    ax.set_xlabel('Chair')
    ax.set_ylabel('Stef')

    # force integer y-axis
    ax.yaxis.get_major_locator().set_params(integer=True)
    ax.xaxis.get_major_locator().set_params(integer=True)

    # leave out empty chairs
    chair_data = [chair for chair in chair_data if len(chair._stef) > 0]

    chair_names = [chair.name for chair in chair_data]
    stef_counts = [len(chair._stef) for chair in chair_data]

    rects = ax.bar(chair_names, stef_counts)
    ax.bar_label(rects, [f'{count}' for count in stef_counts], padding=-32, fontweight='bold')
    

    plt.show()
