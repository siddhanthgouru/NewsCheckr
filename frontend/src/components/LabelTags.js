import React from 'react';

const LabelTags = ({ labels }) => {
  const getLabelStyles = (label) => {
    const lowercaseLabel = label?.toLowerCase() || '';
    
    // Color mapping for different types of labels
    if (lowercaseLabel.includes('reliable') || lowercaseLabel.includes('factual') || lowercaseLabel.includes('well-sourced')) {
      return 'bg-green-100 text-green-800 border-green-200';
    }
    
    if (lowercaseLabel.includes('biased') || lowercaseLabel.includes('satire') || lowercaseLabel.includes('clickbait')) {
      return 'bg-red-100 text-red-800 border-red-200';
    }
    
    if (lowercaseLabel.includes('verification') || lowercaseLabel.includes('mixed') || lowercaseLabel.includes('needs')) {
      return 'bg-yellow-100 text-yellow-800 border-yellow-200';
    }
    
    // Default style for other labels
    return 'bg-blue-100 text-blue-800 border-blue-200';
  };

  if (!labels || labels.length === 0) {
    return null;
  }

  return (
    <div className="flex flex-wrap gap-2">
      {labels.map((label, index) => (
        <span
          key={index}
          className={`inline-flex items-center px-3 py-1.5 rounded-full text-sm font-medium border transition-colors duration-200 ${getLabelStyles(label)}`}
        >
          {label}
        </span>
      ))}
    </div>
  );
};

export default LabelTags;