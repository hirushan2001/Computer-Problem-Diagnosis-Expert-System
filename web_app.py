#!/usr/bin/env python3
"""
Flask Web Application for Computer Problem Diagnosis Expert System
"""

from flask import Flask, render_template, request, jsonify, session
from knowledge_base import ComputerDiagnosisSystem, save_diagnosis
from experta import Fact
from datetime import datetime
import secrets
import json

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

@app.route('/')
def index():
    """Main page"""
    session.clear()
    return render_template('index.html')

@app.route('/diagnose', methods=['POST'])
def diagnose():
    """Process diagnosis request"""
    try:
        data = request.json
        category = data.get('category')
        answers = data.get('answers', {})
        
        # Create expert system instance
        engine = ComputerDiagnosisSystem()
        engine.reset()
        
        # Convert answers to facts
        for key, value in answers.items():
            engine.declare(Fact(**{key: value}))
        
        # Run the engine
        engine.run()
        
        # Get diagnosis result
        if engine.diagnosis_result:
            result = engine.diagnosis_result
            
            # Save to history
            diagnosis_data = {
                'timestamp': datetime.now().isoformat(),
                'diagnosis': result['diagnosis'],
                'solution': result['solution'],
                'severity': result['severity'],
                'facts': answers
            }
            save_diagnosis(diagnosis_data)
            
            return jsonify({
                'success': True,
                'diagnosis': result['diagnosis'],
                'solution': result['solution'],
                'severity': result['severity']
            })
        else:
            return jsonify({
                'success': True,
                'diagnosis': 'General Computer Issue - Basic Troubleshooting',
                'solution': '1. Restart computer\n2. Check all physical connections\n3. Run Windows Update\n4. Update all drivers\n5. Run antivirus scan\n6. Check Event Viewer for errors\n7. Run SFC /scannow\n8. Check Task Manager for resource usage\n9. Clean temp files\n10. Check for overheating',
                'severity': 'low'
            })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/history')
def history():
    """View diagnosis history"""
    try:
        with open('diagnosis_history.json', 'r') as f:
            history_data = json.load(f)
        return render_template('history.html', history=history_data)
    except FileNotFoundError:
        return render_template('history.html', history=[])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)