import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Set the Page Configuration
st.set_page_config(page_title='Bio-Char Pricing', layout='wide', page_icon='✅')

# Write custom CSS styles using Markdown syntax
st.markdown(
    """
    <style>
    /* Increase font size and add padding to number input fields */
    input[type="number"] {
        font-size: 16px;
        padding: 10px;
    }

    /* Adjust width of number input fields */
    input[type="number"] {
        width: 200px;
    }

    /* Add margin to the slider */
    .decoration {
        margin-top: 20px;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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
current_price_Coke = 2205*10
coke_price_yuan = [2007.6917995896292, 3198.236113511565, 4198.84030247787, 4532.334314447339, 4314.80260409325,
                   3778.618659673464, 5200.860987362619, 4113.36416593731, 5245.714081244988, 6517.566310062439,
                   4757.352514343722, 5687.866633166696, 6702.082142591979, 7799.999042604893, 8981.617333207956,
                   10246.937014400735, 11595.958086183304, 13028.68054855565, 14545.104401517772, 16145.229645069678,
                   17829.056279211367, 19596.584303942836, 21447.81371926408, 23382.7445251751, 25401.3767216759,
                   27503.710308766484, 29689.745286446854, 31959.481654716994, 34312.919413576914, 36750.05856302662,
                   39270.899103066105, 41875.44103369535, 44563.6843549144, 47335.62906672323, 50191.27516912185]

coke_price_inr = [price*10 for price in coke_price_yuan]
coke_index = 0
st.write('')  # or st.write(' ')

# Details of Bio-char
current_price_Bio = st.number_input("Enter the Price of Biochar")
price_upper_limit2 = st.number_input("Enter the upper cap for price of Biochar")
price_lower_limit2 = st.number_input("Enter the lower cap for the price of Biochar")
growth_rate2 = st.number_input("Enter the price growth of Biochar")
st.write('')  # or st.write(' ')

# Details of Carbon Credit Pricing
carbon_year = st.number_input("Enter the expected year of implementation of Carbon Credit Pricing")
current_price_carbon = 7
carbon_price_forecast_euro = [10.9831966173848, 12.420351543179319, 16.91546634916859, 26.37129271723667,
                              36.36657560500861,
                              40.319163786647955, 60.08902869234085, 85.99843336436943, 117.38201450708164,
                              156.7339323975646, 203.64927785867707,
                              259.55020654774034, 323.20694035749267, 397.77573032803355, 482.3586660197506,
                              578.5531359898463,
                              684.6085950776343, 804.2921837766115, 936.251115535641, 1082.2444605670792,
                              1240.041179013159,
                              1413.9720590500206, 1602.2646148425981, 1806.8270949689015, 2024.9851228577434,
                              2261.5895459339285,
                              2514.4806355847, 2785.70428237818, 3072.177057483787, 3379.229649955143,
                              3704.3450349566683,
                              4049.6961008108638, 4411.821999570147, 4796.4961544368825, 5200.871875057608]
carbon_price_inr = [int(i * 100) for i in carbon_price_forecast_euro]
carbon_index = 0

# Basic assignment for the plotting

prices = [current_price_Coke]

prices2 = [current_price_Bio]
upper_limits2 = [price_upper_limit2]
lower_limits2 = [price_lower_limit2]

prices3 = [0]

# Set the random seed
np.random.seed(12)

st.write('')  # or st.write(' ')
st.write('')  # or st.write(' ')
st.write('')  # or st.write(' ')

start_range, end_range = st.slider('Select the Years of forecast: ', 2023, 2040, (2023, 2035), step=1)
years = range(start_range, end_range)
if st.button("Get results"):
    # Loop to calculate the values
    for year in years[1:]:
        # For Coke
        projected_price = coke_price_inr[coke_index]
        prices.append(projected_price)
        coke_index+=1

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

        elif year > carbon_year:
            projected_price3 = carbon_price_inr[carbon_index]
            prices3.append(projected_price3)
            carbon_index+=1
        else:
            prices3.append(0)  # Set carbon credit price to 0 before implementation

    # 2.91 is the factor received from Teammate that accounts for the difference in Carbon Emissions due to
    # Coke in Comparison to Biochar

    # For the combined effect of Coke Pricing and Carbon Credit Pricing
    prices4 = [x + (y * 2.91) for x, y in zip(prices, prices3)]

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
    # fig.add_trace(go.Scatter(x=years, y=upper_limits4, mode='lines+markers', name='Upper Limit Coke',
    #                          line=dict(dash='dash')))
    # fig.add_trace(go.Scatter(x=years, y=lower_limits4, mode='lines+markers', name='Lower Limit Coke',
    #                          line=dict(dash='dash')))

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
