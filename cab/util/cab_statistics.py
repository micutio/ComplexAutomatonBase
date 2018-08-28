"""
Statistics module that is supposed to allow printing pre-defined
or customized stats about the simulation in matplotlib graphs.
TODO: Finish implementation. This is still old outdated code that should serve as inspiration only.
"""


import matplotlib.pyplot as plt
plt.xkcd()

__author__ = 'Michael Wagner'
__version__ = '1.0'


class Statistics:
    """
    This class records and outputs statistics about the sugarscape.
    """
    # TODO: Figure out how to make the data input and graph generation generic.
    # What might we want to plot?
    # - values over time
    # - averaged values over time
    # - multiple series in one graph
    # - time either every tick or every n ticks

    def __init__(self, abm, ca, gc):
        """r
        Initializes the Statistics class.
        """
        self.abm = abm
        self.ca = ca
        self.gc = gc
        # Variables to record

    def update_records(self):
        """
        Should be called every tick. Accumulate the desired data and
        store it into the respective data structures.
        """
        pass

    def plot(self):
        """
        Plots all available data in figures.
        """
        plt.title("Sugarscape Information")

        generations = len(self.pop_per_gen)
        gen_line = range(generations)
        pop_graph = plt.subplot(2, 2, 1)
        pop_graph.plot(gen_line, self.pop_per_gen, color="#F0F050", linewidth=1, label="total population")
        pop_graph.plot(gen_line, self.male_per_gen, color="#0000FF", linewidth=1, label="male population")
        pop_graph.plot(gen_line, self.female_per_gen, color="#FF0090", linewidth=1, label="female population")
        for i in range(self.gc.NUM_TRIBES):
            rgb = self.gc.TRIBE_COLORS[i]
            color = '#%02x%02x%02x' % (rgb[0], rgb[1], rgb[2])
            tribe_name = "tribe " + str(i)
            pop_graph.plot(gen_line, self.tribes[i], "-", color=color, linewidth=1, label=tribe_name)
        pop_graph.legend(loc="upper right", fontsize=9)
        plt.ylabel("population and tribes")
        # pop_graph.grid()  # deactivate if using xkcd()
        # pop_graph.legend(("total pop", "male pop", "female pop", "tribes"), loc=7)

        resource_graph = plt.subplot(2, 2, 2)
        resource_graph.plot(gen_line, self.total_sugar, color="#90FF90", linewidth=1, label="available sugar")
        resource_graph.plot(gen_line, self.total_spice, color="#FF9090", linewidth=1, label="available spice")
        resource_graph.legend(loc="upper right", fontsize=9)
        plt.ylabel("resources")
        # resource_graph.grid()  # deactivate if using xkcd()
        # resource_graph.legend(("total sugar", "total spice"), loc=7)

        production_graph = plt.subplot(2, 2, 3)
        if generations > 200:
            n = int(generations / 100)
            time_line = gen_line[0::n]
            prod_sugar_line = self.produced_sugar[0::n]
            trade_sugar_line = self.traded_sugar[0::n]
            prod_spice_line = self.produced_spice[0::n]
            trade_spice_line = self.traded_spice[0::n]
            production_graph.plot(time_line, prod_sugar_line, "-", color="#00FF00", linewidth=1, label="sugar harvested")
            production_graph.plot(time_line, trade_sugar_line, "--", color="#00FF00", linewidth=1, label="sugar traded")
            production_graph.plot(time_line, prod_spice_line, "-", color="#FF0000", linewidth=1, label="spice harvested")
            production_graph.plot(time_line, trade_spice_line, "--", color="#FF0000", linewidth=1, label="spice traded")
        else:
            production_graph.plot(gen_line, self.produced_sugar, "-", color="#00FF00", linewidth=1, label="sugar harvested")
            production_graph.plot(gen_line, self.traded_sugar, "--", color="#00FF00", linewidth=1, label="sugar traded")
            production_graph.plot(gen_line, self.produced_spice, "-", color="#FF0000", linewidth=1, label="spice harvested")
            production_graph.plot(gen_line, self.traded_spice, "--", color="#FF0000", linewidth=1, label="spice traded")
        production_graph.legend(loc="upper right", fontsize=9)
        plt.ylabel("foraging (dotted) and trade (dashed)")
        # production_graph.grid()  # deactivate if using xkcd()

        market_graph = plt.subplot(2, 2, 4)
        # Test: do not plot more than 100 data points
        if generations > 200:
            n = int(generations / 100)
            trade_line = gen_line[0::n]
            sugar_line = self.sugar_price[0::n]
            spice_line = self.spice_price[0::n]
            print("trade_line: %i" % len(trade_line))
            print("sugar_line: %i" % len(sugar_line))
            print("spice_line: %i" % len(spice_line))
            market_graph.plot(trade_line, sugar_line, color="#00FF00", linewidth=1, label="price of sugar")
            market_graph.plot(trade_line, spice_line, color="#FF0000", linewidth=1, label="price of spice")
        else:
            market_graph.plot(gen_line, self.sugar_price, color="#00FF00", linewidth=1, label="price of sugar")
            market_graph.plot(gen_line, self.spice_price, color="#FF0000", linewidth=1, label="price of spice")
        market_graph.legend(loc="upper right", fontsize=9)
        plt.ylabel("market prices")
        # market_graph.grid()  # deactivate if using xkcd()

        plt.show()
