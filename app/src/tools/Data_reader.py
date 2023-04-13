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
                #     "age"  : fhir_data.get_patient_age(),
                #     "race" : fhir_data.get_race(),
                #     "height" : fhir_data.get_patient_height(),
                #     "weight" : fhir_data.get_patient_weight(),
                #     "glucose" : fhir_data.get_patient_glucose(),
                #     "blood_pressure" : fhir_data.get_blood_pressure(),
                #     "BMI" : fhir_data.get_BMI(),
                #     "active medication" : fhir_data.get_active_medication()
                # }
                ###

                ### Get all needed information
                single_patient = fhir_data.get_all()
                return_data.append(single_patient)

        return return_data
        
# the example way to load all patient data into a array    
reader = JSONFolderReader("app/src/source")
reader.read_files()