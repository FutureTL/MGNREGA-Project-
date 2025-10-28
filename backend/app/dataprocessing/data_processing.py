import pandas as pd

def preprocess_mgnrega_data(raw_data):
    records = raw_data.get("records", [])
    if not records:
        return []

    print(f"records", records)
    df= pd.DataFrame(records)
    print(f"df: {df}")
    df = df.apply(pd.to_numeric, errors='ignore')
    print(f"df after applying numeric: {df}")

    numeric_cols= df.select_dtypes(include='number').columns
    print(f"numeric cols: {numeric_cols}")

    # if 'month' not in df.columns:
    #     return df.to_dict(orient='records')
    
    month_order= [
        "Jan", "Feb", "March","April", "May", "June", "July", "Aug", "Sep",
        "Oct", "Nov", "Dec"
    ]
    month_map = {m:i for i,m in enumerate(month_order)}
    print(f"month map created :{month_map}")

    df = df[df['month'].isin(month_order)]
    print(f"the months present in data are: {df}")
    
    aggregated = df.groupby('month', as_index=False)[numeric_cols].mean()
    print(f"aggregated value for months: {aggregated}")

    aggregated['month_order']= aggregated['month'].map(month_map)
    aggregated = aggregated.sort_values('month_order', ascending=False).drop(columns=['month_order'])
    return aggregated.to_dict(orient='records')
