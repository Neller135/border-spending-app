# Spending and cost data with sources
# All figures in AUD unless noted. USD converted at ~0.65 AUD/USD.
# Figures marked "estimated" are indicative and should be treated as approximate.

SPENDING = {
    "australia": {
        "label": "Australia",
        "annual_aud": 2_000_000_000,
        "description": "Border enforcement and management (ABF operations, on-water response, aerial surveillance)",
        "source": "https://www.homeaffairs.gov.au/reports-and-publications/reports/budgets/portfolio-budget-2023-24",
        "note": "2023-24 Home Affairs Portfolio Budget Statement. Covers ABF operations, on-water response, and border management. Does not include offshore processing (~$580M) or broader Home Affairs portfolio.",
    },
    "global": {
        "label": "Global (estimated)",
        "annual_aud": 360_000_000_000,
        "description": "Global border enforcement spending — estimated from published national budgets",
        "source": "https://borderviolence.eu/resources/the-global-border-industrial-complex/",
        "note": "Estimated total combining US DHS (~$25B USD), EU/Frontex, UK, Australia and other major enforcement budgets. No single authoritative global figure exists — treat as indicative.",
    },
}

# Cost per outcome, in AUD
# All figures are ESTIMATES based on published research. Actual costs vary
# significantly by country, program design, implementing organisation, and year.

RESETTLEMENT_COSTS = {
    "refugee_resettlement": {
        "label": "Refugee resettlement — estimated cost",
        "cost_aud": 20_000,
        "unit": "person",
        "description": "Estimated cost per person for full resettlement support including processing, travel, and initial settlement assistance. UNHCR figures vary widely by country ($10,000–$30,000 USD).",
        "source": "https://www.unhcr.org/what-we-do/protect-human-rights/asylum-and-migration/refugee-resettlement",
        "estimated": True,
    },
    "community_sponsorship": {
        "label": "Community sponsorship pathway — estimated cost",
        "cost_aud": 8_000,
        "unit": "person",
        "description": "Estimated lower-cost pathway where community groups cover integration costs. Figure is indicative — Australian community sponsorship programs vary significantly.",
        "source": "https://www.refugeecouncil.org.au/community-refugee-sponsorship/",
        "estimated": True,
    },
    "offshore_processing_per_person": {
        "label": "Current offshore detention (per person/year)",
        "cost_aud": 400_000,
        "unit": "person/year",
        "description": "Australian offshore processing cost per detainee per year — cited by National Commission of Audit (2014) and Amnesty International (2016, ~$570K). Used here for comparison.",
        "source": "https://www.refugeecouncil.org.au/offshore-processing-costs/",
        "estimated": False,
    },
}

PUSH_FACTOR_COSTS = {
    "primary_education": {
        "label": "Primary education (1 year) — estimated",
        "cost_aud": 150,
        "unit": "student",
        "description": "Estimated cost per student per year for primary education in low-income countries. World Bank figures range from $50–$300+ USD depending on country and program quality.",
        "source": "https://data.worldbank.org/indicator/SE.XPD.PRIM.PC.ZS",
        "estimated": True,
    },
    "basic_healthcare": {
        "label": "Basic healthcare package (1 year) — estimated",
        "cost_aud": 100,
        "unit": "person",
        "description": "Estimated cost per person per year for an essential health services package in low-income countries. WHO figures vary significantly by country ($50–$200 USD).",
        "source": "https://www.who.int/health-topics/universal-health-coverage",
        "estimated": True,
    },
    "cash_transfer_poverty": {
        "label": "Cash transfer — estimated",
        "cost_aud": 1_500,
        "unit": "person",
        "description": "Estimated cost of a direct cash transfer sufficient to support a person above $2.15/day for one year, based on GiveDirectly program data. Effectiveness varies by context.",
        "source": "https://www.givedirectly.org/research-at-give-directly/",
        "estimated": True,
    },
    "clean_water_access": {
        "label": "Clean water access — estimated",
        "cost_aud": 50,
        "unit": "person",
        "description": "Estimated cost per person to provide access to safe drinking water in developing countries. World Bank SDG costing estimates vary widely by region and infrastructure context.",
        "source": "https://www.worldbank.org/en/topic/water/brief/the-costs-of-meeting-the-2030-sdg-targets-on-drinking-water-sanitation-and-hygiene",
        "estimated": True,
    },
    "skills_training": {
        "label": "Vocational skills training — estimated",
        "cost_aud": 800,
        "unit": "person",
        "description": "Estimated cost per person for a vocational training program in source countries, based on ILO program data. Costs vary considerably by sector, country, and program length.",
        "source": "https://www.ilo.org/global/topics/skills-knowledge-and-employability/lang--en/index.htm",
        "estimated": True,
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
