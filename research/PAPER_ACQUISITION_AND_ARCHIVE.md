# Paper Acquisition & Archive Protocol — BACSE203

## Purpose

This phase exists to create a stable, auditable full-text corpus **after** candidate-paper verification and **before** detailed evidence extraction.

The project must not spend effort archiving papers that are later excluded, and later chats must not depend only on abstracts or search-result snippets when full text is legitimately available.

## Position in the workflow

**CHAT 01 — Full-Text Verification & Screening**
→ **CHAT 02A — Paper Acquisition & Archive**
→ **CHAT 02 — Evidence Extraction Matrix**
→ **CHAT 03 — Quality Assessment**
→ subsequent synthesis/experiment/manuscript phases.

CHAT 02A is deliberately labelled **02A** so the established numbering of later phases remains stable while the new acquisition checkpoint is inserted between verification and extraction.

## Objective

For every study retained as a primary study after CHAT 01:

1. Locate the legitimate full-text PDF where available.
2. Prefer the official publisher, DOI landing page, institutional repository, author repository, or another legitimate open-access source.
3. Record the exact access source and access status.
4. Download/store the PDF in the user's private/local research archive when legally permitted.
5. Never bypass paywalls, access controls, DRM, or other publisher restrictions.
6. Never commit copyrighted publisher PDFs to the public GitHub repository.
7. Record papers that require institutional/library access so they are not silently treated as unavailable or excluded.
8. Verify that the downloaded PDF corresponds to the verified bibliographic record.

## Access hierarchy

Use this order where practical:

1. Open-access publisher PDF.
2. Official DOI/publisher page with legitimate full-text access.
3. Institutional repository.
4. Author/research-group repository.
5. Legitimate scholarly full-text service/repository.
6. Institutional/library access for paywalled papers.

Do not use pirated copies or unauthorized mirrors.

## Archive policy

The public repository stores:

- bibliographic metadata;
- DOI;
- official/legitimate access link;
- PDF acquisition status;
- access type;
- verification status;
- local filename convention;
- notes about missing pages, supplementary material, or access problems.

The user's private/local archive stores the actual PDFs.

Recommended local structure:

```text
papers/
├── P001_<short-title>.pdf
├── P002_<short-title>.pdf
├── ...
├── P0XX_<short-title>.pdf
└── PAPER_ACCESS_REGISTER.md
```

The `papers/` PDF directory should **not** be pushed to the public GitHub repository unless a file is clearly licensed for redistribution.

## Required register fields

| Field | Requirement |
|---|---|
| Study ID | Must match the verified evidence matrix |
| Short title | Consistent local filename label |
| Full title | Exact verified title |
| Authors | Verified metadata |
| Year | Verified metadata |
| Venue | Exact journal/conference |
| Publisher | Verified publisher |
| DOI | Verified DOI, if assigned |
| Publication type | Journal / conference / other |
| Primary-study status | Included / supporting / excluded |
| Full-text status | Obtained / institutional access / unavailable |
| PDF source | Publisher / repository / other legitimate source |
| Official link | DOI or publisher URL where appropriate |
| PDF filename | Local archive name |
| PDF-to-record check | Pass / needs review |
| Supplementary files | Available / unavailable / not applicable |
| Notes | Access or integrity issues |

## Completion gate

CHAT 02A is complete only when:

- the retained-study list from CHAT 01 is frozen;
- every retained study has an acquisition-register row;
- every legitimately obtainable PDF has been archived locally;
- every inaccessible paper has a documented access status and legitimate access route;
- each archived PDF has been checked against title/DOI/metadata;
- the public repository contains no unauthorized copyrighted PDFs;
- the extraction chat can work from a stable list of verified full texts and explicit missing-evidence statuses.

## Important evidence rule

Obtaining a PDF does **not** mean the paper is high quality or fully accepted as evidence. Inclusion, quality and extraction remain separate decisions.

Likewise, lack of immediate PDF access does not automatically justify exclusion if the paper otherwise meets eligibility criteria; the access problem must be recorded and resolved through legitimate library/publisher routes where possible.

## Handoff to extraction

Once CHAT 02A is complete, update `project/CHAT_HANDOFF.md` with:

- number of retained primary studies;
- number of PDFs obtained;
- number requiring institutional/library access;
- number legitimately unavailable;
- any metadata/PDF mismatches;
- the exact location/name of the access register;
- unresolved acquisition issues;
- the next continuation prompt for CHAT 02 — Evidence Extraction Matrix.
