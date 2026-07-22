
def get_patient(conn,patient_id):
    cursor=conn.cursor()
    cursor.execute("select * from patients where id =%s",(patient_id,))
    patient=cursor.fetchone()
    cursor.close()
    return patient

def get_all_patients(conn):
    cursor=conn.cursor(dictionary=True)
    cursor.execute("select*from patients")
    patients=cursor.fetchall()
    cursor.close()
    return patients

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