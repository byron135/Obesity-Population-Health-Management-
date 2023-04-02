import json
from datetime import datetime

class FHIRDataHelper:
    def __init__(self, file_path):
        self.file_path = file_path
        with open(self.file_path) as f:
            data = f.read()
            self.fhir_obj = json.loads(data)

    def get_patient_name(self):
       
        """
        Perform getting patient name.

        :rtype: string
        """
        name = self.fhir_obj['entry'][0]['resource']['name'][0]
        full_name = name["given"][0] + " " + name["family"]
        return full_name

    def get_patient_age(self):
        """
        Perform getting patient age.

        :rtype: string
        """
        birthdate_str = self.fhir_obj['entry'][0]['resource']['birthDate']
        birthdate = datetime.fromisoformat(birthdate_str)
        
        # calculate the patient's age
        today = datetime.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        
        return age
    
    def get_patient_height(self):
        """
        Perform getting patient height.

        :rtype: string
        """
        height = None
        # loop through all Observation resources to find height readings
        for entry in self.fhir_obj['entry']:
            resource = entry['resource']
            if resource['resourceType'] == 'Observation' and resource['code']['coding'][0]['code'] == '8302-2':
                # extract height reading
                height = resource['valueQuantity']['value']
                # stop searching after finding the first height reading
                break
        height = str(height)+" cm"
        # return height reading
        return height
    
    def get_patient_weight(self):
        """
        Perform getting patient weight.

        :rtype: string
        """
        weight = None
        
        # loop through all Observation resources to find weight readings
        for entry in self.fhir_obj['entry']:
            resource = entry['resource']
            if resource['resourceType'] == 'Observation'and resource['code']['coding'][0]['code'] == '29463-7':
                # extract weight reading
                weight = resource['valueQuantity']['value']
                
                # stop searching after finding the first weight reading
                break
        weight = str(weight)+" kg"

        return weight
    
    def get_patient_glucose(self):
        """
        Perform getting patient glucose.

        :rtype: string
        """        
        glucose = None
        
        # loop through all Observation resources to find glucose readings
        for entry in self.fhir_obj['entry']:
            resource = entry['resource']
            if resource['resourceType'] == 'Observation'and resource['code']['coding'][0]['display'] == "Glucose":
                # extract weight reading
                glucose = resource['valueQuantity']['value']
                # stop searching after finding the first glucose reading
                break
        glucose = str(glucose)+" mg/dl"
        return glucose