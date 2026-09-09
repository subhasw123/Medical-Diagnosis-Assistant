from database.db import get_connection


def get_all_diagnoses():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            p.full_name, p.age, p.gender,
            d.disease, d.confidence, d.diagnosis_date
        FROM diagnoses d
        JOIN patients p ON d.patient_id = p.patient_id
        ORDER BY d.diagnosis_date DESC
    """)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


def get_dashboard_stats():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total_patients FROM patients")
    total_patients = cursor.fetchone()["total_patients"]

    cursor.execute("SELECT COUNT(*) AS total_diagnoses FROM diagnoses")
    total_diagnoses = cursor.fetchone()["total_diagnoses"]

    cursor.close()
    conn.close()
    return {
        "total_patients": total_patients,
        "total_diagnoses": total_diagnoses
    }


# ─── Diagnosis Analytics ────────────────────────────────────────────

def get_diagnosis_analytics():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Total diagnoses
    cursor.execute("SELECT COUNT(*) AS total FROM diagnoses")
    total_diagnoses = cursor.fetchone()["total"]

    # Total unique patients
    cursor.execute("SELECT COUNT(*) AS total FROM patients")
    total_patients = cursor.fetchone()["total"]

    # Avg confidence
    cursor.execute("SELECT ROUND(AVG(confidence), 1) AS avg_conf FROM diagnoses")
    avg_confidence = cursor.fetchone()["avg_conf"] or 0

    # Top 5 most diagnosed diseases
    cursor.execute("""
        SELECT disease, COUNT(*) AS count
        FROM diagnoses
        GROUP BY disease
        ORDER BY count DESC
        LIMIT 5
    """)
    top_diseases = cursor.fetchall()

    # Gender breakdown
    cursor.execute("""
        SELECT gender, COUNT(*) AS count
        FROM patients
        GROUP BY gender
    """)
    gender_breakdown = cursor.fetchall()

    # Age group breakdown
    cursor.execute("""
        SELECT
            CASE
                WHEN age < 18 THEN 'Under 18'
                WHEN age BETWEEN 18 AND 30 THEN '18-30'
                WHEN age BETWEEN 31 AND 50 THEN '31-50'
                WHEN age BETWEEN 51 AND 70 THEN '51-70'
                ELSE 'Over 70'
            END AS age_group,
            COUNT(*) AS count
        FROM patients
        GROUP BY age_group
        ORDER BY count DESC
    """)
    age_groups = cursor.fetchall()

    # Daily activity (last 7 days)
    cursor.execute("""
        SELECT DATE(diagnosis_date) AS day, COUNT(*) AS count
        FROM diagnoses
        WHERE diagnosis_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
        GROUP BY day
        ORDER BY day ASC
    """)
    daily_activity = cursor.fetchall()

    # Hourly usage pattern
    cursor.execute("""
        SELECT HOUR(diagnosis_date) AS hour, COUNT(*) AS count
        FROM diagnoses
        GROUP BY hour
        ORDER BY hour ASC
    """)
    hourly_usage = cursor.fetchall()

    # Recent diagnoses
    cursor.execute("""
        SELECT p.full_name, p.age, p.gender, d.disease, d.confidence, d.diagnosis_date
        FROM diagnoses d
        JOIN patients p ON d.patient_id = p.patient_id
        ORDER BY d.diagnosis_date DESC
        LIMIT 10
    """)
    recent_diagnoses = cursor.fetchall()

    cursor.close()
    conn.close()

    return {
        "total_diagnoses": total_diagnoses,
        "total_patients": total_patients,
        "avg_confidence": avg_confidence,
        "top_diseases": top_diseases,
        "gender_breakdown": gender_breakdown,
        "age_groups": age_groups,
        "daily_activity": daily_activity,
        "hourly_usage": hourly_usage,
        "recent_diagnoses": recent_diagnoses,
    }


# ─── Chatbot Analytics ──────────────────────────────────────────────

def get_chatbot_analytics():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Total questions asked
    cursor.execute("SELECT COUNT(*) AS total FROM chatbot_logs")
    total_questions = cursor.fetchone()["total"]

    # Unique users (by IP)
    cursor.execute("SELECT COUNT(DISTINCT ip_address) AS unique_users FROM chatbot_logs")
    unique_users = cursor.fetchone()["unique_users"]

    # Today's questions
    cursor.execute("""
        SELECT COUNT(*) AS today
        FROM chatbot_logs
        WHERE DATE(asked_at) = CURDATE()
    """)
    today_questions = cursor.fetchone()["today"]

    # Daily activity (last 7 days)
    cursor.execute("""
        SELECT DATE(asked_at) AS day, COUNT(*) AS count
        FROM chatbot_logs
        WHERE asked_at >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
        GROUP BY day
        ORDER BY day ASC
    """)
    daily_activity = cursor.fetchall()

    # Hourly usage pattern
    cursor.execute("""
        SELECT HOUR(asked_at) AS hour, COUNT(*) AS count
        FROM chatbot_logs
        GROUP BY hour
        ORDER BY hour ASC
    """)
    hourly_usage = cursor.fetchall()

    # Top IPs (most active users)
    cursor.execute("""
        SELECT ip_address, COUNT(*) AS count
        FROM chatbot_logs
        WHERE ip_address IS NOT NULL
        GROUP BY ip_address
        ORDER BY count DESC
        LIMIT 5
    """)
    top_users = cursor.fetchall()

    # Recent questions
    cursor.execute("""
        SELECT question, ip_address, asked_at
        FROM chatbot_logs
        ORDER BY asked_at DESC
        LIMIT 15
    """)
    recent_questions = cursor.fetchall()

    cursor.close()
    conn.close()

    return {
        "total_questions": total_questions,
        "unique_users": unique_users,
        "today_questions": today_questions,
        "daily_activity": daily_activity,
        "hourly_usage": hourly_usage,
        "top_users": top_users,
        "recent_questions": recent_questions,
    }