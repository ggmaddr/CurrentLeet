# LeetCode Mastery Game Spec

## 1. Purpose

Build an interactive study game that converts the author's two core notebooks:

- `/Users/gradyta/gresource/CurrentLeet/leet A1.ipynb`
- `/Users/gradyta/gresource/CurrentLeet/leetA2.ipynb`

into a personal LeetCode training system optimized for:

- pattern recognition
- very fast problem classification
- distinguishing near-lookalike problem families
- extracting 1-2 key insights per problem
- memorizing reusable code templates
- reinforcing comments, notes, visual metaphors, and handwritten-style explanations
- training under interview pressure using speed rounds

This is not a generic LeetCode app. It is a personalized cognitive training system built from the author's own notebook style, language, comments, contrasts, and mental models.

## 2. Product Vision

The product should feel like a study RPG plus an interview drill simulator.

Core fantasy:

- The player moves through knowledge regions.
- Each region represents a pattern family or algorithmic world.
- Each node contains problems, pattern templates, key insights, traps, and comparison checkpoints.
- Encounters are short, dense, and replayable.
- The system emphasizes “why this pattern, not the similar one?” more than full coding from scratch.

The app should train the player to answer questions like:

- What pattern is this?
- What tiny keyword changes the answer?
- Is this combinations or permutations?
- Is this sliding window, prefix sum, binary search on answer, DP, graph shortest path, or multiple valid formulations?
- Which invariant makes the solution work?
- Which loop order matters?
- Which state definition matters?
- Which edge case usually breaks this pattern?

## 3. Source-of-Truth Content

The authoritative knowledge sources are the two notebooks above.

### 3.1 Notebook roles

`leet A1.ipynb` is primarily:

- Arrays & Hashing
- Intervals
- Two Pointers
- Prefix Sum
- Stack / Monotonic Stack
- Binary Search
- Sliding Window
- Linked List
- Trees
- Tries
- Backtracking
- Heap / Priority Queue

`leetA2.ipynb` is primarily:

- Graphs
- Matrix as Graph
- Implicit Graph
- Topological Sort
- Shortest Path Algorithms
- MST / Union Find
- Dynamic Programming
- Knapsack
- Interval DP
- Tree DP
- Bitmask DP
- Greedy
- Divide & Conquer
- Segment Tree
- Miscellaneous advanced topics

### 3.2 Content style observed from the notebooks

The implementation must preserve these notebook-native traits:

- Pattern-first teaching, not problem-first teaching
- Heavy use of comparison language: “same as X except Y”
- Repeated emphasis on exact loop direction and state transitions
- Repeated distinction between superficially similar problem types
- Use of compact templates
- Strong attention to edge cases and failure modes
- Visual and spatial explanations
- Recognition cues from wording in the prompt
- Multiple approaches per problem when useful
- Notes that explain when one approach is optimal, educational, or just alternative

### 3.3 Explicit learning behaviors to preserve

The game must support the author's real learning style:

- micro-attention to wording differences
- concept clustering into a network/map
- comparing cousins inside the same pattern family
- extracting one decisive insight per problem
- learning by contrasts, templates, and repeat exposure
- memorizing “recognition signatures”
- understanding when a problem can belong to more than one pattern family
- visualizing transitions, intervals, windows, graph layers, DP state flow, and stack behavior

## 4. Primary Product Goals

### 4.1 Goal A: Pattern recognition speed

Train the player to identify likely solution families in under 5-20 seconds.

### 4.2 Goal B: Contrast mastery

Train the player to distinguish:

- combinations vs permutations
- subset vs subsequence vs substring vs subarray
- BFS vs DFS vs Dijkstra vs topo-DP
- sliding window vs prefix sum + hashmap
- monotonic stack vs heap vs deque
- 0/1 knapsack vs unbounded knapsack vs bounded knapsack
- LIS DP vs LIS binary-search tails
- interval DP shrink vs interval DP split
- backtracking vs memoized DFS vs DP
- graph traversal vs graph DP vs union-find
- binary search on index vs binary search on answer

### 4.3 Goal C: Insight retention

For every problem, surface the smallest number of highest-value facts:

- the main recognition trigger
- the key invariant
- the trap or confusion point
- the critical implementation detail

### 4.4 Goal D: Interview readiness

Train for:

- speed
- verbal explanation
- pattern naming
- tradeoff explanation
- handling “similar but different” follow-up questions

### 4.5 Goal E: Active coaching and progress monitoring

The app must not only quiz. It must actively monitor learning quality over time.

It should detect:

- which areas are untouched
- which areas are weak
- which areas are slow
- which areas are recognized but not implemented well
- which areas are repeatedly confused with sibling patterns

It should then respond by:

- increasing repetition on weak distinctions
- escalating difficulty gradually
- requesting short code-writing drills when recognition alone is insufficient
- surfacing progress bars and gap summaries clearly
- recommending the next best study target

## 5. Non-Goals

The first version should not prioritize:

- a generic public content marketplace
- social features
- polished multiplayer
- automatic code execution for every question type
- broad support for arbitrary notebooks beyond these two sources

Those can come later. V1 should optimize for personalized study effectiveness.

## 6. Recommended Implementation Shape

Build this as a local-first web app.

Recommended stack:

- Frontend: React + TypeScript + Vite
- Styling: CSS variables plus hand-crafted CSS, not a heavy component library by default
- State: Zustand or Redux Toolkit
- Persistence: local JSON or SQLite-backed local service
- Notebook parsing: Python or Node-based extraction pipeline
- Content format after extraction: JSON

Why:

- easy local iteration
- easy card/game rendering
- easy keyboard-first interaction
- straightforward notebook parsing pipeline
- future-friendly for animations and map UI

## 7. Core Architecture

The app should have two major layers:

### 7.1 Knowledge Extraction Layer

Responsible for:

- parsing notebooks
- segmenting content into topics/problems/notes/code blocks/images
- extracting key insights
- building structured content records
- generating question candidates
- building cross-links between similar problems

### 7.2 Gameplay Layer

Responsible for:

- world map navigation
- question sessions
- speedruns
- flashcards
- code-writing drills
- mastery tracking
- streaks
- spaced repetition
- adaptive resurfacing of weak patterns
- coaching feedback
- notification scheduling hooks

## 8. Content Model

Define these entities.

### 8.1 Topic

Represents a major pattern family.

Example fields:

- `id`
- `title`
- `sourceNotebook`
- `displayOrder`
- `description`
- `worldRegion`
- `subtopics[]`
- `prerequisites[]`
- `relatedTopics[]`

Examples:

- Arrays & Hashing
- Binary Search
- Graphs
- Knapsack DP
- Interval DP

### 8.2 Subtopic

Represents a narrower unit inside a topic.

Example:

- Monotonic Stack
- Kahn Toposort
- Dual-Sequence DP
- Matrix as Graph

Fields:

- `id`
- `topicId`
- `title`
- `summary`
- `recognitionCues[]`
- `templateRefs[]`

### 8.3 Problem

Represents a specific notebook problem entry.

Fields:

- `id`
- `leetcodeNumber`
- `title`
- `difficulty`
- `topicId`
- `subtopicId`
- `sourceNotebook`
- `sourceCellIndexes[]`
- `externalLinks[]`
- `problemSummary`
- `authorNotes`
- `keyInsights[]`
- `pitfalls[]`
- `recognitionSignals[]`
- `approaches[]`
- `templateTags[]`
- `visualAssets[]`
- `similarProblemIds[]`
- `contrastProblemIds[]`
- `multiPatternTags[]`

### 8.4 Approach

Represents one solution path for a problem.

Fields:

- `id`
- `problemId`
- `name`
- `pattern`
- `timeComplexity`
- `spaceComplexity`
- `isPrimary`
- `isEducational`
- `whenToUse`
- `whenNotToUse`
- `coreInvariant`
- `implementationNotes[]`
- `templateSnippet`

### 8.5 Insight

This is the most important unit in the whole system.

Fields:

- `id`
- `problemId`
- `kind`
- `text`
- `importance`
- `sourceType`

`kind` examples:

- recognition
- invariant
- loop-order
- edge-case
- compare-contrast
- state-definition
- visual-memory
- trap

### 8.6 Template

Reusable coding skeletons.

Examples:

- BFS layer traversal
- DFS with visited
- backtracking choose/explore/unchoose
- monotonic stack nearest greater/smaller
- binary search left bound
- 1D knapsack optimized loop directions
- topo sort Kahn template
- memo DFS

Fields:

- `id`
- `title`
- `pattern`
- `code`
- `explanation`
- `signatureTriggers[]`
- `relatedProblemIds[]`

### 8.7 Comparison Edge

Represents “looks similar but differs in this tiny way.”

This is central to the author’s learning style.

Fields:

- `id`
- `leftEntityId`
- `rightEntityId`
- `edgeType`
- `differenceSummary`
- `decisionRule`
- `triggerKeywords[]`

`edgeType` examples:

- same-pattern-different-goal
- same-template-different-loop-order
- same-surface-different-state
- alternate-solution-family
- common-confusion

### 8.8 Question

Represents a playable prompt.

Fields:

- `id`
- `sourceEntityId`
- `questionType`
- `prompt`
- `answer`
- `acceptedAnswers[]`
- `choices[]`
- `explanation`
- `difficulty`
- `timeLimitSec`
- `tags[]`
- `masteryWeight`
- `revealFullCodeAfterAnswer`
- `revealFullExplanationAfterAnswer`

### 8.9 Attempt

Represents one player interaction with one question.

Fields:

- `id`
- `questionId`
- `answeredCorrect`
- `responseTimeMs`
- `confidence`
- `usedHint`
- `inputMode`
- `freeTextAnswer`
- `codeSubmission`
- `masteryDelta`
- `weaknessTags[]`
- `timestamp`

### 8.10 Skill Profile

Represents the player model used to adapt study plans.

Fields:

- `topicId`
- `subtopicId`
- `recognitionScore`
- `implementationScore`
- `contrastScore`
- `speedScore`
- `retentionScore`
- `attemptCount`
- `lastReviewedAt`
- `untouched`
- `needsAttention`
- `recommendedNextAction`

## 9. Notebook Extraction Requirements

The extraction pipeline must parse raw `.ipynb` files into structured game content.

### 9.1 Cell segmentation

Parse each notebook cell and classify it as:

- topic heading
- subtopic heading
- problem heading
- concept note
- code solution
- alternate solution
- image reference
- implementation note
- comparison note
- template note

### 9.2 Heading detection

Infer hierarchy from markdown headings:

- `##` major topic
- `###` section/subtopic/difficulty bucket
- `####` usually problem or concept heading
- lower headings may indicate sub-approaches, theory notes, or implementation details

### 9.3 Problem pairing

A problem often appears as:

- markdown problem title
- then one or more code cells
- then explanatory markdown
- then alternate code

The extractor should group adjacent related cells into one problem record.

### 9.4 Code-comment mining

Many crucial insights live in code comments, not only markdown.

Extractor must scan comments for signals like:

- `Idea`
- `Approach`
- `Key`
- `Pattern`
- `Intuition`
- `Note`
- `Edge case`
- `trap`
- `same as`
- `difference`
- `why`
- complexity notes
- loop-order notes

### 9.5 Link mining

Preserve external links such as:

- LeetCode
- AlgoMonster
- visualizers
- diagrams

### 9.6 Image mining

If markdown references local assets, preserve those relationships.

Observed asset usage includes diagrams for:

- move zeroes
- trapped water
- stack behavior
- graph intuition
- DP visualizations
- knapsack
- skyline
- LCS/SCS
- subsets/permutations

### 9.7 Alternate approaches

If the same problem has multiple approaches, do not flatten them into one.

Capture each approach separately when the notes indicate:

- optimal vs educational
- brute force vs optimized
- DP vs BFS
- DFS vs BFS
- heap vs stack
- binary search vs DP

## 10. Insight Extraction Rules

This is the highest-priority logic in the system.

For each problem, extract a maximum of:

- 1 primary recognition insight
- 1 primary invariant insight
- 1 primary pitfall insight
- 1 primary implementation insight
- 1 primary compare/contrast insight if present

The system should prefer compact, high-value insights over verbose summaries.

### 10.1 Examples of insight categories

Recognition:

- “Order matters -> permutations -> target outer loop / recursive accumulate by sum.”
- “Need shortest path in unweighted graph -> BFS.”
- “Need nearest greater/smaller relationship -> monotonic stack.”

Invariant:

- “Increasing mono-stack keeps candidate indices whose values are strictly increasing.”
- “For optimized 0/1 knapsack, iterate capacity right-to-left.”
- “For unbounded knapsack, iterate capacity left-to-right.”

Pitfall:

- “Sliding window with shrinking only works when all values are non-negative.”
- “Binary search on closest elements must not use `abs()` in the comparison rule.”
- “Combination Sum IV counts permutations, not combinations.”

Implementation:

- “Use `remain == 0` / `target hit` as the score point.”
- “Store earliest index for a prefix-balance.”
- “Use border-start traversal instead of per-cell traversal.”

Compare/contrast:

- “Coin Change II counts combinations; Combination Sum IV counts permutations.”
- “LIS has O(n^2) DP and O(n log n) tails methods with different goals and reconstructability tradeoffs.”

Implementation reveal:

- “After the player answers, show the full notebook-derived solution code for the referenced problem whenever available.”
- “After the player answers, explain why the answer was right or wrong and connect it to the full solution.”

## 11. Cross-Linking Rules

The app must not treat problems as isolated flashcards. It must build a network.

### 11.1 Similarity edges

Create links for:

- same pattern
- same template
- same invariant
- same data structure
- same transition type

### 11.2 Contrast edges

Create links for:

- same-looking but different
- different loop order
- different state definition
- order matters vs does not matter
- can use two families, but one is primary

### 11.3 Multi-pattern edges

If a problem can be solved by multiple paradigms, mark:

- primary approach
- secondary approach
- tradeoff note

Examples from the notebooks:

- DP and binary search on answer
- BFS and DP
- DFS memo and bottom-up DP
- heap and quickselect

## 12. Game World Design

The world map should represent algorithmic regions, not a literal fantasy game with unrelated lore.

The UI metaphor can still be playful.

### 12.1 Suggested world regions

- Arrays Plains
- Interval Crossing
- Two Pointer River
- Prefix Sum Archive
- Stack Forge
- Binary Search Observatory
- Window District
- Linked List Dock
- Tree Canopy
- Trie Library
- Backtracking Labyrinth
- Heap Tower
- Graph Frontier
- Topology Citadel
- Shortest Path Transit
- Union Find Quarry
- DP Basin
- Knapsack Depot
- Interval DP Hall
- Bitmask Vault
- Greedy Market
- Segment Tree Observatory

### 12.2 Region goals

Each region should contain:

- topic intro
- recognition cues
- pattern templates
- problem encounters
- comparison gates
- checkpoint boss rounds

### 12.3 Unlocking

Unlock by:

- completing required encounters
- reaching a mastery threshold
- clearing comparison gates that prove discrimination skill

## 13. Game Modes

The app must support multiple complementary training modes.

### 13.1 Explore Mode

Free navigation on the pattern map.

Use cases:

- browse a topic
- review problem clusters
- inspect contrast links
- open notebooks-derived notes

### 13.2 Flashcard Mode

Fast review of atomic facts.

Card styles:

- problem -> pattern
- pattern -> recognition signal
- invariant -> pattern
- problem -> pitfall
- code snippet -> what template is this?

### 13.3 Speedrun Mode

Timed burst of questions.

This is critical for interview prep.

Round lengths:

- 60 sec
- 3 min
- 5 min
- custom

Prompt density should be high.

After each answered prompt in speedrun mode, the app should still support a fast reveal panel containing:

- correctness
- score delta
- key insight
- full code for the referenced problem
- concise explanation

The reveal should be skippable for pure speed sessions and expandable for review sessions.

### 13.4 Compare Mode

A dedicated mode for “same but different.”

Example prompts:

- Combination Sum II vs Combination Sum IV
- Coin Change I vs Coin Change II
- Subsets vs Permutations
- BFS shortest path vs Dijkstra
- LCS vs Edit Distance vs SCS

### 13.5 Boss Mode

Mixed high-pressure diagnostic challenge.

Features:

- pattern identification
- mini explanation
- edge-case check
- choose best approach
- reject wrong lookalike

### 13.6 Template Drill Mode

Show a pattern skeleton with blanks:

- missing loop direction
- missing base case
- missing visited logic
- missing stack pop condition

### 13.7 Memory Palace / Network Mode

A concept graph where nodes are problems and edges represent similarity/contrast.

The player should be able to traverse:

- from a problem to its siblings
- from a pattern to all canonical examples
- from a confusion point to all problems that teach that distinction

### 13.8 Code Writing Drill Mode

This mode is required.

Purpose:

- force active recall beyond recognition
- train small implementation chunks
- reveal whether the player truly owns the template

Prompt styles:

- write the base case
- write the DFS skeleton
- write the BFS queue initialization
- write the monostack pop loop
- write the DP transition
- fill in the loop direction
- complete a small missing code block

The system should start with tiny code fragments and gradually increase difficulty to longer or more complete implementations.

## 14. Question Types

The app should generate many question types from the same source content.

### 14.1 Recognition questions

Examples:

- “What pattern is most likely?”
- “Which data structure is the key one here?”
- “What is the best first approach to try?”

### 14.2 Fill-in-the-blank

Examples:

- “For optimized 0/1 knapsack, iterate capacity from ___ to ___.”
- “Shortest path in unweighted graph -> ___.”
- “Order matters means we are counting ___, not ___.”

### 14.3 Multiple choice

Examples:

- choose primary pattern
- choose invariant
- choose correct pitfall
- choose correct loop order

### 14.4 This-or-that comparison

Examples:

- “Is this combinations or permutations?”
- “Sliding window or prefix sum + hashmap?”
- “BFS or topo sort?”

### 14.5 Why-not questions

Examples:

- “Why does normal sliding window fail here?”
- “Why is `abs()` wrong in this binary-search comparison?”
- “Why can’t we use left-to-right for optimized 0/1 knapsack?”

### 14.6 Ordered steps

Examples:

- arrange algorithm steps in correct order
- arrange binary-search decision logic
- arrange backtracking flow

### 14.7 Code-template questions

Examples:

- identify the template from a snippet
- patch one missing line
- choose the correct base case

### 14.8 Small code writing prompts

Examples:

- “Write the DFS function signature and base case.”
- “Write the left/right pointer update for this binary-search condition.”
- “Write the optimized 1D knapsack loop in the correct direction.”
- “Write the choose/explore/unchoose skeleton.”

These should accept short code snippets, not only full solutions.

### 14.9 Explain-in-one-line questions

Examples:

- “State the key invariant.”
- “What makes this problem a DAG DP?”
- “Why is this a monotonic stack problem?”

### 14.10 Visual reasoning questions

When diagrams exist, ask:

- which boundary matters?
- what does the stack store?
- what do the edges mean?
- what does `dp[i][j]` represent?

### 14.11 Post-answer reveal contract

This is mandatory for the learning experience.

After the player answers a question, the app should reveal:

1. whether the answer is correct
2. updated score / mastery impact
3. the key reason
4. the full notebook-derived code for the referenced problem if available
5. a clear explanation tied to that exact problem
6. optionally, a comparison link to the nearest confusing sibling problem

Even for multiple-choice questions, the player should be able to inspect the full code afterward.

## 15. Personalization Rules

Because this app is built from the author’s notebooks, it must preserve the author’s vocabulary and emphasis.

### 15.1 Preferred tone

Use language like:

- key idea
- tiny difference
- same as X except Y
- caution
- edge case
- loop direction matters
- recognition cue
- pattern signature
- primary trap

### 15.2 Preserve multiple representations

For a concept, preserve:

- formal definition
- compact verbal shortcut
- code template
- comparison note
- visual analogy if present

### 15.3 Do not over-normalize

Do not rewrite all notebook content into sterile textbook prose.

Keep:

- compact style
- emphatic notes
- “this is the only diff”
- “must go R->L”
- “order matters”
- “same as X”

Those phrases are valuable memory anchors.

## 16. Mastery System

The app must track mastery at multiple levels.

### 16.1 Trackable units

- topic mastery
- subtopic mastery
- problem familiarity
- insight recall
- compare/contrast accuracy
- speed under time pressure
- code implementation ability
- untouched coverage

### 16.2 Suggested mastery dimensions

- `recognitionScore`
- `invariantScore`
- `implementationScore`
- `contrastScore`
- `speedScore`
- `retentionScore`
- `coverageScore`

### 16.3 Mastery updates

Increase score more when:

- the answer is correct
- answered fast
- answered in boss mode
- answered after long delay
- the item was historically weak

Decrease or flag when:

- repeatedly missing the same distinction
- confusing cousin problems
- knowing the pattern but missing the invariant
- answering correctly but too slowly
- failing small code-writing prompts

### 16.4 Progress bars and diagnostics

The UI must always expose visible progress indicators.

Required dashboards:

- overall mastery bar
- per-topic mastery bars
- untouched-area indicator
- weak-area indicator
- slow-area indicator
- implementation-vs-recognition split

Examples of player-facing feedback:

- “Strong recognition, weak implementation in Graph BFS.”
- “You have not touched Interval DP yet.”
- “Binary Search accuracy is good, but response time is below target.”

## 17. Spaced Repetition

This app should use spaced repetition, but not only on problem titles.

Review units should include:

- problem-pattern mapping
- key insights
- common traps
- compare/contrast pairs

Schedule should prioritize:

- weak areas
- high-confusion pairs
- interview-critical patterns
- untouched areas that must be covered before the interview

## 18. Adaptive Difficulty

The game should dynamically adapt.

### 18.1 If the player is strong in a topic

Shift toward:

- comparisons
- edge cases
- alternate approaches
- “why not” questions

### 18.2 If the player is weak in a topic

Shift toward:

- easier recognition
- single-insight cards
- template recall
- canonical examples

### 18.3 If the player is specifically confusing cousins

Increase frequency of:

- pairwise comparisons
- micro-keyword discrimination
- loop-order discrimination
- state-definition discrimination

### 18.4 Difficulty ramp

The system must escalate difficulty over time.

Recommended progression:

1. recognition only
2. recognition + explanation
3. compare/contrast
4. invariant and pitfall recall
5. small code fragment writing
6. larger code completion
7. mixed boss-mode under time pressure

Difficulty should also rise within a topic when the player becomes consistently correct and fast.

## 19. Extraction Heuristics for AI-Generated Questions

When generating questions automatically from notebook content, use these heuristics.

### 19.1 Question generation priority order

1. compare/contrast
2. recognition cue
3. key invariant
4. common pitfall
5. implementation detail
6. complexity recall

### 19.2 Good automatic question seeds

Generate questions from lines containing:

- “Key”
- “Idea”
- “Approach”
- “Intuition”
- “Pattern”
- “same as”
- “difference”
- “must”
- “only diff”
- “careful”
- “edge case”
- “optimal”

### 19.3 Avoid low-value cards

Do not generate too many cards that only ask:

- exact complexity with no conceptual value
- trivial syntax
- copied problem statements

Prefer cards that test discrimination and reasoning.

## 20. UX Requirements

### 20.1 Keyboard-first

Must support:

- arrow keys
- number shortcuts for choices
- enter to reveal
- space to continue
- hotkeys to mark confidence

### 20.2 Fast loops

The app should minimize dead time between prompts.

Desired rhythm:

- prompt appears fast
- user answers fast
- feedback is compact
- move to next immediately

### 20.3 Information density

Design for serious study, not casual trivia.

Each screen should surface:

- the essential prompt
- time pressure if active
- confidence input
- concise explanation after answer
- related comparison if helpful

### 20.4 Visual language

Should feel intentional and map-like, not generic dashboard UI.

Use:

- regions
- paths
- nodes
- unlock gates
- mastery glow or signal
- pattern clusters

### 20.5 Persistent coaching HUD

During practice, include a persistent progress HUD with:

- current score
- streak
- timer
- current region/topic
- mastery bar
- weak-area badge
- untouched-area badge
- optional “focus next” recommendation

## 21. Suggested UI Screens

### 21.1 Home / Command Center

Shows:

- today’s review queue
- weak patterns
- current streak
- next recommended region
- speedrun quick start
- untouched regions
- notification/reminder status

### 21.2 World Map

Shows:

- major pattern regions
- completion status
- locked/unlocked areas
- relation lines between regions

### 21.3 Topic Region Screen

Shows:

- canonical templates
- core recognition cues
- problem nodes
- compare gates
- weak spots

### 21.4 Problem Detail Screen

Shows:

- notebook-derived title and links
- key insights
- approaches
- pitfalls
- template
- similar and contrast problems
- linked assets

### 21.5 Session Screen

Used for:

- flashcards
- speedrun
- boss mode

### 21.6 Review Results Screen

Shows:

- missed distinctions
- missed patterns
- timing bottlenecks
- recommended follow-up drills
- code-writing weaknesses
- areas not yet touched

### 21.7 Notifications / Reminder Settings

Shows:

- browser notification permission state
- reminder schedule
- study streak reminders
- “nudge me when I missed today” option
- quiet hours

## 22. Data Pipeline

The implementation should include a repeatable build pipeline.

### 22.1 Pipeline stages

1. Read notebooks
2. Parse cells
3. Detect hierarchy
4. Group problems and approaches
5. Extract notes/comments/assets/links
6. Normalize structured records
7. Build graph edges
8. Generate question bank
9. Save JSON artifacts

### 22.2 Output files

Suggested generated artifacts:

- `generated/topics.json`
- `generated/problems.json`
- `generated/approaches.json`
- `generated/templates.json`
- `generated/questions.json`
- `generated/edges.json`
- `generated/assets.json`
- `generated/full_solutions.json`

## 23. Suggested JSON Shapes

### 23.1 Problem example

```json
{
  "id": "lc-377-combination-sum-iv",
  "leetcodeNumber": 377,
  "title": "Combination Sum IV",
  "topicId": "dp-knapsack",
  "subtopicId": "unbounded-knapsack",
  "sourceNotebook": "leetA2.ipynb",
  "sourceCellIndexes": [232, 234],
  "problemSummary": "Count ordered ways to reach target.",
  "keyInsights": [
    {
      "kind": "compare-contrast",
      "text": "Order matters here, so count permutations rather than combinations."
    },
    {
      "kind": "implementation",
      "text": "Use target as the outer loop in 1D DP to allow different orders."
    }
  ],
  "contrastProblemIds": ["lc-518-coin-change-ii"],
  "templateTags": ["1d-dp", "unbounded", "permutations"]
}
```

### 23.2 Comparison edge example

```json
{
  "id": "edge-377-vs-518",
  "leftEntityId": "lc-377-combination-sum-iv",
  "rightEntityId": "lc-518-coin-change-ii",
  "edgeType": "same-template-different-loop-order",
  "differenceSummary": "Both use coin/target-style DP, but one counts permutations and the other counts combinations.",
  "decisionRule": "If order matters, use the permutation formulation.",
  "triggerKeywords": ["order matters", "different sequences", "arrangements"]
}
```

## 24. V1 Functional Requirements

The first shippable version must support:

- notebook ingestion from the two source files
- generated structured content
- a world map with topic regions
- flashcards
- speedrun mode
- compare mode
- code-writing drill mode
- mastery tracking
- progress bars by topic and overall
- untouched-area tracking
- slow-area tracking
- local persistence
- problem detail pages
- linked similar/contrast navigation
- post-answer reveal with full code and explanation
- browser notification reminders for study

## 25. V1.5 / V2 Ideas

Future features:

- manual curation UI for fixing extracted insights
- voice answer mode
- spoken interview simulation
- write-code sandbox
- hand-drawn diagram overlay
- import more notebooks
- AI tutor follow-up explanation generator
- auto-build daily drill packs

Notification upgrades:

- system-level desktop notifications via wrapper app if available
- adaptive reminders based on missed sessions

## 26. Evaluation Criteria

The build is successful if it helps the author:

- identify patterns faster
- confuse fewer lookalike problems
- recall key insights under time pressure
- explain why one approach beats another
- build a mental network instead of isolated memorization
- improve implementation fluency, not just recognition
- visibly close untouched gaps before the interview

## 27. Implementation Priorities

Recommended execution order:

1. Build notebook parser
2. Build structured content JSON
3. Build comparison-edge generator
4. Build full-solution extraction and post-answer reveal
5. Build flashcards and speedrun
6. Build code-writing drills
7. Build topic/world map
8. Add adaptive review, mastery refinement, and notifications

## 28. Critical Quality Bar

The implementation must respect this rule:

The best content in the system is not the full code solution. The best content is the distilled pattern cue, contrast rule, invariant, and trap that lets the author solve the problem again from memory.

If there is a tradeoff between:

- showing more raw material
- or surfacing the smallest decisive insight

prefer the smallest decisive insight.

## 29. AI Agent Instructions

If another AI agent implements this project, it should:

- treat the two notebooks as primary source material
- preserve author-specific phrasing when useful
- heavily emphasize compare/contrast relationships
- avoid generic educational filler
- extract notebook comments as first-class learning objects
- model questions around recognition and discrimination, not just recollection
- preserve alternate approaches where they teach an important distinction
- monitor the player continuously and adapt difficulty upward
- distinguish recognition skill from implementation skill
- reveal full notebook-derived code after question attempts whenever possible
- show explicit progress bars, weak areas, slow areas, and untouched areas
- include browser notification support for study reminders
- build the content graph before building fancy UI polish

## 30. Immediate Next Deliverables

After this spec, the next practical implementation docs should be:

- a parser spec for `.ipynb` extraction
- a JSON schema file for topics/problems/questions/edges
- a screen-by-screen UI spec
- a gameplay loop spec
- a content curation workflow for correcting AI extraction mistakes
