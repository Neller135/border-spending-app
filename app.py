import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from data import RESETTLEMENT_COSTS, PUSH_FACTOR_COSTS
from api_client import (
    get_country_data,
    get_au_border_spending_aud,
    get_global_border_spending_aud,
    SOURCE_COUNTRIES,
)

st.set_page_config(
    page_title="The Same Money",
    page_icon="🌏",
    layout="wide",
)

st.markdown("""
<style>
.metric-card {
    background: #f0f4f8;
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
}
.big-number { font-size: 2rem; font-weight: 700; color: #1a1a2e; }
.label { font-size: 0.9rem; color: #555; margin-bottom: 0.2rem; }
.comparison-card {
    background: #e8f5e9;
    border-left: 4px solid #43a047;
    border-radius: 6px;
    padding: 1rem 1.2rem;
    margin: 0.5rem 0;
}
.warning-card {
    background: #fff3e0;
    border-left: 4px solid #fb8c00;
    border-radius: 6px;
    padding: 1rem 1.2rem;
    margin: 0.5rem 0;
}
.country-card {
    background: #f3f0ff;
    border-left: 4px solid #7c3aed;
    border-radius: 6px;
    padding: 1rem 1.2rem;
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)


def fmt_aud(n):
    if n >= 1_000_000_000:
        return f"${n/1_000_000_000:.1f}B AUD"
    if n >= 1_000_000:
        return f"${n/1_000_000:.0f}M AUD"
    return f"${n:,.0f} AUD"


def fmt_number(n):
    if n >= 1_000_000_000:
        return f"{n/1_000_000_000:.1f} billion"
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f} million"
    if n >= 1_000:
        return f"{n/1_000:.0f},000"
    return f"{n:,.0f}"


# ── Load data ─────────────────────────────────────────────────────────────────
with st.spinner("Loading latest data from World Bank..."):
    country_data = get_country_data()
    au_spending  = get_au_border_spending_aud()
    gl_spending  = get_global_border_spending_aud()

SPENDING = {"australia": au_spending, "global": gl_spending}

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🌏 The Same Money")
st.subheader("What Australia's border protection budget could do instead")
st.markdown(
    "An interactive tool comparing border enforcement spending to the cost of "
    "humane alternatives — resettlement, and addressing the root causes of displacement."
)
st.divider()
with st.expander("About this data"):
    st.markdown("""
**Border spending figure**

The Australia figure (~$2B) covers Australian Border Force operations, on-water response,
aerial surveillance, and border management, as reported in the
[2023-24 Home Affairs Portfolio Budget Statement](https://www.homeaffairs.gov.au/reports-and-publications/reports/budgets/portfolio-budget-2023-24).
It does not include offshore processing (~$580M extra) or the broader Home Affairs portfolio.
Adding offshore processing brings the total to approximately **$2.6B**.

**Alternative cost figures**

All figures for resettlement, education, healthcare, and other interventions are estimates
based on published data from UNHCR, the World Bank, WHO, ILO, and GiveDirectly.
Costs vary significantly by country, program design, and year.

**Country data**

Population, poverty, and development indicators are loaded live from the World Bank API.
Displacement figures are from UNHCR Global Trends 2023.

**Purpose**

This tool is intended for educational and advocacy purposes, to make the opportunity cost
of border spending visible to a wider audience.
    """)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Settings")

    focus = st.radio(
        "Show spending for:",
        options=["australia", "global"],
        format_func=lambda k: SPENDING[k]["label"],
    )

    pct = st.slider(
        "Redirect this % of spending:",
        min_value=1, max_value=100, value=10, step=1,
    )

    st.divider()
    st.subheader("Focus on source countries")
    all_country_names = {r["iso"]: r["country"] for r in country_data}
    selected_isos = st.multiselect(
        "Select countries to analyse:",
        options=list(all_country_names.keys()),
        default=list(all_country_names.keys()),
        format_func=lambda iso: all_country_names[iso],
    )
    if not selected_isos:
        selected_isos = list(all_country_names.keys())

    st.divider()
    s = SPENDING[focus]
    st.caption(f"**{s['label']} spending ({s['year']})**")
    st.caption(s["description"])
    st.caption(f"[Source]({s['source']})")
    st.caption("Country data: World Bank (live). Displacement: UNHCR 2023.")

spending_aud = SPENDING[focus]["annual_aud"]
redirected   = spending_aud * pct / 100
filtered     = [r for r in country_data if r["iso"] in selected_isos]

# ── Key metrics ───────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">{SPENDING[focus]['label']} annual border spending</div>
        <div class="big-number">{fmt_aud(spending_aud)}</div>
        <div class="label">{s['description']}</div>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">Amount redirected ({pct}%)</div>
        <div class="big-number">{fmt_aud(redirected)}</div>
        <div class="label">Per year, if reallocated</div>
    </div>""", unsafe_allow_html=True)

with col3:
    offshore = RESETTLEMENT_COSTS["offshore_processing_per_person"]["cost_aud"]
    offshore_eq = int(redirected / offshore)
    st.markdown(f"""
    <div class="warning-card">
        <div class="label">Current offshore detention cost</div>
        <div class="big-number">$400K / person / yr</div>
        <div class="label">{pct}% of budget = {fmt_number(offshore_eq)} person-years of detention</div>
    </div>""", unsafe_allow_html=True)

st.divider()

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🏠 Resettlement",
    "🌱 Root Causes",
    "🗺️ Country Profiles",
    "📊 By the Numbers",
])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — Resettlement
# ─────────────────────────────────────────────────────────────────────────────
with tab1:
    st.subheader("What if we resettled people instead?")

    res_cols = st.columns(2)
    resettlement_options = {k: v for k, v in RESETTLEMENT_COSTS.items()
                            if k != "offshore_processing_per_person"}

    for i, (key, item) in enumerate(resettlement_options.items()):
        n = int(redirected / item["cost_aud"])
        with res_cols[i % 2]:
            st.markdown(f"""
            <div class="comparison-card">
                <strong>{item['label']}</strong><br/>
                <span style="font-size:1.8rem;font-weight:700;color:#2e7d32">
                    {fmt_number(n)} people
                </span><br/>
                <span style="font-size:0.85rem;color:#555">
                    at {fmt_aud(item['cost_aud'])} per {item['unit']}
                </span><br/>
                <span style="font-size:0.8rem;color:#777">{item['description']}</span><br/>
                <a href="{item['source']}" style="font-size:0.75rem">Source ↗</a>
            </div>""", unsafe_allow_html=True)

    st.divider()
    st.subheader("Displacement from selected countries")

    df_disp = pd.DataFrame([
        {"country": r["country"], "displaced": r["displaced"]}
        for r in filtered if r["displaced"]
    ]).sort_values("displaced", ascending=True)

    total_displaced = df_disp["displaced"].sum()
    resettlement_cost = RESETTLEMENT_COSTS["refugee_resettlement"]["cost_aud"]
    cost_to_resettle_all = total_displaced * resettlement_cost

    st.info(
        f"**{fmt_number(total_displaced)} people** displaced from selected countries. "
        f"Full resettlement would cost **{fmt_aud(cost_to_resettle_all)}** — "
        f"{'less than' if cost_to_resettle_all < spending_aud else 'compared to'} "
        f"the {SPENDING[focus]['label']} annual border budget of {fmt_aud(spending_aud)}."
    )

    fig = px.bar(df_disp, x="displaced", y="country", orientation="h",
                 color="displaced", color_continuous_scale="Reds",
                 labels={"displaced": "People displaced", "country": ""})
    fig.update_layout(coloraxis_showscale=False, margin=dict(l=0, r=0, t=10, b=0), height=320)
    fig.update_xaxes(tickformat=".2s")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Source: UNHCR Global Trends 2023")

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — Root Causes
# ─────────────────────────────────────────────────────────────────────────────
with tab2:
    st.subheader("What if we invested in source countries instead?")
    st.markdown(
        "Addressing push factors — poverty, education, healthcare — reduces "
        "the conditions that force people to flee."
    )

    outcomes = {item["label"]: int(redirected / item["cost_aud"])
                for item in PUSH_FACTOR_COSTS.values()}

    df_outcomes = pd.DataFrame(
        {"Intervention": list(outcomes.keys()), "People reached": list(outcomes.values())}
    ).sort_values("People reached", ascending=True)

    fig2 = px.bar(df_outcomes, x="People reached", y="Intervention", orientation="h",
                  color="People reached", color_continuous_scale="Greens",
                  title=f"People reached with {pct}% of {SPENDING[focus]['label']} border spending ({fmt_aud(redirected)})")
    fig2.update_layout(coloraxis_showscale=False, margin=dict(l=0, r=0, t=50, b=0), height=380)
    fig2.update_xaxes(tickformat=".2s")
    st.plotly_chart(fig2, use_container_width=True)

    st.divider()
    push_cols = st.columns(2)
    for i, (key, item) in enumerate(PUSH_FACTOR_COSTS.items()):
        n = int(redirected / item["cost_aud"])
        with push_cols[i % 2]:
            st.markdown(f"""
            <div class="comparison-card">
                <strong>{item['label']}</strong><br/>
                <span style="font-size:1.8rem;font-weight:700;color:#2e7d32">
                    {fmt_number(n)} {item['unit']}s
                </span><br/>
                <span style="font-size:0.85rem;color:#555">
                    at {fmt_aud(item['cost_aud'])} per {item['unit']}
                </span><br/>
                <span style="font-size:0.8rem;color:#777">{item['description']}</span><br/>
                <a href="{item['source']}" style="font-size:0.75rem">Source ↗</a>
            </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — Country Profiles (new)
# ─────────────────────────────────────────────────────────────────────────────
with tab3:
    st.subheader("Source country profiles")
    st.markdown("Live data from World Bank. Select a country to see what targeted investment could achieve.")

    country_names = [r["country"] for r in filtered]
    selected_country_name = st.selectbox("Select a country:", options=country_names)
    country = next(r for r in filtered if r["country"] == selected_country_name)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        val = fmt_number(country["population"]) if country["population"] else "N/A"
        st.metric("Population", val)
    with c2:
        val = fmt_number(country["displaced"])
        st.metric("People displaced", val)
    with c3:
        val = f"{country['poverty_pct']:.1f}%" if country["poverty_pct"] else "N/A"
        st.metric("Below $2.15/day", val)
    with c4:
        val = f"${country['gni_pc_usd']:,.0f}" if country["gni_pc_usd"] else "N/A"
        st.metric("GNI per capita (USD)", val)

    st.divider()
    st.subheader(f"What could {fmt_aud(redirected)} do in {country['country']}?")

    # People in poverty
    if country["in_poverty"]:
        poverty_transfer_cost = country["in_poverty"] * PUSH_FACTOR_COSTS["cash_transfer_poverty"]["cost_aud"]
        pct_coverable = min(100, redirected / poverty_transfer_cost * 100)
        st.markdown(f"""
        <div class="country-card">
            <strong>Poverty (cash transfers)</strong><br/>
            {fmt_number(country['in_poverty'])} people live below $2.15/day in {country['country']}.<br/>
            {fmt_aud(redirected)} could lift <strong>{pct_coverable:.0f}%</strong> of them above the poverty line for one year
            ({fmt_number(int(redirected / PUSH_FACTOR_COSTS['cash_transfer_poverty']['cost_aud']))} people).
        </div>""", unsafe_allow_html=True)

    # Education
    edu_n = int(redirected / PUSH_FACTOR_COSTS["primary_education"]["cost_aud"])
    st.markdown(f"""
    <div class="country-card">
        <strong>Education</strong><br/>
        {fmt_aud(redirected)} could fund one year of primary education for
        <strong>{fmt_number(edu_n)} children</strong>
        at {fmt_aud(PUSH_FACTOR_COSTS['primary_education']['cost_aud'])} per child.
    </div>""", unsafe_allow_html=True)

    # Healthcare
    health_n = int(redirected / PUSH_FACTOR_COSTS["basic_healthcare"]["cost_aud"])
    st.markdown(f"""
    <div class="country-card">
        <strong>Healthcare</strong><br/>
        {fmt_aud(redirected)} could provide basic healthcare to
        <strong>{fmt_number(health_n)} people</strong>
        for one year.
    </div>""", unsafe_allow_html=True)

    # Clean water
    water_n = int(redirected / PUSH_FACTOR_COSTS["clean_water_access"]["cost_aud"])
    st.markdown(f"""
    <div class="country-card">
        <strong>Clean water</strong><br/>
        {fmt_aud(redirected)} could give access to safe drinking water to
        <strong>{fmt_number(water_n)} people</strong>.
    </div>""", unsafe_allow_html=True)

    if country["health_pc_usd"]:
        st.caption(
            f"Current health spending in {country['country']}: "
            f"${country['health_pc_usd']:.0f} USD per person per year (World Bank)"
        )

# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 — By the Numbers
# ─────────────────────────────────────────────────────────────────────────────
with tab4:
    st.subheader("Cost per person: enforcement vs. alternatives")

    cost_comparison = {
        "Offshore detention (AU, per person/yr)": RESETTLEMENT_COSTS["offshore_processing_per_person"]["cost_aud"],
        "Full refugee resettlement":              RESETTLEMENT_COSTS["refugee_resettlement"]["cost_aud"],
        "Community sponsorship":                  RESETTLEMENT_COSTS["community_sponsorship"]["cost_aud"],
        "Skills training":                        PUSH_FACTOR_COSTS["skills_training"]["cost_aud"],
        "Cash transfer (poverty)":                PUSH_FACTOR_COSTS["cash_transfer_poverty"]["cost_aud"],
        "Primary education (1 yr)":               PUSH_FACTOR_COSTS["primary_education"]["cost_aud"],
        "Basic healthcare (1 yr)":                PUSH_FACTOR_COSTS["basic_healthcare"]["cost_aud"],
        "Clean water access":                     PUSH_FACTOR_COSTS["clean_water_access"]["cost_aud"],
    }

    df_costs = pd.DataFrame({
        "Intervention": list(cost_comparison.keys()),
        "Cost per person (AUD)": list(cost_comparison.values()),
    }).sort_values("Cost per person (AUD)", ascending=False)

    colors = ["#e53935" if "detention" in r.lower() else "#43a047"
              for r in df_costs["Intervention"]]

    fig3 = go.Figure(go.Bar(
        x=df_costs["Cost per person (AUD)"],
        y=df_costs["Intervention"],
        orientation="h",
        marker_color=colors,
    ))
    fig3.update_layout(
        title="Cost per person: enforcement (red) vs. alternatives (green)",
        xaxis_tickformat="$,.0f",
        margin=dict(l=0, r=0, t=50, b=0),
        height=380,
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.divider()
    st.subheader("Summary table")

    rows = [
        {
            "Scenario": f"{SPENDING['australia']['label']} border spending (annual)",
            "Amount": fmt_aud(SPENDING["australia"]["annual_aud"]),
            "People reached (est.)": "—",
        },
        {
            "Scenario": f"{SPENDING['global']['label']} border spending (annual)",
            "Amount": fmt_aud(SPENDING["global"]["annual_aud"]),
            "People reached (est.)": "—",
        },
    ]
    for key, item in {**{k: v for k, v in RESETTLEMENT_COSTS.items() if k != "offshore_processing_per_person"},
                      **PUSH_FACTOR_COSTS}.items():
        n = int(redirected / item["cost_aud"])
        rows.append({
            "Scenario": f"{pct}% AU spending → {item['label']}",
            "Amount": fmt_aud(redirected),
            "People reached (est.)": fmt_number(n),
        })

    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

st.divider()
st.caption(
    "**Disclaimer:** Spending figures are estimates from publicly available budget documents. "
    "Cost-per-outcome figures vary by country, program design, and year — use as indicative only. "
    "Country data sourced live from World Bank API. Displacement data: UNHCR Global Trends 2023. "
    "Built for educational and advocacy purposes."
)
