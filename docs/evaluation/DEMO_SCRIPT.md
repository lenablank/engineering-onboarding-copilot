### Technical Setup

- [ ] Close all unnecessary applications
- [ ] Clear browser cache and cookies
- [ ] Prepare browser tabs in order:
  1. Production homepage: https://engineering-onboarding-copilot.vercel.app
  2. GitHub repo: https://github.com/lenablank/engineering-onboarding-copilot
  3. Trello board: https://trello.com/b/7nSinl9T/engineering-onboarding-copilot-msse-capstone
  4. GitHub Actions: https://github.com/lenablank/engineering-onboarding-copilot/actions
- [ ] Test microphone (clear audio, no echo)
- [ ] Test screen recording (readable text, 1080p minimum)
- [ ] Have government-issued ID ready
- [ ] Set recording window to production site

### Environment

- [ ] Quiet room (no background noise)
- [ ] Good lighting (face clearly visible)
- [ ] Professional appearance
- [ ] Water nearby (stay hydrated!)

---

## 📝 SCRIPT

### SECTION 1: Introduction & ID Verification (1 minute)

**[ACTION: Start recording. Show yourself on camera. Smile. Hold up ID to camera for 5 seconds, then set it aside.]**

**YOU SAY:**

"Hello, my name is Elena Blank. I'm presenting the Engineering Onboarding Copilot.

**[ACTION: Pause while holding ID]**

Today, I'll be demonstrating a RAG-powered documentation assistant with automated gap detection. This is a full-stack project that I've built over twelve weeks, from conception through production deployment.

Let me share my screen and walk you through the entire system."

**[ACTION: Switch to screen share. Show homepage.]**

---

### SECTION 2: Problem Statement (1.5 minutes)

**[ACTION: Stay on homepage, use cursor to point at relevant text as you speak.]**

**YOU SAY:**

"The problem I'm solving is real: new engineers waste hours asking teammates basic questions like 'What's our deployment process?' Meanwhile, existing documentation is fragmented, outdated, or simply undiscoverable.

What makes this even worse is that teams don't know which documentation gaps exist until someone asks the same question for the third time.

My solution has three core capabilities:

First: It answers engineering questions with confidence scoring and source references.

Second: When it doesn't have enough information to answer confidently, it responds with a clear fallback message instead of hallucinating.

And three -- this is my favourite, it automatically logs those low-confidence questions as documentation gaps, creating a data-driven roadmap for improving your knowledge base over time.

So it can help to make documentation better with every question."

---

### SECTION 3: Architecture & Technology Decisions (2.5 minutes)

**[ACTION: Open GitHub repo, navigate to docs/technical/SYSTEM_ARCHITECTURE.md, scroll slowly to show diagrams]**

**YOU SAY:**

"Let me show you the architecture. This is a full-stack web application with a React frontend, a FastAPI backend, and a RAG pipeline powered by two free-tier APIs.

The frontend is built with Next.js 14, TypeScript, and Tailwind CSS. It's deployed on Vercel with automatic deployments on every git push.

The backend is Python with FastAPI, deployed on Render's free tier. The RAG pipeline uses three key components:

First, Cohere's model for embeddings. This is an, API-based, completely free model and it gives us a good semantic understanding.

Second, ChromaDB as our vector database. It's embedded, persistent, and handles all our semantic search.

Third, Groq's model for text generation. Groq gives us 14,400 free requests per day with incredibly fast inference times.

For documentation gap tracking, I'm using SQLite embedded in the backend—zero configuration, easy to inspect, perfect for this use case.

What I also want to emphasize about technology choices: the total infrastructure cost for this entire project is zero dollars. Not just 'cheap' — it's actually zero.

I made this decision deliberately to demonstrate that you can build production-quality AI systems without expensive infrastructure.

And because everything runs on free tiers, this system can stay deployed indefinitely without any recurring costs."

---

### SECTION 4: Feature Demo - Question & Answer (3.5 minutes)

**[ACTION: Navigate to production /ask page]**

**YOU SAY:**

"Now let me show you the core features. From the main page, let's go to the Ask page. I'm going to ask a question that I know is well-documented.

[Type]: 'How do I set up my development environment?'

[Click Ask]

Watch what happens. The system is querying the vector database, retrieving relevant documentation chunks, calculating confidence, and generating an answer.

[Wait for response]

Perfect. Look at this response. First, notice the confidence badge—77% confidence, which is above our 70% threshold. This tells the user the system found strong supporting evidence.

Second, see these sources at the bottom? Every answer links back to the original documentation. If I click on them, I can see exactly which files were used. This is crucial for trust -- users can verify the information themselves.

Now let me show you the fallback behavior. I'm going to ask something that's engineering-related but isn't covered in our documentation.

[Type]: 'What is our on-call rotation schedule?'

[Click Ask]

This is a legitimate operational question that engineers need to know, but our documentation focuses on technical setup, not team processes. Watch the confidence score.

[Wait for response]

See that? The confidence dropped to around 12%. The system recognizes this as a legitimate engineering question, but there's no documentation about on-call schedules in our knowledge base.

So instead of making something up, it responds with a clear message: 'This appears to be a valid engineering question, but we don't have documentation covering it yet. Your question has been logged to help us improve our knowledge base.'

This is the key to preventing hallucinations. When confidence is below 70%, we trigger a fallback response. And—this is important—if the question relates to engineering topics, we log it as a documentation gap.

Now, the system is smart enough to distinguish between valid questions and spam. If someone asks about the weather or types gibberish, they get a different response: 'This question doesn't appear to relate to engineering documentation.' Those don't get logged because they're not actionable documentation gaps.

And here's what I really love about this approach: the user can see the confidence score. If you've used ChatGPT, Claude, or most popular AI tools, they never show you confidence. You get an answer, and you have no idea if it's based on solid information or completely hallucinated. You have to trust blindly or manually verify everything.

With this system, that confidence badge is always visible. 77% confidence means strong evidence. Low confidence (below 70%) means the system doesn't have enough documentation to answer reliably. The user knows immediately whether to trust the answer or be skeptical. That transparency is critical for professional tools where wrong information has real consequences.

Now here's something important: the system uses intelligent spam filtering. It doesn't log every low-confidence question—only questions that actually relate to engineering topics.

Let me show you what I mean. If someone asks about the weather or any other unrelated topics, the system recognizes that's not engineering related and responds with a different message. Those questions never make it to the dashboard.

But if someone asks a legitimate engineering question like 'What's our on-call rotation?' —- that's a real operational question that engineers need to know. Even though we don't have documentation for it, the system recognizes it as valid and logs it there.

This filtering happens automatically using a confidence threshold of 11%. Questions below that are checked for engineering relevance. This keeps the Gap Radar clean and actionable.

But we remember, that our low-confidence question just got added to our Gap Radar, which I'll show you next."

**[ACTION: Pause briefly, let the screen settle]**

---

### SECTION 5: Feature Demo - Gap Radar (DIFFERENTIATOR) (5 minutes)

**[ACTION: Click "View Gaps" button or navigate to /gaps page]**

**YOU SAY:**

"This is the Gap Radar dashboard, and this is what makes this project unique.

Every time a user asks a question that the system can't answer confidently, it gets logged here with the question text, the confidence score, how many times it's been asked, and its status.

Look at this table. These are real gaps that have been detected during my testing. See this one here
'What is our on-call rotation schedule?' it's been asked multiple times with confidence around 12%. This tells me loud and clear: we need to add operational process documentation.

Now, let me show you the management workflow. Each gap has three statuses: New, Reviewed, and Resolved.

When a gap first appears, it's marked as 'New'—meaning the team hasn't looked at it yet.

I can filter to show only new gaps. [Click Status filter, select 'New']

A documentation maintainer would review these, and here's where the action controls come in. See this dropdown in the Actions column?

[Click the status dropdown for a gap, change it to 'Reviewed']

I can change the status directly from this table. Once a gap is acknowledged, I mark it as 'Reviewed.'

After the documentation is actually updated to address the gap, I mark it as 'Resolved.'

And if a gap turns out to be invalid or a duplicate, I can delete it entirely using this delete button.

[Point to delete button, don't actually delete]

The sorting let you organize to prioritize what to fix first.

[Click sort controls to show 'Most frequent first']

And look at these statistics at the top: total gaps logged, total occurrences across all gaps, and a breakdown by status. This is the data-driven roadmap for documentation improvement.

Here's why this matters: most documentation is written once and never updated. Teams don't know what's missing until someone complains. The Gap Radar flips that model. Now, every question -- even the ones you can't answer yet, becomes actionable data.

This dashboard tells you exactly where to focus your time. And because this is tracking frequency, you're not just fixing random gaps, you're fixing the gaps that matter most to your users."

**[ACTION: Pause for 2 seconds, let the point land]**

---

### SECTION 6: Code Walkthrough (4 minutes)

**[ACTION: Navigate to GitHub repo, go to backend/app/services/rag_service.py]**

**YOU SAY:**

"Now let me show you how this works under the hood. This is the RAG service—the core of the question-answering pipeline.

[Scroll to the ask_question method]

When a question comes in, we first generate an embedding using the Cohere API. That embedding gets compared against all the document chunks in our vector database.

[Scroll to the _calculate_confidence method]

Here's the confidence calculation. This is critical. I'm using three weighted factors:

Fifty percent weight on the similarity scores -— how well do the retrieved chunks match the question semantically?

Twenty-five percent weight on the number of unique sources -— are we pulling from multiple documents or just one?

And twenty-five percent weight on context sufficiency -- did we retrieve enough total text to actually answer the question?

If the final confidence is below 0.7, we trigger the fallback response. If it's below 0.15, we log it as a documentation gap.

[Scroll down to show gap logging]

I tested different weighting schemes during Sprint 2 and found this combination gives the best balance between answering questions and catching genuine gaps.

[ACTION: Navigate to backend/app/services/gap_service.py]\*\*

Now here's the Gap Service. When a low-confidence question comes in, we don't just log it blindly.

[Scroll to show the hash-based deduplication]

We calculate a hash of the question text to detect duplicates. If someone asks the exact same question ten times, it only creates one gap entry but increments the frequency counter.

We also store the retrieval context—what documents were considered—so you can debug why the confidence was low.

[ACTION: Navigate to frontend/src/app/gaps/page.tsx]\*\*

And here's the frontend for the Gap Radar. This is a React component with real-time filtering, sorting, and status updates.

[Scroll briefly to show the code structure]

Notice the API calls are clean, the error handling is comprehensive, and the UI updates are animated with Framer Motion for a polished user experience."

---

### SECTION 7: Testing & CI/CD (2.5 minutes)

**[ACTION: Navigate to GitHub repo, show backend/tests/ directory]**

**YOU SAY:**

"Let me show you the testing strategy. I have five test files covering 46 different test functions.

[Click on test_rag_pipeline.py]

This file tests the core RAG pipeline with mocked LLM responses. I'm testing that confidence calculations work correctly, that fallback behavior triggers at the right threshold, and that sources are properly extracted.

[Navigate to test_gap_service.py]

This file tests the gap detection logic—deduplication, frequency tracking, and status transitions.

These are automated tests that run on every commit through GitHub Actions.

[ACTION: Navigate to .github/workflows/ in the repo]\*\*

Here are my CI/CD workflows. I have two workflows: one for backend and one for frontend.

[Click on backend-ci.yml to show it]

The backend workflow installs Python dependencies, runs pytest with coverage reporting, and validates that all tests pass before the code can be merged.

[ACTION: Navigate to GitHub Actions tab]\*\*

And here you can see the actual CI/CD runs. Every push to the main branch triggers these checks automatically.

[Point to a recent successful run]

Green checkmarks mean the build passed. If a test fails, the workflow fails, and I get immediate feedback that something broke.

This is continuous integration in action—automated testing on every commit ensures code quality and catches bugs before they reach production."

---

### SECTION 8: Deployment & Infrastructure (1.5 minutes)

**[ACTION: Show Trello board]**

**YOU SAY:**

"Let me show you the agile process. This is my Trello board documenting all three sprints.

[Scroll through Sprint 0, 1, 2, 3 columns briefly]

Sprint 0 was planning and proof-of-concept. Sprint 1 built the core RAG pipeline. Sprint 2 added the Gap Radar feature. And Sprint 3 focused on production deployment and testing.

[ACTION: Return to production application]\*\*

Now, the deployment. The frontend is hosted on Vercel—free tier, automatic deployments, built-in CDN. The backend is on Render—also free tier.

The entire system is live and has been running in production for two weeks.

---

### SECTION 9: Evaluation & Results (1.5 minutes)

**[ACTION: Navigate to GitHub repo, open docs/evaluation/sprint-3-formal-evaluation.md or show it on screen]**

**YOU SAY:**

"Before recording this demo, I ran a formal evaluation with ten test cases covering different question types and edge cases.

[Scroll to show the test results table]

The results: ten out of ten test cases passed with an average response time of 1.4 seconds. That's 100% accuracy.

The test cases included well-documented questions, undocumented questions, edge cases like empty input, and every question was handled appropriately.

This evaluation is documented in the repository with full details on each test case, the expected behavior, the actual behavior, and the confidence scores."

---

### SECTION 10: Conclusion & Reflection (1.5 minutes)

**[ACTION: Return to the homepage or stay on evaluation doc]**

**YOU SAY:**

"To summarize: I've built a production-quality RAG application with three core features—question answering with confidence scoring, fallback behavior to prevent hallucinations, and automated documentation gap detection.

The system is deployed, tested, and has been running in production for two weeks. It's documented with design and testing documentation, backed by comprehensive automated tests, and deployed through CI/CD pipelines.

The total infrastructure cost is zero dollars, demonstrating that you can build sophisticated AI systems without expensive infrastructure.

What I learned from this project: First, confidence scoring is essential for production RAG systems. Users need to know when they can trust an answer.

Second, the Gap Radar feature taught me that AI systems shouldn't just answer questions —- they should identify when they can't answer and show it as actionable data.

Third, cost-conscious engineering matters. Free tiers are completely viable for many production use cases if you architect thoughtfully.

If I were to extend this project, I'd add three things: user authentication so teams can track who's asking what, integration with Slack so engineers can ask questions without leaving their workflow, and maybe automated weekly reports showing the most frequent gaps so teams can prioritize documentation work.

Thank you for watching. All the code, documentation, and evaluation results are available in the GitHub repository. I'm very grateful for this experience."

**[ACTION: Show yourself on camera again briefly, smile]**

**[End recording]**

---

## 🎯 POST-RECORDING CHECKLIST

- [ ] Watch the full recording to verify:
  - [ ] ID was clearly visible (5 seconds minimum)
  - [ ] Audio is clear throughout (no muting, no echo)
  - [ ] Screen share is readable (all text legible)
  - [ ] Demo flows smoothly (no technical issues)
  - [ ] All features demonstrated work correctly
  - [ ] Timing is 15-20 minutes (check actual length)
- [ ] Export as MP4 (H.264 codec, 1080p, <500MB if possible)
- [ ] Upload to YouTube as unlisted video
- [ ] Test that video plays correctly on YouTube
- [ ] Copy YouTube link and add to CAPSTONE_SUBMISSION_LINKS.md
- [ ] Commit and push the updated links file

---

## 📌 IMPORTANT REMINDERS

### Things That Will Cost You Points:

- ❌ Video shorter than 15 minutes or longer than 20 minutes
- ❌ ID not visible or not clearly legible
- ❌ Features don't work during demo (TEST EVERYTHING BEFORE RECORDING!)
- ❌ Audio is unclear or missing
- ❌ Screen share is pixelated or text is unreadable
- ❌ You're not visible on camera
- ❌ Unprofessional presentation (messy background, casual language, etc.)

### Things That Will Earn You Points:

- ✅ Thorough demonstration of ALL features
- ✅ Clear explanation of technical decisions and trade-offs
- ✅ Professional delivery and presentation
- ✅ Deployed, working application
- ✅ Evidence of testing and CI/CD
- ✅ Documentation of gap detection (your differentiator!)
- ✅ Exactly 15-20 minutes (shows you practiced and timed it)

---

## 💡 TIPS FOR SUCCESS

1. **Practice 2-3 times before recording**: Get comfortable with the flow, smooth out rough spots
2. **Have water nearby**: Your mouth will get dry talking for 18 minutes
3. **Speak clearly and at a moderate pace**: Pretend you're explaining to a senior engineer who's new to the project
4. **Use your cursor to point**: Help viewers follow along by highlighting what you're talking about
5. **Smile at the beginning and end**: First impressions and last impressions matter
6. **If something breaks during recording**: Acknowledge it briefly, explain why (e.g., "cold start delay"), and move on professionally
7. **Don't apologize unnecessarily**: You built something impressive—own it!

---

**Good luck! You've got this. 🚀**
