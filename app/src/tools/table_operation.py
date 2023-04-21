import pandas as pd

def filter_patients(df, age_threshold, gender, bmi_threshold):
    """
        Filter patients based on the age, gender, and bmi.

        :rtype: df
    """    
    filtered_df = df.query(f"age >= {age_threshold} and gender == '{gender}' and BMI >= {bmi_threshold}")
    return filtered_df