import React from 'react';

const CredibilityBar = ({ score }) => {
  // Determine color based on score
  const getScoreColor = (score) => {
    if (score >= 80) return 'bg-green-500';
    if (score >= 60) return 'bg-yellow-500';
    if (score >= 40) return 'bg-orange-500';
    return 'bg-red-500';
  };

  const getScoreLabel = (score) => {
    if (score >= 80) return 'High';
    if (score >= 60) return 'Medium';
    if (score >= 40) return 'Low';
    return 'Very Low';
  };

  const scoreColor = getScoreColor(score);
  const scoreLabel = getScoreLabel(score);

  return (
    <div className="space-y-2">
      {/* Score and Label */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <span className="text-3xl font-bold text-gray-800">
            {score.toFixed(1)}%
          </span>
          <span className={`px-3 py-1 rounded-full text-sm font-semibold text-white ${scoreColor}`}>
            {scoreLabel} Credibility
          </span>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="w-full bg-gray-200 rounded-full h-4 overflow-hidden">
        <div
          className={`h-full rounded-full transition-all duration-1000 ease-out ${scoreColor}`}
          style={{ 
            width: `${Math.min(score, 100)}%`,
            transition: 'width 1.5s ease-out'
          }}
        />
      </div>

      {/* Scale Labels */}
      <div className="flex justify-between text-xs text-gray-500 mt-1">
        <span>0%</span>
        <span>25%</span>
        <span>50%</span>
        <span>75%</span>
        <span>100%</span>
      </div>
    </div>
  );
};

export default CredibilityBar;