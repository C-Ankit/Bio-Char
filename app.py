import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd
import io
import chardet
import random

st.set_page_config(
    page_title='Bio-Char Timeline Dashboard',
    page_icon='✅',
    layout='wide'
)


# To select the starting supply rate of Biochar
def select_start(state_name):
    if state_name in ['Haryana', 'Madhya Pradesh', 'Maharashtra', 'Punjab', 'Uttar Pradesh']:
        return 0.13
    elif state_name in ['Andhra Pradesh', 'Bihar', 'Gujarat', 'Karnataka', 'Rajasthan', ' Tamil Nadu', 'West Bengal']:
        return 0.11
    else:
        return 0.10


# To select the in between growth rate of Biochar
def select_mid(state_name):
    if state_name in ['Rajasthan', 'Haryana', 'Gujarat', 'Maharashtra', 'Madhya Pradesh', 'Andhra Pradesh',
                      'Tamil Nadu']:
        return 0.15
    elif state_name in ['Uttar Pradesh', 'Karnataka', 'Odisha', 'Punjab', 'Bihar']:
        return 0.12
    else:
        return 0.11


# To select the end growth rate of Biochar
def select_end(state_name):
    if state_name in ['Assam', 'Madhya Pradesh', 'Arunachal Pradesh', 'Maharashtra', 'Nagaland', 'Meghalaya',
                      'Mizoram']:
        return 0.17
    elif state_name in ['Tripura', 'Chhattisgarh', 'Odisha', 'Uttarakhand', 'West Bengal', 'Manipur']:
        return 0.15
    else:
        return 0.12


# Make a list
year_list = []
supply_list = []

# dashboard title
st.title("Bio-Char Timeline")

st.write('')  # or st.write(' ')
st.write('')  # or st.write(' ')

# Markdown the details of sidebar
st.markdown('Welcome to Bio-char Dashboard. Please go to the Sidebar and make a selection.')
st.write('')  # or st.write(' ')

# Creating the Sidebar
st.sidebar.header('Dashboard `version 1`')

# Define the options for the Selectbox
options = ['Particular Plant', 'Company', 'Country']

# Create the Selectbox
selection = st.sidebar.selectbox('Select an option', options)

# Provide an Industry input
industry_list = ['Steel', 'Cement', 'Aluminium']
industry = st.sidebar.selectbox("Select the Industry", industry_list)

if industry == 'Cement':
    factor = 0.035
    std = 5
    CAGR = 0.0457
elif industry == 'Steel':
    factor = 0.70
    std = 80
    CAGR = 0.0855
elif industry == 'Aluminium':
    factor = 0.47
    std = 50
    CAGR = 0.067

# Display the selected option
st.write('You selected:', selection)

if selection == 'Particular Plant':

    indian_states = ['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat',
                     'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra',
                     'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim',
                     'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal']
    state = st.selectbox("Select the state in which Plant is Located", indian_states)

    # Take number input
    cap1 = st.number_input('Enter the annual production capacity of plant (In Million Tonnes)')

    # Take year of implementation as input
    year = st.number_input('Enter the year of starting pilot for the plant')

    # Using it as Counter to count the number of years
    c = 1

    if st.button("Calculate Bio-char Requirement"):
        dem1 = float(cap1) * factor * 1000
        st.write("The calculated requirement is:", dem1, "(In 10^3 Tonnes) ")

        # Do value assignment
        requirement = dem1
        initial_supply = dem1 * 0.10
        supply_list.append(initial_supply)
        total_supply = initial_supply
        year_list.append(year)

        # Looping until whole requirement is fulfilled
        while total_supply < requirement:
            if c <= 2:
                growth_add = select_start(state)
            elif 2 < c < 5:
                growth_add = select_mid(state)
            else:
                growth_add = select_end(state)

            supply_increase_amount = total_supply * growth_add
            total_supply += supply_increase_amount
            year += 1
            year_list.append(year)
            supply_list.append(total_supply)
            c += 1

        # Plot the figure for the plant requirement
        # Create the figure
        fig = go.Figure()
        # Put a random seed
        np.random.seed(42)
        # Add traces for Biochar Price
        fig.add_trace(
            go.Scatter(x=year_list, y=supply_list + np.random.normal(0, std, len(supply_list)), mode='lines+markers',
                       name='Biochar Supply'))

        # Update the layout
        fig.update_layout(
            title=dict(text='Biochar Supply Projection', font=dict(size=24), x=0.5, xanchor='center'),
            xaxis=dict(title='Years', showgrid=True),
            yaxis=dict(title='Supply (In 10^3 Tonnes)', showgrid=True),
            legend=dict(x=0, y=1, xanchor='left', yanchor='top'),
        )

        # Set the figure size (optional)
        fig.update_layout(
            autosize=False,
            width=1300,
            height=700
        )
        # Add a vertical line on the last point
        last_year = year_list[-1]
        last_supply = supply_list[-1]

        fig.add_shape(
            type="line",
            x0=last_year,
            x1=last_year,
            y0=0,
            y1=last_supply,
            line=dict(color="red", width=2),
        )

        # Add an invisible trace for the legend of the vertical line
        fig.add_trace(go.Scatter(
            x=[None],
            y=[None],
            mode='lines',
            line=dict(color='red', width=2),
            name="Year Total Coke Replaced with Biochar",
            showlegend=True,
            legendgroup='vertical_line'
        ))

        # Show the figure
        st.plotly_chart(fig)

# Calculations for the Whole Country
if selection == "Country":
    # Make a list
    year_list2 = []
    supply_list2 = []

    # Take input of current requirement
    cap2 = st.number_input("Enter the current annual production capacity (In Million Ton).")

    # Take year of implementation as input
    year = st.number_input('Enter the year of starting pilot plant')

    # Using it as Counter to count the number of years
    c = 1

    if st.button("Calculate Bio-char Requirement"):
        dem2 = float(cap2) * factor * 1000
        st.write("The requirement for Biochar for current year is : ", dem2, " (In 10^3 Tonnes)")

        st.subheader("Showing the plot for requirement fulfillment by considering CAGR of industry")

        # Do value assignment
        requirement = dem2
        # demand_industry.append(requirement)
        initial_supply = dem2 * 0.10
        supply_list2.append(initial_supply)
        total_supply = initial_supply
        year_list2.append(year)

        # Looping until whole requirement is fulfilled
        while total_supply < requirement:
            if c <= 2:
                growth_add = 0.11
            elif 2 < c < 5:
                growth_add = 0.13
            else:
                growth_add = 0.15

            supply_increase_amount = total_supply * growth_add
            total_supply += supply_increase_amount
            year += 1
            year_list2.append(year)
            supply_list2.append(total_supply)
            c += 1
            requirement = requirement * (1 + CAGR)

        # Plot the figure for the Industry requirement

        # Create the figure
        fig = go.Figure()
        # Put a random seed
        np.random.seed(42)

        # Add traces for Biochar Price
        fig.add_trace(
            go.Scatter(x=year_list2, y=supply_list2 + np.random.normal(0, std, len(supply_list2)), mode='lines+markers',
                       name='Biochar Supply'))

        # Update the layout
        fig.update_layout(
            title=dict(text='Biochar Supply Projection', font=dict(size=24), x=0.5, xanchor='center'),
            xaxis=dict(title='Years', showgrid=True),
            yaxis=dict(title='Supply (In 10^3 Tonnes)', showgrid=True),
            legend=dict(x=0, y=1, xanchor='left', yanchor='top'),
        )

        # Set the figure size (optional)
        fig.update_layout(
            autosize=False,
            width=1300,
            height=700
        )
        # Add a vertical line on the last point
        last_year = year_list2[-1]
        last_supply = supply_list2[-1]

        fig.add_shape(
            type="line",
            x0=last_year,
            x1=last_year,
            y0=0,
            y1=last_supply,
            line=dict(color="red", width=2),
        )

        # Add an invisible trace for the legend of the vertical line
        fig.add_trace(go.Scatter(
            x=[None],
            y=[None],
            mode='lines',
            line=dict(color='red', width=2),
            name="Year Total Coke Replaced with Biochar",
            showlegend=True,
            legendgroup='vertical_line'
        ))

        # Show the figure
        st.plotly_chart(fig)

# Calculations for the whole company
# noinspection PyNoneFunctionAssignment
if selection == "Company":

    # Creating the demo data
    data = {
        'Plant_name_location': ['Bhogasamudram, Tadipatri Mandal, Anantapur District, Andhra Pradesh - 515413',
                                'Adityapuram Sawa Shambhupura Road Dist. Chittorgarh, Rajasthan-312622',
                                'Vill. Post Budawada Mandal-Jaggiyapet, District Krishna, Andhra Pradesh-521175'],
        'Production_capacity(In Million Ton)': [25, 30, 22],
    }
    df = pd.DataFrame(data)

    # Add a button to view the demo data
    if st.button('View Demo Data'):
        st.write(df.head())
    df1 = pd.DataFrame()

    # Select File to Upload
    uploaded_file = st.file_uploader("Upload the data of plants production capacities(W/O Serial No)[In CSV format]",
                                     type=["csv"])
    if uploaded_file is not None:
        try:
            # Read the file
            if uploaded_file.type == 'application/vnd.ms-excel':
                # Read the content of the uploaded file using BytesIO buffer
                buffer = io.BytesIO(uploaded_file.read())

                # Use chardet to detect encoding
                encoding = chardet.detect(buffer.getvalue())['encoding']

                # Reset buffer's position back to the start
                buffer.seek(0)

                # Read the Excel file using detected encoding
                df1 = pd.read_excel(buffer, engine='openpyxl')
            else:
                df1 = pd.read_csv(uploaded_file)

            # Display Df.head
            st.text("Plant details received")
            st.empty()
            st.write(df1.head())

        except Exception as e:
            st.error(f"An error occurred: {e}")

    # take the pilot year as input
    year = st.number_input('Enter the year of starting the first pilot')

    # variable to store the input year to use later on
    year_proxy = year

    # Button to run the model
    if st.button(" Run Calculations"):

        # make a new column of biochar requirement
        df1['biochar_requirement(10^3 ton)'] = df1.iloc[:, 1] * factor * 1000
        df1 = df1.drop_duplicates()

        # Get the first column index
        column_index_1 = df1.columns[0]

        # Get the second column index
        column_index_2 = df1.columns[2]

        # Create key-value pair from the two columns using column indices
        key_value_pair = df1.set_index(column_index_1)[column_index_2].to_dict()

        # set total supply and demand
        total_demand = df1['biochar_requirement(10^3 ton)'].sum()
        st.write('Total demand is :', total_demand)
        total_supply = 0  # for initial year

        # create 5 temporary variables for different stages
        temp1, temp2, temp3, temp4, temp5 = 0, 0, 0, 0, 0

        # to store the values of different stages
        stage1, stage2, stage3, stage4, stage5 = list(), list(), list(), list(), list()

        # Final list to store the sum of all 5 stages
        final_list = list()
        final_list.append(0)

        # Make a list to save years
        year_final = list()
        year_final.append(year_proxy)

        # Counter to keep track of years
        c1, c2, c3, c4, c5 = 0, 0, 0, 0, 0

        # Starting rate
        start_rate = 0.2
        # Growth rate
        growth = 0.18

        # Set up a random seed for repeating all random samplings
        np.random.seed(42)

        # stage 1
        # Number of random pairs you want to select
        num_random_pairs_1 = 1

        # Select random keys and pop their corresponding values from the dictionary
        random_keys_1 = random.sample(list(key_value_pair.keys()), num_random_pairs_1)
        random_pairs_1 = [(key, key_value_pair.pop(key)) for key in random_keys_1]

        # Sum up the values in random pairs
        sum_of_values_1 = sum(value for _, value in random_pairs_1)

        # Stage 2
        # Number of random pairs you want to select
        num_random_pairs_2 = 2

        # Select random keys and pop their corresponding values from the dictionary
        random_keys_2 = random.sample(list(key_value_pair.keys()), num_random_pairs_2)
        random_pairs_2 = [(key, key_value_pair.pop(key)) for key in random_keys_2]

        # Sum up the values in random pairs
        sum_of_values_2 = sum(value for _, value in random_pairs_2)

        # Stage 3
        # Number of random pairs you want to select
        num_random_pairs_3 = 4

        # Select random keys and pop their corresponding values from the dictionary
        random_keys_3 = random.sample(list(key_value_pair.keys()), num_random_pairs_3)
        random_pairs_3 = [(key, key_value_pair.pop(key)) for key in random_keys_3]

        # Sum up the values in random pairs
        sum_of_values_3 = sum(value for _, value in random_pairs_3)

        # Stage 4
        # Number of random pairs you want to select
        num_random_pairs_4 = 6

        # Select random keys and pop their corresponding values from the dictionary
        random_keys_4 = random.sample(list(key_value_pair.keys()), num_random_pairs_4)
        random_pairs_4 = [(key, key_value_pair.pop(key)) for key in random_keys_4]

        # Sum up the values in random pairs
        sum_of_values_4 = sum(value for _, value in random_pairs_4)

        # Stage 5

        # Sum up the values in all the remaining pairs
        sum_of_values_5 = sum(key_value_pair.values())

        # operate a loop until total supply is less than total demand
        while total_supply < total_demand:
            # Different conditions for starting of different stages
            if c1 == 0:  # Stage 1
                temp1 += sum_of_values_1 * start_rate
            elif c1 > 0:
                temp1 += stage1[-1] * growth
            if c2 == 2:  # Stage 2
                temp2 += sum_of_values_2 * start_rate
            elif c2 > 2:
                temp2 += stage2[-1] * growth
            if c3 == 4:  # Stage 3
                temp3 += sum_of_values_3 * start_rate
            elif c3 > 4:
                temp3 += stage3[-1] * growth
            if c4 == 5:  # Stage 4
                temp4 += sum_of_values_4 * start_rate
            elif c4 > 5:
                temp4 += stage4[-1] * growth
            if c5 == 6:  # Stage 5
                temp5 += sum_of_values_5 * start_rate
            elif c5 > 6:
                temp5 += stage5[-1] * growth

            # Appending the values in the corresponding lists
            if temp1 < sum_of_values_1:
                stage1.append(temp1)
            else:
                stage1.append(sum_of_values_1)
            if temp2 < sum_of_values_2:
                stage2.append(temp2)
            else:
                stage2.append(sum_of_values_2)
            if temp3 < sum_of_values_3:
                stage3.append(temp3)
            else:
                stage3.append(sum_of_values_3)
            if temp4 < sum_of_values_4:
                stage4.append(temp4)
            else:
                stage4.append(sum_of_values_4)
            if temp5 < sum_of_values_5:
                stage5.append(temp5)
            else:
                stage5.append(sum_of_values_5)

            # Updating the total supply
            total_supply = stage1[-1] + stage2[-1] + stage3[-1] + stage4[-1] + stage5[-1]
            final_list.append(total_supply)

            # Updating the year
            year += 1
            year_final.append(year)

            c1 += 1
            c2 += 1
            c3 += 1
            c4 += 1
            c5 += 1

        # Create the figure
        fig = go.Figure()
        # Put a random seed
        np.random.seed(42)

        # Add traces for Biochar Price
        fig.add_trace(go.Scatter(x=year_final, y=final_list + np.random.normal(0, std, len(final_list)),
                       mode='lines+markers',
                       name='Biochar Supply'))

        # Create traces for vertical lines and plot legends
        fig.add_trace(go.Scatter(
                x=[year_proxy, year_proxy],
                y=[min(final_list), max(final_list)],
                mode='lines',
                line=dict(dash='dot', color='red'),
                name='Start of Stage 1'))

        # Create traces for vertical lines and plot legends
        fig.add_trace(go.Scatter(
            x=[year_proxy + 2, year_proxy + 2],
            y=[min(final_list), max(final_list)],
            mode='lines',
            line=dict(dash='dot', color='green'),
            name='Start of Stage 2'))

        # Create traces for vertical lines and plot legends
        fig.add_trace(go.Scatter(
            x=[year_proxy + 4, year_proxy + 4],
            y=[min(final_list), max(final_list)],
            mode='lines',
            line=dict(dash='dot', color='blue'),
            name='Start of Stage 3'))
        # Create traces for vertical lines and plot legends
        fig.add_trace(go.Scatter(
            x=[year_proxy + 5, year_proxy + 5],
            y=[min(final_list), max(final_list)],
            mode='lines',
            line=dict(dash='dot', color='black'),
            name='Start of Stage 4'))

        # Create traces for vertical lines and plot legends
        fig.add_trace(go.Scatter(
            x=[year_proxy + 6, year_proxy + 6],
            y=[min(final_list), max(final_list)],
            mode='lines',
            line=dict(dash='dot', color='magenta'),
            name='Start of Stage 5'))

        # Update the layout
        fig.update_layout(
            title=dict(text='Biochar Supply Projection', font=dict(size=24), x=0.5, xanchor='center'),
            xaxis=dict(title='Years', showgrid=True),
            yaxis=dict(title='Supply (In 10^3 Tonnes)', showgrid=True),
            legend=dict(x=1, y=0, xanchor='right', yanchor='bottom'),
        )

        # Set the figure size (optional)
        fig.update_layout(
            autosize=False,
            width=1200,
            height=600
        )

        # Show the figure
        st.plotly_chart(fig)

        # Display the Plants that were selected on different stages
        st.write(' ')
        st.write(' ')
        st.write('Plants selected for stage 1 are :', random_keys_1)
        st.write(' ')
        st.write(' ')
        st.write('Plants selected for stage 2 are :', random_keys_2)
        st.write(' ')
        st.write(' ')
        st.write('Plants selected for stage 3 are :', random_keys_3)
        st.write(' ')
        st.write(' ')
        st.write('Plants selected for stage 4 are :', random_keys_4)
        st.write(' ')
        st.write(' ')
        st.write('Plants selected for stage 5 are :', list(key_value_pair.keys()))
