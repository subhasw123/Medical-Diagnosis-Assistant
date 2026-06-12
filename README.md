# Medical Diagnosis Assistant

A simple Flask-based medical diagnosis assistant scaffold.

## Project Structure

- `app.py` - Flask entry point
- `config.py` - Configuration settings
- `requirements.txt` - Python dependencies
- `.env` - Environment variables and database credentials
- `database/db.py` - MySQL connection helper
- `database/schema.sql` - Database table definitions
- `database/seed_data.sql` - Seed sample data
- `dataset/diseases.csv` - Disease dataset sample
- `dataset/symptoms.json` - Symptom reference data
- `ml/train_model.py` - Model training script
- `ml/preprocess.py` - Data preprocessing helper
- `ml/predictor.py` - Prediction helper
- `ml/models/` - Serialized model artifacts
- `artifacts/` - Feature and symptom metadata
- `routes/` - Flask route modules
- `services/` - Business logic services

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `.env` file with database credentials.
3. Initialize the database using `database/schema.sql` and `database/seed_data.sql`.
