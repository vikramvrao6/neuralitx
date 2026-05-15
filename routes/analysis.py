from flask import Blueprint, request, jsonify, render_template
from core.signal_processor import process_eeg
from core.neural_network import run_inference
from core.rag_system import get_rag_context
from core.llm_interpreter import generate_explanation, format_results
import sqlite3
import os

analysis_bp = Blueprint("analysis", __name__)

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'database', 'neuralytic.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@analysis_bp.route("/analyze", methods=["POST"])
def analyze():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    upload_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    file.save(file_path)
    
    try:
        signal_results = process_eeg(file_path)
        nn_result = run_inference(signal_results['band_powers'])
        rag_context = get_rag_context(signal_results['band_powers'], signal_results['artifact_info'])
        explanation = generate_explanation(signal_results['band_powers'], signal_results['artifact_info'], nn_result, rag_context)
        results = format_results(signal_results['band_powers'], signal_results['artifact_info'], nn_result, rag_context, explanation)
        
        db = get_db()
        db.execute(
            "INSERT INTO analysis_results (processing_status, artifact_flags, frequency_band_data, nn_output, rag_context, llm_explanation) VALUES (?, ?, ?, ?, ?, ?)",
            ('complete', str(signal_results['artifact_info']), str(signal_results['band_powers']), str(nn_result), rag_context, explanation)
        )
        db.commit()
        db.close()
        
        return jsonify(results)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analysis_bp.route("/results/<int:result_id>")
def results(result_id):
    db = get_db()
    result = db.execute("SELECT * FROM analysis_results WHERE id = ?", (result_id,)).fetchone()
    db.close()
    
    if not result:
        return "Result not found", 404
    
    return render_template("results.html", result=result)