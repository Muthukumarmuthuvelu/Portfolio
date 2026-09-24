---
title: Using AEM Guides and DITA to build content AI can use
category: Platforms & tools
minutes: 3
summary: Why DITA's topic structure suits AI retrieval, and what AEM Guides adds around it.
---
An AI assistant answers from chunks of your content. The cleaner, smaller and better labelled those chunks are, the better the answers. DITA, the Darwin Information Typing Architecture, was designed for exactly this kind of modular content, and Adobe Experience Manager (AEM) Guides adds the enterprise layer around it.

## Why DITA suits AI

- **Topic-based.** Each topic covers one task, concept or reference, which makes it a natural retrieval unit.
- **Typed structure.** A task topic has defined places for prerequisites, steps and results, so a system can tell a procedure from background reading.
- **Built-in metadata.** Attributes such as product, audience, platform and version let you filter content before the AI ever sees it.
- **Reuse.** Content references and key references keep one source of truth, so there is one answer instead of five near-duplicates.
- **Conditional publishing.** Filter files produce a variant for each product or release from the same source.

## What AEM Guides adds

AEM Guides is Adobe's DITA-based authoring and publishing solution built on Adobe Experience Manager. Around the DITA standard it provides the operational layer a large team needs: browser-based authoring, review and approval workflows, versioning and baselines, permissions, translation management and publishing to several outputs. Feature details vary by version, so confirm them in Adobe's current documentation.

## A practical pattern

1. **Write one-purpose topics** with specific, task-worded titles, such as "Reset the gateway to factory settings".
2. **Fill in metadata** on every topic and map, using a controlled taxonomy for product, version, audience and content type.
3. **Write a real short description.** It doubles as a summary that helps retrieval.
4. **Publish an AI feed** alongside your human outputs: clean, structured text with its metadata, ready for indexing.
5. **Re-index on every approved release** and retire superseded topics so the assistant never quotes an old version.

## Write for chunks, not pages

An assistant may read one topic with no surrounding context. Avoid phrases such as "as described above", repeat the product name and version where they matter, and keep steps self-contained.

## Watch-outs

DITA does not fix weak content. A badly written task in perfect XML still produces a bad answer. Very large topics defeat chunking, and inconsistent tagging makes filters unreliable. Governance matters as much as the tool.

## Takeaway

DITA gives AI the structure and labels it needs, and AEM Guides gives the team the workflow to keep them accurate at scale. Together they turn documentation into a governed knowledge source rather than a pile of pages.
