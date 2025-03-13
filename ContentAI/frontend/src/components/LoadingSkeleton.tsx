import React from 'react';

interface LoadingSkeletonProps {
  count?: number;
  height?: string;
  width?: string;
  className?: string;
}

const LoadingSkeleton: React.FC<LoadingSkeletonProps> = ({
  count = 1,
  height = '20px',
  width = '100%',
  className = ''
}) => {
  return (
    <>
      {Array(count).fill(0).map((_, i) => (
        <div
          key={i}
          className={`loading-skeleton ${className}`}
          style={{ height, width, marginBottom: '10px' }}
        />
      ))}
    </>
  );
};

export default LoadingSkeleton;
