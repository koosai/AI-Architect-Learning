import React, { useState, useRef, useEffect } from 'react';
import styles from './styles.module.css';

interface CompareSliderProps {
  before: string | React.ReactNode;
  after: string | React.ReactNode;
  labels?: string[]; // E.g. ['旧架构', '新架构']
}

export default function CompareSlider({ before, after, labels = ['旧架构', '新架构'] }: CompareSliderProps): JSX.Element {
  const [sliderPosition, setSliderPosition] = useState(50); // percentage (0-100)
  const containerRef = useRef<HTMLDivElement>(null);
  const isDragging = useRef(false);

  const handleMove = (clientX: number) => {
    if (!containerRef.current) return;
    const rect = containerRef.current.getBoundingClientRect();
    const x = clientX - rect.left;
    const percentage = Math.min(100, Math.max(0, (x / rect.width) * 100));
    setSliderPosition(percentage);
  };

  const handleTouchMove = (e: TouchEvent) => {
    if (!isDragging.current) return;
    handleMove(e.touches[0].clientX);
  };

  const handleMouseMove = (e: MouseEvent) => {
    if (!isDragging.current) return;
    handleMove(e.clientX);
  };

  const handleMouseUp = () => {
    isDragging.current = false;
    document.removeEventListener('mousemove', handleMouseMove);
    document.removeEventListener('mouseup', handleMouseUp);
  };

  const handleTouchEnd = () => {
    isDragging.current = false;
    document.removeEventListener('touchmove', handleTouchMove);
    document.removeEventListener('touchend', handleTouchEnd);
  };

  const handleMouseDown = (e: React.MouseEvent) => {
    e.preventDefault();
    isDragging.current = true;
    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);
  };

  const handleTouchStart = () => {
    isDragging.current = true;
    document.addEventListener('touchmove', handleTouchMove, { passive: true });
    document.addEventListener('touchend', handleTouchEnd);
  };

  // Clean up event listeners on unmount
  useEffect(() => {
    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
      document.removeEventListener('touchmove', handleTouchMove);
      document.removeEventListener('touchend', handleTouchEnd);
    };
  }, []);

  const renderContent = (content: string | React.ReactNode) => {
    if (typeof content === 'string') {
      return <img src={content} alt="architecture comparison" draggable="false" />;
    }
    return content;
  };

  return (
    <div className={styles.container} ref={containerRef}>
      {/* Before Content (Base) */}
      <div className={styles.beforeWrapper}>
        <div className={styles.imageWrapper}>
          {renderContent(before)}
        </div>
        {labels[0] && <div className={`${styles.label} ${styles.labelBefore}`}>{labels[0]}</div>}
      </div>

      {/* After Content (Overlayed) */}
      <div className={styles.afterWrapper} style={{ width: `${sliderPosition}%` }}>
        {/* We need a wrapper with full container width to avoid shrinking */}
        <div
          className={styles.imageWrapper}
          style={{ width: containerRef.current ? containerRef.current.getBoundingClientRect().width : '100%' }}
        >
          {renderContent(after)}
        </div>
        {labels[1] && <div className={`${styles.label} ${styles.labelAfter}`}>{labels[1]}</div>}
      </div>

      {/* Dragging Handle */}
      <div
        className={styles.handle}
        style={{ left: `${sliderPosition}%` }}
        onMouseDown={handleMouseDown}
        onTouchStart={handleTouchStart}
      >
        <div className={styles.handleButton}>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="11 17 6 12 11 7"></polyline>
            <polyline points="13 17 18 12 13 7"></polyline>
          </svg>
        </div>
      </div>
    </div>
  );
}
