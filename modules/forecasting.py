import pandas as pd
from sklearn.linear_model import LinearRegression


def workforce_forecast(df):

    monthly = (
        df.groupby(["Joining_Year", "Joining_Month"])
        .size()
        .reset_index(name="New_Joiners")
    )

    monthly["Month_Index"] = range(len(monthly))

    model = LinearRegression()

    X = monthly[["Month_Index"]]
    y = monthly["New_Joiners"]

    model.fit(X, y)

    future_index = pd.DataFrame({
        "Month_Index": range(
            len(monthly),
            len(monthly) + 6
        )
    })

    prediction = model.predict(future_index)

    future_index["Forecast_New_Joiners"] = prediction.round().astype(int)

    future_index["Forecast_Month"] = [
        f"Month {i}"
        for i in range(1, 7)
    ]

    return monthly, future_index