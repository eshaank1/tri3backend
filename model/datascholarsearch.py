from sqlalchemy import Column, Integer, String
from __init__ import db

class Data(db.Model):
    __tablename__ = "data"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    city = Column(String)
    state = Column(String)
    zip = Column(String)
    school_url = Column(String)
    admission_rate = Column(String)
    average_sat = Column(String)
    address = Column(String)
    tuition_in_state = Column(String)
    tuition_out_of_state = Column(String)

    def __init__(self, name="null", city="null", state="null", zip_code="null", school_url="null", admission_rate="null", average_sat="null", address="null", tuition_in_state="null", tuition_out_of_state="null"):
        self.name = name
        self.city = city
        self.state = state
        self.zip = zip_code
        self.school_url = school_url
        self.admission_rate = admission_rate
        self.average_sat = average_sat
        self.address = address
        self.tuition_in_state = tuition_in_state
        self.tuition_out_of_state = tuition_out_of_state
    
    def __repr__(self):
        return f"id='{self.id}', name='{self.name}', city='{self.city}', state='{self.state}', zip='{self.zip}', school_url='{self.school_url}', admission_rate='{self.admission_rate}', average_sat='{self.average_sat}', address='{self.address}', tuition_in_state='{self.tuition_in_state}', tuition_out_of_state='{self.tuition_out_of_state}'"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "city": self.city,
            "state": self.state,
            "zip": self.zip,
            "school_url": self.school_url,
            "admission_rate": self.admission_rate,
            "average_sat": self.average_sat,
            "address": self.address,
            "tuition_in_state": self.tuition_in_state,
            "tuition_out_of_state": self.tuition_out_of_state
        }

def init_data():
    with open("data.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            college = eval(line)
            db.session.add(Data(name=college["Name"], city=college["City"], state=college["State"], zip_code=college["Zip"], school_url=college["School URL"], admission_rate=college["Admission Rate Overall"], average_sat=college["SAT Scores Average Overall"], address=college["Address"], tuition_in_state=college["Tuition (In-State)"], tuition_out_of_state=college["Tuition (Out-of-State)"]))
            
    db.session.commit()
