import pandas as pd
import plotly.express as px

# načítanie CSV
df = pd.read_csv("csu_data.csv", sep=";")

# print(df.head())

# filter
df = df[
    (df["Ukazatel"] == "Počet hostů") &
    (df["Rezidence"] == "Celkem")
]

# graf
fig = px.bar(
    df,
    x="ČR, Reg. soudržnosti, Kraje",
    y="Hodnota",
    title="Počet hostů podľa krajov (2024)"
)

fig.show()