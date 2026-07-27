// src/components/progress/progressStore.ts
// 用 localStorage 记录学习进度：已完成课程、测验成绩、连续天数。
// 无后端也能让仪表盘/进度/成就“活”起来；将来接后端可替换实现。
export interface Progress {
  completed: Record<string, number>;   // lessonId -> 完成时间戳
  quiz: Record<string, { score: number; total: number; at: number }>;
  lastActiveDay: string;               // YYYY-MM-DD
  streak: number;
  bestStreak: number;
  xp: number;
}

const KEY = 'aia.progress.v1';
const empty: Progress = { completed: {}, quiz: {}, lastActiveDay: '', streak: 0, bestStreak: 0, xp: 0 };

function canUse() { return typeof window !== 'undefined' && !!window.localStorage; }
const today = () => new Date().toISOString().slice(0, 10);

export function load(): Progress {
  if (!canUse()) return empty;
  try { return { ...empty, ...JSON.parse(window.localStorage.getItem(KEY) || '{}') }; }
  catch { return empty; }
}
export function save(p: Progress) { if (canUse()) try { window.localStorage.setItem(KEY, JSON.stringify(p)); } catch {} }

// 记一次活跃，维护连续天数
export function touchDay(p: Progress): Progress {
  const d = today();
  if (p.lastActiveDay === d) return p;
  const yst = new Date(Date.now() - 86400000).toISOString().slice(0, 10);
  const streak = p.lastActiveDay === yst ? p.streak + 1 : 1;
  return { ...p, lastActiveDay: d, streak, bestStreak: Math.max(p.bestStreak, streak) };
}
export function completeLesson(p: Progress, id: string): Progress {
  if (p.completed[id]) return p;
  return touchDay({ ...p, completed: { ...p.completed, [id]: Date.now() }, xp: p.xp + 40 });
}
export function recordQuiz(p: Progress, id: string, score: number, total: number): Progress {
  return touchDay({ ...p, quiz: { ...p.quiz, [id]: { score, total, at: Date.now() } }, xp: p.xp + score * 10 });
}
export function completedCount(p: Progress): number { return Object.keys(p.completed).length; }
