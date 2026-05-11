class DatasetRegistry:

    datasets = {}

    @classmethod
    def register_dataset(cls, name, dataframe):

        cls.datasets[name] = dataframe

    @classmethod
    def get_dataset(cls, name):

        return cls.datasets.get(name)

    @classmethod
    def list_datasets(cls):

        return list(cls.datasets.keys())