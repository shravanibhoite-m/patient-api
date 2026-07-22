#get a patient info by id
def get_patient(conn,patient_id):
    cursor=conn.cursor(dictionary=True)
    cursor.execute("select * from patients where id =%s",(patient_id,))
    patient=cursor.fetchone()
    cursor.close()
    return patient
#get all patients from db
def get_all_patients(conn):
    cursor=conn.cursor(dictionary=True)
    cursor.execute("select*from patients")
    patients=cursor.fetchall()
    cursor.close()
    return patients
# add new patient
def create_patient(conn, patient: dict):
    cursor = conn.cursor()
    insert_values = """
        INSERT INTO patients (name, age, gender, email, phone_num, password, active, blood_group, emergency_contact, city, pincode)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_values, (
        patient["name"],
        patient["age"],
        patient["gender"],
        patient["email"],
        patient["phone_num"],
        patient["password"],
        patient["active"],
        patient["blood_group"],
        patient["emergency_contact"],
        patient["city"],
        patient["pincode"]
    ))
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    return new_id
#update patient resource
def updated_patient_resource(conn,patient_id,patient):
    cursor=conn.cursor()
    update_query="""UPDATE patients SET name=%s,age=%s,gender=%s,email=%s,phone_num=%s,password=%s,active=%s,blood_group=%s,emergency_contact=%s,city=%s,pincode=%s WHERE id=%s """
    values = (patient.name, patient.age, patient.gender, patient.email, patient.phone_num,
          patient.password, patient.active, patient.blood_group, patient.emergency_contact,
          patient.city, patient.pincode, patient_id)
    cursor.execute(update_query,values)
    conn.commit()
    rows_affected=cursor.rowcount
    cursor.close()
    return rows_affected
#update patient field
def update_patient_record(conn,patient_id,updated_data):
    existing_data=get_patient(conn,patient_id)
    if existing_data is None:
        return None
    existing_data.update(updated_data)
    cursor=conn.cursor()
    query="""UPDATE patients SET name=%s,age=%s,gender=%s,email=%s,phone_num=%s,password=%s,active=%s,blood_group=%s,emergency_contact=%s,city=%s,pincode=%s WHERE id=%s """
    values=(existing_data["name"],existing_data["age"],existing_data["gender"],existing_data["email"],existing_data["phone_num"],existing_data["password"],existing_data["active"],existing_data["blood_group"],existing_data["emergency_contact"],existing_data["city"],existing_data["pincode"],patient_id)
    cursor.execute(query,values)
    conn.commit()
    cursor.close()
    return get_patient(conn,patient_id)
#delete patient resource
def delete_patient(conn,patient_id):
    cursor=conn.cursor()
    cursor.execute("DELETE FROM patients WHERE id=%s",(patient_id,))
    conn.commit()
    rows_affected=cursor.rowcount
    cursor.close()
    return rows_affected