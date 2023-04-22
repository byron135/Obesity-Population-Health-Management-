import pandas as pd

def filter_patients(df, age_threshold, gender, bmi_threshold):
    """
        Filter patients based on the age, gender, and bmi.

        :rtype: df
    """    
    filtered_df = df.query(f"age >= {age_threshold} and gender == '{gender}' and BMI >= {bmi_threshold}")
    return filtered_df

def filter_patients_race(df, age_threshold,race, bmi_threshold):

    filtered_df = df.query(f"race == '{race}' and BMI >= {bmi_threshold} and age >= {age_threshold}")

    return filtered_df

def filter_smoking_status(df, smoking_status, bmi_threshold):

    filtered_df = df.query(f"smoking_status == '{smoking_status}' and BMI >= {bmi_threshold}")

    return filtered_df