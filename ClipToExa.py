import pandas as pd
from f2_utils.dbconnect.dbconnect import open_exaconnection
from f2_utils.sqlutils.sqlutils import write_table
from f2_utils.sqlutils.queryband import add_queryband


class ClipToExa(object):
    """ClipToExa allows you to bring your clipboard into table on exasol.
    But you may also use it for an ordinary DataFrame on the fly."""

    def __init__(self, tablename="tmp_clipboard_del7", dev_mode=False, df=None):
        super(ClipToExa, self).__init__()
        self.tablename = tablename
        # TODO: the constructor is too dirty -> refactor (e.g. spaghetti to functions)
        # TODO: Assure that input data is clean enough (test dirty inputs)
        if dev_mode:
            self.dataframe = self.dev_data()
        elif isinstance(df, pd.DataFrame):
            self.dataframe = df
        else:
            self.dataframe = pd.read_clipboard()
        self.cols = [self.string_cleaner(c) for c in self.dataframe.columns]
        self.dataframe.columns = self.cols
        print("Initiated the following DataFrame:", self.dataframe.head(), sep="\n")

    def dev_data(self):
        print("dev mode on")
        return pd.DataFrame(
            {
                "A Ha": 0.1,
                " B eta ": 1,
                "C": "foo",
                "D": pd.Timestamp("20010102"),
                "E": pd.Series([1.0] * 3).astype("float32"),
                "F": False,
                "G": pd.Series([1] * 3, dtype="int8"),
            }
        )

    def string_cleaner(self, string):
        for unwanted in [" ", "-"]:
            string = str(string).replace(unwanted, "_")
        return string

    def type_converter(self, df, col):
        if df[col].dtype == "datetime64[ns]":
            return "TIMESTAMP"
        elif df[col].dtype in ["float32", "float64"]:
            return "FLOAT"
        elif df[col].dtype in ["int8", "int64"]:
            return "BIGINT"
        elif df[col].dtype == "bool":
            return "BOOL"
        elif df[col].dtype == "object":
            return "CLOB"

    def py_dtypes_to_exa_dtypes(self):
        """Returns {'column': exa_dtype} e.g.: 'sid_forderung': 'BIGINT'"""
        exa_dtypes = {}
        for c in self.cols:
            exa_dtypes[c] = self.type_converter(self.dataframe, c)
        return exa_dtypes

    def create_sql_script(self):
        types = self.py_dtypes_to_exa_dtypes()
        sql = f"create or replace table abt_ds.{self.tablename} (\n"
        for col in self.cols:
            if col != self.cols[len(self.cols) - 1]:
                sql += f"    {col} {types[col]},\n"
            else:
                sql += f"    {col} {types[col]}\n)\n;"
        return sql

    def create_table(self, connection):
        sql = self.create_sql_script()
        connection.execute(add_queryband(sql))
        print(f"abt_ds.{self.tablename} has been created")

    def fill_table(self, connection):
        write_table(
            src=self.dataframe,
            connection=connection,
            schema="abt_ds",
            table=self.tablename,
        )
        print(f"abt_ds.{self.tablename} has been filled")

    def main(self):
        with open_exaconnection("exasol_prax") as conn:
            self.create_table(conn)
            self.fill_table(conn)
        print("Try", f"select * from abt_ds.{self.tablename};", sep="\n")


if __name__ == "__main__":
    cx = ClipToExa(tablename="Chat_del30", dev_mode=False)
    # sql = cx.create_sql_script()
    # print(sql)
    cx.main()
