import os
import json
from datetime import datetime
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AIAnalyzer:
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
        else:
            print("Warning: OpenAI API key not found. Using fallback analysis.")
    
    def analyze(self, processed_data, analysis_type='trends'):
        """Analyze processed data and provide insights"""
        if self.openai_api_key:
            return self._analyze_with_ai(processed_data, analysis_type)
        else:
            return self._analyze_with_fallback(processed_data, analysis_type)
    
    def _analyze_with_ai(self, processed_data, analysis_type):
        """Analyze data using OpenAI API"""
        try:
            # Prepare data summary for AI analysis
            data_summary = self._prepare_data_summary(processed_data)
            
            # Create prompt based on analysis type
            if analysis_type == 'trends':
                prompt = self._create_trends_prompt(data_summary)
            elif analysis_type == 'pricing':
                prompt = self._create_pricing_prompt(data_summary)
            elif analysis_type == 'demand':
                prompt = self._create_demand_prompt(data_summary)
            else:
                prompt = self._create_general_prompt(data_summary)
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert airline industry analyst. Provide clear, actionable insights based on the data provided."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            ai_insights = response.choices[0].message.content
            
            # Parse and structure the response
            structured_insights = self._structure_ai_response(ai_insights, analysis_type)
            
            return {
                'ai_analysis': structured_insights,
                'raw_response': ai_insights,
                'analysis_type': analysis_type,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"AI analysis failed: {e}")
            return self._analyze_with_fallback(processed_data, analysis_type)
    
    def _analyze_with_fallback(self, processed_data, analysis_type):
        """Fallback analysis without AI"""
        insights = {
            'summary': [],
            'recommendations': [],
            'trends': [],
            'analysis_type': analysis_type,
            'timestamp': datetime.now().isoformat()
        }
        
        # Extract key metrics
        routes_data = processed_data.get('routes', {})
        summary_data = processed_data.get('summary', {})
        
        # Generate insights based on data patterns
        if analysis_type == 'trends':
            insights['trends'] = self._analyze_trends_fallback(routes_data)
        elif analysis_type == 'pricing':
            insights['trends'] = self._analyze_pricing_fallback(routes_data)
        elif analysis_type == 'demand':
            insights['trends'] = self._analyze_demand_fallback(routes_data)
        else:
            insights['trends'] = self._analyze_general_fallback(routes_data, summary_data)
        
        # Generate recommendations
        insights['recommendations'] = self._generate_recommendations(routes_data, summary_data)
        
        return insights
    
    def _prepare_data_summary(self, processed_data):
        """Prepare a summary of the data for AI analysis"""
        summary = {
            'total_routes': len(processed_data.get('routes', {})),
            'route_statistics': {},
            'overall_summary': processed_data.get('summary', {})
        }
        
        for route, data in processed_data.get('routes', {}).items():
            if 'statistics' in data:
                stats = data['statistics']
                summary['route_statistics'][route] = {
                    'avg_price': stats.get('avg_price', 0),
                    'demand_score': stats.get('demand_score', 0),
                    'price_volatility': stats.get('price_volatility', 0),
                    'price_trend': stats.get('price_trend', 'unknown'),
                    'best_booking_window': stats.get('best_booking_window', {})
                }
        
        return summary
    
    def _create_trends_prompt(self, data_summary):
        """Create prompt for trend analysis"""
        return f"""
        Analyze the following airline booking data and provide insights about market trends:
        
        Data Summary:
        {json.dumps(data_summary, indent=2)}
        
        Please provide:
        1. Key market trends you observe
        2. Seasonal patterns or anomalies
        3. Price trend analysis for each route
        4. Recommendations for travelers and businesses
        5. Future market predictions based on current patterns
        
        Format your response as a structured analysis with clear sections.
        """
    
    def _create_pricing_prompt(self, data_summary):
        """Create prompt for pricing analysis"""
        return f"""
        Analyze the following airline pricing data and provide pricing insights:
        
        Data Summary:
        {json.dumps(data_summary, indent=2)}
        
        Please provide:
        1. Pricing patterns and strategies
        2. Price volatility analysis
        3. Optimal booking timing recommendations
        4. Price comparison across routes
        5. Factors affecting pricing decisions
        
        Focus on actionable pricing insights for travelers and businesses.
        """
    
    def _create_demand_prompt(self, data_summary):
        """Create prompt for demand analysis"""
        return f"""
        Analyze the following airline demand data and provide demand insights:
        
        Data Summary:
        {json.dumps(data_summary, indent=2)}
        
        Please provide:
        1. Demand patterns and drivers
        2. High-demand vs low-demand routes
        3. Seasonal demand variations
        4. Demand forecasting insights
        5. Business opportunities based on demand patterns
        
        Focus on demand analysis and market opportunities.
        """
    
    def _create_general_prompt(self, data_summary):
        """Create general analysis prompt"""
        return f"""
        Provide a comprehensive analysis of the following airline booking data:
        
        Data Summary:
        {json.dumps(data_summary, indent=2)}
        
        Please provide:
        1. Overall market overview
        2. Key insights and patterns
        3. Business implications
        4. Recommendations for different stakeholders
        5. Risk factors and opportunities
        
        Provide a balanced analysis covering multiple aspects of the airline market.
        """
    
    def _structure_ai_response(self, ai_response, analysis_type):
        """Structure the AI response into organized insights"""
        # This is a simple structure - in a real implementation, you might use
        # more sophisticated parsing or ask the AI to structure its response
        return {
            'analysis': ai_response,
            'key_points': self._extract_key_points(ai_response),
            'confidence_score': 0.85  # Placeholder
        }
    
    def _extract_key_points(self, ai_response):
        """Extract key points from AI response"""
        # Simple extraction - split by sentences and identify key points
        sentences = ai_response.split('. ')
        key_points = []
        
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in ['trend', 'increase', 'decrease', 'recommend', 'opportunity', 'risk']):
                key_points.append(sentence.strip())
        
        return key_points[:5]  # Limit to 5 key points
    
    def _analyze_trends_fallback(self, routes_data):
        """Fallback trend analysis"""
        trends = []
        
        for route, data in routes_data.items():
            if 'statistics' in data:
                stats = data['statistics']
                trend = stats.get('price_trend', 'stable')
                avg_price = stats.get('avg_price', 0)
                
                if trend == 'increasing':
                    trends.append(f"{route}: Prices are trending upward (avg: ${avg_price:.0f})")
                elif trend == 'decreasing':
                    trends.append(f"{route}: Prices are trending downward (avg: ${avg_price:.0f})")
                else:
                    trends.append(f"{route}: Prices are relatively stable (avg: ${avg_price:.0f})")
        
        return trends
    
    def _analyze_pricing_fallback(self, routes_data):
        """Fallback pricing analysis"""
        pricing_insights = []
        
        prices = []
        for route, data in routes_data.items():
            if 'statistics' in data:
                prices.append(data['statistics'].get('avg_price', 0))
        
        if prices:
            avg_price = sum(prices) / len(prices)
            min_price = min(prices)
            max_price = max(prices)
            
            pricing_insights.extend([
                f"Average ticket price across all routes: ${avg_price:.0f}",
                f"Price range: ${min_price:.0f} - ${max_price:.0f}",
                f"Price volatility: {max_price/min_price:.1f}x difference between cheapest and most expensive routes"
            ])
        
        return pricing_insights
    
    def _analyze_demand_fallback(self, routes_data):
        """Fallback demand analysis"""
        demand_insights = []
        
        high_demand_routes = []
        low_demand_routes = []
        
        for route, data in routes_data.items():
            if 'statistics' in data:
                demand_score = data['statistics'].get('demand_score', 5)
                if demand_score > 7:
                    high_demand_routes.append(route)
                elif demand_score < 4:
                    low_demand_routes.append(route)
        
        if high_demand_routes:
            demand_insights.append(f"High demand routes: {', '.join(high_demand_routes)}")
        if low_demand_routes:
            demand_insights.append(f"Low demand routes: {', '.join(low_demand_routes)}")
        
        return demand_insights
    
    def _analyze_general_fallback(self, routes_data, summary_data):
        """General fallback analysis"""
        insights = []
        
        total_routes = len(routes_data)
        insights.append(f"Analyzed {total_routes} routes")
        
        if summary_data:
            avg_price = summary_data.get('overall_avg_price', 0)
            insights.append(f"Overall average price: ${avg_price:.0f}")
            
            high_demand = summary_data.get('high_demand_routes', [])
            if high_demand:
                insights.append(f"High demand routes: {', '.join(high_demand)}")
        
        return insights
    
    def _generate_recommendations(self, routes_data, summary_data):
        """Generate recommendations based on data"""
        recommendations = []
        
        # Booking recommendations
        for route, data in routes_data.items():
            if 'statistics' in data:
                best_window = data['statistics'].get('best_booking_window', {})
                if best_window:
                    days_ahead = best_window.get('days_ahead', 7)
                    avg_price = best_window.get('avg_price', 0)
                    recommendations.append(f"Book {route} {days_ahead} days ahead for best prices (avg: ${avg_price:.0f})")
        
        # General recommendations
        if summary_data:
            high_demand_routes = summary_data.get('high_demand_routes', [])
            if high_demand_routes:
                recommendations.append(f"Consider alternative routes to avoid high demand: {', '.join(high_demand_routes)}")
        
        return recommendations[:5]  # Limit to 5 recommendations
