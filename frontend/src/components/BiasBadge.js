import React from 'react';

const BiasBadge = ({ bias }) => {
  const getBiasStyles = (bias) => {
    switch (bias?.toLowerCase()) {
      case 'left':
        return {
          bg: 'bg-blue-500',
          text: 'text-white',
          icon: '←'
        };
      case 'right':
        return {
          bg: 'bg-red-500',
          text: 'text-white',
          icon: '→'
        };
      case 'center':
      default:
        return {
          bg: 'bg-gray-500',
          text: 'text-white',
          icon: '●'
        };
    }
  };

  const styles = getBiasStyles(bias);

  return (
    <div className={`inline-flex items-center px-4 py-2 rounded-full font-semibold text-sm ${styles.bg} ${styles.text}`}>
      <span className="mr-2 text-lg">{styles.icon}</span>
      <span>{bias || 'Unknown'}</span>
    </div>
  );
};

export default BiasBadge;