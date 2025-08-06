# NewsCheckr Frontend

React-based frontend for the NewsCheckr ML news analysis API. Provides a clean, responsive interface for analyzing news article credibility and political bias.

## Features

- **Single-page interface** - No routing, simple and focused
- **URL input and analysis** - Enter any news article URL for analysis
- **Real-time loading states** - Animated spinner during API calls
- **Rich results display**:
  - Article summary as plain text
  - Credibility score with animated progress bar
  - Color-coded political bias badges (Blue=Left, Red=Right, Gray=Center)
  - Analysis labels as styled pill tags
- **Comprehensive error handling** - User-friendly error messages
- **Responsive design** - Built with Tailwind CSS
- **Modern React patterns** - Hooks, functional components

## Quick Start

### Prerequisites

- Node.js 16+ installed
- NewsCheckr backend API running on `http://localhost:5000`

### Installation

```bash
# Navigate to frontend directory
cd NewsCheckr/frontend

# Install dependencies
npm install

# Start development server
npm start
```

The app will open at `http://localhost:3000`

## Project Structure

```
frontend/
├── public/
│   └── index.html          # HTML template
├── src/
│   ├── components/         # Reusable React components
│   │   ├── BiasBadge.js    # Political bias indicator
│   │   ├── CredibilityBar.js # Animated progress bar
│   │   ├── ErrorMessage.js  # Error display component
│   │   ├── LabelTags.js     # Pill-style labels
│   │   ├── LoadingSpinner.js # Loading animation
│   │   └── ResultsDisplay.js # Main results container
│   ├── App.js              # Main application component
│   ├── index.js            # React entry point
│   └── index.css           # Tailwind CSS imports
├── package.json            # Dependencies and scripts
├── tailwind.config.js      # Tailwind configuration
└── postcss.config.js       # PostCSS configuration
```

## Components Overview

### App.js
- Main application component
- Manages state (URL input, loading, results, errors)
- Handles API calls to backend
- Coordinates all child components

### BiasBadge.js
- Displays political bias with color coding:
  - **Blue (Left)**: ← Left
  - **Red (Right)**: → Right  
  - **Gray (Center)**: ● Center

### CredibilityBar.js
- Animated horizontal progress bar
- Color-coded by score:
  - **Green**: 80-100% (High)
  - **Yellow**: 60-79% (Medium)
  - **Orange**: 40-59% (Low)
  - **Red**: 0-39% (Very Low)

### LabelTags.js
- Pill-style tags for analysis labels
- Color-coded by content:
  - **Green**: "Reliable", "Factual", "Well-sourced"
  - **Red**: "Biased", "Satire", "Clickbait"
  - **Yellow**: "Verification", "Mixed", "Needs"
  - **Blue**: Default for other labels

### LoadingSpinner.js
- Reusable animated loading spinner
- Multiple sizes (sm, md, lg)
- CSS-based animations

### ErrorMessage.js
- User-friendly error display
- Dismissible with close button
- Styled for visibility without being intrusive

### ResultsDisplay.js
- Main container for analysis results
- Integrates all result components
- Shows metadata and disclaimers

## API Integration

The frontend calls the NewsCheckr backend API:

```javascript
// Main analysis endpoint
POST http://localhost:5000/analyze
{
  "url": "https://example.com/news-article"
}

// Expected response
{
  "source": "example.com",
  "credibility_score": 87.4,
  "bias": "Center",
  "summary": "Article summary...",
  "labels": ["Factual", "Well-sourced"],
  "metadata": { ... }
}
```

## Styling

Built with **Tailwind CSS** for:
- Responsive design
- Consistent spacing and colors
- Utility-first approach
- Easy customization

### Key Design Elements

- **Gradient backgrounds** - Blue to indigo gradients
- **Card-based layout** - Clean white cards with shadows
- **Color system**:
  - Blue: Primary actions and left bias
  - Red: Right bias and errors
  - Green: Success and high credibility
  - Yellow: Warnings and medium credibility
  - Gray: Neutral and center bias

## Development

### Available Scripts

```bash
# Development server
npm start

# Production build
npm run build

# Run tests
npm test

# Eject from Create React App (not recommended)
npm run eject
```

### Environment Setup

The app uses a proxy configuration to connect to the backend:

```json
// In package.json
"proxy": "http://localhost:5000"
```

This allows calls to `/analyze` to be automatically proxied to `http://localhost:5000/analyze`

## Error Handling

Comprehensive error handling for:

- **Invalid URLs** - Client-side validation
- **Network errors** - Connection failures to backend
- **API errors** - Backend error responses
- **Timeout errors** - Long-running requests
- **Parsing errors** - Malformed responses

Error messages are user-friendly and actionable.

## Browser Support

Supports all modern browsers:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Production Deployment

### Build for Production

```bash
npm run build
```

This creates an optimized build in the `build/` directory.

### Deployment Options

1. **Static Hosting** (Netlify, Vercel, GitHub Pages)
2. **Traditional Web Server** (Nginx, Apache)
3. **Docker Container**

### Environment Variables

For production, you may need to configure:

```bash
# Backend API URL (if different from localhost:5000)
REACT_APP_API_URL=https://api.newscheckr.com
```

Then update the fetch URL in `App.js`:

```javascript
const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:5000';
const response = await fetch(`${apiUrl}/analyze`, {...});
```

## Performance

- **Fast loading** - Optimized React build
- **Lazy loading** - Components load as needed
- **Efficient re-renders** - React hooks and state management
- **Small bundle size** - Tree-shaking and code splitting

## Customization

### Adding New Features

1. **New Analysis Types** - Add components similar to `BiasBadge.js`
2. **Additional Visualizations** - Extend `ResultsDisplay.js`
3. **More Input Types** - Add text input, file upload, etc.
4. **Themes** - Customize Tailwind configuration

### Styling Changes

Modify `tailwind.config.js` for:
- Custom colors
- New spacing
- Additional animations
- Font changes

## Troubleshooting

### Common Issues

1. **Backend not running**
   - Error: "Unable to connect to NewsCheckr API"
   - Solution: Start the Flask backend on port 5000

2. **CORS errors**
   - Error: "Cross-origin request blocked"
   - Solution: Backend includes CORS headers

3. **Build failures**
   - Check Node.js version (16+ required)
   - Clear `node_modules` and reinstall

4. **Styling not applied**
   - Ensure Tailwind is properly configured
   - Check `index.css` imports Tailwind directives

## Contributing

To contribute to the frontend:

1. Follow React best practices
2. Use functional components and hooks
3. Maintain TypeScript compatibility (if adding types)
4. Add proper PropTypes for components
5. Write tests for new components
6. Follow the existing code style

## License

Part of the NewsCheckr project. For demonstration purposes.