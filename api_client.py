"""
Live data from World Bank and UNHCR APIs, with Streamlit caching.
Falls back to static figures if APIs are unreachable.
"""

import requests
import streamlit as st

WORLD_BANK_BASE = "https://api.worldbank.org/v2"

SOURCE_COUNTRIES = {
    "AFG": "Afghanistan",
    "SYR": "Syrian Arab Republic",
    "VEN": "Venezuela",
    "SSD": "South Sudan",
    "MMR": "Myanmar",
    "SOM": "Somalia",
    "COD": "DR Congo",
    "UKR": "Ukraine",
    "ETH": "Ethiopia",
    "SDN": "Sudan",
}

# UNHCR displacement estimates (2023) — static fallback since UNHCR API
# aggregates don't break down cleanly by origin country in one call.
DISPLACEMENT_FALLBACK = {
    "AFG": 6_100_000,
    "SYR": 6_500_000,
    "VEN": 7_700_000,
    "SSD": 2_300_000,
    "MMR": 1_200_000,
    "SOM":   800_000,
    "COD": 1_000_000,
    "UKR": 6_200_000,
    "ETH":   900_000,
    "SDN": 1_900_000,
}


def _wb_fetch(indicator: str, iso_codes: list[str]) -> dict:
    """Fetch a World Bank indicator for a list of ISO3 codes. Returns {iso: value}."""
    codes = ";".join(iso_codes)
    url = f"{WORLD_BANK_BASE}/country/{codes}/indicator/{indicator}"
    try:
        r = requests.get(url, params={"format": "json", "mrv": 3, "per_page": 100}, timeout=8)
        r.raise_for_status()
        rows = r.json()[1] or []
        result = {}
        for row in rows:
            iso = row.get("countryiso3code")
            val = row.get("value")
            if iso and val is not None and iso not in result:
                result[iso] = val
        return result
    except Exception:
        return {}


@st.cache_data(ttl=3600, show_spinner=False)
def get_country_data(iso_codes=None) -> list:
    """
    Return a list of dicts with country-level data for the source countries.
    Uses World Bank API; falls back to static displacement data if unavailable.
    """
    codes = iso_codes or list(SOURCE_COUNTRIES.keys())

    poverty     = _wb_fetch("SI.POV.DDAY",    codes)   # % below $2.15/day
    population  = _wb_fetch("SP.POP.TOTL",    codes)   # total population
    gni_pc      = _wb_fetch("NY.GNP.PCAP.CD", codes)   # GNI per capita USD
    edu_spend   = _wb_fetch("SE.XPD.TOTL.GD.ZS", codes) # education % of GDP
    health_spend= _wb_fetch("SH.XPD.CHEX.PC.CD", codes) # health spend per capita USD

    rows = []
    for iso in codes:
        name = SOURCE_COUNTRIES.get(iso, iso)
        pop  = population.get(iso)
        pov  = poverty.get(iso)
        rows.append({
            "iso":          iso,
            "country":      name,
            "population":   pop,
            "displaced":    DISPLACEMENT_FALLBACK.get(iso, 0),
            "poverty_pct":  pov,
            "gni_pc_usd":   gni_pc.get(iso),
            "edu_gdp_pct":  edu_spend.get(iso),
            "health_pc_usd":health_spend.get(iso),
            # How many people live below poverty line
            "in_poverty":   int(pop * pov / 100) if pop and pov else None,
        })
    return rows


@st.cache_data(ttl=3600, show_spinner=False)
def get_au_border_spending_aud() -> dict:
    """
    Returns Australian border spending figure.
    Source: Home Affairs Portfolio Budget Statement 2023-24.
    Not available via public API — curated figure.
    """
    return {
        "annual_aud": 4_200_000_000,
        "label": "Australia",
        "description": "Home Affairs portfolio (ABF, detention, offshore processing)",
        "source": "https://www.homeaffairs.gov.au/about-us/corporate/budget",
        "year": "2023-24",
    }


@st.cache_data(ttl=3600, show_spinner=False)
def get_global_border_spending_aud() -> dict:
    """
    Global border enforcement estimate. No single live API — curated from
    OECD/IMF/Frontex/DHS published figures.
    """
    return {
        "annual_aud": 360_000_000_000,
        "label": "Global (est.)",
        "description": "US, EU, UK, Australia and other major enforcement budgets combined",
        "source": "https://borderviolence.eu/resources/the-global-border-industrial-complex/",
        "year": "2022-23",
    }
