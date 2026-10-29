Editor-in-Chief
Computer Methods and Programs in Biomedicine
Elsevier

October 29, 2026

Dear Editor,

We are pleased to submit our manuscript entitled "Transparent Implementation and Verification of a Medicine Substitution-Scoring Algorithm: Deterministic Scoring and Unit-Consistent Dose Handling" for consideration for publication in Computer Methods and Programs in Biomedicine.

**Why this submission is appropriate for CMPB:**
CMPB publishes computational methods and programs in biomedicine with emphasis on reproducibility and verification. Our work directly addresses the journal's core scope: we provide an independently verifiable implementation of a published medicine-substitution algorithm, expose internal inconsistencies in the original specification, and provide a complete computational artifact (code, data, tests) that meets the highest standards of computational reproducibility.

**What is known about the topic:**
Caviglioli et al. (2025) published a degree-of-substitutability (DS) score for ranking medicine alternatives during shortages. Their method encodes products on EDQM Standard Terms and computes a pairwise distance. However, their implementation is an unreleased Excel macro — no public source code or dataset accompanies the paper. An independent group cannot re-run the algorithm, confirm its published numbers, or adapt it without re-implementing from the specification.

**What our study adds:**
1. **Independent, deterministic implementation** of the published DS algorithm in Python, with no hard-coded results.
2. **Complete verification** against every labelled result the paper releases (Tables 4, 6, 7, 8): 196 assertions, all passing.
3. **Documented reconciliation** of a genuine internal inconsistency: a transposition of two adjacent Table 1 rows (TRA-0039/TRA-0040) inferred from published scores restores 32/32 match on Table 8. The reconciliation is explicitly labelled as inferred, not authoritatively confirmed.
4. **Unit-convention transparency** for fixed-dose-combination NDXUP (Equation 4): no single convention reproduces all five Table 7 sums (unit-aware: 3/5; literal: 4/5). Both conventions are reported side by side.
5. **Explicit extension (V3)** for fixed-dose-combination reconstruction, clearly labelled as our own unvalidated adaptation — no clinical interchangeability claimed.
6. **Full computational artifact** (code, data, tests, figures) deposited in a public repository with a persistent identifier: Zenodo DOI `10.5281/zenodo.23774017` (v1.0.1).

**Confirmation:**
- This work has not been published previously and is not under consideration elsewhere.
- All authors have approved the manuscript and agree to its submission.
- No human-subjects research or patient data were involved; ethics statement: not applicable.
- No specific funding was received.
- Generative AI (ChatGPT) was used for research discovery and manuscript preparation; authors take full responsibility.
- All authors declare no competing interests.

We believe this manuscript meets CMPB's standards for computational reproducibility and transparency. We are happy to provide any additional materials or clarifications during the review process.

Sincerely,

Yash Mahajan (Corresponding Author)
Pimpri Chinchwad College of Engineering
Pune, 411044, Maharashtra, India
Email: yash.mahajan23@pccoepune.org