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
                single_patient = {
                    "name" : fhir_data.get_patient_name(),
                    "age"  : fhir_data.get_patient_age(),
                    "height" : fhir_data.get_patient_height(),
                    "weight" : fhir_data.get_patient_weight(),
                    "glucose" : fhir_data.get_patient_glucose()
                }
                return_data.append(single_patient)
                
        print(return_data)

        return return_data
        
# the example way to load all patient data into a array    
# reader = JSONFolderReader("source")
# reader.read_files()