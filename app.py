# Import Streamlit for building the interactive web application.
import streamlit as st
import matplotlib.pyplot as plt

# Import Pandas for loading and working with the analysis dataset.
import pandas as pd


# Configure the browser tab and overall page layout.
# This must be the first Streamlit command in the application.
st.set_page_config(
    page_title="Shelter Return Analysis",
    page_icon="🐾",
    layout="wide"
)


# Display the main title and project description.
st.title("Shelter Return Analysis")

st.subheader(
    "Identifying Factors Associated with 30-Day Returns After Adoption"
)

st.write(
    """
    This interactive analysis explores adoption records from the
    Austin Animal Center and examines characteristics associated with
    animals returning to the shelter within 30 days of adoption.
    """
)


# Load the analysis-ready dataset created in the Jupyter analysis.
# The file path is relative to app.py, which is located in the project root.
analysis = pd.read_csv(
    "data/shelter_return_analysis.csv"
)


# Display a simple confirmation that the application loaded the data.
st.success(
    f"Analysis dataset loaded successfully: {len(analysis):,} adoption events"
)

# Calculate the headline metrics shown at the top of the dashboard.
# These provide a quick summary of the final analytical cohort.

total_adoptions = len(analysis)

total_returns = analysis["Returned_30"].sum()

return_rate = analysis["Returned_30"].mean() * 100


# Create three equal-width columns for the headline metrics.
metric_col1, metric_col2, metric_col3 = st.columns(3)


# Display the total number of adoption events included in the analysis.
metric_col1.metric(
    label="Adoption Events",
    value=f"{total_adoptions:,}"
)


# Display the number of adoption events followed by a return
# to the shelter within 30 days.
metric_col2.metric(
    label="30-Day Returns",
    value=f"{total_returns:,}"
)


# Display the overall percentage of adoption events that resulted
# in a return within 30 days.
metric_col3.metric(
    label="30-Day Return Rate",
    value=f"{return_rate:.2f}%"
)


# Add a visual separator before the first analysis section.
st.divider()


# Introduce the animal type analysis.
st.header("Return Rate by Animal Type")

st.write(
    """
    Return rates vary substantially across animal types.
    Dogs had the highest return rate among the major adoption groups,
    while cats had a considerably lower rate.
    """
)


# Calculate the number of adoption events, number of 30-day returns,
# and return rate for each animal type.
animal_type_summary = (
    analysis
    .groupby("Animal Type", observed=True)
    .agg(
        Adoptions=("Returned_30", "size"),
        Returns=("Returned_30", "sum"),
        Return_Rate=("Returned_30", "mean")
    )
    .reset_index()
)


# Convert the return rate from a decimal to a percentage.
animal_type_summary["Return Rate (%)"] = (
    animal_type_summary["Return_Rate"] * 100
)


# Sort the results from highest to lowest return rate.
animal_type_summary = animal_type_summary.sort_values(
    "Return Rate (%)",
    ascending=False
)


# Display the return rates as a Streamlit bar chart.
# Create a Matplotlib bar chart so we have full control over
# the axis labels and overall chart formatting.

fig, ax = plt.subplots(figsize=(7, 3.5))

ax.bar(
    animal_type_summary["Animal Type"],
    animal_type_summary["Return Rate (%)"]
)

# Add descriptive axis labels and a chart title.
ax.set_xlabel("Animal Type")
ax.set_ylabel("30-Day Return Rate (%)")
ax.set_title("30-Day Shelter Return Rate by Animal Type")

# Keep the animal type labels horizontal so they are easy to read.
ax.tick_params(
    axis="x",
    labelrotation=0
)

# Remove unnecessary chart borders for a cleaner appearance.
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Prevent labels from being cut off.
fig.tight_layout()

# Display the Matplotlib chart in the Streamlit application.
# Display the chart at its natural figure size instead of
# stretching it across the entire Streamlit page.
st.pyplot(
    fig,
    width="content"
)


# Highlight the main finding from this comparison.
st.info(
    "Dogs had a 9.03% 30-day return rate compared with 3.10% for cats."
)

# Add a separator before the age analysis section.
st.divider()


# Introduce the age-at-adoption analysis.
st.header("Return Rate by Age at Adoption")

st.write(
    """
    Return rates also varied substantially by age. Animals under six
    months had the lowest observed return rate, while adult animals
    between one and seven years had the highest rates.
    """
)


# Define the logical order for the age groups.
# Without this order, Pandas may display the categories alphabetically.
age_order = [
    "Under 6 months",
    "6–12 months",
    "1–3 years",
    "3–7 years",
    "7+ years"
]


# Calculate adoption counts, returns, and return rates
# for each age group.
age_summary = (
    analysis
    .groupby("Age Group", observed=True)
    .agg(
        Adoptions=("Returned_30", "size"),
        Returns=("Returned_30", "sum"),
        Return_Rate=("Returned_30", "mean")
    )
    .reset_index()
)


# Convert the return rate to a percentage.
age_summary["Return Rate (%)"] = (
    age_summary["Return_Rate"] * 100
)


# Convert Age Group to an ordered category so the chart
# progresses naturally from youngest to oldest.
age_summary["Age Group"] = pd.Categorical(
    age_summary["Age Group"],
    categories=age_order,
    ordered=True
)

age_summary = age_summary.sort_values("Age Group")


# Create a compact bar chart.
fig, ax = plt.subplots(figsize=(7, 3.5))

ax.bar(
    age_summary["Age Group"].astype(str),
    age_summary["Return Rate (%)"]
)

# Label the chart clearly.
ax.set_xlabel("Age at Adoption")
ax.set_ylabel("30-Day Return Rate (%)")
ax.set_title("30-Day Return Rate by Age at Adoption")

# Slightly rotate the longer age labels so they remain readable.
ax.tick_params(
    axis="x",
    labelrotation=20
)

# Remove unnecessary borders.
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

fig.tight_layout()


# Display the chart without stretching it across the page.
st.pyplot(
    fig,
    width="content"
)


# Highlight the main finding.
st.info(
    "Animals under 6 months had a 3.22% return rate, compared with "
    "9.47% for animals age 1–3 years and 9.80% for animals age 3–7 years."
)

# Add a separator before the prior shelter history section.
st.divider()


# Introduce the prior shelter history analysis.
st.header("Return Rate by Prior Shelter History")

st.write(
    """
    Animals with previous recorded shelter intakes had substantially
    higher 30-day return rates than animals with no earlier intake
    observed in the available shelter records.
    """
)


# Define the logical order for prior intake history.
history_order = [
    "0",
    "1",
    "2+"
]


# Calculate adoption counts, returns, and return rates
# for each previous-intake group.
history_summary = (
    analysis
    .groupby("Previous Intake Group", observed=True)
    .agg(
        Adoptions=("Returned_30", "size"),
        Returns=("Returned_30", "sum"),
        Return_Rate=("Returned_30", "mean")
    )
    .reset_index()
)


# Convert the return rate from a decimal to a percentage.
history_summary["Return Rate (%)"] = (
    history_summary["Return_Rate"] * 100
)


# Convert the previous-intake group to an ordered category
# so the chart progresses from no previous intakes to two or more.
history_summary["Previous Intake Group"] = pd.Categorical(
    history_summary["Previous Intake Group"],
    categories=history_order,
    ordered=True
)

history_summary = history_summary.sort_values(
    "Previous Intake Group"
)


# Create a compact bar chart.
fig, ax = plt.subplots(figsize=(7, 3.5))

ax.bar(
    history_summary["Previous Intake Group"].astype(str),
    history_summary["Return Rate (%)"]
)


# Add clear chart labels.
ax.set_xlabel("Previous Recorded Intakes")
ax.set_ylabel("30-Day Return Rate (%)")
ax.set_title("30-Day Return Rate by Prior Shelter History")


# Keep the category labels horizontal.
ax.tick_params(
    axis="x",
    labelrotation=0
)


# Remove unnecessary chart borders.
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

fig.tight_layout()


# Display the chart at its natural size.
st.pyplot(
    fig,
    width="content"
)


# Highlight the main finding.
st.info(
    "The return rate increased from 5.74% for animals with no previous "
    "recorded intakes to 11.05% with one previous intake and 14.78% "
    "with two or more previous intakes."
)

# Add a separator before the interactive portion of the dashboard.
st.divider()


# Introduce the interactive explorer.
st.header("Interactive Return Explorer")

st.write(
    """
    Select animal characteristics below to explore how the observed
    30-day return rate changes for different groups of adoption events.
    """
)


# Create three columns so the filters appear side by side.
filter_col1, filter_col2, filter_col3 = st.columns(3)


# Create the animal type filter.
# "All" allows the visitor to include every animal type.
animal_type_options = [
    "All"
] + sorted(
    analysis["Animal Type"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

selected_animal_type = filter_col1.selectbox(
    "Animal Type",
    animal_type_options
)


# Create the age-group filter.
# Use the same logical age ordering used in the analysis.
age_options = [
    "All",
    "Under 6 months",
    "6–12 months",
    "1–3 years",
    "3–7 years",
    "7+ years"
]

selected_age_group = filter_col2.selectbox(
    "Age at Adoption",
    age_options
)


# Create the prior-shelter-history filter.
history_options = [
    "All",
    "0",
    "1",
    "2+"
]

selected_history = filter_col3.selectbox(
    "Previous Recorded Intakes",
    history_options
)


# Start with the complete analysis dataset.
# A copy is used so the original dataframe remains unchanged.
filtered_data = analysis.copy()


# Apply the animal type filter only when the visitor
# selects a specific animal type.
if selected_animal_type != "All":
    filtered_data = filtered_data[
        filtered_data["Animal Type"].astype(str)
        == selected_animal_type
    ]


# Apply the age-group filter only when a specific
# age group is selected.
if selected_age_group != "All":
    filtered_data = filtered_data[
        filtered_data["Age Group"].astype(str)
        == selected_age_group
    ]


# Apply the shelter-history filter only when a specific
# previous-intake group is selected.
if selected_history != "All":
    filtered_data = filtered_data[
        filtered_data["Previous Intake Group"].astype(str)
        == selected_history
    ]


# Calculate metrics for the selected group.
filtered_adoptions = len(filtered_data)

filtered_returns = filtered_data["Returned_30"].sum()

if filtered_adoptions > 0:
    filtered_return_rate = (
        filtered_data["Returned_30"].mean() * 100
    )
else:
    filtered_return_rate = 0


# Display the results of the selected filters.
result_col1, result_col2, result_col3 = st.columns(3)

result_col1.metric(
    "Adoption Events",
    f"{filtered_adoptions:,}"
)

result_col2.metric(
    "30-Day Returns",
    f"{filtered_returns:,}"
)

result_col3.metric(
    "30-Day Return Rate",
    f"{filtered_return_rate:.2f}%"
)


# Warn the visitor when the selected combination has very
# few observations because small samples can produce unstable rates.
if 0 < filtered_adoptions < 100:
    st.warning(
        "This selection contains fewer than 100 adoption events. "
        "Interpret the observed return rate cautiously."
    )


# Display a message if the selected combination contains no records.
if filtered_adoptions == 0:
    st.warning(
        "No adoption events match this combination of filters."
    )
    
# Add a separator before the statistical modeling section.
st.divider()


# Introduce the multivariable analysis.
st.header("What Remained Associated After Adjustment?")

st.write(
    """
    The comparisons above examine characteristics individually. To see
    whether the major patterns remained after accounting for multiple
    characteristics at the same time, a multivariable logistic regression
    model was fitted in the final analysis.

    The model included animal type, age at adoption, prior shelter history,
    and time from intake to adoption.
    """
)


# Store the most important adjusted odds ratios from the final
# logistic regression model.
#
# An odds ratio above 1 indicates higher odds of a 30-day return
# compared with the reference group.
model_summary = pd.DataFrame({
    "Comparison": [
        "Dog vs Cat",
        "Age 6–12 months vs Under 6 months",
        "Age 1–3 years vs Under 6 months",
        "Age 3–7 years vs Under 6 months",
        "Age 7+ years vs Under 6 months",
        "1 previous intake vs None",
        "2+ previous intakes vs None"
    ],
    "Adjusted Odds Ratio": [
        2.28,
        1.70,
        2.28,
        2.28,
        1.87,
        1.48,
        1.75
    ]
})


# Display the model results in a clean table.
st.dataframe(
    model_summary,
    hide_index=True,
    width="content"
)


# Highlight the three major conclusions from the adjusted model.
st.subheader("Key Adjusted Findings")

finding_col1, finding_col2, finding_col3 = st.columns(3)


# Animal type finding.
finding_col1.metric(
    "Dogs vs Cats",
    "2.28× odds"
)

finding_col1.caption(
    "Dogs had 2.28 times the odds of a 30-day return compared with cats."
)


# Age finding.
finding_col2.metric(
    "Adult Animals",
    "≈2.28× odds"
)

finding_col2.caption(
    "Animals age 1–7 years had approximately 2.28 times the odds "
    "of return compared with animals under 6 months."
)


# Prior shelter history finding.
finding_col3.metric(
    "2+ Previous Intakes",
    "1.75× odds"
)

finding_col3.caption(
    "Animals with two or more previous recorded intakes had 1.75 "
    "times the odds of return compared with animals with none."
)


# Explain how the model results should be interpreted.
st.info(
    "These are adjusted associations, not causal effects. "
    "The model helps determine whether patterns remain after accounting "
    "for the other characteristics included in the analysis."
)

# Add a separator before the practical interpretation section.
st.divider()


# Explain how the findings could potentially be used by a shelter.
st.header("What Could This Mean for Shelters?")

st.write(
    """
    The analysis does not predict whether an individual animal will be
    returned. Instead, it identifies characteristics associated with
    higher observed short-term return rates.

    These patterns could help shelters identify adoption groups that may
    benefit from additional support after adoption.
    """
)


# Present several potential operational applications of the findings.
use_col1, use_col2, use_col3 = st.columns(3)


use_col1.subheader("Targeted Follow-Up")

use_col1.write(
    """
    Shelters could consider additional post-adoption check-ins for
    groups associated with higher observed return rates.
    """
)


use_col2.subheader("Adopter Support")

use_col2.write(
    """
    Additional resources, guidance, or behavioral support could be
    offered during the first several weeks after adoption.
    """
)


use_col3.subheader("Further Investigation")

use_col3.write(
    """
    Higher-return groups could be studied further to understand
    factors not captured in the available shelter data.
    """
)


# Clearly state the limitations of using the analysis operationally.
st.warning(
    "These findings should not be used to discourage or restrict "
    "individual adoptions. The analysis identifies population-level "
    "associations and does not determine whether a specific animal "
    "will be returned."
)


# Add a final section explaining the major limitations of the analysis.
st.subheader("Important Limitations")

st.write(
    """
    This analysis uses observational data from a single shelter system.
    The available records do not capture every factor that may influence
    an adoption outcome, including adopter characteristics, household
    environment, behavioral concerns, and detailed reasons for returns.

    Prior shelter history is limited to intake events observable within
    the available dataset, and the 30-day outcome captures only
    short-term returns.
    """
)