'''
This class is written to track the persons
detected by the detection model so as to enable
counting of the persons.
'''

class trackPerson:
    def __init__(self,personID,centroid):
        # save the person's identification
        self.personID = personID
        # using the peron's centroid
        self.centroids = [centroid]
        
        # a boolean to indicate if counted
        self.counted = False