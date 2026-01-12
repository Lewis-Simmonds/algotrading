# Logic to show result from backtest

import matplotlib.pyplot as plt

def show_results(results):
    results['total'].plot()
    plt.show()