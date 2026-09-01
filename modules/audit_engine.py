import pandas as pd
from pathlib import Path
from datetime import datetime

LOG_FILE = Path("audit_log.csv")

def write_log(activity, dataset_name, records):

    row = pd.DataFrame([{
        "timestamp": datetime.now(),
        "activity": activity,
        "dataset": dataset_name,
        "records": records
    }])

    if LOG_FILE.exists():
        row.to_csv(LOG_FILE, mode="a", index=False, header=False)
    else:
        row.to_csv(LOG_FILE, index=False)

def read_logs():

    if LOG_FILE.exists():
        return pd.read_csv(LOG_FILE)

    return pd.DataFrame(
        columns=["timestamp","activity","dataset","records"]
    )