from database.db import get_connection

def save_patient(full_name, age, gender):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO patients
    (full_name, age, gender)
    VALUES (%s, %s, %s)
    """

    values = (full_name, age, gender)

    cursor.execute(query, values)

    conn.commit()

    patient_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return patient_id