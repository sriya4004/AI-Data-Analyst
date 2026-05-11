import duckdb


class DuckDBTool:

    def __init__(self):

        self.connection = duckdb.connect(database=':memory:')

    def register_dataframe(self, table_name, dataframe):

        self.connection.register(table_name, dataframe)

    def run_query(self, query):

        result = self.connection.execute(query).fetchdf()

        return result.to_dict(orient="records")