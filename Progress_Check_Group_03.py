# # -*- coding: utf-8 -*-
# """
# Created on Thu Apr 30 17:04:08 2026

# @author: Alex Jacoby, Matthew Cioffero, Connor Neuser, Nick Vorwald
# """

#importing streamlit
import streamlit as st

st.title("EOQ Cost Calculator")

# Input section
col1, col2 = st.columns(2)

# Dictionary and variables
eoq_data = {
    "Q": 0,
    "H": 0,
    "i": 0.0,
    "C": 0.0
}

# Ask for input variables
eoq_data["Q"] = st.number_input("Enter Order Quantity (Q):", min_value=1)

# Create a toggle for the Holding Cost
input_method = st.radio(
    "How would you like to provide the Holding Cost?",
    ["I have the Holding Cost (H)", "I have the Carrying Rate (i) and Unit Cost (C)"]
)

# Options for Carrying Cost input
if input_method == "I have the Holding Cost (H)":
    eoq_data["H"] = st.number_input(
        "Enter Holding Cost per unit (H):",
        min_value=0.0,
        value=5.0
    )
    h_final = eoq_data["H"]
else:
    eoq_data["i"] = st.number_input(
        "Enter Carrying Rate (i) as a decimal (e.g., 0.20):",
        min_value=0.0,
        max_value=1.0,
        value=0.20
    )
    eoq_data["C"] = st.number_input(
        "Enter Unit Cost (C):",
        min_value=0.0,
        value=50.0
    )
    h_final = eoq_data["i"] * eoq_data["C"]

# Calculation
carrying_cost = (eoq_data["Q"] / 2) * h_final

# Display Output
st.divider()
st.subheader(f"Total Annual Carrying Cost: ${carrying_cost:,.2f}")

calculate = st.button("Calculate EOQ")

#Other Data input
annual_demand  = st.number_input("Annual Demand")
working_days = st.number_input("Working Days Per Year")
ordering_cost = st.number_input("Ordering Cost")

if calculate == True and annual_demand>=0 and working_days>=0 and ordering_cost>=0:
    eoq = ((2*annual_demand*ordering_cost)/carrying_cost)**0.5
    st.success(f"The optimal order quantity is {eoq} units per order")