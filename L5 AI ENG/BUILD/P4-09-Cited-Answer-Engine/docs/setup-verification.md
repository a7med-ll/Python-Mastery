# Setup verification — 10 October 2026

Run from the project directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
docker compose up -d
python -m streamlit run app.py
```

Windows PowerShell activation: `.venv\Scripts\Activate.ps1` (create with `python -m venv .venv`). Open http://localhost:8501. First model loading needs download access; Qdrant uses http://localhost:6333.

Verification scope:

- Created and activated an isolated temporary venv with Python 3.13; pip worked. No project venv existed initially.
- Existing app actually runs from `~/Desktop/Python Mastery/.venv`, Python 3.14.3. Both requirements dry-run and actual install with `--no-index` succeeded there (all packages already satisfied); `pip check` reported no broken requirements. A fresh internet installation was not performed.
- Installed direct versions: Streamlit 1.65.0, PyMuPDF 1.28.2, SentenceTransformers 6.1.0, NumPy 2.5.3, qdrant-client 1.19.1, torch 2.14.1. Requirements remain unchanged and unpinned; this is an environment snapshot, not a lockfile.
- Docker Compose configuration parsed successfully. Qdrant's HTTP endpoint responded, version 1.19.2. `docker compose up -d` succeeded and recreated the service container using its existing persistent named volume. The compose file remains unchanged: `latest`, port 6333, and a named volume.
- Streamlit health endpoint returned `ok`; existing process uses `python -m streamlit run app.py`. No new query suite was run and the live index was not modified.
- `evaluate.py` reads `data/sample.pdf`; that file was preserved. Do not move it without changing the evaluator. Evaluation can mutate its Qdrant collection, so it was not run as a support-file check.

Assets inventory: architecture PNG/SVG and evaluation-summary PNG/SVG exist. `hero.png`, `upload-index.png`, `retrieval.png`, `contradiction.png`, `abstention.png`, and `cross-page.png` are absent. Do not reference these missing files in the future README.
