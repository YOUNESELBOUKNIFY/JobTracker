# job_scraper/utils/in_memory_pipeline.py
import pandas as pd

class PandasPipeline:
    def __init__(self):
        self.items = []

    def process_item(self, item, spider):
        self.items.append(item)
        return item

    def get_dataframe(self):
        return pd.DataFrame(self.items)
