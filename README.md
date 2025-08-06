# NewsCheckr

> Full-stack ML-powered news analysis platform with React frontend

**NewsCheckr** analyzes news articles from any URL and provides credibility scores, political bias detection, and AI-generated summaries. Built with Python Flask backend and modern React frontend.

## Key Features

### Article Analysis
- **Credibility Scoring**: 0-100% reliability rating with color-coded progress bars
- **Political Bias Detection**: Left/Center/Right classification with visual indicators
- **Smart Labeling**: "Highly Reliable", "Needs Verification", "Likely Biased", etc.
- **Article Summarization**: AI-generated 1-2 sentence summaries

### Modern Web Interface
- Clean, responsive React frontend with Tailwind CSS
- Real-time analysis with loading states
- Color-coded bias badges (Blue Left, Red Right, Gray Center)
- Animated credibility progress bars
- Error handling with user-friendly messages

### Machine Learning Backend
- **Credibility Classifier**: Random Forest with TF-IDF features
- **Bias Classifier**: Multinomial Naive Bayes for political lean detection
- **Text Summarization**: Multiple algorithms (LSA, TextRank, LexRank)
- **Source Intelligence**: Built-in ratings for 20+ major news outlets

### Technical Stack
- **Backend**: Python Flask, scikit-learn, NLTK, newspaper4k
- **Frontend**: React 18, Tailwind CSS, modern hooks
- **Deployment**: Docker ready, CORS enabled

## How It Works

1. **Enter URL** - User pastes any news article URL
2. **Smart Scraping** - Extracts article content and metadata  
3. **ML Analysis** - Runs through credibility and bias models
4. **Generate Summary** - Creates concise summary using NLP
5. **Visual Results** - Displays scores, badges, and insights

## Sample Analysis

```json
{
  "source": "reuters.com",
  "credibility_score": 87.4,
  "bias": "Center", 
  "summary": "The Federal Reserve announced a 0.25% rate increase...",
  "labels": ["Highly Reliable", "Well-sourced"]
}
```


## Installation & Setup

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

## UI Components

### Credibility Bar
- **80-100%**: High credibility (green)
- **60-79%**: Medium credibility (yellow)  
- **40-59%**: Low credibility (orange)
- **0-39%**: Very low credibility (red)

### Political Bias Badges
- **Left**: Blue badge with arrow
- **Right**: Red badge with arrow  
- **Center**: Gray badge with dot

### Analysis Labels
- **Reliable**: "Highly Reliable", "Well-sourced", "Factual"
- **Questionable**: "Biased", "Clickbait", "Satire"
- **Mixed**: "Needs Verification", "Mixed Reliability"

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [newspaper4k](https://github.com/AndyTheFactory/newspaper4k) for article extraction
- [scikit-learn](https://scikit-learn.org/) for ML models
- [React](https://reactjs.org/) and [Tailwind CSS](https://tailwindcss.com/) for the frontend
- [NLTK](https://www.nltk.org/) for natural language processing

## Contact

Siddhanth Gouru - [@siddhanthgouru](https://twitter.com/siddhanthgouru) - siddhanth.gouru@example.com

Project Link: [https://github.com/siddhanthgouru/NewsCheckr](https://github.com/siddhanthgouru/NewsCheckr)