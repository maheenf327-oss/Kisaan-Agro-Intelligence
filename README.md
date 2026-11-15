### 🌾 KISAAN: CLIMATE RESILIENT AGRO INTELLIGENCE
NASA Space Apps Challenge 2026 — Field Shift: Adapting Farms with NASA Data

### Description:
Kisaan is an interactive geospatial climate simulator and crop decision-support platform designed to protect farmers whose generational planting wisdom is giving way due to rapid climate volatility. By combining multi-year NASA Power API Data (`TS`, `T2M_MIN`, `GWETPROF`) with UN FAO EcoCrop survival limits, Kisaan helps both veteran farmers and the new generation evaluate seasonal risks and adapt before risking a harvest

### My Files:
`NASA_Final_Project.py`: Main application script handling the Streamlit UI, `st.session_state` map coordinates, OpenStreetMap geocoding, multi-year NASA POWER API requests, and the crop evaluation and substitution engine.
`.streamlit/config.toml`: Custom dark-space theme configuration built following Streamlit's official styling documentation.
`requirements.txt`**: Lists the four Python libraries (`streamlit`, `requests`, `pandas`, `geopy`) required to run the app locally.

### How The System Works:
1. **Live Geospatial Explorer:** Uses `geopy` (`Nominatim`) and native `st.map()` backed by `st.session_state.df` so users can search any farming location and verify their field coordinates visually.
2. **Multi-Year NASA Telemetry & Stress-Testing:** Loops across three years (`2025`, `2024`, `2023`) to fetch surface heat (`TS`), nighttime frost (`T2M_MIN`), and root-zone soil moisture (`GWETPROF`) from the **NASA POWER Agroclimatology API (`community=ag`)**, paired with a `-5.0°C` to `+5.0°C` temperature stress-test slider.
3. **Automated Crop Substitution:** Evaluates historical extremes against verified **UN FAO EcoCrop** limits in `CROP_DATABASE` and recommends viable replacement crops with exact sowing-to-harvest dates when a primary crop fails.

### How To Run & Recommended Test Case:
1. Install dependencies and launch the app:
   ```bash
   pip install -r requirements.txt
   python -m streamlit run NASA_Final_Project.py
   ```
2. Test Case for Alternative Crop Recommendation:
    **Location:** `Lahore` | **Crop:** `potato` | **Sowing Date:** `2025/09/30` | **Temp Spike:** `0.00`
    *(Potato fails early-season heat above 24.0°C, and the engine automatically recommends *GRAM* with exact alternative planting dates).*

### AI / Super Intelligence Disclosure
All application architecture and code were hand-written by me. AI tools were used strictly as a reference assistant to look up library syntax, troubleshoot `datetime` and API debugging errors, and proofread documentation.