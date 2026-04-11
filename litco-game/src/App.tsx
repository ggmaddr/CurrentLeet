import { ChangeEvent, useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  buildTopicStats,
  clearCustomBundles,
  findProblem,
  loadGeneratedBundle,
  loadAttempts,
  mergeBundle,
  saveAttempts,
  saveCustomBundle,
  scoreQuestion
} from "./content";
import type { AttemptRecord, ContentBundle, Question } from "./types";

type Screen = "home" | "speedrun" | "flashcard" | "library" | "manage";

const SPEEDRUN_SIZE = 15;
const KEY_LABELS = ["A", "B", "C", "D"];

// ─── App shell ────────────────────────────────────────────────────────────────

function App() {
  const [bundle, setBundle] = useState<ContentBundle | null>(null);
  const [attempts, setAttempts] = useState<AttemptRecord[]>(() => loadAttempts());
  const [screen, setScreen] = useState<Screen>("home");
  const [speedrunSeed, setSpeedrunSeed] = useState(0);
  const [flashcardSeed, setFlashcardSeed] = useState(0);
  const [selectedTopic, setSelectedTopic] = useState<string>("all");
  const [notificationStatus, setNotificationStatus] = useState<NotificationPermission>(
    "Notification" in window ? Notification.permission : "denied"
  );
  const [loadingError, setLoadingError] = useState<string | null>(null);

  useEffect(() => {
    loadGeneratedBundle()
      .then((gen) => {
        setBundle(mergeBundle(gen));
        setLoadingError(null);
      })
      .catch((err: Error) => setLoadingError(err.message));
  }, []);

  useEffect(() => {
    saveAttempts(attempts);
  }, [attempts]);

  const topicStats = useMemo(
    () => (bundle ? buildTopicStats(bundle, attempts) : []),
    [bundle, attempts]
  );

  const weakTopics = useMemo(
    () =>
      [...topicStats]
        .filter((t) => t.answered > 0)
        .sort((a, b) => {
          const la = a.correct / Math.max(a.answered, 1);
          const lb = b.correct / Math.max(b.answered, 1);
          return la - lb || b.avgTimeMs - a.avgTimeMs;
        })
        .slice(0, 5),
    [topicStats]
  );

  const untouchedTopics = useMemo(
    () => topicStats.filter((t) => t.untouched),
    [topicStats]
  );

  function refreshBundle() {
    loadGeneratedBundle()
      .then((gen) => {
        setBundle(mergeBundle(gen));
        setLoadingError(null);
      })
      .catch((err: Error) => setLoadingError(err.message));
  }

  async function enableNotifications() {
    if (!("Notification" in window)) return;
    const result = await Notification.requestPermission();
    setNotificationStatus(result);
    if (result === "granted") {
      new Notification("LITCO GAME", {
        body: "Study reminder active. Come back for a speedrun."
      });
    }
  }

  function handleImportedBundle(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file) return;
    file.text().then((text) => {
      try {
        const parsed = JSON.parse(text) as ContentBundle;
        saveCustomBundle(parsed);
        refreshBundle();
      } catch {
        alert("Invalid JSON bundle format.");
      }
    });
    // reset file input so same file can be re-imported
    event.target.value = "";
  }

  function handleClearCustom() {
    if (!confirm("Clear all custom bundles? This cannot be undone.")) return;
    clearCustomBundles();
    refreshBundle();
  }

  function startSpeedrun(topic = "all") {
    setSelectedTopic(topic);
    setSpeedrunSeed((s) => s + 1);
    setScreen("speedrun");
  }

  function startFlashcards(topic = "all") {
    setSelectedTopic(topic);
    setFlashcardSeed((s) => s + 1);
    setScreen("flashcard");
  }

  if (loadingError) {
    return (
      <div className="app-shell centered">
        <div className="pixel-panel error-panel">
          <p className="eyebrow">SYSTEM ERROR</p>
          <h1>LITCO GAME</h1>
          <p>Could not load question pool.</p>
          <pre>{loadingError}</pre>
          <p className="muted">Run the generation script or check that <code>data/generated/content.json</code> exists.</p>
        </div>
      </div>
    );
  }

  if (!bundle) {
    return (
      <div className="app-shell centered">
        <div className="pixel-panel loading-panel">
          <p className="eyebrow blink">LOADING</p>
          <h1>LITCO GAME</h1>
          <p>Assembling question pool from notebooks...</p>
          <div className="loading-bar">
            <div className="loading-fill" />
          </div>
        </div>
      </div>
    );
  }

  const totalAnswered = new Set(attempts.map((a) => a.questionId)).size;
  const totalCorrect = attempts.filter((a) => a.correct).length;
  const streak = computeStreak(attempts);
  const accuracy = attempts.length > 0 ? Math.round((totalCorrect / attempts.length) * 100) : 0;

  return (
    <div className="app-shell">
      <header className="top-bar">
        <div className="brand">
          <span className="brand-icon">▶</span>
          <span className="brand-name">LITCO GAME</span>
          <span className="brand-sub">LC MASTERY</span>
        </div>
        <nav className="top-nav">
          {(["home", "speedrun", "flashcard", "library", "manage"] as Screen[]).map((s) => (
            <button
              key={s}
              className={`nav-btn ${screen === s ? "active" : ""}`}
              onClick={() => {
                if (s === "speedrun") startSpeedrun(selectedTopic);
                else if (s === "flashcard") startFlashcards(selectedTopic);
                else setScreen(s);
              }}
            >
              {NAV_ICONS[s]} {s.toUpperCase()}
            </button>
          ))}
        </nav>
        <div className="hud-bar">
          <HudStat label="QST" value={bundle.meta.questionCount} />
          <HudStat label="DONE" value={totalAnswered} />
          <HudStat label="ACC" value={`${accuracy}%`} />
          <HudStat label="STREAK" value={streak} glow={streak >= 5} />
        </div>
      </header>

      <main className="main-area">
        {screen === "home" && (
          <HomeScreen
            bundle={bundle}
            topicStats={topicStats}
            weakTopics={weakTopics}
            untouchedTopics={untouchedTopics}
            totalAnswered={totalAnswered}
            streak={streak}
            notificationStatus={notificationStatus}
            onStartSpeedrun={startSpeedrun}
            onStartFlashcards={startFlashcards}
            onEnableNotifications={enableNotifications}
          />
        )}
        {screen === "speedrun" && (
          <SpeedrunScreen
            key={speedrunSeed}
            bundle={bundle}
            attempts={attempts}
            selectedTopic={selectedTopic}
            onRecord={(attempt) => setAttempts((cur) => [...cur, attempt])}
            onGoHome={() => setScreen("home")}
          />
        )}
        {screen === "flashcard" && (
          <FlashcardScreen
            key={flashcardSeed}
            bundle={bundle}
            attempts={attempts}
            selectedTopic={selectedTopic}
            onRecord={(attempt) => setAttempts((cur) => [...cur, attempt])}
            onGoHome={() => setScreen("home")}
          />
        )}
        {screen === "library" && <LibraryScreen bundle={bundle} onStartSpeedrun={startSpeedrun} />}
        {screen === "manage" && (
          <ManageScreen
            bundle={bundle}
            onImportedBundle={handleImportedBundle}
            onClearCustom={handleClearCustom}
          />
        )}
      </main>
    </div>
  );
}

const NAV_ICONS: Record<Screen, string> = {
  home: "⌂",
  speedrun: "▶",
  flashcard: "◈",
  library: "≡",
  manage: "⚙"
};

// ─── Home screen ───────────────────────────────────────────────────────────────

function HomeScreen({
  bundle,
  topicStats,
  weakTopics,
  untouchedTopics,
  totalAnswered,
  streak,
  notificationStatus,
  onStartSpeedrun,
  onStartFlashcards,
  onEnableNotifications
}: {
  bundle: ContentBundle;
  topicStats: ReturnType<typeof buildTopicStats>;
  weakTopics: ReturnType<typeof buildTopicStats>;
  untouchedTopics: ReturnType<typeof buildTopicStats>;
  totalAnswered: number;
  streak: number;
  notificationStatus: NotificationPermission;
  onStartSpeedrun: (topic?: string) => void;
  onStartFlashcards: (topic?: string) => void;
  onEnableNotifications: () => void;
}) {
  return (
    <div className="home-grid">
      {/* Hero panel */}
      <section className="pixel-panel hero-panel">
        <div className="hero-text">
          <p className="eyebrow">COMMAND CENTER</p>
          <h2>GRADY'S LC MASTERY WORLD</h2>
          <p className="hero-sub">
            {totalAnswered === 0
              ? "No attempts yet. Launch a speedrun to begin."
              : `${totalAnswered} questions answered · ${untouchedTopics.length} topics untouched · ${streak} day streak`}
          </p>
        </div>
        <div className="hero-actions">
          <button className="btn primary large" onClick={() => onStartSpeedrun("all")}>
            ▶ SPEEDRUN ALL
          </button>
          <button className="btn secondary large" onClick={() => onStartFlashcards("all")}>
            ◈ FLASHCARDS
          </button>
          {notificationStatus !== "granted" && (
            <button className="btn ghost" onClick={onEnableNotifications}>
              🔔 Enable reminders
            </button>
          )}
        </div>
      </section>

      {/* Weak areas + untouched */}
      <div className="side-panels">
        <section className="pixel-panel">
          <h3 className="panel-title">⚠ WEAK AREAS</h3>
          {weakTopics.length === 0 ? (
            <p className="muted">Start sessions to build your profile.</p>
          ) : (
            weakTopics.map((t) => (
              <div key={t.title} className="topic-row" onClick={() => onStartSpeedrun(t.title)}>
                <div className="topic-row-info">
                  <span className="topic-name">{t.title}</span>
                  <span className="topic-pct bad">
                    {Math.round((t.correct / Math.max(t.answered, 1)) * 100)}%
                  </span>
                </div>
                <MeterBar value={t.correct} max={t.answered} variant="bad" />
              </div>
            ))
          )}
        </section>

        <section className="pixel-panel">
          <h3 className="panel-title">○ UNTOUCHED</h3>
          {untouchedTopics.length === 0 ? (
            <p className="muted good">All topics explored.</p>
          ) : (
            untouchedTopics.slice(0, 8).map((t) => (
              <div key={t.title} className="topic-row" onClick={() => onStartSpeedrun(t.title)}>
                <span className="topic-name">{t.title}</span>
                <span className="muted">{t.total}q</span>
              </div>
            ))
          )}
        </section>
      </div>

      {/* Topic world map */}
      <section className="pixel-panel topic-map-panel">
        <h3 className="panel-title">◉ WORLD MAP</h3>
        <div className="topic-map">
          {topicStats.map((t) => {
            const pct = t.answered === 0 ? 0 : Math.round((t.correct / t.answered) * 100);
            const state = t.untouched ? "untouched" : pct >= 80 ? "mastered" : pct >= 50 ? "learning" : "weak";
            return (
              <button
                key={t.title}
                className={`topic-node ${state}`}
                onClick={() => onStartSpeedrun(t.title)}
                title={`${t.answered}/${t.total} answered · ${pct}% accuracy`}
              >
                <span className="topic-node-title">{t.title}</span>
                <span className="topic-node-count">{t.total}q</span>
                <MeterBar value={t.correct} max={Math.max(t.answered, 1)} variant={state === "weak" ? "bad" : "good"} compact />
              </button>
            );
          })}
        </div>
      </section>

      {/* Quick topic launch */}
      <section className="pixel-panel quick-launch-panel">
        <h3 className="panel-title">⚡ QUICK LAUNCH</h3>
        <div className="quick-btns">
          {bundle.topics.slice(0, 12).map((topic) => (
            <button key={topic.id} className="btn ghost small" onClick={() => onStartSpeedrun(topic.title)}>
              {topic.title}
            </button>
          ))}
        </div>
      </section>
    </div>
  );
}

// ─── Speedrun screen ───────────────────────────────────────────────────────────

function SpeedrunScreen({
  bundle,
  attempts,
  selectedTopic,
  onRecord,
  onGoHome
}: {
  bundle: ContentBundle;
  attempts: AttemptRecord[];
  selectedTopic: string;
  onRecord: (attempt: AttemptRecord) => void;
  onGoHome: () => void;
}) {
  // Filter and sort questions
  const questions = useMemo<Question[]>(() => {
    let pool = bundle.questions;

    // topic filter
    if (selectedTopic !== "all") {
      pool = pool.filter((q) => q.topic === selectedTopic);
    }

    // prefer MC questions
    const mc = pool.filter((q) => q.choices && q.choices.length >= 2);
    const rest = pool.filter((q) => !q.choices || q.choices.length < 2);
    pool = [...mc, ...rest];

    // Sort by least-answered first
    const countMap = new Map<string, number>();
    attempts.forEach((a) => countMap.set(a.questionId, (countMap.get(a.questionId) ?? 0) + 1));

    return [...pool]
      .sort((a, b) => (countMap.get(a.id) ?? 0) - (countMap.get(b.id) ?? 0))
      .slice(0, SPEEDRUN_SIZE);
  }, [bundle, attempts, selectedTopic]);

  const [index, setIndex] = useState(0);
  const [selectedChoice, setSelectedChoice] = useState<string | null>(null);
  const [revealed, setRevealed] = useState(false);
  const [correct, setCorrect] = useState<boolean | null>(null);
  const [startedAt, setStartedAt] = useState(() => Date.now());
  const [sessionResults, setSessionResults] = useState<{ correct: boolean; timeMs: number }[]>([]);
  const [showFullCode, setShowFullCode] = useState(false);
  const [timeLeft, setTimeLeft] = useState<number>(30);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const current = questions[index];
  const problem = current ? findProblem(bundle, current) : undefined;
  const isLastQuestion = index >= questions.length - 1;

  // Timer
  useEffect(() => {
    if (!current || revealed) {
      if (timerRef.current) clearInterval(timerRef.current);
      return;
    }
    const limit = current.timeLimitSec > 0 ? current.timeLimitSec : 30;
    setTimeLeft(limit);
    timerRef.current = setInterval(() => {
      setTimeLeft((t) => {
        if (t <= 1) {
          clearInterval(timerRef.current!);
          if (!revealed) submitAnswer("");
          return 0;
        }
        return t - 1;
      });
    }, 1000);
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [index, current]);

  // Keyboard shortcuts
  const submitAnswer = useCallback(
    (choice: string) => {
      if (revealed) return;
      if (timerRef.current) clearInterval(timerRef.current);
      const isCorrect = scoreQuestion(choice, current);
      setCorrect(isCorrect);
      setSelectedChoice(choice);
      setRevealed(true);
      setShowFullCode(false);
      const timeMs = Date.now() - startedAt;
      setSessionResults((r) => [...r, { correct: isCorrect, timeMs }]);
      onRecord({
        questionId: current.id,
        correct: isCorrect,
        timeMs,
        topic: current.topic,
        subtopic: current.subtopic,
        type: current.questionType
      });
    },
    [revealed, current, startedAt, onRecord]
  );

  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if (revealed) {
        if (e.key === " " || e.key === "Enter") {
          e.preventDefault();
          goNext();
        }
        return;
      }
      if (!current?.choices?.length) return;
      const idx = ["1", "2", "3", "4"].indexOf(e.key);
      if (idx >= 0 && idx < current.choices.length) {
        submitAnswer(current.choices[idx]);
      }
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [revealed, current, submitAnswer]);

  function goNext() {
    setIndex((i) => i + 1);
    setSelectedChoice(null);
    setRevealed(false);
    setCorrect(null);
    setShowFullCode(false);
    setStartedAt(Date.now());
  }

  // Session complete
  if (!current || index >= questions.length) {
    const totalCorrect = sessionResults.filter((r) => r.correct).length;
    const avgTime = sessionResults.length
      ? Math.round(sessionResults.reduce((s, r) => s + r.timeMs, 0) / sessionResults.length / 1000)
      : 0;
    return (
      <div className="session-complete">
        <div className="pixel-panel complete-panel">
          <p className="eyebrow">SESSION COMPLETE</p>
          <h2 className={totalCorrect / questions.length >= 0.8 ? "good" : "neutral"}>
            {totalCorrect >= questions.length
              ? "PERFECT RUN"
              : totalCorrect / questions.length >= 0.8
              ? "GREAT SESSION"
              : totalCorrect / questions.length >= 0.5
              ? "KEEP TRAINING"
              : "NEEDS WORK"}
          </h2>
          <div className="complete-stats">
            <div className="stat-big">
              <span className="stat-val good">{totalCorrect}</span>
              <span className="stat-label">CORRECT</span>
            </div>
            <div className="stat-big">
              <span className="stat-val bad">{sessionResults.length - totalCorrect}</span>
              <span className="stat-label">MISSED</span>
            </div>
            <div className="stat-big">
              <span className="stat-val">{avgTime}s</span>
              <span className="stat-label">AVG TIME</span>
            </div>
          </div>
          <MeterBar value={totalCorrect} max={sessionResults.length} variant="good" />
          <div className="complete-actions">
            <button className="btn primary" onClick={() => { setIndex(0); setSessionResults([]); setStartedAt(Date.now()); }}>
              ▶ PLAY AGAIN
            </button>
            <button className="btn secondary" onClick={onGoHome}>
              ⌂ COMMAND CENTER
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (questions.length === 0) {
    return (
      <div className="pixel-panel">
        <p className="eyebrow">NO QUESTIONS</p>
        <p>No questions found for topic: <strong>{selectedTopic}</strong></p>
        <button className="btn secondary" onClick={onGoHome}>Back</button>
      </div>
    );
  }

  const limit = current.timeLimitSec > 0 ? current.timeLimitSec : 30;
  const timerPct = Math.max(0, (timeLeft / limit) * 100);
  const timerClass = timeLeft <= 5 ? "critical" : timeLeft <= 10 ? "warning" : "normal";

  return (
    <div className="speedrun-layout">
      {/* Progress header */}
      <div className="run-header pixel-panel">
        <div className="run-meta">
          <span className="eyebrow">{current.topic}</span>
          <span className="divider">›</span>
          <span className="eyebrow muted">{current.subtopic || current.questionType}</span>
        </div>
        <div className="run-progress">
          <span className="progress-text">
            {index + 1} / {questions.length}
          </span>
          <div className="progress-track">
            {questions.map((_, i) => (
              <div
                key={i}
                className={`progress-pip ${i < index ? (sessionResults[i]?.correct ? "done-good" : "done-bad") : i === index ? "current" : ""}`}
              />
            ))}
          </div>
        </div>
        <div className={`timer ${timerClass}`}>
          <div className="timer-bar" style={{ width: `${timerPct}%` }} />
          <span className="timer-label">{timeLeft}s</span>
        </div>
      </div>

      {/* Question card */}
      <div className="pixel-panel question-panel">
        <div className="q-badges">
          <span className="badge type-badge">{current.questionType || "question"}</span>
          <span className={`badge diff-badge ${current.difficulty}`}>{current.difficulty}</span>
          {current.title && <span className="badge">{current.title}</span>}
        </div>

        <p className="question-prompt">{current.prompt}</p>

        {current.choices && current.choices.length >= 2 ? (
          <div className="choices-grid">
            {current.choices.map((choice, i) => {
              let cls = "choice-btn";
              if (revealed) {
                const isAnswer = scoreQuestion(choice, current);
                if (isAnswer) cls += " correct-choice";
                else if (choice === selectedChoice && !isAnswer) cls += " wrong-choice";
                else cls += " dim-choice";
              }
              return (
                <button
                  key={choice}
                  className={cls}
                  onClick={() => submitAnswer(choice)}
                  disabled={revealed}
                >
                  <span className="choice-key">{KEY_LABELS[i]}</span>
                  <span className="choice-text">{choice}</span>
                </button>
              );
            })}
          </div>
        ) : (
          <div className="open-answer">
            <p className="muted small">Flashcard — think about your answer, then reveal.</p>
            <button className="btn primary" onClick={() => submitAnswer(current.answer)} disabled={revealed}>
              REVEAL ANSWER
            </button>
          </div>
        )}
      </div>

      {/* Reveal panel */}
      {revealed && (
        <div className={`pixel-panel reveal-panel ${correct ? "reveal-correct" : "reveal-wrong"}`}>
          <div className="reveal-header">
            <span className={`result-badge ${correct ? "good" : "bad"}`}>
              {correct ? "✓ CORRECT" : "✗ WRONG"}
            </span>
            <span className="reveal-answer-label">
              Answer: <strong>{current.answer}</strong>
            </span>
          </div>

          {current.fullExplanation && (
            <p className="reveal-explanation">{current.fullExplanation}</p>
          )}

          {(current.fullCode || problem?.code) && (
            <div className="reveal-code-section">
              <button className="btn ghost small" onClick={() => setShowFullCode((v) => !v)}>
                {showFullCode ? "▲ HIDE CODE" : "▼ VIEW FULL CODE"}
              </button>
              {showFullCode && (
                <pre className="code-block">{current.fullCode || problem?.code}</pre>
              )}
            </div>
          )}

          {current.links && current.links.length > 0 && (
            <div className="reveal-links">
              {current.links.map((link) => (
                <a key={link} href={link} target="_blank" rel="noreferrer" className="link-btn">
                  ↗ Open Problem
                </a>
              ))}
            </div>
          )}

          <button className="btn primary" onClick={goNext}>
            {isLastQuestion ? "VIEW RESULTS" : "NEXT →"} <span className="key-hint">[SPACE]</span>
          </button>
        </div>
      )}
    </div>
  );
}

// ─── Flashcard screen ──────────────────────────────────────────────────────────

function FlashcardScreen({
  bundle,
  attempts,
  selectedTopic,
  onRecord,
  onGoHome
}: {
  bundle: ContentBundle;
  attempts: AttemptRecord[];
  selectedTopic: string;
  onRecord: (attempt: AttemptRecord) => void;
  onGoHome: () => void;
}) {
  const cards = useMemo<Question[]>(() => {
    let pool = bundle.questions;
    if (selectedTopic !== "all") {
      pool = pool.filter((q) => q.topic === selectedTopic);
    }
    // Prefer flashcard type, but include all
    const flashcards = pool.filter((q) => q.questionType === "flashcard");
    const others = pool.filter((q) => q.questionType !== "flashcard");
    pool = [...flashcards, ...others];

    const countMap = new Map<string, number>();
    attempts.forEach((a) => countMap.set(a.questionId, (countMap.get(a.questionId) ?? 0) + 1));

    return [...pool]
      .sort((a, b) => (countMap.get(a.id) ?? 0) - (countMap.get(b.id) ?? 0))
      .slice(0, 30);
  }, [bundle, attempts, selectedTopic]);

  const [index, setIndex] = useState(0);
  const [flipped, setFlipped] = useState(false);
  const [startedAt] = useState(() => Date.now());

  const current = cards[index];

  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if (e.key === " " || e.key === "Enter") {
        e.preventDefault();
        if (!flipped) setFlipped(true);
        else goNext(true);
      }
      if (e.key === "ArrowRight" && flipped) goNext(true);
      if (e.key === "ArrowLeft" && flipped) goNext(false);
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [flipped, index]);

  function goNext(correct: boolean) {
    if (current) {
      onRecord({
        questionId: current.id,
        correct,
        timeMs: Date.now() - startedAt,
        topic: current.topic,
        subtopic: current.subtopic,
        type: current.questionType
      });
    }
    setIndex((i) => i + 1);
    setFlipped(false);
  }

  if (!current || index >= cards.length) {
    return (
      <div className="session-complete">
        <div className="pixel-panel complete-panel">
          <p className="eyebrow">DECK COMPLETE</p>
          <h2>ALL CARDS REVIEWED</h2>
          <div className="complete-actions">
            <button className="btn primary" onClick={() => { setIndex(0); setFlipped(false); }}>
              ↺ RESTART DECK
            </button>
            <button className="btn secondary" onClick={onGoHome}>⌂ HOME</button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flashcard-layout">
      <div className="run-header pixel-panel">
        <span className="eyebrow">{current.topic} › {current.subtopic || "Flashcard"}</span>
        <span className="progress-text">{index + 1} / {cards.length}</span>
        <button className="btn ghost small" onClick={onGoHome}>⌂</button>
      </div>

      <div className={`flashcard ${flipped ? "flipped" : ""}`} onClick={() => !flipped && setFlipped(true)}>
        <div className="card-inner">
          <div className="card-front pixel-panel">
            <p className="eyebrow">QUESTION</p>
            <p className="card-text">{current.prompt}</p>
            <p className="card-hint muted">SPACE / Click to reveal</p>
          </div>
          <div className="card-back pixel-panel">
            <p className="eyebrow">ANSWER</p>
            <p className="card-text answer-text">{current.answer}</p>
            {current.fullExplanation && (
              <p className="card-explanation muted">{current.fullExplanation.slice(0, 300)}</p>
            )}
            {current.fullCode && (
              <details>
                <summary className="code-toggle">View code</summary>
                <pre className="code-block small">{current.fullCode}</pre>
              </details>
            )}
          </div>
        </div>
      </div>

      {flipped && (
        <div className="flashcard-actions">
          <button className="btn bad large" onClick={() => goNext(false)}>
            ✗ MISSED <span className="key-hint">[←]</span>
          </button>
          <button className="btn good large" onClick={() => goNext(true)}>
            ✓ GOT IT <span className="key-hint">[→]</span>
          </button>
        </div>
      )}
    </div>
  );
}

// ─── Library screen ────────────────────────────────────────────────────────────

function LibraryScreen({
  bundle,
  onStartSpeedrun
}: {
  bundle: ContentBundle;
  onStartSpeedrun: (topic: string) => void;
}) {
  const [filter, setFilter] = useState("");
  const [activeTopic, setActiveTopic] = useState("all");

  const filtered = useMemo(() => {
    return bundle.problems.filter((p) => {
      const topicMatch = activeTopic === "all" || p.topic === activeTopic;
      const textMatch =
        !filter ||
        `${p.title} ${p.topic} ${p.subtopic} ${p.summary}`.toLowerCase().includes(filter.toLowerCase());
      return topicMatch && textMatch;
    });
  }, [bundle, filter, activeTopic]);

  return (
    <div className="library-layout">
      <div className="pixel-panel library-controls">
        <h2 className="panel-title">≡ PROBLEM LIBRARY</h2>
        <div className="library-filters">
          <input
            className="filter-input"
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            placeholder="Search problems..."
          />
          <select
            className="topic-select"
            value={activeTopic}
            onChange={(e) => setActiveTopic(e.target.value)}
          >
            <option value="all">All Topics</option>
            {bundle.topics.map((t) => (
              <option key={t.id} value={t.title}>{t.title}</option>
            ))}
          </select>
          {activeTopic !== "all" && (
            <button className="btn ghost small" onClick={() => onStartSpeedrun(activeTopic)}>
              ▶ Practice This Topic
            </button>
          )}
        </div>
        <p className="muted small">{filtered.length} problems</p>
      </div>

      <div className="library-list">
        {filtered.slice(0, 100).map((problem) => (
          <article key={problem.id} className="pixel-panel library-item">
            <div className="lib-item-header">
              <div>
                <p className="eyebrow">{problem.topic} / {problem.subtopic}</p>
                <h3 className="lib-title">
                  {problem.number ? `${problem.number}. ` : ""}{problem.title}
                </h3>
              </div>
              <span className={`badge diff-badge ${problem.difficulty}`}>{problem.difficulty}</span>
            </div>
            {problem.summary && <p className="lib-summary">{problem.summary}</p>}
            {problem.insights && problem.insights.length > 0 && (
              <div className="lib-insights">
                {problem.insights.slice(0, 3).map((ins, i) => (
                  <span key={i} className="insight-chip">◆ {ins}</span>
                ))}
              </div>
            )}
            {problem.links && problem.links.length > 0 && (
              <div className="lib-links">
                {problem.links.slice(0, 2).map((link) => (
                  <a key={link} href={link} target="_blank" rel="noreferrer" className="link-btn small">
                    ↗ LC
                  </a>
                ))}
              </div>
            )}
            {problem.code && (
              <details>
                <summary className="code-toggle">View code</summary>
                <pre className="code-block">{problem.code}</pre>
              </details>
            )}
          </article>
        ))}
        {filtered.length > 100 && (
          <p className="muted small">Showing first 100 of {filtered.length}. Use filters to narrow down.</p>
        )}
      </div>
    </div>
  );
}

// ─── Manage screen ─────────────────────────────────────────────────────────────

function ManageScreen({
  bundle,
  onImportedBundle,
  onClearCustom
}: {
  bundle: ContentBundle;
  onImportedBundle: (event: ChangeEvent<HTMLInputElement>) => void;
  onClearCustom: () => void;
}) {
  return (
    <div className="manage-layout">
      <div className="pixel-panel">
        <h2 className="panel-title">⚙ QUESTION POOL MANAGER</h2>
        <p className="muted">
          Import custom JSON bundles to expand the question pool, or clear custom bundles to reset to the notebook-generated base content.
        </p>
        <div className="manage-actions">
          <label className="btn primary file-input-label">
            ⊕ IMPORT JSON BUNDLE
            <input type="file" accept="application/json" onChange={onImportedBundle} />
          </label>
          <button className="btn danger" onClick={onClearCustom}>
            ⊗ CLEAR CUSTOM BUNDLES
          </button>
        </div>
      </div>

      <div className="pixel-panel">
        <h3 className="panel-title">POOL STATUS</h3>
        <div className="stats-grid">
          <div className="stat-item">
            <span className="stat-num">{bundle.meta.topicCount}</span>
            <span className="stat-lbl">TOPICS</span>
          </div>
          <div className="stat-item">
            <span className="stat-num">{bundle.meta.problemCount}</span>
            <span className="stat-lbl">PROBLEMS</span>
          </div>
          <div className="stat-item">
            <span className="stat-num">{bundle.meta.questionCount}</span>
            <span className="stat-lbl">QUESTIONS</span>
          </div>
        </div>
        <p className="muted small">Sources: {bundle.meta.sourceNotebooks.join(", ")}</p>
      </div>

      <div className="pixel-panel">
        <h3 className="panel-title">JSON BUNDLE FORMAT</h3>
        <p className="muted small">Custom bundles must follow this shape:</p>
        <pre className="code-block small">{BUNDLE_FORMAT_HINT}</pre>
      </div>

      <div className="pixel-panel">
        <h3 className="panel-title">INVOKE EXPERT TESTER</h3>
        <p className="muted">
          To generate new questions using the expert subagent, run in your terminal:
        </p>
        <pre className="code-block small">claude --agent expert-grady-lc-tester "Create 20 questions on Knapsack DP loop direction"</pre>
        <p className="muted small">
          The agent will write a new JSON file to <code>data/custom/</code>. Import it here to add to your pool.
        </p>
      </div>
    </div>
  );
}

const BUNDLE_FORMAT_HINT = `{
  "meta": { "sourceNotebooks": ["custom"],
            "topicCount": 1, "problemCount": 5, "questionCount": 20 },
  "topics": [{ "id": "graphs", "title": "Graphs", "subtopics": ["BFS"] }],
  "problems": [{ "id": "lc-200", "title": "Number of Islands",
    "number": 200, "topic": "Graphs", "subtopic": "BFS",
    "difficulty": "medium", "notebook": "custom",
    "source_cells": [], "summary": "...", "notes": "",
    "code": "def numIslands(...):", "links": ["https://..."],
    "insights": ["BFS / DFS from each unvisited land cell"],
    "recognition_cues": ["grid", "connected components"] }],
  "questions": [{ "id": "q-graphs-bfs-1",
    "problemId": "lc-200", "topic": "Graphs", "subtopic": "BFS",
    "topicId": "graphs", "subtopicId": "bfs",
    "difficulty": "medium", "title": "Islands - Pattern",
    "questionType": "multiple_choice",
    "prompt": "Number of Islands: Given an m×n grid of '1' (land) and '0' (water), count distinct islands. Which traversal strategy to use?",
    "answer": "DFS or BFS from each unvisited '1', mark visited",
    "acceptedAnswers": ["DFS or BFS", "flood fill"],
    "choices": ["DFS or BFS from each unvisited '1', mark visited",
                "Sort cells by value then sweep",
                "Binary search for island boundaries",
                "Use Union-Find only, no traversal needed"],
    "tags": ["graphs", "bfs", "dfs"],
    "timeLimitSec": 20, "masteryWeight": 1.0,
    "fullCode": "def numIslands(grid):\\n  ...",
    "fullExplanation": "Flood-fill pattern...",
    "links": ["https://leetcode.com/problems/number-of-islands/"],
    "revealFullCodeAfterAnswer": true,
    "revealFullExplanationAfterAnswer": true }]
}`;

// ─── Shared components ────────────────────────────────────────────────────────

function MeterBar({
  value,
  max,
  variant = "good",
  compact = false
}: {
  value: number;
  max: number;
  variant?: string;
  compact?: boolean;
}) {
  const pct = max === 0 ? 0 : Math.min(100, Math.round((value / max) * 100));
  return (
    <div className={`meter-bar ${compact ? "compact" : ""}`}>
      <div className={`meter-fill ${variant}`} style={{ width: `${pct}%` }} />
    </div>
  );
}

function HudStat({ label, value, glow = false }: { label: string; value: string | number; glow?: boolean }) {
  return (
    <div className={`hud-stat ${glow ? "glow" : ""}`}>
      <span className="hud-val">{value}</span>
      <span className="hud-lbl">{label}</span>
    </div>
  );
}

// ─── Utilities ─────────────────────────────────────────────────────────────────

function computeStreak(attempts: AttemptRecord[]): number {
  if (attempts.length === 0) return 0;
  const days = new Set(
    attempts.map((a) => {
      // This isn't stored in AttemptRecord — we use a placeholder
      return 0;
    })
  );
  return days.size;
}

export default App;
