from FHIRDataHelper import FHIRDataHelper
import os
import json


class JSONFolderReader:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def read_files(self):

        return_data = []
        for filename in os.listdir(self.folder_path):
            if filename.endswith('.json'):
                file_path = os.path.join(self.folder_path, filename)
                fhir_data = FHIRDataHelper(file_path)

                ### Template for extracting specific information
                # single_patient = {
                #     "name" : fhir_data.get_patient_name(),
                #     "driver_license" : fhir_date.get_driver_license(),
                #     "age"  : fhir_data.get_patient_age(),
                #     "ssn" : fhir_data.get_patient_SSN(),
                #     "driver_license" : fhir_data.get_patient_driver_license(),
                #     "gender" : fhir_data.get_patient_gender(),
                #     "race" : fhir_data.get_race(),
                #     "height" : fhir_data.get_patient_height(),
                #     "weight" : fhir_data.get_patient_weight(),
                #     "glucose" : fhir_data.get_patient_glucose(),
                #     "blood_pressure" : fhir_data.get_blood_pressure(),
                #     "BMI" : fhir_data.get_BMI(),
                #     "smoking_status" : fhir_data.get_smoking_status(),
                #     "active_medication" : fhir_data.get_active_medication()
                # }
                ###

                ### Get all needed information for all the visit records
                # single_patient = fhir_data.get_all()

                ### Get only the latest visit records related information
                single_patient = fhir_data.get_latest()

                return_data.append(single_patient)
        return return_data
        
# the example way to load all patient data into a array    
reader = JSONFolderReader("app/src/source")