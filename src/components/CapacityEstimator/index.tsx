import React, { useState } from 'react';
import styles from './styles.module.css';

export default function CapacityEstimator(): JSX.Element {
  const [dau, setDau] = useState(10); // in Millions (10M default)
  const [reqsPerDay, setReqsPerDay] = useState(20); // requests per day
  const [readRatio, setReadRatio] = useState(90); // 90% read default
  const [readSize, setReadSize] = useState(50); // KB
  const [writeSize, setWriteSize] = useState(10); // KB
  const [retention, setRetention] = useState(365); // 365 days

  // Calculations
  const dauRaw = dau * 1000000;
  const dailyTotalReqs = dauRaw * reqsPerDay;
  const avgQps = Math.round(dailyTotalReqs / 86400);
  const peakQps = Math.round(avgQps * 2);

  const readQps = avgQps * (readRatio / 100);
  const writeQps = avgQps * (1 - readRatio / 100);

  // Network Bandwidth in Mbps: QPS * Size(KB) * 8(bits/byte) / 1024(KB/MB)
  const readBandwidth = Math.round((readQps * readSize * 8) / 1024 * 10) / 10;
  const writeBandwidth = Math.round((writeQps * writeSize * 8) / 1024 * 10) / 10;
  const totalBandwidth = Math.round((readBandwidth + writeBandwidth) * 10) / 10;

  // Storage calculation: Daily write size = writeQps * 86400 * writeSize(KB)
  // in GB: writeQps * 86400 * writeSize / 1024 / 1024
  const dailyWriteGb = Math.round((writeQps * 86400 * writeSize) / (1024 * 1024) * 10) / 10;
  const totalStorageTb = Math.round((dailyWriteGb * retention) / 1024 * 10) / 10;

  const formatNumber = (num: number) => {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  };

  return (
    <div className={styles.card}>
      <h4 className={styles.title}>
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
          <rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect>
          <line x1="16" y1="11" x2="16" y2="16"></line>
          <line x1="12" y1="11" x2="12" y2="16"></line>
          <line x1="8" y1="11" x2="8" y2="16"></line>
          <line x1="12" y1="7" x2="12.01" y2="7"></line>
        </svg>
        系统容量估算器 (Capacity & QPS Estimator)
      </h4>

      <div className={styles.layout}>
        <div className={styles.inputsPane}>
          <div className={styles.sliderGroup}>
            <div className={styles.sliderHeader}>
              <span>日活用户数 (DAU)</span>
              <span className={styles.sliderVal}>{dau} M (百万)</span>
            </div>
            <input
              type="range"
              min="1"
              max="100"
              value={dau}
              onChange={(e) => setDau(Number(e.target.value))}
              className={styles.inputSlider}
            />
          </div>

          <div className={styles.sliderGroup}>
            <div className={styles.sliderHeader}>
              <span>人均每日请求数</span>
              <span className={styles.sliderVal}>{reqsPerDay} 次</span>
            </div>
            <input
              type="range"
              min="1"
              max="100"
              value={reqsPerDay}
              onChange={(e) => setReqsPerDay(Number(e.target.value))}
              className={styles.inputSlider}
            />
          </div>

          <div className={styles.sliderGroup}>
            <div className={styles.sliderHeader}>
              <span>读写比例 (Read Ratio)</span>
              <span className={styles.sliderVal}>{readRatio}% 读 / {100 - readRatio}% 写</span>
            </div>
            <input
              type="range"
              min="50"
              max="99"
              value={readRatio}
              onChange={(e) => setReadRatio(Number(e.target.value))}
              className={styles.inputSlider}
            />
          </div>

          <div className={styles.sliderGroup}>
            <div className={styles.sliderHeader}>
              <span>读 / 写单次 Payload 大小</span>
              <span className={styles.sliderVal}>{readSize} KB (读) / {writeSize} KB (写)</span>
            </div>
            <div style={{ display: 'flex', gap: '1rem', marginTop: '0.2rem' }}>
              <input
                type="range"
                min="1"
                max="500"
                value={readSize}
                onChange={(e) => setReadSize(Number(e.target.value))}
                className={styles.inputSlider}
                style={{ flex: 1 }}
              />
              <input
                type="range"
                min="1"
                max="100"
                value={writeSize}
                onChange={(e) => setWriteSize(Number(e.target.value))}
                className={styles.inputSlider}
                style={{ flex: 1 }}
              />
            </div>
          </div>

          <div className={styles.sliderGroup}>
            <div className={styles.sliderHeader}>
              <span>数据保留时长 (Retention)</span>
              <span className={styles.sliderVal}>{retention} 天</span>
            </div>
            <input
              type="range"
              min="30"
              max="1000"
              value={retention}
              onChange={(e) => setRetention(Number(e.target.value))}
              className={styles.inputSlider}
            />
          </div>
        </div>

        <div className={styles.resultsPane}>
          <div className={styles.resultTitle}>估算输出 (Estimated Outputs)</div>
          <div className={styles.resultsList}>
            <div className={styles.resultRow}>
              <span className={styles.resultName}>平均 QPS (Avg QPS)</span>
              <span className={styles.resultVal}>{formatNumber(avgQps)} /s</span>
            </div>
            <div className={styles.resultRow}>
              <span className={styles.resultName}>峰值 QPS (Peak QPS)</span>
              <span className={styles.resultVal} style={{ color: 'var(--brand-yellow)' }}>
                {formatNumber(peakQps)} /s
              </span>
            </div>
            <div className={styles.resultRow}>
              <span className={styles.resultName}>网络总带宽 (Bandwidth)</span>
              <span className={styles.resultVal} style={{ color: 'var(--brand-cyan)' }}>
                {formatNumber(totalBandwidth)} Mbps
              </span>
            </div>
            <div className={styles.resultRow}>
              <span className={styles.resultName}>单日新增存储 (Daily Write)</span>
              <span className={styles.resultVal}>{formatNumber(dailyWriteGb)} GB</span>
            </div>
            <div className={styles.resultRow}>
              <span className={styles.resultName}>总存储空间 (Total Storage)</span>
              <span className={styles.resultVal} style={{ color: 'var(--brand-red)' }}>
                {formatNumber(totalStorageTb)} TB
              </span>
            </div>

            <div className={styles.formulaBox}>
              <strong>🧮 心算公式</strong><br />
              • QPS = (DAU * Reqs) / 86,400<br />
              • 带宽 = (ReadQPS * ReadSize + WriteQPS * WriteSize) * 8<br />
              • 存储 = DailyWriteGb * Retention (未计副本数)
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
