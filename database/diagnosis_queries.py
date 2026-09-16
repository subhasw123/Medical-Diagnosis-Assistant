from database.db import get_connection


def save_patient(full_name, age, gender, user_id=None):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO patients
    (full_name, age, gender, user_id)
    VALUES (%s,%s,%s,%s)
    """

    cursor.execute(
        query,
        (full_name, age, gender, user_id)
    )

    conn.commit()

    patient_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return patient_id


def save_diagnosis(
    patient_id,
    disease,
    confidence,
    advice=""
):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO diagnoses
    (
        patient_id,
        disease,
        confidence,
        advice
    )
    VALUES (%s,%s,%s,%s)
    """

    cursor.execute(
        query,
        (
            patient_id,
            disease,
            confidence,
            advice
        )
    )

    conn.commit()

    cursor.close()
    conn.close()


def get_history(user_id):

    conn = get_connection()

    cursor = conn.cursor(
        dictionary=True
    )

    query = """
    SELECT

        p.full_name,
        p.age,
        p.gender,

        d.disease,
        d.confidence,
        d.diagnosis_date

    FROM diagnoses d

    JOIN patients p
    ON p.patient_id = d.patient_id

    WHERE p.user_id = %s

    ORDER BY d.diagnosis_date DESC
    """

    cursor.execute(query, (user_id,))

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows