# # -*- coding: utf-8 -*- 
# """
# Created on Thu Apr 30 17:04:08 2026

# @author: Alex Jacoby, Matthew Cioffero, Connor Neuser, Nick Vorwald
# """

#importing streamlit and pandas
import streamlit as st
import pandas as pd

#Title
st.title("EOQ Cost Calculator")

#Calculate button
calculate = st.button("Calculate EOQ and Ordering Schedule")  
#Graph option
graph = st.checkbox("Display Graphical Results")


# Create a toggle for the Holding Cost
input_method = st.radio(
    "How would you like to provide the Holding Cost?",
    ["I have the Holding Cost (H)", "I have the Carrying Rate (i) and Unit Cost (C)"]
)

# Options for Carrying Cost input
if input_method == "I have the Holding Cost (H)":
    holding_cost = st.number_input(
        "Enter Holding Cost per unit (H):",
        min_value=0.0
    )
else:
    i = st.number_input(
        "Enter Carrying Rate (i) as a decimal (e.g., 0.20):",
        min_value=0.0,
        max_value=1.0,
    )
    c = st.number_input(
        "Enter Unit Cost (C):",
        min_value=0.0,
    )
    holding_cost = i * c


#Other Data input
annual_demand  = st.number_input("Annual Demand")
working_days = st.number_input("Working Days Per Year")
ordering_cost = st.number_input("Ordering Cost")

#Option to compare current and optimal order quantity
compare = st.checkbox("Compare Current to Optimum Order Quantity")
if compare==True:
       c_q = st.number_input("Current Order Quantity")

if calculate == True and holding_cost <=0 and annual_demand <=0 and working_days<=0 and ordering_cost<=0:
    st.warning("One or more of your variables need attention")
    st.warning("Note: All variables must be greater than zero")
    #Calculations
    
if calculate == True and holding_cost>0 and annual_demand>0 and working_days>0 and ordering_cost>0:
    eoq = round(((2*annual_demand*ordering_cost)/holding_cost)**0.5)
    order_cycle = (eoq/annual_demand)*working_days
    yearly_orders = annual_demand/eoq    
    annual_carrying = (eoq/ 2) * holding_cost
    annual_ordering = yearly_orders*ordering_cost
    total_cost = annual_carrying+annual_ordering
    
    #Displayed ordering information
    st.subheader("Ordering Information")
    st.divider()
    st.write(f"The optimal order quantity is {eoq} units per order")
    st.divider()
    st.write(f"You will need to re-order every {order_cycle:,.2f} days")
    st.divider()
    st.write(f"You will need to place {yearly_orders:,.2f} orders per year")
    
    #Displayed cost information
    st.divider()
    st.subheader("Optimal Yearly Costs")
    st.divider()
    st.write(f"Total Annual Carrying Cost: ${annual_carrying:,.2f}")
    st.divider()
    st.write(f"Total Annual Ordering Cost: ${annual_ordering:,.2f}")
    st.divider()
    st.write(f"Total Stocking Cost: ${total_cost:,.2f}")
    
    
    if compare == True and c_q>0:
        #Calculate current stats and savings
        c_annual_carrying = (c_q/ 2) * holding_cost
        c_annual_ordering = (annual_demand/c_q)*ordering_cost
        c_total_cost = c_annual_carrying+c_annual_ordering
        savings = c_total_cost-total_cost
                
        #Display Current Stats and potential savings
        st.divider()
        st.subheader("Current Yearly Expenses")
        st.divider()
        st.write(f"Current Annual Carrying Cost: ${c_annual_carrying:,.2f}")
        st.divider()
        st.write(f"Current Annual Ordering Cost: ${c_annual_ordering:,.2f}")
        st.divider()
        st.write(f"Current Total Stocking Cost: ${c_total_cost:,.2f}")
        st.divider()
        st.write(f"By changing order quantity, you can save up to ${savings:,.2f} per year.")
  
        #Error for zero or negative order quantity
    if compare ==True and c_q <=0:
        st.write("Current Order Quantity Must Exceed 0")

    #Graphical results
    #Creating datatable
    if graph == True:
        #Defines x axis bounds of graph
        lbound = round(0.1*eoq)
        ubound = round(2*eoq)
        #Creates dataframe to graph from
        df = pd.DataFrame({"Order Quantity": pd.Series(range(lbound,ubound))})
        df["Annual Carrying Cost"] = (df["Order Quantity"] / 2) * holding_cost
        df["Annual Ordering Cost"] = (annual_demand / df["Order Quantity"]) * ordering_cost
        df["Total Cost"] = df["Annual Carrying Cost"] + df["Annual Ordering Cost"]
       #Eliminates a line for order quantity on the graph
        df = df.set_index("Order Quantity")
        #Graph
        st.line_chart(df, x_label= "Order Quantity", y_label = "Total Cost ($)")














        
    
    
