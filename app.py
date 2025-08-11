from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import json
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.utils import PlotlyJSONEncoder
import numpy as np
from data_scraper import AirlineDataScraper
from data_processor import DataProcessor
from ai_analyzer import AIAnalyzer

app = Flask(__name__)
CORS(app)

# Initialize components
scraper = AirlineDataScraper()
processor = DataProcessor()
ai_analyzer = AIAnalyzer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/fetch-data', methods=['POST'])
def fetch_data():
    try:
        data = request.get_json()
        source = data.get('source', 'skyscanner')
        routes = data.get('routes', ['SYD-MEL', 'SYD-BNE', 'MEL-BNE'])
        days_ahead = data.get('days_ahead', 30)
        
        raw_data = scraper.fetch_data(source, routes, days_ahead)
        processed_data = processor.process_data(raw_data)
        
        return jsonify({
            'success': True,
            'data': processed_data,
            'message': f'Successfully fetched data for {len(routes)} routes'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_data():
    try:
        data = request.get_json()
        analysis_type = data.get('type', 'trends')
        processed_data = data.get('data', {})
        
        insights = ai_analyzer.analyze(processed_data, analysis_type)
        
        return jsonify({
            'success': True,
            'insights': insights
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/charts', methods=['POST'])
def generate_charts():
    try:
        data = request.get_json()
        chart_type = data.get('type', 'price_trends')
        processed_data = data.get('data', {})
        
        charts = processor.generate_charts(processed_data, chart_type)
        
        return jsonify({
            'success': True,
            'charts': charts
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/routes')
def get_available_routes():
    routes = [
        {'code': 'SYD-MEL', 'name': 'Sydney to Melbourne'},
        {'code': 'SYD-BNE', 'name': 'Sydney to Brisbane'},
        {'code': 'MEL-BNE', 'name': 'Melbourne to Brisbane'},
        {'code': 'SYD-PER', 'name': 'Sydney to Perth'},
        {'code': 'MEL-PER', 'name': 'Melbourne to Perth'},
        {'code': 'BNE-PER', 'name': 'Brisbane to Perth'},
        {'code': 'SYD-ADL', 'name': 'Sydney to Adelaide'},
        {'code': 'MEL-ADL', 'name': 'Melbourne to Adelaide'},
        {'code': 'BNE-ADL', 'name': 'Brisbane to Adelaide'},
        {'code': 'SYD-CBR', 'name': 'Sydney to Canberra'},
        {'code': 'MEL-CBR', 'name': 'Melbourne to Canberra'},
        {'code': 'BNE-CBR', 'name': 'Brisbane to Canberra'}
    ]
    return jsonify(routes)

@app.route('/api/sample-data')
def get_sample_data():
    sample_data = {
        'routes': {
            'SYD-MEL': {
                'prices': [120, 135, 110, 125, 140, 115, 130, 145, 120, 135],
                'dates': [(datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(10)],
                'demand_score': 8.5
            },
            'SYD-BNE': {
                'prices': [95, 105, 90, 100, 110, 85, 95, 105, 90, 100],
                'dates': [(datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(10)],
                'demand_score': 7.8
            },
            'MEL-BNE': {
                'prices': [85, 95, 80, 90, 100, 75, 85, 95, 80, 90],
                'dates': [(datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(10)],
                'demand_score': 6.9
            }
        },
        'summary': {
            'total_routes': 3,
            'avg_price': 105.5,
            'price_volatility': 15.2,
            'high_demand_routes': ['SYD-MEL', 'SYD-BNE']
        }
    }
    return jsonify(sample_data)
@app.route('/api/flight-status', methods=['POST'])
def flight_status():
    """Get real-time flight status for a given flight number and optional date."""
    try:
        data = request.get_json()
        flight_number = data.get('flight_number')
        flight_date = data.get('flight_date')
        status = scraper.get_flight_status(flight_number, flight_date)
        return jsonify({'success': True, 'status': status})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/airport-info', methods=['POST'])
def airport_info():
    """Get airport information by IATA code."""
    try:
        data = request.get_json()
        iata_code = data.get('iata_code')
        info = scraper.get_airport_info(iata_code)
        return jsonify({'success': True, 'airport_info': info})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/airline-info', methods=['POST'])
def airline_info():
    """Get airline information by IATA code."""
    try:
        data = request.get_json()
        iata_code = data.get('iata_code')
        info = scraper.get_airline_info(iata_code)
        return jsonify({'success': True, 'airline_info': info})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/historical-flights', methods=['POST'])
def historical_flights():
    """Get historical flights for a route and date."""
    try:
        data = request.get_json()
        dep_iata = data.get('dep_iata')
        arr_iata = data.get('arr_iata')
        flight_date = data.get('flight_date')
        flights = scraper.get_historical_flights(dep_iata, arr_iata, flight_date)
        return jsonify({'success': True, 'flights': flights})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
