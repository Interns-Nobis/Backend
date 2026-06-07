from pydantic import BaseModel


class CandidatePersonal(BaseModel):

    candidate_id: str

    first_name: str
    middle_name: str | None = None
    last_name: str

    date_of_birth: str

    email: str
    mobile_number: str

    mother_tongue: str

    present_address: str
    present_city: str
    present_state: str
    present_pincode: str

    permanent_address: str
    permanent_city: str
    permanent_state: str
    permanent_pincode: str

    bank_name: str
    branch: str
    ifsc_code: str
    account_number: str

    pan_number: str
    aadhaar_number: str

    passport_number: str | None = None
    citizenship: str | None = None

    emergency_contact_name: str
    emergency_contact_relation: str
    emergency_contact_mobile: str