<<<<<<< HEAD
# AgriVoice - Enhanced AI-Powered Farming Assistant

A comprehensive farming assistant application with machine learning capabilities, built with Django REST Framework backend and React frontend.

## 🚀 Features

### 🤖 AI & Machine Learning
- **ML-Enhanced Crop Prediction**: Uses Random Forest classifier trained on environmental data
- **AI Assistant**: Powered by OpenAI GPT-3.5-turbo and Sarvam AI with conversation memory
- **Smart Recommendations**: Context-aware farming advice

### 🔐 Authentication & Security
- **Token-based Authentication**: Secure user sessions with Django REST Framework
- **User Management**: Registration and login system
- **Protected Endpoints**: All API endpoints require authentication

### 📊 Data Management
- **Query History**: Track all user questions and AI responses
- **Prediction History**: Store and review crop predictions
- **Conversation Memory**: AI remembers previous interactions

### 🌾 Farming Tools
- **Crop Library**: Comprehensive database of crop information
- **Soil Advisor**: Personalized soil management recommendations
- **Weather Integration**: Real-time weather data and forecasting
- **Voice Commands**: Speech-to-text for hands-free operation

### 🎨 Visual Design
- **Realistic Images**: High-quality farming and crop photography from Unsplash
- **Modern UI**: Clean Material-UI components with professional styling
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices

### 🖼️ Image Customization
The application uses high-quality images from Unsplash (free for commercial use). To customize images:
1. Replace image URLs in component files (Dashboard.js, CropLibrary.js, etc.)
2. Use your own images by placing them in `src/assets/` and importing them
3. All images are optimized for web delivery with appropriate sizing

## 🛠️ Technology Stack

### Backend
- **Django 4.x**: Web framework
- **Django REST Framework**: API development
- **SQLite**: Database
- **Scikit-learn**: Machine learning
- **OpenAI API**: AI responses
- **Joblib**: Model serialization

### Frontend
- **React 18**: UI framework
- **Material-UI**: Component library
- **React Router**: Navigation
- **Axios**: HTTP client
- **Framer Motion**: Animations

## 📦 Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- Git

### Backend Setup

1. **Clone and navigate to backend:**
   ```bash
   cd d:\agrivoice\backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Train ML model:**
   ```bash
   python ml_model/train.py
   ```

6. **Start Django server:**
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. **Navigate to React app:**
   ```bash
   cd d:\agrivoice\agrivoice-ui
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm start
   ```

## 🔧 Configuration

### OpenAI API Key
Add your OpenAI API key to `backend/agrivoice/settings.py`:
```python
OPENAI_API_KEY = "your-api-key-here"
```

### Sarvam AI API Key
Add your Sarvam AI API key to `backend/agrivoice/settings.py`:
```python
SARVAM_API_KEY = "your-api-key-here"
```

### Weather API
The app uses OpenWeatherMap API (free tier included).

## 📊 ML Model Details

### Training Data
- **Features**: Rainfall, Temperature, Humidity, Soil pH
- **Crops**: Rice, Wheat, Maize, Cotton, Sugarcane, Soybean, Potato, Tomato
- **Algorithm**: Random Forest Classifier
- **Accuracy**: ~38.5% (can be improved with more data)

### Model Enhancement
To improve accuracy:
1. Add more training data
2. Include additional features (soil nutrients, pest data)
3. Use more advanced algorithms (Neural Networks)
4. Implement cross-validation

## 🌐 API Endpoints

### Authentication
- `POST /api/auth/token/login/` - User login
- `POST /api/auth/users/` - User registration

### Core Features
- `GET /api/crops/` - Get crop library
- `POST /api/predict/` - ML crop prediction
- `POST /api/ask/` - AI assistant query (supports model parameter: "openai" or "sarvam")
- `POST /api/soil/` - Soil advice
- `POST /api/forecast/` - Weather forecast

### History & Memory
- `GET /api/history/` - Query history
- `GET /api/predictions/` - Prediction history
- `GET /api/conversation/` - Full conversation log

## 🚀 Deployment

### Backend Deployment
```bash
# Production settings
python manage.py collectstatic
# Use Gunicorn or similar WSGI server
```

### Frontend Deployment
```bash
npm run build
# Serve build/ directory with nginx/apache
```

## 📈 Future Enhancements

- **Advanced ML Models**: Neural networks for better predictions
- **Real-time Data**: IoT sensor integration
- **Mobile App**: React Native implementation
- **Multi-language**: Support for local languages
- **Offline Mode**: Progressive Web App features
- **Analytics Dashboard**: Farming insights and trends

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📄 License

MIT License - see LICENSE file for details

## 📞 Support

For questions or issues:
- Create an issue on GitHub
- Check the documentation
- Review the code comments

---

**AgriVoice** - Empowering farmers with AI and data-driven insights 🌱
=======
# AgriVoice-Ai-assistent
>>>>>>> 2de018adac229ccf469340f8131008586dc515ff
