import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.utils import PlotlyJSONEncoder
import json
from collections import Counter

class DataProcessor:
    def __init__(self):
        pass
    
    def process_data(self, raw_data):
        """Process raw airline data and extract insights"""
        processed_data = {
            'routes': {},
            'summary': {},
            'insights': {}
        }
        
        # Process each route
        for route, route_data in raw_data.items():
            processed_route = self._process_route_data(route, route_data)
            processed_data['routes'][route] = processed_route
        
        # Generate summary statistics
        processed_data['summary'] = self._generate_summary(processed_data['routes'])
        
        # Generate insights
        processed_data['insights'] = self._generate_insights(processed_data['routes'])
        
        return processed_data
    
    def _process_route_data(self, route, route_data):
        """Process individual route data"""
        prices = route_data.get('prices', [])
        dates = route_data.get('dates', [])
        
        if not prices or not dates:
            return {}
        
        # Convert to pandas DataFrame for analysis
        df = pd.DataFrame({
            'date': dates,
            'price': prices,
            'airline': route_data.get('airlines', ['Unknown'] * len(prices)),
            'departure_time': route_data.get('departure_times', [''] * len(prices)),
            'arrival_time': route_data.get('arrival_times', [''] * len(prices)),
            'duration': route_data.get('duration', [''] * len(prices)),
            'stops': route_data.get('stops', [''] * len(prices))
        })
        
        # Convert date strings to datetime
        df['date'] = pd.to_datetime(df['date'])
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        
        # Calculate statistics
        stats = {
            'min_price': float(df['price'].min()),
            'max_price': float(df['price'].max()),
            'avg_price': float(df['price'].mean()),
            'median_price': float(df['price'].median()),
            'price_std': float(df['price'].std()),
            'price_volatility': float(df['price'].std() / df['price'].mean() * 100),
            'total_flights': len(df),
            'cheapest_date': df.loc[df['price'].idxmin(), 'date'].strftime('%Y-%m-%d'),
            'most_expensive_date': df.loc[df['price'].idxmax(), 'date'].strftime('%Y-%m-%d'),
            'price_trend': self._calculate_price_trend(df),
            'demand_score': self._calculate_demand_score(df),
            'popular_airlines': self._get_popular_airlines(df),
            'best_booking_window': self._find_best_booking_window(df)
        }
        
        return {
            'raw_data': route_data,
            'processed_df': df.to_dict('records'),
            'statistics': stats
        }
    
    def _calculate_price_trend(self, df):
        """Calculate price trend (increasing, decreasing, or stable)"""
        if len(df) < 2:
            return 'insufficient_data'
        
        # Calculate linear regression slope
        x = np.arange(len(df))
        y = df['price'].values
        slope = np.polyfit(x, y, 1)[0]
        
        if slope > 5:
            return 'increasing'
        elif slope < -5:
            return 'decreasing'
        else:
            return 'stable'
    
    def _calculate_demand_score(self, df):
        """Calculate demand score based on price patterns"""
        if len(df) < 3:
            return 5.0
        
        # Factors affecting demand score:
        # 1. Price volatility (higher volatility = higher demand)
        # 2. Weekend vs weekday pricing
        # 3. Price trend
        
        volatility_score = min(10, df['price'].std() / df['price'].mean() * 50)
        
        # Weekend premium
        df['is_weekend'] = df['date'].dt.weekday >= 5
        weekend_avg = df[df['is_weekend']]['price'].mean()
        weekday_avg = df[~df['is_weekend']]['price'].mean()
        
        if weekday_avg > 0:
            weekend_premium = (weekend_avg - weekday_avg) / weekday_avg
            weekend_score = min(10, weekend_premium * 20)
        else:
            weekend_score = 5
        
        # Price trend score
        trend_scores = {'increasing': 8, 'decreasing': 3, 'stable': 5}
        trend_score = trend_scores.get(self._calculate_price_trend(df), 5)
        
        # Calculate weighted average
        demand_score = (volatility_score * 0.4 + weekend_score * 0.3 + trend_score * 0.3)
        
        return round(demand_score, 1)
    
    def _get_popular_airlines(self, df):
        """Get most popular airlines for the route"""
        airline_counts = Counter(df['airline'])
        return [{'airline': airline, 'count': count} for airline, count in airline_counts.most_common(3)]
    
    def _find_best_booking_window(self, df):
        """Find the best booking window (days in advance)"""
        if len(df) < 7:
            return {'days_ahead': 7, 'avg_price': float(df['price'].mean())}
        
        # Group by days ahead and calculate average price
        df['days_ahead'] = (df['date'] - df['date'].min()).dt.days
        
        window_stats = df.groupby('days_ahead')['price'].agg(['mean', 'count']).reset_index()
        window_stats = window_stats[window_stats['count'] >= 2]  # At least 2 data points
        
        if len(window_stats) == 0:
            return {'days_ahead': 7, 'avg_price': float(df['price'].mean())}
        
        best_window = window_stats.loc[window_stats['mean'].idxmin()]
        
        return {
            'days_ahead': int(best_window['days_ahead']),
            'avg_price': float(best_window['mean'])
        }
    
    def _generate_summary(self, routes_data):
        """Generate summary statistics across all routes"""
        all_prices = []
        route_stats = []
        
        for route, data in routes_data.items():
            if 'statistics' in data:
                stats = data['statistics']
                all_prices.extend([stats['min_price'], stats['max_price'], stats['avg_price']])
                route_stats.append({
                    'route': route,
                    'avg_price': stats['avg_price'],
                    'demand_score': stats['demand_score'],
                    'price_volatility': stats['price_volatility']
                })
        
        if not all_prices:
            return {}
        
        # Sort routes by demand score
        route_stats.sort(key=lambda x: x['demand_score'], reverse=True)
        
        return {
            'total_routes': len(routes_data),
            'overall_avg_price': float(np.mean(all_prices)),
            'overall_price_range': {
                'min': float(np.min(all_prices)),
                'max': float(np.max(all_prices))
            },
            'high_demand_routes': [route['route'] for route in route_stats[:3]],
            'low_demand_routes': [route['route'] for route in route_stats[-3:]],
            'most_expensive_routes': sorted(route_stats, key=lambda x: x['avg_price'], reverse=True)[:3],
            'cheapest_routes': sorted(route_stats, key=lambda x: x['avg_price'])[:3]
        }
    
    def _generate_insights(self, routes_data):
        """Generate actionable insights from the data"""
        insights = {
            'price_insights': [],
            'demand_insights': [],
            'booking_insights': [],
            'route_insights': []
        }
        
        # Price insights
        avg_prices = [data['statistics']['avg_price'] for data in routes_data.values() if 'statistics' in data]
        if avg_prices:
            insights['price_insights'].append({
                'type': 'price_range',
                'message': f"Average ticket prices range from ${min(avg_prices):.0f} to ${max(avg_prices):.0f}",
                'priority': 'medium'
            })
        
        # Demand insights
        high_demand_routes = []
        for route, data in routes_data.items():
            if 'statistics' in data and data['statistics']['demand_score'] > 7:
                high_demand_routes.append(route)
        
        if high_demand_routes:
            insights['demand_insights'].append({
                'type': 'high_demand',
                'message': f"High demand detected on routes: {', '.join(high_demand_routes)}",
                'priority': 'high'
            })
        
        # Booking insights
        for route, data in routes_data.items():
            if 'statistics' in data:
                best_window = data['statistics']['best_booking_window']
                insights['booking_insights'].append({
                    'type': 'optimal_booking',
                    'route': route,
                    'message': f"Best booking window for {route}: {best_window['days_ahead']} days ahead (avg: ${best_window['avg_price']:.0f})",
                    'priority': 'medium'
                })
        
        return insights
    
    def generate_charts(self, processed_data, chart_type='price_trends'):
        """Generate visualization charts"""
        charts = {}
        
        if chart_type == 'price_trends':
            charts['price_trends'] = self._create_price_trends_chart(processed_data)
        elif chart_type == 'demand_heatmap':
            charts['demand_heatmap'] = self._create_demand_heatmap(processed_data)
        elif chart_type == 'route_comparison':
            charts['route_comparison'] = self._create_route_comparison_chart(processed_data)
        elif chart_type == 'all':
            charts['price_trends'] = self._create_price_trends_chart(processed_data)
            charts['demand_heatmap'] = self._create_demand_heatmap(processed_data)
            charts['route_comparison'] = self._create_route_comparison_chart(processed_data)
        
        return charts
    
    def _create_price_trends_chart(self, processed_data):
        """Create price trends chart"""
        fig = go.Figure()
        
        for route, data in processed_data['routes'].items():
            if 'raw_data' in data:
                raw_data = data['raw_data']
                fig.add_trace(go.Scatter(
                    x=raw_data['dates'],
                    y=raw_data['prices'],
                    mode='lines+markers',
                    name=route,
                    line=dict(width=2),
                    marker=dict(size=6)
                ))
        
        fig.update_layout(
            title='Airline Ticket Price Trends',
            xaxis_title='Date',
            yaxis_title='Price (AUD)',
            hovermode='x unified',
            template='plotly_white'
        )
        
        return json.dumps(fig, cls=PlotlyJSONEncoder)
    
    def _create_demand_heatmap(self, processed_data):
        """Create demand heatmap chart"""
        routes = []
        demand_scores = []
        
        for route, data in processed_data['routes'].items():
            if 'statistics' in data:
                routes.append(route)
                demand_scores.append(data['statistics']['demand_score'])
        
        fig = go.Figure(data=go.Heatmap(
            z=[demand_scores],
            x=routes,
            y=['Demand Score'],
            colorscale='RdYlGn',
            zmin=0,
            zmax=10
        ))
        
        fig.update_layout(
            title='Route Demand Heatmap',
            xaxis_title='Routes',
            yaxis_title='',
            template='plotly_white'
        )
        
        return json.dumps(fig, cls=PlotlyJSONEncoder)
    
    def _create_route_comparison_chart(self, processed_data):
        """Create route comparison chart"""
        routes = []
        avg_prices = []
        demand_scores = []
        
        for route, data in processed_data['routes'].items():
            if 'statistics' in data:
                routes.append(route)
                avg_prices.append(data['statistics']['avg_price'])
                demand_scores.append(data['statistics']['demand_score'])
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=routes,
            y=avg_prices,
            name='Average Price',
            yaxis='y',
            marker_color='lightblue'
        ))
        
        fig.add_trace(go.Scatter(
            x=routes,
            y=demand_scores,
            name='Demand Score',
            yaxis='y2',
            mode='lines+markers',
            line=dict(color='red', width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title='Route Comparison: Price vs Demand',
            xaxis_title='Routes',
            yaxis=dict(title='Average Price (AUD)', side='left'),
            yaxis2=dict(title='Demand Score', side='right', overlaying='y', range=[0, 10]),
            template='plotly_white',
            barmode='group'
        )
        
        return json.dumps(fig, cls=PlotlyJSONEncoder)
