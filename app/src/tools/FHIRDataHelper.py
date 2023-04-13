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

        :rtype: tuple(list(value), str)
        """
        height = []
        # loop through all Observation resources to find height readings
        for entry in self.fhir_obj['entry']:
            resource = entry['resource']
            if resource['resourceType'] == 'Observation' and resource['code']['coding'][0]['code'] == '8302-2':
                # extract height reading
                height.append(str(resource['valueQuantity']['value']))
                # stop searching after finding the first height reading -> store all the height readings
        # return height reading
        return (height, "cm")
    
    def get_patient_weight(self):
        """
        Perform getting patient weight.

        :rtype: tuple(list(value), str)
        """
        weight = []
        
        # loop through all Observation resources to find weight readings
        for entry in self.fhir_obj['entry']:
            resource = entry['resource']
            if resource['resourceType'] == 'Observation'and resource['code']['coding'][0]['code'] == '29463-7':
                # extract weight reading
                weight.append(str(resource['valueQuantity']['value']))
                # stop searching after finding the first weight reading-> store all the weight readings
        return (weight, "kg")
    
    def get_patient_glucose(self):
        """
        Perform getting patient glucose.

        :rtype: tuple(list(value), str)
        """        
        glucose = []
        
        # loop through all Observation resources to find glucose readings
        for entry in self.fhir_obj['entry']:
            resource = entry['resource']
            if resource['resourceType'] == 'Observation'and resource['code']['coding'][0]['display'] == "Glucose":
                # extract weight reading
                glucose.append(str(resource['valueQuantity']['value']))
                # stop searching after finding the first glucose reading-> store all the glucose readings
        return (glucose, "mg/dl")

    def get_blood_pressure(self):
        """
        Perform getting patient blood pressure(low, high).

        :rtype: tuple(list(tuple(value, value)), str)
        """    
        # Extract blood pressure observations
        blood_pressure = []

        # loop through all Observation resources to find blood pressure readings
        for entry in self.fhir_obj['entry']:
            resource = entry['resource']
            if resource['resourceType'] == 'Observation'and resource['code']['coding'][0]['code'] == "55284-4":
                # extract weight reading
                blood_pressure.append((str(resource['component'][0]['valueQuantity']['value']), str(resource['component'][1]['valueQuantity']['value'])))

        return (blood_pressure, "mmHg")

    def get_BMI(self):
        """
        Perform getting patient BMI.

        :rtype: tuple(list(value), str)
        """    
        # Extract blood pressure observations
        bmi = []

        # loop through all Observation resources to find blood pressure readings
        for entry in self.fhir_obj['entry']:
            resource = entry['resource']
            if resource['resourceType'] == 'Observation'and resource['code']['coding'][0]['code'] == "39156-5":
                # extract weight reading
                bmi.append(str(resource['valueQuantity']['value']))

        return (bmi, "kg/m2")

    def get_race(self):
       
        """
        Perform getting patient race.

        :rtype: (string, string)
        """
        race1 = self.fhir_obj['entry'][0]['resource']['extension'][0]['extension'][1]['valueString']
        race2 = self.fhir_obj['entry'][0]['resource']['extension'][1]['extension'][1]['valueString']
        return (race1, race2)

    def get_active_medication(self):
        """
        Perform getting patient active medication.

        :rtype: list(string)
        """    
        # Extract blood pressure observations
        medications = []

        # loop through all Observation resources to find blood pressure readings
        for entry in self.fhir_obj['entry']:
            resource = entry['resource']
            if resource['resourceType'] == 'MedicationRequest' and resource['status'] == "active":
                # extract weight reading
                medications.append(resource['medicationCodeableConcept']['text'])

        return medications
    
    def get_all(self):
        """
        Perform getting all patient needed information.

        :rtype: dict
        """    
        name = self.get_patient_name()
        age = self.get_patient_age()
        race = self.get_race()
        height = []
        weight = []
        glucose = []
        bmi = []
        blood_pressure = []
        medications = []
        # loop to get other information
        for entry in self.fhir_obj['entry']:
            resource = entry['resource']
            if resource['resourceType'] == 'Observation' and resource['code']['coding'][0]['code'] == '8302-2':
                height.append(str(resource['valueQuantity']['value']))
            elif resource['resourceType'] == 'Observation'and resource['code']['coding'][0]['code'] == '29463-7':
                weight.append(str(resource['valueQuantity']['value']))
            elif resource['resourceType'] == 'Observation'and resource['code']['coding'][0]['display'] == "Glucose":
                glucose.append(str(resource['valueQuantity']['value']))
            elif resource['resourceType'] == 'Observation'and resource['code']['coding'][0]['code'] == "55284-4":
                blood_pressure.append((str(resource['component'][0]['valueQuantity']['value']), str(resource['component'][1]['valueQuantity']['value'])))
            elif resource['resourceType'] == 'Observation'and resource['code']['coding'][0]['code'] == "39156-5":
                bmi.append(str(resource['valueQuantity']['value']))
            elif resource['resourceType'] == 'MedicationRequest' and resource['status'] == "active":
                medications.append(resource['medicationCodeableConcept']['text'])
        return {
                    "name" : name,
                    "age"  : age,
                    "race" : race,
                    "height" : (height, "cm"),
                    "weight" : (weight, "kg"),
                    "glucose" : (glucose, "mg/dl"),
                    "blood_pressure" : (blood_pressure, "mmHg"),
                    "BMI" : (bmi, "kg/m2"),
                    "active_medication" : medications
                }
    def get_latest(self):
        """
        Perform getting all latest patient needed information.

        :rtype: dict
        """    
        patient_info = self.get_all()
        return {
                    "name" : patient_info['name'],
                    "age"  : patient_info['age'],
                    "race" : patient_info['race'],
                    "height" : (patient_info['height'][0][-1] if len(patient_info['height'][0]) > 0 else '', "cm"),
                    "weight" : (patient_info['weight'][0][-1] if len(patient_info['weight'][0]) > 0 else '', "kg"),
                    "glucose" : (patient_info['glucose'][0][-1] if len(patient_info['glucose'][0]) > 0 else '', "mg/dl"),
                    "blood_pressure" : (patient_info['blood_pressure'][0][-1] if len(patient_info['blood_pressure'][0]) > 0 else '', "mmHg"),
                    "BMI" : (patient_info['BMI'][0][-1] if len(patient_info['BMI'][0]) > 0 else '', "kg/m2"),
                    "active_medication" : patient_info['active_medication']
                }