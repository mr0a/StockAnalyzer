from plugins import EMA, CPR


class StockAnalyzer:
    def __init__(self):
        self.plugins = []

    def register_plugin(self, plugin):
        self.plugins.append(plugin)

    def analyze(self, data):
        for plugin in self.plugins:
            result = plugin.calculate(data)
            print("Plugin:", type(plugin).__name__)
            print("Result:", result)
            print()
