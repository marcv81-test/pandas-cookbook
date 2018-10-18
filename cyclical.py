import math
import matplotlib
import pandas

# Cyclical day

df = pandas.read_csv("cyclical-day.csv", parse_dates=["datetime"])

def day_ratio(s):
    day = pandas.Timedelta(days=1)
    return (s - pandas.to_datetime(s.dt.date)) / day

angle = 2 * math.pi * day_ratio(df["datetime"])
df["day_x"] = angle.apply(math.cos)
df["day_y"] = angle.apply(math.sin)

df.plot.scatter("day_x", "day_y").set_aspect('equal')
matplotlib.pyplot.show()

# Cyclical week

df = pandas.read_csv("cyclical-week.csv", parse_dates=["datetime"])

def week_ratio(s):
    return (s.dt.dayofweek + day_ratio(s)) / 7

angle = 2 * math.pi * week_ratio(df["datetime"])
df["week_x"] = angle.apply(math.cos)
df["week_y"] = angle.apply(math.sin)

df.plot.scatter("week_x", "week_y").set_aspect('equal')
matplotlib.pyplot.show()

# Cyclical month

df = pandas.read_csv("cyclical-month.csv", parse_dates=["datetime"])

def month_ratio(s):
    return (s.dt.day - 1 + day_ratio(s)) / s.dt.daysinmonth

angle = 2 * math.pi * month_ratio(df["datetime"])
df["month_x"] = angle.apply(math.cos)
df["month_y"] = angle.apply(math.sin)

df.plot.scatter("month_x", "month_y").set_aspect('equal')
matplotlib.pyplot.show()

# Cyclical year

df = pandas.read_csv("cyclical-year.csv", parse_dates=["datetime"])

def year_ratio(s):
    return (s.dt.month - 1 + month_ratio(s)) / 12

angle = 2 * math.pi * year_ratio(df["datetime"])
df["year_x"] = angle.apply(math.cos)
df["year_y"] = angle.apply(math.sin)

# The 15th day is not the exact middle of each month: slightly irregular
df.plot.scatter("year_x", "year_y").set_aspect('equal')
matplotlib.pyplot.show()
