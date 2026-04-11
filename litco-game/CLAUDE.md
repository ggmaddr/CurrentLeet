# LITCO GAME — Developer Guide

Grady's personal LeetCode mastery game. Pixel RPG UI. Built from two notebooks.

## Project layout

```
litco-game/
├── src/
│   ├── App.tsx        — all screens: home, speedrun, flashcard, library, manage
│   ├── content.ts     — bundle loading, merging, scoring, stats
│   ├── types.ts       — TypeScript types (Question, Problem, ContentBundle, etc.)
│   └── styles.css     — full pixel-game CSS (Share Tech Mono font, dark theme)
├── scripts/
│   └── generate_question_pool.py  — expert question generator (run to rebuild pool)
├── data/
│   ├── generated/content.json     — source-of-truth (also copied to public/)
│   └── custom/                    — custom JSON bundles imported by user
├── public/
│   └── generated/content.json     — served by Vite dev server
└── CLAUDE.md                      — this file
```

## Dev commands

```bash
npm run dev       # start dev server at http://localhost:4173
npm run build     # TypeScript check + Vite build
python3 scripts/generate_question_pool.py  # rebuild question pool from notebooks
```

**After running the generator**: both `data/generated/content.json` AND `public/generated/content.json` are updated automatically.

## Source notebooks (read-only)

- `/Users/gradyta/gresource/CurrentLeet/leet A1.ipynb`
  Arrays, Intervals, Two Pointers, Prefix Sum, Stack/Mono Stack, Binary Search, Sliding Window, Linked List, Trees, Tries, Backtracking, Heap

- `/Users/gradyta/gresource/CurrentLeet/leetA2.ipynb`
  Graphs, Matrix as Graph, Topo Sort, Shortest Path, Union Find, DP (all variants), Knapsack, Interval DP, Tree DP, Bitmask DP, Greedy, Segment Tree

## Question pool design

### Types (in priority order)
1. `multiple_choice` — 4 plausible confusor choices (70%+ of questions)
2. `flashcard` — single key insight or recognition cue
3. `fill_blank` — ___ gaps for invariants and loop directions
4. `this_or_that` — binary comparison (BFS vs DFS, SW vs prefix sum, etc.)

**NO code-writing questions.** Use MC with confusing code snippets instead.

### Quality rules
- All MC choices must be plausible to someone who partially knows the topic
- NEVER use generic wrong choices like "Sort first and apply greedy"
- For LC-specific questions: include 2-3 sentence problem description in prompt
- All questions must have `fullCode` (Python) and `fullExplanation`
- All questions must have `topicId` and `subtopicId`

### Expert handcrafted questions (35+)
Located at the bottom of `generate_question_pool.py` in the `HANDCRAFTED` list.
These cover the most important invariants, contrasts, and pitfalls from the notebooks:
- Knapsack loop direction (0/1 R→L, unbounded L→R)
- Coin Change II vs Combination Sum IV (combinations vs permutations)
- LCS vs Edit Distance transitions
- BFS vs Dijkstra, multi-source BFS
- Monotonic stack direction (decreasing → next greater)
- Pacific Atlantic reverse DFS
- Binary search left vs right bound
- Backtracking: combinations vs permutations vs subsets

## ContentBundle JSON schema

```typescript
type ContentBundle = {
  meta: { sourceNotebooks: string[]; topicCount: number; problemCount: number; questionCount: number; };
  topics: Array<{ id: string; title: string; subtopics: string[]; }>;
  problems: Array<{
    id: string; title: string; number: number | null;
    topic: string; subtopic: string; topicId: string; subtopicId: string;
    difficulty: string; notebook: string; source_cells: number[];
    summary: string; notes: string; code: string;
    links: string[]; insights: string[]; recognition_cues: string[];
  }>;
  questions: Array<{
    id: string; problemId: string;
    topic: string; subtopic: string; topicId: string; subtopicId: string;
    difficulty: string; title: string;
    questionType: "multiple_choice" | "flashcard" | "fill_blank" | "this_or_that";
    prompt: string; answer: string; acceptedAnswers: string[]; choices: string[];
    tags: string[]; timeLimitSec: number; masteryWeight: number;
    fullCode: string; fullExplanation: string; links: string[];
    revealFullCodeAfterAnswer: boolean; revealFullExplanationAfterAnswer: boolean;
  }>;
};
```

## Custom question bundles

Users can import additional JSON bundles via the Manage screen.
Custom bundles are stored in `localStorage` and merged with the base bundle at startup.
They must follow the ContentBundle schema above.

Files dropped in `data/custom/` must be manually imported through the UI.

## Using the expert-grady-lc-tester subagent

The subagent is at `/Users/gradyta/gresource/.claude/agents/expert-grady-lc-tester.md`.

**To generate new questions:**
```bash
# In a new Claude Code session at /Users/gradyta/gresource:
# Claude will auto-suggest the agent, or you can prompt:
# "Use the expert-grady-lc-tester agent to create 25 questions on Knapsack DP"
```

The agent will:
1. Read the relevant notebook sections
2. Create discriminating questions focused on Grady's learning patterns
3. Write a JSON bundle to `data/custom/<topic>-questions.json`
4. Report what was created

**To import into the game:**
Open the app → Manage → "IMPORT JSON BUNDLE" → select the file from `data/custom/`

## App screens

- **Home**: topic world map, weak areas, untouched topics, quick launch buttons
- **Speedrun**: timed Q&A with progress pips, timer bar, choice highlighting, full reveal after answer
- **Flashcard**: 3D flip card with keyboard shortcuts (Space to flip, ← miss / → got it)
- **Library**: searchable problem list with code reveal
- **Manage**: import/clear custom bundles, JSON format reference, agent instructions

## Keyboard shortcuts (speedrun)
- `1/2/3/4` — select MC choice
- `Space / Enter` — reveal (after choosing) or next question
- Timer auto-submits on expiry

## Keyboard shortcuts (flashcard)
- `Space / Enter` — flip card
- `←` — missed
- `→` — got it

## Grady's learning priorities (from notebooks)

1. Pattern recognition speed (< 5-20 seconds per problem)
2. Cousin discrimination: "Why NOT sliding window?" "Why unbounded needs L→R?"
3. Loop direction invariants
4. Recognition cue vocabulary: monotone, boundary, in-degree-0, etc.
5. Post-answer reveals: always show full code + explanation

## What NOT to do

- Do NOT add code-writing questions (removed by design)
- Do NOT use generic wrong choices ("Brute force", "Sort first")
- Do NOT add extra features beyond what's listed in spec
- Do NOT remove the "View Full Code" reveal from speedrun answers
- Do NOT skip `topicId`/`subtopicId` on generated questions
