import pandas as pd
import streamlit as st
import plotly.express as px
import streamlit.components.v1 as components

menu_dict = {'Report a Bug':'mailto:gabyl@post.bgu.ac.il', 'About': "This dashboard contains information about students' spending habits"}
# Set page title and layout
st.set_page_config(page_title='Student Spending Analysis', page_icon=":student:", layout='wide', menu_items=menu_dict)
st.title('Student Spending Analysis')

# Helper function to format numbers
def format_number(number):
    return f"${number:,.2f}"

# Function to set background color and text color
def set_bg_color():
    st.markdown(
        f"""
         <style>
         .stApp {{
             background-color: #b1c9e3;
             color: #787474; 
         }}
         .stPlotlyChart {{
             background-color: #b1c9e3;
             color: #787474;
         }}
         .stMetric {{
             background-color: #dbdb1f;
             border-radius: 10px;
             padding: 10px;
         }}
         .stSelectbox, .stMultiselect, .stTextInput, .stButton {{
             background-color: #787474;
             color: #E0E0E0; /* Brighter text color */
             border-radius: 5px;
         }}
         .stMarkdown {{
             color: black; /* Brighter text color */
         }}
         </style>
         """,
        unsafe_allow_html=True
    )


# Set background color
set_bg_color()

def ColourWidgetText(wgt_txt, wch_colour = '#000000'):
    htmlstr = """<script>var elements = window.parent.document.querySelectorAll('*'), i;
                    for (i = 0; i < elements.length; ++i) { if (elements[i].innerText == |wgt_txt|) 
                        elements[i].style.color = ' """ + wch_colour + """ '; } </script>  """

    htmlstr = htmlstr.replace('|wgt_txt|', "'" + wgt_txt + "'")
    components.html(f"{htmlstr}", height=0, width=0)

# Reading the CSV file
file_path = r"student_spending.csv"
df = pd.read_csv(file_path)
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

# Calculate average values
average_food_spending = round(df['food'].mean(), 2)
average_tuition_spending = round(df['tuition'].mean(), 2)
average_income = round(df['monthly_income'].mean(), 2)
average_housing_spending = round(df['housing'].mean(), 2)
average_transportation_spending = round(df['transportation'].mean(), 2)
average_technology_spending = round(df['technology'].mean(), 2)
average_personal_care_spending = round(df['personal_care'].mean(), 2)
average_entertainment_spending = round(df['entertainment'].mean(), 2)
average_books_supplies_spending = round(df['books_supplies'].mean(), 2)

# Display metrics
average_spending_text = 'Average spending on'
per_month = 'per month'
col1, col2, col3 = st.columns((1, 1, 3), gap='small')
with col1:
    st.markdown('Average Spending Stats')
    st.metric(label=f'**Food**', value=f'{average_food_spending} $', help=f'{average_spending_text} Food {per_month}')
    st.metric(label=f'**Tuition**', value=f'{average_tuition_spending} $', help=f'{average_spending_text} Tuition {per_month}')
    st.metric(label=f'**Housing**', value=f'{average_housing_spending} $', help=f'{average_spending_text} Housing {per_month}')
    st.metric(label=f'**Technology**', value=f'{average_technology_spending} $', help=f'{average_spending_text} Technology {per_month}')

    ColourWidgetText(f'**Food**', '#00B0F0')  # colour only metric text
    ColourWidgetText(f'{average_food_spending} $', '#0a0a0a')

    ColourWidgetText(f'**Tuition**', '#00B0F0')  # colour only metric text
    ColourWidgetText(f'{average_tuition_spending} $', '#0a0a0a')

    ColourWidgetText(f'**Housing**', '#00B0F0')  # colour only metric text
    ColourWidgetText(f'{average_housing_spending} $', '#0a0a0a')

    ColourWidgetText(f'**Technology**', '#00B0F0')  # colour only metric text
    ColourWidgetText(f'{average_technology_spending} $', '#0a0a0a')


with col2:

    st.markdown('Average Spending Stats')
    st.metric(label=f'**Transportation**', value=f'{average_transportation_spending} $', help=f'{average_spending_text} Transportation {per_month}')
    st.metric(label=f'**Entertainment**', value=f'{average_entertainment_spending} $', help=f'{average_spending_text} Entertainment {per_month}')
    st.metric(label=f'**Books Supplies**', value=f'{average_books_supplies_spending} $', help=f'{average_spending_text} Books Supplies {per_month}')
    st.metric(label=f'**Personal Care**', value=f'{average_personal_care_spending} $', help=f'{average_spending_text} Personal Care {per_month}')

    ColourWidgetText(f'**Transportation**', '#00B0F0')  # colour only metric text
    ColourWidgetText(f'{average_transportation_spending} $', '#0a0a0a')

    ColourWidgetText(f'**Entertainment**', '#00B0F0')  # colour only metric text
    ColourWidgetText(f'{average_entertainment_spending} $', '#0a0a0a')

    ColourWidgetText(f'**Books Supplies**', '#00B0F0')  # colour only metric text
    ColourWidgetText(f'{average_books_supplies_spending} $', '#0a0a0a')

    ColourWidgetText(f'**Personal Care**', '#00B0F0')  # colour only metric text
    ColourWidgetText(f'{average_personal_care_spending} $', '#0a0a0a')


# Pie chart for preferred payment method
with col3:
    payment_method_counts = df['preferred_payment_method'].value_counts()
    fig_pie = px.pie(payment_method_counts, values=payment_method_counts.values, names=payment_method_counts.index,
                     title='Preferred Payment Methods', color_discrete_sequence=px.colors.sequential.RdBu)
    fig_pie.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#E0E0E0'  # Brighter text color
    )
    st.plotly_chart(fig_pie)

# Define categories to display
categories = ['housing', 'food', 'transportation', 'books_supplies', 'entertainment', 'personal_care', 'technology', 'health_wellness', 'miscellaneous']

# Calculate percentage of spending for each gender in each category
df_perc = df.groupby('gender')[categories].sum()
df_perc = df_perc.div(df_perc.sum(axis=1), axis=0) * 100

# Reshape data for plotting
df_melt = df_perc.reset_index().melt(id_vars='gender', var_name='category', value_name='percentage')



# Layout with columns for checkboxes and chart
col4, col5 = st.columns([1, 3])

with col4:
    st.markdown("## Select Categories to Display")
    selected_categories = []
    for category in categories:
        if st.checkbox(f'{category}', value=True):
            selected_categories.append(category)

with col5:
    # Filter data to selected categories
    df_melt_filtered = df_melt[df_melt['category'].isin(selected_categories)]

    # Bar chart for percentage of spending by gender
    st.markdown("## Percentage of Dollars Spent by Gender in Each Category")
    fig = px.bar(df_melt_filtered, x='category', y='percentage', color='gender',
                barmode='group', labels={'percentage': 'Percentage of Total Spending (%)'},
                color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#E0E0E0'  # Brighter text color
    )
    st.plotly_chart(fig)

# Calculate average spending per category per year in school
df_avg = df.groupby('year_in_school')[categories].mean().reset_index()
df_avg = df_avg.melt(id_vars='year_in_school', var_name='category', value_name='average_spending')

# Add this line to ensure unique combinations of year_in_school and category
df_avg = df_avg.groupby(['year_in_school', 'category'])['average_spending'].mean().reset_index()

# Create a mapping of categories to numerical values
category_mapping = {
    'Freshman': 1,
    'Sophomore': 2,
    'Junior': 3,
    'Senior': 4
}

# Apply the mapping to create a numerical column for sorting
df_avg['year_in_school_num'] = df_avg['year_in_school'].map(category_mapping)
spending_categories1 = ['tuition','housing', 'food', 'transportation', 'books_supplies', 'entertainment', 'personal_care', 'technology', 'health_wellness', 'miscellaneous']

# Line chart for average spending by year in school
st.title('Average Spending by Year in School', help='Choose which categories you want to show, we suggest no more than 3-4')
selected_categories = st.multiselect('Select Categories', spending_categories1, default=['housing','food'])
filtered_data = df_avg[df_avg['category'].isin(selected_categories)]

# Sort by the numerical column
filtered_data = filtered_data.sort_values(by='year_in_school_num')

# Plot with Plotly
fig = px.line(filtered_data, x='year_in_school', y='average_spending', color='category',
              labels={'year_in_school': 'Year in School', 'average_spending': 'Average Spending'},
              line_shape='spline', color_discrete_sequence=px.colors.sequential.RdBu)
fig.update_layout(
    xaxis={'categoryorder': 'array', 'categoryarray': sorted(category_mapping.values())},  # Use numerical order
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color='#787474'  # Brighter text color
)
st.plotly_chart(fig)

spending_categories = ['housing', 'food', 'transportation', 'books_supplies', 'entertainment', 'personal_care', 'technology', 'health_wellness', 'miscellaneous']

# Calculate total spending per student
df['total_spending'] = df[spending_categories].sum(axis=1)

# Group by major and calculate total spending and number of students per major
df_major = df.groupby('major').agg(total_spending=('total_spending', 'sum'), num_students=('total_spending', 'size')).reset_index()
df_major['normalized_spending'] = df_major['total_spending'] / df_major['num_students']


# Bar chart for average spending by major
st.title('Average Spending by Major', help='Choose which categories you want to show')
selected_categories = st.multiselect('Select Spending Categories to Display', spending_categories, default=['technology', 'books_supplies'])
if selected_categories:
    df_avg_spending = df.groupby('major')[selected_categories].mean().reset_index()
    df_melt = pd.melt(df_avg_spending, id_vars='major', value_vars=selected_categories, var_name='Category', value_name='Average Spending')
    fig = px.bar(df_melt, x='major', y='Average Spending', color='Category', barmode='group',
                 title='Average Spending by Major', labels={'major': 'Major', 'Average Spending': 'Average Spending (USD)'},
                 color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#787474', # Brighter text color
        xaxis = {'tickfont': {'color': '#787474'}}  # X-axis tick color
    )
    st.plotly_chart(fig)
else:
    st.write("Please select at least one spending category to display.")
