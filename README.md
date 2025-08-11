# Airline Booking Market Demand Analyzer

A comprehensive web application for analyzing airline booking market demand trends, pricing patterns, and providing actionable insights for the Australian airline industry.

## Features

### 🚀 Core Functionality
- **Data Scraping**: Fetch airline booking data from multiple sources (Skyscanner, Google Flights, mock data)
- **AI-Powered Analysis**: Intelligent insights using OpenAI API (with fallback analysis)
- **Interactive Visualizations**: Dynamic charts and graphs using Plotly
- **Real-time Processing**: Clean and process data to extract meaningful insights
- **Responsive Web Interface**: Modern, user-friendly dashboard

### 📊 Analysis Capabilities
- **Price Trend Analysis**: Track pricing patterns over time
- **Demand Scoring**: Calculate demand scores based on multiple factors
- **Route Comparison**: Compare different airline routes
- **Booking Optimization**: Find optimal booking windows
- **Market Insights**: Identify high-demand periods and locations

### 🎯 Key Insights Provided
- Popular routes and demand patterns
- Price trends and volatility analysis
- Seasonal variations and anomalies
- Optimal booking timing recommendations
- Business opportunities and risk factors

## Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly
- **AI Integration**: OpenAI API
- **Web Scraping**: BeautifulSoup, Selenium
- **Data Sources**: Skyscanner, Google Flights (mock implementations)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone or download the project**
   ```bash
   cd airline_booking_analyzer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration** (Optional)
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key for enhanced AI analysis:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     AVIATIONSTACK_API_KEY=your_aviationstack_api_key_here
     ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the web interface**
   - Open your browser and go to: `http://localhost:5000`

## Usage

### Getting Started
1. **Select Data Source**: Choose between mock data (for demo) or real sources
2. **Configure Routes**: Select the airline routes you want to analyze
3. **Set Time Range**: Choose how many days ahead to analyze (7-90 days)
4. **Run Analysis**: Click "Analyze" to fetch and process data

### Understanding the Results

#### Market Summary
- **Total Routes**: Number of routes analyzed
- **Average Price**: Overall average ticket price
- **Price Range**: Minimum to maximum prices across routes
- **High Demand Routes**: Routes with highest demand scores

#### Visualizations
- **Price Trends**: Line charts showing price changes over time
- **Demand Heatmap**: Color-coded demand scores for each route
- **Route Comparison**: Bar charts comparing prices and demand across routes

#### AI Insights
- **Trends**: Market trend analysis and patterns
- **Recommendations**: Actionable advice for travelers and businesses

## Project Structure

```
airline_booking_analyzer/
├── app.py                 # Main Flask application
├── data_scraper.py        # Data fetching and scraping logic
├── data_processor.py      # Data processing and analysis
├── ai_analyzer.py         # AI-powered insights
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── .env.example          # Environment variables template
└── templates/
    └── index.html        # Main web interface
```

## API Endpoints

### Data Fetching
- `POST /api/fetch-data` - Fetch airline booking data
- `GET /api/routes` - Get available routes
- `GET /api/sample-data` - Get sample data for demonstration
- `POST /api/flight-status` - Get real-time flight status by flight number
- `POST /api/airport-info` - Get airport information by IATA code
- `POST /api/airline-info` - Get airline information by IATA code
- `POST /api/historical-flights` - Get historical flights for a route and date

### Analysis
- `POST /api/analyze` - Get AI-powered insights
- `POST /api/charts` - Generate visualization charts

## Data Sources

### Current Implementation
- **Mock Data**: Realistic simulated data for demonstration
- **Skyscanner**: Placeholder for Skyscanner integration
- **Google Flights**: Placeholder for Google Flights integration

### Future Enhancements
- Real-time data scraping from airline websites
- Integration with travel APIs
- Historical data analysis
- Predictive modeling
- Real-time flight status, airport and airline lookup, historical flight data (Aviationstack)

## Customization

### Adding New Routes
Edit the `get_available_routes()` function in `app.py` to add new airline routes.

### Modifying Analysis Logic
Update the `DataProcessor` class in `data_processor.py` to customize analysis algorithms.

### Enhancing AI Insights
Modify the `AIAnalyzer` class in `ai_analyzer.py` to improve AI-powered analysis.

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`

2. **Port Already in Use**
   - Change the port in `app.py`: `app.run(debug=True, host='0.0.0.0', port=5001)`

3. **AI Analysis Not Working**
   - Check if OpenAI API key is set in `.env` file
   - The app will use fallback analysis if no API key is provided

4. **Charts Not Displaying**
   - Ensure internet connection for Plotly CDN
   - Check browser console for JavaScript errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For questions or issues:
1. Check the troubleshooting section
2. Review the code comments
3. Create an issue in the repository

## Future Roadmap

- [ ] Real-time data scraping
- [ ] Advanced predictive analytics
- [ ] Mobile app version
- [ ] Multi-language support
- [ ] Export functionality
- [ ] User authentication
- [ ] Historical data storage
- [ ] Email alerts for price changes

---

**Advanced Features**
- Real-time flight status lookup
- Airport and airline information lookup
- Historical flight data for route/date
- Simple in-memory caching for API responses (see data_scraper.py)

**Note**: This application is designed for educational and demonstration purposes. For production use, ensure compliance with data usage policies and implement proper security measures.
