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
coke_price_yuan = [3346.152999316049, 8883.989204198791, 19439.075474434587, 34971.71538925416, 55488.71661642554, 80988.91160136886, 111472.5005864759, 146939.44922901344, 187389.7634189597, 232823.4421461492, 283240.4855838312, 338640.8937022925, 399024.666506629, 464391.8039959667, 534742.3061704555, 610076.1730300698, 690393.4045748139, 775694.000804687, 865977.9617196894, 961245.2873198208]

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
carbon_price_forecast_euro = [10.9831966173848, 20.700585905298865, 40.27491987897284, 74.69355408865874, 123.69583539118577, 195.91430411393569, 291.97778762070385, 417.8738258715717, 570.3693610645367, 761.5837337102265, 989.5494550956128, 1261.1769025643364, 1570.4904779275646, 1932.8266779787837, 2343.8224782300813, 2811.23972784182, 3326.5723764705267, 3908.12528560064, 4549.325148375322, 5258.7194391014555]
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
