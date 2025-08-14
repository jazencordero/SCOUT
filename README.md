# SCOUT — Future Founder Radar (Finland)

Streamlit app that sources potential founders across Finland by archetype (Commercial / Technical / Domain), enriches via OpenAI, and ranks by founder-likelihood.

## Quickstart (local)
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
# copy .env.example to .env and add keys
streamlit run app.py
