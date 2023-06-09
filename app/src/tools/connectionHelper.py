import pymssql
import csv


#from Data_reader import JSONFolderReader
# from . import table_operation as to
import pandas as pd

server = 'health6440server.database.windows.net'
database = 'fhir_6440'
username = 'byron135'
password = 'Cs6440asd'
connection = pymssql.connect(server, username, password, database)
cursor = connection.cursor()

# DO NOT CALL - SERVER SIDE USE ONLY
def table_import(cursor, table_name, data):
    for item in data:
        cursor.execute(f"""
            MERGE INTO {table_name} AS target
            USING (VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)) AS source (SSN, FullName, age, driver_license, gender, race, height, pweight, glucose, high_blood_pressure, low_blood_pressure, BMI, smoking_status, active_medication)
            ON target.SSN = source.SSN
            WHEN MATCHED THEN 
                UPDATE SET FullName = source.FullName, age = source.age, driver_license = source.driver_license, gender = source.gender, race = source.race, height = source.height, pweight = source.pweight, glucose = source.glucose, high_blood_pressure = source.high_blood_pressure, low_blood_pressure = source.low_blood_pressure, BMI = source.BMI, smoking_status = source.smoking_status, active_medication = source.active_medication
            WHEN NOT MATCHED THEN
                INSERT (SSN, FullName, age, driver_license, gender, race, height, pweight, glucose, high_blood_pressure, low_blood_pressure, BMI, smoking_status, active_medication)
                VALUES (source.SSN, source.FullName, source.age, source.driver_license, source.gender, source.race, source.height, source.pweight, source.glucose, source.high_blood_pressure, source.low_blood_pressure, source.BMI, source.smoking_status, source.active_medication);
        """, (item['ssn'], item['name'], item['age'], item['driver_license'], item['gender'], item['race'][0], item['height'][0], item['weight'][0], item['glucose'][0], item['blood_pressure'][0][1], item['blood_pressure'][0][0], item['BMI'][0], item['smoking_status'], item['active_medication']))
    connection.commit()
# reader = JSONFolderReader("app/src/source")
# data = reader.read_files()
# table_import(cursor, 'patient', data)
# print("done")
# DO NOT CALL - SERVER SIDE USE ONLY


def data_import(df, csv_filename, cursor, table_name, item):
    # Append item to the DataFrame
    new_row = pd.Series(item)
    df = df.append(new_row, ignore_index=True)

    # Append item to the CSV file
    with open(csv_filename, 'a') as f:
        f.write(','.join(map(str, item.values())) + '\n')

    # Insert or update item in the SQL table
    cursor.execute(f"""
        MERGE INTO {table_name} AS target
        USING (VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)) AS source (SSN, FullName, age, driver_license, gender, race, height, pweight, glucose, high_blood_pressure, low_blood_pressure, BMI, active_medication)
        ON target.SSN = source.SSN
        WHEN MATCHED THEN 
            UPDATE SET FullName = source.FullName, age = source.age, driver_license = source.driver_license, gender = source.gender, race = source.race, height = source.height, pweight = source.pweight, glucose = source.glucose, high_blood_pressure = source.high_blood_pressure, low_blood_pressure = source.low_blood_pressure, BMI = source.BMI, active_medication = source.active_medication
        WHEN NOT MATCHED THEN
            INSERT (SSN, FullName, age, driver_license, gender, race, height, pweight, glucose, high_blood_pressure, low_blood_pressure, BMI, active_medication)
            VALUES (source.SSN, source.FullName, source.age, source.driver_license, source.gender, source.race, source.height, source.pweight, source.glucose, source.high_blood_pressure, source.low_blood_pressure, source.BMI, source.active_medication);
    """, (item['ssn'], item['name'], item['age'], item['driver_license'], item['gender'], item['race'], item['height'], item['weight'], item['glucose'], item['blood_pressure'][1], item['blood_pressure'][0], item['BMI'], item['active_medication']))
    connection.commit()

    return df

def save_to_csv(columns, data, output_filename):
    with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(columns)
        for row in data:
            writer.writerow(row)


def get_columns(cursor, table_name):
    cursor.execute("""
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = %s
        ORDER BY ORDINAL_POSITION
    """, (table_name,))
    columns = [row[0] for row in cursor.fetchall()]
    return columns

def generate_insert_statements(table_name, columns, data):
    insert_statements = []
    for row in data:
        values = ', '.join("'{}'".format(str(value).replace("'", "''")) for value in row)
        insert_statement = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({values});"
        insert_statements.append(insert_statement)
    return insert_statements

def get_df_from_csv(csv_file):
    df = pd.read_csv(csv_file)
    return df

def convert_to_csv(df, csv_file):
    df.to_csv(csv_file, index=False)

def get_csv_from_server(cursor, table_name):
    # Modify the SELECT statement to exclude the specified columns
    cursor.execute(f"""
        SELECT age, gender, race, height, pweight, glucose, high_blood_pressure, low_blood_pressure, BMI, active_medication
        FROM {table_name}
    """)
    data = cursor.fetchall()
    
    # Update the columns list to match the selected columns
    columns = ['age', 'gender', 'race', 'height', 'pweight', 'glucose', 'high_blood_pressure', 'low_blood_pressure', 'BMI', 'active_medication']
    save_to_csv(columns, data, table_name + '.csv')


def init():
    get_csv_from_server(cursor, 'patient')


### procedure ###
init()
# df = get_df_from_csv('patient.csv')

# # Then we can do filtering on the df and then use convert_to_csv to get desired csv
# # TODO
# # some filtering method

# #example
# df = to.filter_patients(df, 50, 'female', '25')


# # after save to output.csv
# convert_to_csv(df, 'output.csv')