import pandas

# Dataframe info

df = pandas.read_csv(
    "sample.csv",
    dtype={"user": "object"},
    parse_dates=["datetime"])

print(df.info(memory_usage="deep"))

# Time since previous transaction for each user

grouped = df[["user", "datetime"]].sort_values(by="datetime").groupby("user")
df["previous_datetime"] = df["datetime"] - grouped["datetime"].shift(1)

# Transactions within the past hour for each user

def hour_indices(s):
    hour = pandas.Timedelta(hours=1)
    for datetime in s:
        valid = s.between(datetime - hour, datetime, inclusive=False)
        yield s[valid].index

def hour_count(s):
    for indices in hour_indices(s):
        yield indices.size

def hour_sum(s):
    for indices in hour_indices(s):
        yield sum(df["amount"][indices])

grouped = df[["user", "datetime"]].sort_values(by="datetime").groupby("user")
df["hour_count"] = grouped["datetime"].transform(hour_count)
df["hour_sum"] = grouped["datetime"].transform(hour_sum)

print(df.sort_values(by="datetime"))

# Totals for each user

def totals(df):
    total = df[["user", "amount"]].groupby("user")["amount"].transform("sum").rename("total")
    count = df[["user"]].groupby("user")["user"].transform("count").rename("count")
    df = pandas.concat([df["user"], total, count], axis=1)
    df = df.drop_duplicates().sort_values(by="user").reset_index(drop=True)
    return df

print(totals(df))
