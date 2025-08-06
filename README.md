# NewsCheckr 📰🤖

> Full-stack ML-powered news analysis platform with React frontend

**NewsCheckr** analyzes news articles from any URL and provides credibility scores, political bias detection, and AI-generated summaries. Built with Python Flask backend and modern React frontend.

![NewsCheckr Screenshot](https://via.placeholder.com/800x400/4F46E5/FFFFFF?text=NewsCheckr+Interface)

## 🚀 Live Demo

Try it out: [Demo Link] (Add your deployed URL here)

## ✨ Key Features

### 🔍 **Article Analysis**
- **Credibility Scoring**: 0-100% reliability rating with color-coded progress bars
- **Political Bias Detection**: Left/Center/Right classification with visual indicators
- **Smart Labeling**: "Highly Reliable", "Needs Verification", "Likely Biased", etc.
- **Article Summarization**: AI-generated 1-2 sentence summaries

### 🌐 **Modern Web Interface** 
- Clean, responsive React frontend with Tailwind CSS
- Real-time analysis with loading states
- Color-coded bias badges (🔵 Left, 🔴 Right, ⚫ Center)
- Animated credibility progress bars
- Error handling with user-friendly messages

### 🧠 **Machine Learning Backend**
- **Credibility Classifier**: Random Forest with TF-IDF features
- **Bias Classifier**: Multinomial Naive Bayes for political lean detection
- **Text Summarization**: Multiple algorithms (LSA, TextRank, LexRank)
- **Source Intelligence**: Built-in ratings for 20+ major news outlets

### ⚡ **Technical Stack**
- **Backend**: Python Flask, scikit-learn, NLTK, newspaper4k
- **Frontend**: React 18, Tailwind CSS, modern hooks
- **Deployment**: Docker ready, CORS enabled

## 🎯 How It Works

1. **Enter URL** → User pastes any news article URL
2. **Smart Scraping** → Extracts article content and metadata  
3. **ML Analysis** → Runs through credibility and bias models
4. **Generate Summary** → Creates concise summary using NLP
5. **Visual Results** → Displays scores, badges, and insights

## 📊 Sample Analysis

```json
{
  "source": "reuters.com",
  "credibility_score": 87.4,
  "bias": "Center", 
  "summary": "The Federal Reserve announced a 0.25% rate increase...",
  "labels": ["Highly Reliable", "Well-sourced"]
}
```

## 🏗️ Architecture

```
┌─────────────────┐    HTTP/JSON    ┌──────────────────┐
│   React Frontend │ ──────────────► │   Flask API      │
│   (Port 3000)   │                 │   (Port 5001)    │
└─────────────────┘                 └──────────────────┘
        │                                    │
        ├── URL Input                        ├── Web Scraping
        ├── Loading States                   ├── ML Classification  
        ├── Results Display                  ├── Text Summarization
        └── Error Handling                   └── Source Intelligence
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- Git

### Backend Setup
```bash
git clone https://github.com/siddhanthgouru/NewsCheckr.git
cd NewsCheckr

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python3 -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# Start API server
python3 api.py
```

### Frontend Setup
```bash
# New terminal window
cd NewsCheckr/frontend

# Install dependencies
npm install

# Start development server
npm start
```

Visit `http://localhost:3000` to use the application!

## 📁 Project Structure

```
NewsCheckr/
├── 🐍 Backend (Python Flask)
│   ├── api.py              # Main Flask application
│   ├── scraper.py          # Web scraping (newspaper4k)
│   ├── models.py           # ML models (credibility & bias)
│   ├── summarizer.py       # Text summarization
│   └── test_examples.py    # Test data and examples
│
├── ⚛️ Frontend (React)
│   ├── src/
│   │   ├── App.js          # Main application
│   │   └── components/     # React components
│   │       ├── CredibilityBar.js  # Progress bar
│   │       ├── BiasBadge.js       # Political bias
│   │       └── ResultsDisplay.js  # Results layout
│   └── package.json        # Node.js dependencies
│
└── 📚 Documentation
    ├── README.md           # This file
    └── requirements.txt    # Python dependencies
```

## 🔧 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check and API info |
| POST | `/analyze` | Analyze article from URL |
| POST | `/test` | Test with raw text |
| GET | `/sources` | List known sources |
| GET | `/debug` | Debug model status |

### Example API Usage

```bash
curl -X POST http://localhost:5001/analyze \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.reuters.com/business/economy/"}'
```

## 🎨 UI Components

### Credibility Bar
- 🟢 **80-100%**: High credibility (green)
- 🟡 **60-79%**: Medium credibility (yellow)  
- 🟠 **40-59%**: Low credibility (orange)
- 🔴 **0-39%**: Very low credibility (red)

### Political Bias Badges
- 🔵 **Left**: Blue badge with ← arrow
- 🔴 **Right**: Red badge with → arrow  
- ⚫ **Center**: Gray badge with ● dot

### Analysis Labels
- 🟢 **Reliable**: "Highly Reliable", "Well-sourced", "Factual"
- 🔴 **Questionable**: "Biased", "Clickbait", "Satire"
- 🟡 **Mixed**: "Needs Verification", "Mixed Reliability"

## 🚀 Deployment

### Docker Deployment
```bash
# Build and run with Docker
docker build -t newscheckr .
docker run -p 5001:5001 newscheckr
```

### Production Considerations
- Use Gunicorn for Flask production server
- Deploy frontend to CDN (Netlify, Vercel)
- Add Redis caching for article results
- Implement rate limiting and authentication
- Use real ML training data for better accuracy

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [newspaper4k](https://github.com/AndyTheFactory/newspaper4k) for article extraction
- [scikit-learn](https://scikit-learn.org/) for ML models
- [React](https://reactjs.org/) and [Tailwind CSS](https://tailwindcss.com/) for the frontend
- [NLTK](https://www.nltk.org/) for natural language processing

## 📧 Contact

Siddhanth Gouru - [@siddhanthgouru](https://twitter.com/siddhanthgouru) - siddhanth.gouru@example.com

Project Link: [https://github.com/siddhanthgouru/NewsCheckr](https://github.com/siddhanthgouru/NewsCheckr)

---

⭐ **Star this repo if you found it helpful!** ⭐