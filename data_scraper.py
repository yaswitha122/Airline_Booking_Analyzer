import requests
import time
import random
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import json
import pandas as pd
import os

class AirlineDataScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.aviationstack_key = os.getenv('AVIATIONSTACK_API_KEY')
        self.aviationstack_url = 'http://api.aviationstack.com/v1/flights'
        
        # Debug: Check if API key is loaded
        if not self.aviationstack_key:
            print("⚠️  WARNING: AVIATIONSTACK_API_KEY not found in environment variables!")
            print("   Please create a .env file with: AVIATIONSTACK_API_KEY=your_key_here")
        else:
            print(f"✅ Aviationstack API key loaded: {self.aviationstack_key[:8]}...")

    def check_api_key(self):
        """Check if API key is available and valid"""
        if not self.aviationstack_key:
            return False, "API key not set. Please add AVIATIONSTACK_API_KEY to your .env file"
        return True, "API key is set"

    def fetch_data(self, source='aviationstack', routes=None, days_ahead=30):
        """Fetch airline booking data from specified source"""
        if routes is None:
            routes = ['SYD-MEL', 'SYD-BNE', 'MEL-BNE']
        if source == 'aviationstack':
            return self._fetch_aviationstack_data(routes, days_ahead)
        elif source == 'skyscanner':
            return self._fetch_skyscanner_data(routes, days_ahead)
        elif source == 'google_flights':
            return self._fetch_google_flights_data(routes, days_ahead)
        elif source == 'mock_data':
            return self._generate_mock_data(routes, days_ahead)
        else:
            raise ValueError(f"Unsupported data source: {source}")

    def _fetch_aviationstack_data(self, routes, days_ahead):
        """Fetch data from Aviationstack API for the given routes and days ahead"""
        if not self.aviationstack_key:
            raise Exception("Aviationstack API key not set in environment variable 'AVIATIONSTACK_API_KEY'.")
        data = {}
        for route in routes:
            origin, dest = route.split('-')
            route_data = {
                'prices': [],
                'dates': [],
                'airlines': [],
                'departure_times': [],
                'arrival_times': [],
                'flight_numbers': [],
                'duration': [],
                'stops': []
            }
            for i in range(min(days_ahead, 7)):  # Limit to 7 days for demo/API quota
                date = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
                params = {
                    'access_key': self.aviationstack_key,
                    'dep_iata': origin,
                    'arr_iata': dest,
                    'flight_date': date,
                    'limit': 20
                }
                try:
                    resp = self.session.get(self.aviationstack_url, params=params, timeout=15)
                    if resp.status_code == 200:
                        flights = resp.json().get('data', [])
                        for flight in flights:
                            airline = flight.get('airline', {}).get('name', 'Unknown')
                            dep_time = flight.get('departure', {}).get('scheduled', '')
                            arr_time = flight.get('arrival', {}).get('scheduled', '')
                            flight_num = flight.get('flight', {}).get('iata', '')
                            duration = ''  # Aviationstack free tier does not provide duration
                            stops = 'Direct'  # Assume direct for now
                            # Simulate price (since Aviationstack does not provide price)
                            price = random.randint(80, 250)
                            route_data['prices'].append(price)
                            route_data['dates'].append(date)
                            route_data['airlines'].append(airline)
                            route_data['departure_times'].append(dep_time)
                            route_data['arrival_times'].append(arr_time)
                            route_data['flight_numbers'].append(flight_num)
                            route_data['duration'].append(duration)
                            route_data['stops'].append(stops)
                    else:
                        print(f"Aviationstack API error: {resp.status_code} {resp.text}")
                except Exception as e:
                    print(f"Aviationstack API request failed: {e}")
                time.sleep(1)  # Avoid hitting rate limits
            data[route] = route_data
        return data

    def _fetch_skyscanner_data(self, routes, days_ahead):
        """Fetch data from Skyscanner (mock implementation)"""
        data = {}
        
        for route in routes:
            route_data = {
                'prices': [],
                'dates': [],
                'airlines': [],
                'departure_times': [],
                'arrival_times': []
            }
            
            # Generate mock data for demonstration
            base_price = random.randint(80, 200)
            for i in range(min(days_ahead, 14)):  # Limit to 14 days for demo
                date = datetime.now() + timedelta(days=i)
                price = base_price + random.randint(-30, 50)
                route_data['prices'].append(max(50, price))
                route_data['dates'].append(date.strftime('%Y-%m-%d'))
                route_data['airlines'].append(random.choice(['Qantas', 'Virgin Australia', 'Jetstar', 'Rex']))
                route_data['departure_times'].append(f"{random.randint(6, 22):02d}:{random.randint(0, 59):02d}")
                route_data['arrival_times'].append(f"{random.randint(6, 22):02d}:{random.randint(0, 59):02d}")
            
            data[route] = route_data
            
        return data
    
    def _fetch_google_flights_data(self, routes, days_ahead):
        """Fetch data from Google Flights (mock implementation)"""
        return self._fetch_skyscanner_data(routes, days_ahead)
    
    def _generate_mock_data(self, routes, days_ahead):
        """Generate realistic mock data for demonstration"""
        data = {}
        
        # Define base prices for different routes
        base_prices = {
            'SYD-MEL': 120,
            'SYD-BNE': 95,
            'MEL-BNE': 85,
            'SYD-PER': 180,
            'MEL-PER': 160,
            'BNE-PER': 170,
            'SYD-ADL': 110,
            'MEL-ADL': 90,
            'BNE-ADL': 100,
            'SYD-CBR': 70,
            'MEL-CBR': 80,
            'BNE-CBR': 85
        }
        
        airlines = ['Qantas', 'Virgin Australia', 'Jetstar', 'Rex']
        
        for route in routes:
            base_price = base_prices.get(route, 100)
            route_data = {
                'prices': [],
                'dates': [],
                'airlines': [],
                'departure_times': [],
                'arrival_times': [],
                'duration': [],
                'stops': []
            }
            
            for i in range(min(days_ahead, 30)):
                date = datetime.now() + timedelta(days=i)
                
                # Add weekend premium
                weekend_multiplier = 1.2 if date.weekday() >= 5 else 1.0
                
                # Add seasonal variation
                month = date.month
                seasonal_multiplier = 1.3 if month in [12, 1, 2] else 0.9 if month in [6, 7, 8] else 1.0
                
                # Add random variation
                random_variation = random.uniform(0.8, 1.3)
                
                price = int(base_price * weekend_multiplier * seasonal_multiplier * random_variation)
                route_data['prices'].append(max(50, price))
                route_data['dates'].append(date.strftime('%Y-%m-%d'))
                route_data['airlines'].append(random.choice(airlines))
                route_data['departure_times'].append(f"{random.randint(6, 22):02d}:{random.randint(0, 59):02d}")
                route_data['arrival_times'].append(f"{random.randint(6, 22):02d}:{random.randint(0, 59):02d}")
                route_data['duration'].append(f"{random.randint(1, 3)}h {random.randint(0, 59)}m")
                route_data['stops'].append(random.choice(['Direct', '1 stop', '2 stops']))
            
            data[route] = route_data
            
        return data
    
    def get_route_info(self, route_code):
        """Get information about a specific route"""
        route_info = {
            'SYD-MEL': {'distance': 713, 'typical_duration': '1h 25m', 'popular_airlines': ['Qantas', 'Virgin Australia', 'Jetstar']},
            'SYD-BNE': {'distance': 732, 'typical_duration': '1h 30m', 'popular_airlines': ['Qantas', 'Virgin Australia', 'Jetstar']},
            'MEL-BNE': {'distance': 1370, 'typical_duration': '2h 15m', 'popular_airlines': ['Qantas', 'Virgin Australia', 'Jetstar']},
            'SYD-PER': {'distance': 3291, 'typical_duration': '4h 15m', 'popular_airlines': ['Qantas', 'Virgin Australia']},
            'MEL-PER': {'distance': 2707, 'typical_duration': '3h 45m', 'popular_airlines': ['Qantas', 'Virgin Australia']},
            'BNE-PER': {'distance': 3605, 'typical_duration': '4h 45m', 'popular_airlines': ['Qantas', 'Virgin Australia']}
        }
        return route_info.get(route_code, {})
    def get_flight_status(self, flight_number, flight_date=None):
        """Get real-time flight status by flight number and optional date."""
        if not self.aviationstack_key:
            print("❌ No API key available, using mock data")
            return self._get_mock_flight_status(flight_number, flight_date)
        
        print(f"🔍 Looking up flight: {flight_number} on {flight_date or 'any date'}")
        
        params = {
            'access_key': self.aviationstack_key,
            'flight_iata': flight_number
        }
        if flight_date:
            params['flight_date'] = flight_date
            
        try:
            print(f"🌐 Making API request to Aviationstack...")
            resp = self.session.get(self.aviationstack_url, params=params, timeout=15)
            print(f"📡 API Response Status: {resp.status_code}")
            
            if resp.status_code == 200:
                data = resp.json()
                flights = data.get('data', [])
                print(f"✈️  Found {len(flights)} flights")
                
                if flights:
                    return flights
                else:
                    print("⚠️  No flights found in API response, using mock data")
                    return self._get_mock_flight_status(flight_number, flight_date)
            else:
                print(f"❌ API Error: {resp.status_code} - {resp.text}")
                print("🔄 Falling back to mock data")
                return self._get_mock_flight_status(flight_number, flight_date)
                
        except Exception as e:
            print(f"❌ API request failed: {e}")
            print("🔄 Falling back to mock data")
            return self._get_mock_flight_status(flight_number, flight_date)

    def _get_mock_flight_status(self, flight_number, flight_date=None):
        """Generate mock flight status data for testing"""
        print(f"🎭 Generating mock flight status for {flight_number}")
        
        # Generate realistic mock data
        statuses = ['scheduled', 'active', 'landed', 'cancelled', 'diverted']
        airlines = ['Qantas', 'Virgin Australia', 'Jetstar', 'Rex']
        
        mock_flight = {
            'flight': {
                'iata': flight_number,
                'icao': f'QF{random.randint(100, 999)}'
            },
            'airline': {
                'name': random.choice(airlines),
                'iata': 'QF'
            },
            'departure': {
                'airport': 'Sydney Airport',
                'iata': 'SYD',
                'scheduled': f"{flight_date or '2024-01-15'}T{random.randint(6, 22):02d}:{random.randint(0, 59):02d}:00"
            },
            'arrival': {
                'airport': 'Melbourne Airport', 
                'iata': 'MEL',
                'scheduled': f"{flight_date or '2024-01-15'}T{random.randint(8, 23):02d}:{random.randint(0, 59):02d}:00"
            },
            'flight_status': random.choice(statuses)
        }
        
        return [mock_flight]

    def get_airport_info(self, iata_code):
        """Get airport information by IATA code."""
        if not self.aviationstack_key:
            print("❌ No API key available, using mock airport data")
            return self._get_mock_airport_info(iata_code)
            
        print(f"🏢 Looking up airport: {iata_code}")
        
        url = 'http://api.aviationstack.com/v1/airports'
        params = {
            'access_key': self.aviationstack_key,
            'iata_code': iata_code
        }
        
        try:
            resp = self.session.get(url, params=params, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                airports = data.get('data', [])
                if airports:
                    return airports
                else:
                    print("⚠️  No airport found, using mock data")
                    return self._get_mock_airport_info(iata_code)
            else:
                print(f"❌ API Error: {resp.status_code}")
                return self._get_mock_airport_info(iata_code)
        except Exception as e:
            print(f"❌ API request failed: {e}")
            return self._get_mock_airport_info(iata_code)

    def _get_mock_airport_info(self, iata_code):
        """Generate mock airport data"""
        airports = {
            'SYD': {'airport_name': 'Sydney Airport', 'iata_code': 'SYD', 'city_name': 'Sydney', 'country_name': 'Australia', 'timezone': 'Australia/Sydney', 'latitude': -33.9399, 'longitude': 151.1753},
            'MEL': {'airport_name': 'Melbourne Airport', 'iata_code': 'MEL', 'city_name': 'Melbourne', 'country_name': 'Australia', 'timezone': 'Australia/Melbourne', 'latitude': -37.8136, 'longitude': 144.9631},
            'BNE': {'airport_name': 'Brisbane Airport', 'iata_code': 'BNE', 'city_name': 'Brisbane', 'country_name': 'Australia', 'timezone': 'Australia/Brisbane', 'latitude': -27.3842, 'longitude': 153.1175},
            'PER': {'airport_name': 'Perth Airport', 'iata_code': 'PER', 'city_name': 'Perth', 'country_name': 'Australia', 'timezone': 'Australia/Perth', 'latitude': -31.9403, 'longitude': 115.9669},
            'ADL': {'airport_name': 'Adelaide Airport', 'iata_code': 'ADL', 'city_name': 'Adelaide', 'country_name': 'Australia', 'timezone': 'Australia/Adelaide', 'latitude': -34.9285, 'longitude': 138.6007},
            'CBR': {'airport_name': 'Canberra Airport', 'iata_code': 'CBR', 'city_name': 'Canberra', 'country_name': 'Australia', 'timezone': 'Australia/Sydney', 'latitude': -35.3069, 'longitude': 149.1950}
        }
        
        return [airports.get(iata_code, {
            'airport_name': f'Unknown Airport ({iata_code})',
            'iata_code': iata_code,
            'city_name': 'Unknown',
            'country_name': 'Unknown',
            'timezone': 'UTC',
            'latitude': 0,
            'longitude': 0
        })]

    def get_airline_info(self, iata_code):
        """Get airline information by IATA code."""
        if not self.aviationstack_key:
            print("❌ No API key available, using mock airline data")
            return self._get_mock_airline_info(iata_code)
            
        print(f"✈️  Looking up airline: {iata_code}")
        
        url = 'http://api.aviationstack.com/v1/airlines'
        params = {
            'access_key': self.aviationstack_key,
            'iata_code': iata_code
        }
        
        try:
            resp = self.session.get(url, params=params, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                airlines = data.get('data', [])
                if airlines:
                    return airlines
                else:
                    print("⚠️  No airline found, using mock data")
                    return self._get_mock_airline_info(iata_code)
            else:
                print(f"❌ API Error: {resp.status_code}")
                return self._get_mock_airline_info(iata_code)
        except Exception as e:
            print(f"❌ API request failed: {e}")
            return self._get_mock_airline_info(iata_code)

    def _get_mock_airline_info(self, iata_code):
        """Generate mock airline data"""
        airlines = {
            'QF': {'airline_name': 'Qantas Airways', 'iata_code': 'QF', 'country_name': 'Australia', 'icao_code': 'QFA', 'callsign': 'QANTAS'},
            'VA': {'airline_name': 'Virgin Australia', 'iata_code': 'VA', 'country_name': 'Australia', 'icao_code': 'VOZ', 'callsign': 'VELOCITY'},
            'JQ': {'airline_name': 'Jetstar Airways', 'iata_code': 'JQ', 'country_name': 'Australia', 'icao_code': 'JST', 'callsign': 'JETSTAR'},
            'ZL': {'airline_name': 'Regional Express', 'iata_code': 'ZL', 'country_name': 'Australia', 'icao_code': 'RXA', 'callsign': 'REX'}
        }
        
        return [airlines.get(iata_code, {
            'airline_name': f'Unknown Airline ({iata_code})',
            'iata_code': iata_code,
            'country_name': 'Unknown',
            'icao_code': 'UNK',
            'callsign': 'UNKNOWN'
        })]

    def get_historical_flights(self, dep_iata, arr_iata, flight_date):
        """Get historical flights for a route and date."""
        if not self.aviationstack_key:
            print("❌ No API key available, using mock historical data")
            return self._get_mock_historical_flights(dep_iata, arr_iata, flight_date)
            
        print(f"📅 Looking up historical flights: {dep_iata} → {arr_iata} on {flight_date}")
        
        params = {
            'access_key': self.aviationstack_key,
            'dep_iata': dep_iata,
            'arr_iata': arr_iata,
            'flight_date': flight_date
        }
        
        try:
            resp = self.session.get(self.aviationstack_url, params=params, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                flights = data.get('data', [])
                if flights:
                    return flights
                else:
                    print("⚠️  No historical flights found, using mock data")
                    return self._get_mock_historical_flights(dep_iata, arr_iata, flight_date)
            else:
                print(f"❌ API Error: {resp.status_code}")
                return self._get_mock_historical_flights(dep_iata, arr_iata, flight_date)
        except Exception as e:
            print(f"❌ API request failed: {e}")
            return self._get_mock_historical_flights(dep_iata, arr_iata, flight_date)

    def _get_mock_historical_flights(self, dep_iata, arr_iata, flight_date):
        """Generate mock historical flight data"""
        print(f"🎭 Generating mock historical flights for {dep_iata} → {arr_iata}")
        
        airlines = ['Qantas', 'Virgin Australia', 'Jetstar', 'Rex']
        statuses = ['scheduled', 'active', 'landed', 'cancelled']
        
        flights = []
        for i in range(random.randint(3, 8)):  # Generate 3-8 flights
            flight = {
                'flight': {
                    'iata': f'QF{random.randint(100, 999)}',
                    'icao': f'QFA{random.randint(1000, 9999)}'
                },
                'airline': {
                    'name': random.choice(airlines),
                    'iata': 'QF'
                },
                'departure': {
                    'airport': f'{dep_iata} Airport',
                    'iata': dep_iata,
                    'scheduled': f"{flight_date}T{random.randint(6, 22):02d}:{random.randint(0, 59):02d}:00",
                    'actual': f"{flight_date}T{random.randint(6, 22):02d}:{random.randint(0, 59):02d}:00"
                },
                'arrival': {
                    'airport': f'{arr_iata} Airport',
                    'iata': arr_iata,
                    'scheduled': f"{flight_date}T{random.randint(8, 23):02d}:{random.randint(0, 59):02d}:00",
                    'actual': f"{flight_date}T{random.randint(8, 23):02d}:{random.randint(0, 59):02d}:00"
                },
                'flight_status': random.choice(statuses)
            }
            flights.append(flight)
        
        return flights

    # Simple in-memory cache for API responses (for demo, not production)
    _cache = {}
    def cached_api_call(self, url, params, cache_minutes=10):
        key = f"{url}|{json.dumps(params, sort_keys=True)}"
        now = time.time()
        if key in self._cache:
            cached = self._cache[key]
            if now - cached['time'] < cache_minutes * 60:
                return cached['data']
        resp = self.session.get(url, params=params, timeout=15)
        if resp.status_code == 200:
            data = resp.json().get('data', [])
            self._cache[key] = {'data': data, 'time': now}
            return data
        else:
            raise Exception(f"Aviationstack API error: {resp.status_code} {resp.text}")
