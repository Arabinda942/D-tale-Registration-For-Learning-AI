# -*- coding: utf-8 -*-
"""
Deterministic 50-assignment generator.
Same chapter -> same 50 assignments, every time (needed so completed-index
tracking in the database stays valid across restarts).
"""

CONCEPT_TEMPLATES = [
    "In your own words, explain what '{k}' means and why it matters. (3\u20134 sentences)",
    "Give one real-world example of '{k}' that you have personally seen or used.",
    "What would change if '{k}' did not exist? Write 3 sentences.",
    "Teach '{k}' to a friend who has never heard of it, in 80 words or fewer.",
    "Write one question you would ask an expert about '{k}', and your best guess at the answer.",
    "List 2 things you already knew about '{k}' and 1 thing that surprised you in this chapter.",
    "Find one recent article, video, or post about '{k}' and summarize it in 2 sentences.",
    "Sketch a simple diagram (on paper) explaining '{k}', then describe it in words below.",
    "Where in your daily life or studies could '{k}' actually be useful? Be specific.",
    "Write a 1-line definition of '{k}' simple enough for a 10-year-old to understand.",
    "Explain '{k}' to someone who disagrees it's useful \u2014 what would you say?",
    "What's the biggest misconception people have about '{k}'? How would you correct it?",
]

PRACTICE_TEMPLATES = [
    "Try '{k}' yourself right now. Write 3 sentences about what happened.",
    "Use '{k}' to solve one small real problem from your own life, studies, or work.",
    "Search for 3 companies or products that rely on '{k}' and name them.",
    "Compare '{k}' to one other idea from this chapter \u2014 2 similarities, 2 differences.",
    "Spend 10 minutes exploring '{k}' hands-on, then write down one thing that didn't work as expected.",
    "Explain '{k}' using an analogy you came up with yourself (not one from the chapter).",
    "Ask someone else what they think '{k}' means, then compare it to the chapter's definition.",
]

CODE_TEMPLATES = [
    "Write a short code snippet that demonstrates '{k}'.",
    "Take the example code for '{k}' from this chapter and modify it to do something slightly different.",
    "Break the '{k}' code on purpose (introduce one error), then fix it and write down what you learned.",
    "Add a comment to every line of the '{k}' example explaining what that line does.",
    "Rewrite the '{k}' example using different variable or function names, plus one extra feature.",
    "What error message would you expect if '{k}' was used incorrectly? Try it and check.",
    "Combine '{k}' with one other concept from this chapter into a single small script.",
    "Time how long it takes you to get a working '{k}' example running. Write down where you got stuck.",
    "Explain, line by line, what happens when '{k}' runs \u2014 as if narrating it to a beginner.",
]

REFLECT_TEMPLATES = [
    "Write a 3-question quiz about this chapter (covering '{k}') and answer it yourself.",
    "What's the one idea about '{k}' from this chapter you would explain to a friend first? Why?",
    "Rate your understanding of '{k}' from 1\u20135 and write one sentence on what would get you to a 5.",
    "Summarize this entire chapter in exactly 3 sentences, using the word '{k}' at least once.",
    "If you had to use '{k}' in a job interview answer, what would you say?",
]


def _template_pool(kind):
    """Return the ordered pool of templates available to a chapter of this kind."""
    if kind in ("code", "project"):
        return CONCEPT_TEMPLATES + PRACTICE_TEMPLATES + CODE_TEMPLATES + REFLECT_TEMPLATES
    return CONCEPT_TEMPLATES + PRACTICE_TEMPLATES + REFLECT_TEMPLATES


def generate_assignments(chapter):
    """
    Deterministically generate exactly 50 assignment strings for a chapter dict
    that has 'id', 'kind', and exactly 10 'keywords'.

    Method: 50 assignments = 5 rounds x 10 keywords. Within a round every
    keyword is used exactly once, paired with one template. The template used
    per round is chosen by striding evenly across the whole template pool,
    offset by the chapter id, so two chapters of the same 'kind' don't produce
    identically-templated assignment sets, and no (keyword, template) pair
    repeats within the 50.
    """
    keywords = chapter["keywords"]
    assert len(keywords) == 10, "generate_assignments requires exactly 10 keywords"
    pool = _template_pool(chapter["kind"])
    rounds = 5
    stride = len(pool) // rounds  # spread the 5 rounds across the full pool
    offset = (chapter["id"] * 7) % len(pool)

    assignments = []
    for round_num in range(rounds):
        tmpl_idx = (offset + round_num * stride) % len(pool)
        template = pool[tmpl_idx]
        for kw_idx, keyword in enumerate(keywords):
            assignments.append(template.format(k=keyword))
    return assignments  # length always 50, in stable order
