import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Logout function
def logout():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.page = "Login"

# Sales Predictor Page
def sales_predictor():
    st.subheader("Sales Prediction Dashboard")
    st.write("Input sales data for the prediction and analysis:")
    
    months = ["January", "February", "March", "April", "May", "June"]
    sales_input = st.text_input("Enter sales data (comma-separated for each month)", value=st.session_state.get("sales_input", ""))
    
    if sales_input:
        try:
            sales = list(map(int, sales_input.split(',')))
            if len(sales) != len(months):
                st.error("Please provide sales data for all 6 months.")
            else:
                sales_data = pd.DataFrame({"Month": months, "Sales": sales})
                sales_data["Month"] = pd.Categorical(sales_data["Month"], categories=months, ordered=True)
                
                st.bar_chart(sales_data.set_index("Month"))
                st.line_chart(sales_data.set_index("Month"))
                
                # Pie Chart
                colors = ["red", "yellow", "green", "blue", "grey", "pink"]
                max_index = np.argmax(sales)
                explode = [0.1 if i == max_index else 0 for i in range(len(sales))]
                
                fig, ax = plt.subplots()
                ax.pie(sales, labels=months, autopct="%1.1f%%", colors=colors, explode=explode, startangle=90)
                ax.axis("equal")
                st.pyplot(fig)
                
                # Predictions
                future_months = ["July", "August", "September"]
                future_sales = [sales[-1] + 20, sales[-1] + 30, sales[-1] + 40]
                prediction_data = pd.DataFrame({"Month": future_months, "Predicted Sales": future_sales})
                st.table(prediction_data)
                
                # Download Reports and Logout Button Side by Side
                csv_data = sales_data.to_csv(index=False)
                col1, col2 = st.columns(2)

                with col1:
                    st.download_button("Download Sales Data", data=csv_data, file_name="sales_report.csv", mime="text/csv")
                with col2:
                    if st.button("Logout"):
                        logout()
                
        except ValueError:
            st.error("Invalid sales data. Please enter numeric values separated by commas.")
