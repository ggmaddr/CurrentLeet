import type { AttemptRecord, ContentBundle, Problem, Question, Topic } from "./types";

export type TopicStats = {
  title: string;
  total: number;
  answered: number;
  correct: number;
  avgTimeMs: number;
  untouched: boolean;
};

const STORAGE_KEY = "litco-custom-question-bundles";
const ATTEMPT_KEY = "litco-attempts";

export async function loadGeneratedBundle(): Promise<ContentBundle> {
  const response = await fetch("/generated/content.json");
  if (!response.ok) {
    throw new Error("Failed to load generated content.json");
  }
  return (await response.json()) as ContentBundle;
}

export function mergeBundle(base: ContentBundle): ContentBundle {
  const custom = loadCustomBundles();
  const merged = custom.reduce<ContentBundle>(
    (acc, bundle) => ({
      meta: {
        sourceNotebooks: [...new Set([...acc.meta.sourceNotebooks, ...(bundle.meta?.sourceNotebooks ?? ["custom"])])],
        topicCount: 0,
        problemCount: acc.problems.length + bundle.problems.length,
        questionCount: acc.questions.length + bundle.questions.length
      },
      topics: mergeTopics(acc.topics, bundle.topics),
      problems: mergeById(acc.problems, bundle.problems),
      questions: mergeById(acc.questions, bundle.questions)
    }),
    {
      ...base,
      meta: { ...base.meta }
    }
  );
  merged.meta.topicCount = merged.topics.length;
  merged.meta.problemCount = merged.problems.length;
  merged.meta.questionCount = merged.questions.length;
  return merged;
}

function mergeById<T extends { id: string }>(left: T[], right: T[]): T[] {
  const map = new Map<string, T>();
  [...left, ...right].forEach((item) => map.set(item.id, item));
  return [...map.values()];
}

function mergeTopics(left: Topic[], right: Topic[]): Topic[] {
  const map = new Map<string, Topic>();
  [...left, ...right].forEach((topic) => {
    const prev = map.get(topic.id);
    if (!prev) {
      map.set(topic.id, topic);
      return;
    }
    map.set(topic.id, {
      ...prev,
      subtopics: [...new Set([...prev.subtopics, ...topic.subtopics])].sort()
    });
  });
  return [...map.values()].sort((a, b) => a.title.localeCompare(b.title));
}

export function saveCustomBundle(bundle: ContentBundle): void {
  const current = loadCustomBundles();
  current.push(bundle);
  localStorage.setItem(STORAGE_KEY, JSON.stringify(current));
}

export function replaceCustomBundles(bundles: ContentBundle[]): void {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(bundles));
}

export function clearCustomBundles(): void {
  localStorage.removeItem(STORAGE_KEY);
}

export function loadCustomBundles(): ContentBundle[] {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) {
    return [];
  }
  try {
    return JSON.parse(raw) as ContentBundle[];
  } catch {
    return [];
  }
}

export function loadAttempts(): AttemptRecord[] {
  const raw = localStorage.getItem(ATTEMPT_KEY);
  if (!raw) {
    return [];
  }
  try {
    return JSON.parse(raw) as AttemptRecord[];
  } catch {
    return [];
  }
}

export function saveAttempts(attempts: AttemptRecord[]): void {
  localStorage.setItem(ATTEMPT_KEY, JSON.stringify(attempts));
}

export function buildTopicStats(bundle: ContentBundle, attempts: AttemptRecord[]): TopicStats[] {
  return bundle.topics.map((topic) => {
    const questions = bundle.questions.filter((question) => question.topic === topic.title);
    const topicAttempts = attempts.filter((attempt) => attempt.topic === topic.title);
    const answered = new Set(topicAttempts.map((attempt) => attempt.questionId)).size;
    const correct = topicAttempts.filter((attempt) => attempt.correct).length;
    const avgTimeMs =
      topicAttempts.length > 0
        ? Math.round(topicAttempts.reduce((sum, attempt) => sum + attempt.timeMs, 0) / topicAttempts.length)
        : 0;
    return {
      title: topic.title,
      total: questions.length,
      answered,
      correct,
      avgTimeMs,
      untouched: answered === 0
    };
  });
}

export function scoreQuestion(answer: string, question: Question): boolean {
  const normalized = normalize(answer);
  if (!normalized) {
    return false;
  }
  return question.acceptedAnswers.some((candidate) => normalize(candidate).includes(normalized) || normalized.includes(normalize(candidate)));
}

function normalize(value: string): string {
  return value.toLowerCase().replace(/\s+/g, " ").trim();
}

export function findProblem(bundle: ContentBundle, question: Question): Problem | undefined {
  return bundle.problems.find((problem) => problem.id === question.problemId);
}
