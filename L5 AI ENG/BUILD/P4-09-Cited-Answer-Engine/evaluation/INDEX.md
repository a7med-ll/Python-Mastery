# Evaluation evidence index

- **Atlas final grounded result:** 11/12, 91.7%, score 9/10. See [report](atlas_final_report.md), [CSV](atlas_final_results.csv), [JSON](atlas_final_results.json), and [browser records](browser_records_atlas_final.json). The evidence/status-only 12/12 result is a different criterion and must not replace the grounded result.
- **Boreal:** separate synthetic challenge; see [report](boreal_final_report.md), [CSV](boreal_final_results.csv), [JSON](boreal_final_results.json), and [browser records](browser_records_boreal_final.json). Do not merge its results into the Atlas score.
- Earlier `test_results*`, `adversarial_report*`, and browser records retain their original run names. `test_manifest.json` and `boreal_test_manifest.json` are expected-case manifests, not executed results.
- JPG files are historical browser proof, not polished app screenshots.
- PDFs are in [examples](../examples/test_questions.md). Report links were updated for that location; raw CSV/JSON contents were preserved.
- Precision@3 values of 0.40 (fixed-size) and 0.33 (paragraph-aware) are reported in existing project documentation and the visual asset. No underlying chunking CSV was found in the available outputs; no benchmark was rerun here.
