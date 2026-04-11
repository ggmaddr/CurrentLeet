export type Topic = {
  id: string;
  title: string;
  subtopics: string[];
};

export type Problem = {
  id: string;
  title: string;
  number: number | null;
  topic: string;
  subtopic: string;
  difficulty: string;
  notebook: string;
  source_cells: number[];
  summary: string;
  notes: string;
  code: string;
  links: string[];
  insights: string[];
  recognition_cues: string[];
};

export type Question = {
  id: string;
  problemId: string;
  topic: string;
  subtopic: string;
  topicId?: string;
  subtopicId?: string;
  difficulty: string;
  title: string;
  questionType: "multiple_choice" | "flashcard" | "fill_blank" | "this_or_that" | string;
  prompt: string;
  answer: string;
  acceptedAnswers: string[];
  choices: string[];
  tags: string[];
  timeLimitSec: number;
  masteryWeight: number;
  fullCode: string;
  fullExplanation: string;
  links: string[];
  revealFullCodeAfterAnswer: boolean;
  revealFullExplanationAfterAnswer: boolean;
};

export type ContentBundle = {
  meta: {
    sourceNotebooks: string[];
    topicCount: number;
    problemCount: number;
    questionCount: number;
  };
  topics: Topic[];
  problems: Problem[];
  questions: Question[];
};

export type AttemptRecord = {
  questionId: string;
  correct: boolean;
  timeMs: number;
  topic: string;
  subtopic: string;
  type: string;
};
