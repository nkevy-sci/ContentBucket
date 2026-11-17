# Suggested statistical corrections — not applied to the post

The webpage currently follows `spec.docx`, with light spelling, punctuation, and grammar edits. The substantive errors below are intentionally retained in the webpage at the author’s request. This is a separate revision checklist.

## 1. Distinguish U from a rank sum

Replace “These U values are called ranked sums” with “These values are Mann–Whitney U statistics.” Use “rank sum,” rather than “ranked sum,” when discussing the sum of pooled ranks.

The Mann–Whitney U and Wilcoxon rank-sum tests are equivalent formulations when the alternatives, tie treatment, and p-value method match; their raw statistics differ. The Wilcoxon signed-rank test is a separate procedure for paired observations.

With the post’s convention (count Maura’s wins plus half her ties), U_M = R_M − n_M(n_M + 1)/2. Here, Maura’s pooled midrank sum is R_M = 43.5, so U_M = 43.5 − 21 = 22.5. Kim’s rank sum is 34.5 and U_K = 13.5. Rank sums total 78; the U values total 36. Do not mix those denominators.

Source: [SciPy’s notes on the relationship between U and the rank sum](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mannwhitneyu.html#notes).

## 2. Label Table 5’s numbers as contributions, not six U statistics

The values 4.5, 4, 4.5, 1.5, 4, and 4 are the contributions of Maura’s individual scores to U_M. Their sum, 22.5, is U_M. Replace “Call this value U_M” with “Add these contributions to obtain U_M,” and label that row “Contribution to U_M.”

The underlying arithmetic in Tables 5 and 6 is correct.

## 3. Fix the best-game probability and its explanation

Update: the author confirmed 3/12, and the adjacent 3/10 typo has now been corrected. Equation-aware extraction found that Word already contained a 3/12 answer fraction and a 3/12 feedback fraction; both are restored. The prior claim that the feedback probability was missing was an extraction error.

State that one of the twelve distinct games is selected with equal probability. The events “Maura’s best game” and “Kim’s best game” are mutually exclusive outcomes of this single selection, so their probabilities add. Multiplying would answer a different question about a joint event.

The number twelve comes from six separate games per player, not from independence of the scores. Replace the number-question feedback accordingly.

## 4. Present independence as an assumption, with a precise meaning

Different teams and separate games do not establish independence. Shared schedules, opponents, training conditions, or other factors can create associations. Repeated games for the same player can also be dependent.

Suggested wording: “For this simplified example, we assume the game scores are independent observations. Knowing one score does not change the probability distribution of another.” Explain that this assumption needs justification in a real analysis. The quiz’s claim that different games automatically establish independence should also change.

## 5. Revise the normal-distribution and nonparametric explanation

A lower bound of zero does not, by itself, make a normal approximation unusable. It means an exact unbounded normal distribution cannot literally describe every possible score. Whether an approximation is useful depends on the distribution and context.

“Nonparametric” does not mean assumption-free. Explain that this method avoids specifying a normal score distribution, while still requiring appropriate sampling and independence assumptions. Six observations per player give little information about the distribution’s shape and may provide limited power.

## 6. State a hypothesis that accounts for ties and matches the question

The standard equal-distributions null implies P(M > K) + 0.5 P(M = K) = 0.5, not necessarily P(M > K) = 0.5 when ties are possible. The converse does not generally hold: a tie-adjusted comparison probability of 0.5 does not establish equal distributions.

Choose the alternative in advance: a directional question about Maura tending to score more calls for a one-sided alternative; a question about any distributional difference calls for a two-sided alternative. Do not choose the direction after seeing the results.

Also replace “better shooter” with “tends to score more points.” Total points alone do not measure shooting ability; playing time, shot attempts, and other factors matter.

## 7. Specify the significance level, table convention, and tie handling

“Look up the maximum U” is not a universal rule. Some tables use the smaller U; the linked table uses upper critical values. Identify which convention is in use.

The source also displays `22.5_Maura > 31_Critical`; this inequality is false and should read `<` when comparing those numbers. It has been restored verbatim for the author’s review.

For samples of six and six, the cited critical value 31 belongs to that table’s one-sided 0.025 / two-sided 0.05 section. A one-sided 0.05 test uses a different critical value. Moreover, these scores contain many ties, so the untied table does not by itself justify the stated significance decision.

Use a method that handles ties, such as an appropriate permutation test, and report its assumptions, alternative, p-value, and significance level. If retaining the conclusion, make clear which calculation supports it. Failure to reject does not show that the players are equal.

Sources: [George Mason critical-value table](https://mason.gmu.edu/~alaemmer/bio214/mwu-table2.pdf), [Shier’s guide, including ties](https://www.statstutor.ac.uk/resources/uploaded/mannwhitney.pdf), and [SciPy’s guidance for small samples with ties](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mannwhitneyu.html#notes).

## 8. Reverse the Mann–Whitney review-question feedback

The “regular, well-defined pattern” option currently receives “Right!” It should receive corrective feedback. The small-sample comparison option currently receives “No”; it should receive affirmative feedback, qualified by independence and the need to handle ties appropriately.

The mere presence of outliers does not make a test valid or invalid. The test uses ranks, so extreme magnitudes have less influence than in procedures based directly on numerical distances; its other assumptions still matter.

## 9. Separate effect size from significance

Replace “If the Mann–Whitney U test fails … calculate CLES instead” and “While it’s less accurate.” CLES describes the size of an observed ordering effect; a significance test evaluates compatibility with a null hypothesis. One is not an inferior fallback for the other. Report effect size regardless of statistical significance, ideally with uncertainty.

## 10. Correct CLES’s denominator and interpretation

Replace “Maura’s ranked sum by the total rank” with “Maura’s U statistic by the number of cross-player comparisons: 22.5/(6 × 6).”

For the tie-adjusted version used here:

`CLES = (wins + 0.5 × ties) / comparisons = (20 + 0.5 × 5) / 36 = 62.5%.`

There are 20 strict wins, 5 ties, and 11 losses among the 36 observed pairings. The strict observed probability of Maura scoring more is 20/36 ≈ 55.6%; the tie probability is 5/36 ≈ 13.9%.

Thus, 62.5% is a tie-adjusted sample comparison measure, not the strict probability of winning. The first CLES review option needs the half-tie term if this is the definition being taught.

## 11. Avoid turning a sample description into an unqualified forecast

Replace “62.5% chance … during the next game” with a statement about randomly selected scores from the observed samples. Estimating future performance requires representative observations and assumptions that future conditions resemble those sampled. Six games per player leave substantial uncertainty.

## 12. Correct the CLES distractor feedback

The probability that two samples come from the same population is not what a Mann–Whitney p-value reports. Replace the feedback suggesting that this is simply a description of the Mann–Whitney test. A p-value is calculated under a specified null hypothesis; it does not assign a probability that the null hypothesis is true.

## Verification of this checklist

Numerical values were independently recomputed from the specification’s scores. No proposed substantive correction in this checklist has been applied to the restored page. The reference document remains unchanged.
