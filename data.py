# Spending and cost data with sources
# All figures in AUD unless noted. USD converted at ~0.65 AUD/USD.

SPENDING = {
    "australia": {
        "label": "Australia",
        "annual_aud": 4_200_000_000,  # ~$4.2B AUD
        "description": "Australian Home Affairs portfolio (border force, offshore processing, detention)",
        "source": "https://www.homeaffairs.gov.au/about-us/corporate/budget",
        "note": "2023-24 Portfolio Budget Statement. Includes ABF, immigration detention, offshore processing.",
    },
    "global": {
        "label": "Global (est.)",
        "annual_aud": 360_000_000_000,  # ~USD 234B → AUD ~360B
        "description": "Global border enforcement spending estimate",
        "source": "https://borderviolence.eu/resources/the-global-border-industrial-complex/",
        "note": "Global estimate includes US ($25B), EU/Frontex, UK, Australia and others. IMF/OECD data.",
    },
}

# Cost per outcome, in AUD
RESETTLEMENT_COSTS = {
    "refugee_resettlement": {
        "label": "Refugee resettlement (full process)",
        "cost_aud": 20_000,
        "unit": "person",
        "description": "UNHCR estimate for full resettlement support including processing, travel, initial settlement",
        "source": "https://www.unhcr.org/what-we-do/protect-human-rights/asylum-and-migration/refugee-resettlement",
    },
    "community_sponsorship": {
        "label": "Community sponsorship pathway",
        "cost_aud": 8_000,
        "unit": "person",
        "description": "Lower-cost pathway where community groups cover integration costs",
        "source": "https://www.refugeecouncil.org.au/community-refugee-sponsorship/",
    },
    "offshore_processing_per_person": {
        "label": "Current offshore detention (per person/year)",
        "cost_aud": 400_000,
        "unit": "person/year",
        "description": "Australian offshore processing cost per detainee per year — for comparison",
        "source": "https://www.refugeecouncil.org.au/offshore-processing-costs/",
    },
}

PUSH_FACTOR_COSTS = {
    "primary_education": {
        "label": "Primary education (1 year)",
        "cost_aud": 150,
        "unit": "child",
        "description": "Cost per child per year for quality primary education in low-income source countries",
        "source": "https://data.worldbank.org/indicator/SE.XPD.PRIM.PC.ZS",
    },
    "basic_healthcare": {
        "label": "Basic healthcare package (1 year)",
        "cost_aud": 100,
        "unit": "person",
        "description": "WHO essential health services package per person per year in low-income countries",
        "source": "https://www.who.int/health-topics/universal-health-coverage",
    },
    "cash_transfer_poverty": {
        "label": "Cash transfer out of extreme poverty",
        "cost_aud": 1_500,
        "unit": "person",
        "description": "GiveDirectly-style direct cash transfer sufficient to lift a person above $2.15/day poverty line for one year",
        "source": "https://www.givedirectly.org/research-at-give-directly/",
    },
    "clean_water_access": {
        "label": "Clean water access",
        "cost_aud": 50,
        "unit": "person",
        "description": "Cost per person to provide access to safe drinking water in developing countries",
        "source": "https://www.worldbank.org/en/topic/water/brief/the-costs-of-meeting-the-2030-sdg-targets-on-drinking-water-sanitation-and-hygiene",
    },
    "skills_training": {
        "label": "Vocational skills training",
        "cost_aud": 800,
        "unit": "person",
        "description": "Cost per person for a vocational training program in source countries (ILO estimate)",
        "source": "https://www.ilo.org/global/topics/skills-knowledge-and-employability/lang--en/index.htm",
    },
}

TOP_SOURCE_COUNTRIES = [
    {"country": "Afghanistan", "displaced": 6_100_000},
    {"country": "Syria", "displaced": 6_500_000},
    {"country": "Venezuela", "displaced": 7_700_000},
    {"country": "Ukraine", "displaced": 6_200_000},
    {"country": "South Sudan", "displaced": 2_300_000},
    {"country": "Myanmar", "displaced": 1_200_000},
    {"country": "Somalia", "displaced": 800_000},
    {"country": "Democratic Republic of Congo", "displaced": 1_000_000},
]
