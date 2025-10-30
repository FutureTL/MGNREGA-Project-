# import pandas as pd

# def preprocess_mgnrega_data(raw_data):
#     records = raw_data.get("records", [])
#     if not records:
#         return []

#     print(f"records", records)
#     df= pd.DataFrame(records)
#     print(f"df: {df}")
#     df = df.apply(pd.to_numeric, errors='ignore')
#     print(f"df after applying numeric: {df}")

#     numeric_cols= df.select_dtypes(include='number').columns
#     print(f"numeric cols: {numeric_cols}")

#     # if 'month' not in df.columns:
#     #     return df.to_dict(orient='records')
    
#     month_order= [
#         "Jan", "Feb", "March","April", "May", "June", "July", "Aug", "Sep",
#         "Oct", "Nov", "Dec"
#     ]
#     month_map = {m:i for i,m in enumerate(month_order)}
#     print(f"month map created :{month_map}")

#     df = df[df['month'].isin(month_order)]
#     print(f"the months present in data are: {df}")
    
#     aggregated = df.groupby('month', as_index=False)[numeric_cols].mean()
#     print(f"aggregated value for months: {aggregated}")

#     aggregated['month_order']= aggregated['month'].map(month_map)
#     aggregated = aggregated.sort_values('month_order', ascending=False).drop(columns=['month_order'])
#     return aggregated.to_dict(orient='records')


import pandas as pd

def preprocess_mgnrega_data(raw_data):
    records = raw_data.get("records", [])
    if not records:
        return {}

    df = pd.DataFrame(records)
    df = df.apply(pd.to_numeric, errors='ignore')

    numeric_cols = df.select_dtypes(include='number').columns

    # Ensure month column exists and is valid
    month_order = [
        "Jan", "Feb", "March", "April", "May", "June",
        "July", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]
    month_map = {m: i for i, m in enumerate(month_order)}
    df = df[df["month"].isin(month_order)]

    # Aggregate numeric data by month (mean for now)
    aggregated = df.groupby("month", as_index=False)[numeric_cols].mean()
    aggregated["month_order"] = aggregated["month"].map(month_map)
    aggregated = aggregated.sort_values("month_order", ascending=False).drop(columns=["month_order"])

    # Define categories
    categories = {
        "Employment & Labour": [
            "Total_Individuals_Worked",
            "Total_Households_Worked",
            "Average_days_of_employment_provided_per_Household",
            "Total_No_of_HHs_completed_100_Days_of_Wage_Employment",
            "Differently_abled_persons_worked",
            "Persondays_of_Central_Liability_so_far",
            
        ],
        "Wages & Expenditure": [
            "Approved_Labour_Budget",
            "Wages",
            "Average_Wage_rate_per_day_per_person",
            "Total_Exp",
            "Material_and_skilled_Wages",
            "Total_Adm_Expenditure",
            "percent_of_Expenditure_on_Agriculture_Allied_Works",
            "percent_of_NRM_Expenditure",
            "percentage_payments_gererated_within_15_days"
        ],
        "Works & Progress": [
            "Number_of_Ongoing_Works",
            "Number_of_Completed_Works",
            "Total_No_of_Works_Takenup",
            "Number_of_GPs_with_NIL_exp",
            "percent_of_Category_B_Works",
            "Total_No_of_Active_Workers",
            "Total_No_of_Active_Job_Cards",
            "Total_No_of_JobCards_issued",
            "Total_No_of_Workers",
            
        ],
        "Demographics & Inclusion": [
            "SC_persondays",
            "SC_workers_against_active_workers",
            "ST_persondays",
            "ST_workers_against_active_workers",
            "Women_Persondays",
        ]
    }

    # Prepare segregated data
    segregated_data = {}
    for category, cols in categories.items():
        valid_cols = ["month"] + [c for c in cols if c in aggregated.columns]
        segregated_data[category] = aggregated[valid_cols].to_dict(orient="records")

    return segregated_data
