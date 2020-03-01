import json
import math
import os


def bake_correlation_statistic(df, drops, correlation_func, output_file):

    if not os.path.exists(os.path.dirname(output_file)):
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

    statistic = {}

    progress = 0.0
    works = float(len(df.columns) * len(df.columns))

    progress_report = 2

    for x in df.columns:
        if x in drops:
            continue

        if statistic.get(x, None) is None:
            statistic[x] = {}

        for y in df.columns:
            if y in drops:
                continue

            tau, p_value = correlation_func(df, x, y)

            if math.isnan(tau) or math.isnan(p_value):
                pass

            progress += 1

            if progress % progress_report == 0:
                print("{}%.....".format(round((progress / works) * 100.0, 4)))

            statistic[x][y] = {
                "p": str(p_value),
                "tau": str(tau),
            }

    with open(output_file, "w") as f:
        json.dump(statistic, f, indent=2)
