import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Set the Page Configuration
st.set_page_config(page_title='Bio-Char Pricing', layout='wide', page_icon='✅')

# Dashboard title
st.title("Bio-Char Vs Coke Pricing")

st.write('')  # or st.write(' ')
st.write('')  # or st.write(' ')

st.subheader("Please enter the following details to proceed further. Enter all prices in INR/Ton and price growth in "
             "Decimal e.g. 0.08 for 8 percent growth annually")
st.write('')  # or st.write(' ')
st.write('')  # or st.write(' ')
st.write('')  # or st.write(' ')

# Details for Coke
current_price_Coke = st.number_input("Enter the Price of Coke")
price_upper_limit = st.number_input("Enter the upper cap of price of Coke")
price_lower_limit = st.number_input("Enter the lower cap of price of Coke ")
growth_rate = st.number_input("Enter the price growth for coke")
st.write('')  # or st.write(' ')

# Details of Bio-char
current_price_Bio = st.number_input("Enter the Price of Biochar")
price_upper_limit2 = st.number_input("Enter the upper cap for price of Biochar")
price_lower_limit2 = st.number_input("Enter the lower cap for the price of Biochar")
growth_rate2 = st.number_input("Enter the price growth of Biochar")
st.write('')  # or st.write(' ')

# Details of Carbon Credit Pricing
carbon_year = st.number_input("Enter the expected year of implementation of Carbon Credit Pricing")
current_price_carbon = st.number_input("Enter the Price of Carbon Credit")
price_upper_limit3 = st.number_input("Enter the upper cap of Carbon Credit price")
price_lower_limit3 = st.number_input("Enter the lower cap of Carbon Credit price")
growth_rate3 = st.number_input("Enter the price growth of Carbon Credit")

# Basic assignment for the plotting

prices = [current_price_Coke]
upper_limits = [price_upper_limit]
lower_limits = [price_lower_limit]

prices2 = [current_price_Bio]
upper_limits2 = [price_upper_limit2]
lower_limits2 = [price_lower_limit2]

prices3 = []
upper_limits3 = []
lower_limits3 = []

# Set the random seed
np.random.seed(12)

st.write('')  # or st.write(' ')
st.write('')  # or st.write(' ')
st.write('')  # or st.write(' ')

# Set the range of years for observation
start_range, end_range = st.slider('Select the Years of forecast: ', 2023, 2050, (2023, 2040), step=1)
years = range(start_range, end_range)

if st.button("Get results"):
    # Loop to calculate the values
    for year in years[1:]:
        # For Coke
        projected_price = prices[-1] * (1 + growth_rate)
        projected_upper_limit = upper_limits[-1] * (1 + growth_rate)
        projected_lower_limit = lower_limits[-1] * (1 + growth_rate)

        projected_price += np.random.normal(0, 1) * prices[-1] * 0.05
        projected_upper_limit += np.random.normal(0, 1) * upper_limits[-1] * 0.05
        projected_lower_limit += np.random.normal(0, 1) * lower_limits[-1] * 0.05

        prices.append(projected_price)
        upper_limits.append(projected_upper_limit)
        lower_limits.append(projected_lower_limit)

        # For Biochar
        projected_price2 = prices2[-1] * (1 + growth_rate2)
        projected_upper_limit2 = upper_limits2[-1] * (1 + growth_rate2)
        projected_lower_limit2 = lower_limits2[-1] * (1 + growth_rate2)

        projected_price2 += np.random.normal(0, 1) * prices2[-1] * 0.03
        projected_upper_limit2 += np.random.normal(0, 1) * upper_limits2[-1] * 0.03
        projected_lower_limit2 += np.random.normal(0, 1) * lower_limits2[-1] * 0.03
        prices2.append(projected_price2)
        upper_limits2.append(projected_upper_limit2)
        lower_limits2.append(projected_lower_limit2)

        # For Carbon Credits Price
        if year == carbon_year:
            prices3.append(current_price_carbon)
            upper_limits3.append(price_upper_limit3)
            lower_limits3.append(price_lower_limit3)

        elif year > carbon_year:
            projected_price3 = prices3[-1] * (1 + growth_rate3)
            projected_upper_limit3 = upper_limits3[-1] * (1 + growth_rate3)
            projected_lower_limit3 = lower_limits3[-1] * (1 + growth_rate3)

            projected_price3 += np.random.normal(0, 1) * prices3[-1] * 0.03
            projected_upper_limit3 += np.random.normal(0, 1) * upper_limits3[-1] * 0.03
            projected_lower_limit3 += np.random.normal(0, 1) * lower_limits3[-1] * 0.03

            prices3.append(projected_price3)
            upper_limits3.append(projected_upper_limit3)
            lower_limits3.append(projected_lower_limit3)
        else:
            prices3.append(0)  # Set carbon credit price to 0 before implementation
            upper_limits3.append(0)
            lower_limits3.append(0)

    # 2.91 is the factor received from Teammate that accounts for the difference in Carbon Emissions due to
    # Coke in Comparison to Biochar

    # For the combined effect of Coke Pricing and Carbon Credit Pricing
    prices4 = [x + (y * 2.91) for x, y in zip(prices, prices3)]
    upper_limits4 = [x + (y * 2.91) for x, y in zip(upper_limits, upper_limits3)]
    lower_limits4 = [x + (y * 2.91) for x, y in zip(lower_limits, lower_limits3)]

    # Convert range object to a list
    years = list(range(start_range, end_range))

    # Create the figure
    fig = go.Figure()

    # Add traces for Biochar Price
    fig.add_trace(go.Scatter(x=years, y=prices2, mode='lines+markers', name='Biochar Price'))
    fig.add_trace(go.Scatter(x=years, y=upper_limits2, mode='lines+markers', name='Upper Limit Biochar',
                             line=dict(dash='dash')))
    fig.add_trace(go.Scatter(x=years, y=lower_limits2, mode='lines+markers', name='Lower Limit Biochar',
                             line=dict(dash='dash')))

    # Add traces for Coke Price (With Carbon Credit)
    fig.add_trace(go.Scatter(x=years, y=prices4, mode='lines+markers', name='Coke Price\n(With Carbon Credit)'))
    fig.add_trace(go.Scatter(x=years, y=upper_limits4, mode='lines+markers', name='Upper Limit Coke',
                             line=dict(dash='dash')))
    fig.add_trace(go.Scatter(x=years, y=lower_limits4, mode='lines+markers', name='Lower Limit Coke',
                             line=dict(dash='dash')))

    # Update the layout
    fig.update_layout(
        title=dict(text='Price Projection', font=dict(size=24), x=0.5, xanchor='center'),
        xaxis=dict(title='Years', showgrid=True),
        yaxis=dict(title='Price (In INR / Ton)', showgrid=True),
        legend=dict(x=0, y=1, xanchor='left', yanchor='top'),
    )

    # Set the figure size (optional)
    fig.update_layout(
        autosize=False,
        width=1300,
        height=700
    )

    # Show the figure
    st.plotly_chart(fig)
