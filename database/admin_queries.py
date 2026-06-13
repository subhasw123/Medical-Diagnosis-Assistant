from database.db import get_connection


def get_all_diagnoses():

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            p.full_name,
            p.age,
            p.gender,
            d.disease,
            d.confidence,
            d.diagnosis_date
        FROM diagnoses d
        JOIN patients p
            ON d.patient_id = p.patient_id
        ORDER BY d.diagnosis_date DESC
    """)

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results

def get_dashboard_stats():

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT COUNT(*) AS total_patients FROM patients"
    )

    total_patients = cursor.fetchone()["total_patients"]

    cursor.execute(
        "SELECT COUNT(*) AS total_diagnoses FROM diagnoses"
    )

    total_diagnoses = cursor.fetchone()["total_diagnoses"]

    cursor.close()
    conn.close()

    return {
        "total_patients": total_patients,
        "total_diagnoses": total_diagnoses
    }