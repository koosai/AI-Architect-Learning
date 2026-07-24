import React, { useState } from 'react';
import styles from './styles.module.css';

interface Question {
  q: string;
  options: string[];
  answer: number | string; // Index (0-indexed) or text string
  explain: string;
}

interface QuizCardProps {
  questions: Question[];
}

export default function QuizCard({ questions }: QuizCardProps): JSX.Element {
  const [currentIdx, setCurrentIdx] = useState(0);
  const [selectedOptIdx, setSelectedOptIdx] = useState<number | null>(null);
  const [submitted, setSubmitted] = useState(false);
  const [score, setScore] = useState(0);
  const [answersHistory, setAnswersHistory] = useState<(number | null)[]>(new Array(questions.length).fill(null));

  const question = questions[currentIdx];
  if (!question) return <div className={styles.card}>暂无测验题目</div>;

  // Find index of correct answer.
  // Supports three author conventions:
  //   1. numeric index (answer: 1)         -> used by the vast majority of chapters
  //   2. full option text (answer: "先查缓存…") -> exact string match
  //   3. option letter  (answer: "B")      -> match the option whose text starts with "B." / "B、" / "B)"
  let correctOptIdx = 0;
  if (typeof question.answer === 'number') {
    correctOptIdx = question.answer;
  } else {
    const target = question.answer.toString().trim();
    // (2) exact full-text match
    let idx = question.options.findIndex((opt) => opt.trim() === target);
    // (3) single-letter answer matching a lettered option prefix ("B" -> "B. …")
    if (idx === -1 && /^[A-Za-z]$/.test(target)) {
      const letterRe = new RegExp('^' + target + '\\s*[.)、\\uFF0E]', 'i');
      idx = question.options.findIndex((opt) => letterRe.test(opt.trim()));
    }
    if (idx !== -1) correctOptIdx = idx;
  }

  const handleSelect = (idx: number) => {
    if (submitted) return;
    setSelectedOptIdx(idx);
  };

  const handleSubmit = () => {
    if (selectedOptIdx === null || submitted) return;
    setSubmitted(true);
    
    const updatedHistory = [...answersHistory];
    updatedHistory[currentIdx] = selectedOptIdx;
    setAnswersHistory(updatedHistory);

    if (selectedOptIdx === correctOptIdx) {
      setScore((prev) => prev + 1);
    }
  };

  const handleNext = () => {
    if (currentIdx + 1 < questions.length) {
      setCurrentIdx((prev) => prev + 1);
      // Restore previous state if answered, otherwise clean state
      const nextAnswer = answersHistory[currentIdx + 1];
      setSelectedOptIdx(nextAnswer);
      setSubmitted(nextAnswer !== null);
    }
  };

  const handlePrev = () => {
    if (currentIdx > 0) {
      setCurrentIdx((prev) => prev - 1);
      const prevAnswer = answersHistory[currentIdx - 1];
      setSelectedOptIdx(prevAnswer);
      setSubmitted(prevAnswer !== null);
    }
  };

  const getOptionClass = (idx: number) => {
    if (!submitted) {
      return selectedOptIdx === idx ? `${styles.optionBtn} ${styles.optionSelected}` : styles.optionBtn;
    }
    // Submitted state
    if (idx === correctOptIdx) {
      return `${styles.optionBtn} ${styles.optionCorrect}`;
    }
    if (selectedOptIdx === idx && idx !== correctOptIdx) {
      return `${styles.optionBtn} ${styles.optionIncorrect}`;
    }
    return styles.optionBtn;
  };

  return (
    <div className={styles.card}>
      <div className={styles.header}>
        <span className={styles.title}>章末自测 (Question {currentIdx + 1} of {questions.length})</span>
        <span className={styles.score}>得分: {score} / {questions.length}</span>
      </div>

      <p className={styles.questionText}>{question.q}</p>

      <div className={styles.optionsList}>
        {question.options.map((option, idx) => (
          <button
            key={idx}
            className={getOptionClass(idx)}
            onClick={() => handleSelect(idx)}
            disabled={submitted}
          >
            {option}
          </button>
        ))}
      </div>

      {submitted && (
        <div className={styles.explainBox}>
          <strong>💡 解析说明：</strong>
          <p style={{ margin: '0.2rem 0 0 0' }}>{question.explain}</p>
        </div>
      )}

      <div className={styles.footer}>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <button className={styles.navBtn} onClick={handlePrev} disabled={currentIdx === 0}>
            上一题
          </button>
          <button className={styles.navBtn} onClick={handleNext} disabled={currentIdx === questions.length - 1}>
            下一题
          </button>
        </div>

        {!submitted ? (
          <button
            className={styles.submitBtn}
            onClick={handleSubmit}
            disabled={selectedOptIdx === null}
          >
            提交答案
          </button>
        ) : (
          <span style={{ fontSize: '0.85rem', fontWeight: 'bold', color: selectedOptIdx === correctOptIdx ? 'var(--brand-green)' : 'var(--brand-red)' }}>
            {selectedOptIdx === correctOptIdx ? '🎉 回答正确' : '❌ 回答错误'}
          </span>
        )}
      </div>
    </div>
  );
}
