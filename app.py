# CIW Model Application created with Shiny for Python (Core syntax, not Express)

# -----------------------------------------------------------------------------
# Library imports
# -----------------------------------------------------------------------------

from shiny import (App, ui, render, reactive, Inputs, Outputs, Session)
from shinywidgets import output_widget, render_widget
import shinyswatch
import plotly.graph_objects as go
import pandas as pd
from pathlib import Path
from faicons import icon_svg

# Import the wrapper objects for model interaction.
from ciw_model import Experiment, multiple_replications

# -----------------------------------------------------------------------------
# Static text
# -----------------------------------------------------------------------------

MODAL = """
It provides a Shiny for Python interface to a `ciw` discrete-event simulation
model. This allows users to easily experiment with the simulation model.

The web app is hosted on a free tier of shinyapps.io.
"""

INTRO = """
This app is based on a 
[ciw example](https://health-data-science-or.github.io/simpy-streamlit-tutorial/content/03_streamlit/13_ciw_backend.html) 
that simulates a simple call centre model.
"""

MODELDESCRIPTION = """
## Model Summary

In this model:

1. Patients ring the urgent care call centre and wait for an operator.
2. A given proportion of patients will then require callback from a nurse.

The simulation allows you to alter the number of call operators and nurses on
duty.

You can then view the subsequent impact on caller wait times and staff
utilisation (i.e. the proportion of time that operators or nurses spent on
call, whilst on duty).
"""

ABOUT = """
## About

This work is produced using entirely free and open-source software in python.

> This model is independent research supported by the National Institute for
Health Research Applied Research Collaboration South West Peninsula. The views
expressed in this publication are those of the author(s) and not necessarily 
those of the National Institute for Health Research or the Department of Health
and Social Care.
"""

SIMSOFTWARE = """
## Modelling and Simulation Software

The model is written in python3 and `ciw`. The simulation libary `ciw` is a
network based DES package.

> Detailed documentation for `ciw` and additional models can be found here:
https://ciw.readthedocs.io
"""

DOCS_LINK = """
## Model Documentation

Live documentation including STRESS-DES reporting for the model and 
is available at: https://pythonhealthdatascience.github.io/stars-ciw-example/
"""

TABLE_TITLE = "### Tabular results"
TABLE_TOOLTIP = """
Average results across replications: mean, standard deviation (std), minimum
(min), first quartile (25%), median (50%), third quartile (75%) and
maximum (max)
"""

GRAPH_TITLE = "### Graphical results"
GRAPH_TOOLTIP = """
Histogram plotting the average wait time or utilisation from each replication.
Will be unhelpful if all results are 0.
"""
GRAPH_INFO = "Please select a performance measure:"

GITHUBLINK = "https://github.com/pythonhealthdatascience/stars-ciw-example/"
DOCSLINK = "https://pythonhealthdatascience.github.io/stars-ciw-example/"

REP_ERROR = """<p style='color: #CC5500;'><b>Error: Set number of replications
to 1 or above</b></p>"""

# -----------------------------------------------------------------------------
# User interface: define layout and structure of app
# e.g. input controls, output displays
# -----------------------------------------------------------------------------

app_ui = ui.page_fluid(

    # Page header
    ui.row(
        # Logo
        ui.column(
            # Column width (required by function but we override with style)
            6,
            # Logo
            ui.tags.div(
                ui.tags.img(
                    src="stars_logo.png", height="100px"),
            ),
            # Ensure that the column always takes up 110px
            style="flex: 0 0 110px; max-width: 110px;",
        ),
        # Heading and introduction
        ui.column(
            # Column width (required by function but we override with style)
            6,
            # Title
            ui.h1(
                "Ciw Urgent Care Call Centre Model", style="margin-top: 10px;"),
            # Intro section
            ui.markdown(INTRO),
            # Button to navigate to GitHub code
            ui.input_action_button(
                id="github_btn",
                label="View code on GitHub" ,  
                icon=icon_svg("github")
            ),
            ui.tags.script(f"""
                document.getElementById('github_btn').onclick = function() {{
                    window.open('{GITHUBLINK}', '_blank');
                }};
            """),
            # Button to view model documentation
            ui.input_action_button(
                id="docs_btn",
                label="View model documentation" ,  
                icon=icon_svg("book")
            ),
            ui.tags.script(f"""
                document.getElementById('docs_btn').onclick = function() {{
                    window.open('{DOCSLINK}', '_blank');
                }};
            """),
            # Resize width to fill space, alongside the fixed logo column
            style="flex: 1; min-width: 0;",
        ),
    ),

    # Blank space
    ui.div().add_style("height:20px;"),

    # Sidebar and main panel
    ui.navset_tab(
        # Panel for the simulation page
        ui.nav_panel("Interactive simulation", 
            ui.layout_sidebar(
                # Sidebar content
                ui.sidebar(
                    
                    # Number of call operators
                    ui.tooltip(
                        ui.input_slider(id="n_operators",
                                        label="Call operators",
                                        min=1,
                                        max=40,
                                        value=13,
                                        ticks=False),
                        "Number of call operators on duty"
                    ),

                    # Number of nurses on duty
                    ui.tooltip(
                        ui.input_slider(id="n_nurses",
                                        label="Nurse practitioners",
                                        min=1,
                                        max=20,
                                        value=9,
                                        ticks=False),
                        "Number of nurses on duty"
                    ),

                    # Chance of nurse callback
                    ui.tooltip(
                        ui.input_slider(id="chance_callback",
                                        label="Probability of nurse callback",
                                        min=0.0,
                                        max=1.0,
                                        value=0.4,
                                        ticks=False),
                        """The probability of nurse callback: 0 means never,
                        0.5 means 50% of the time, and 1 means always"""
                    ),

                    # Number of replications
                    ui.tooltip(
                        # We set a minimum which applies to the arrow clicked,
                        # but user can still override minimum by typing
                        ui.input_numeric(id="n_reps",
                                        label="Replications",
                                        value=10,
                                        min=1),
                        "How many times to run the model (minimum 1)"
                    ),
                    # Error message if number of replications is set to <1
                    ui.output_ui("rep_error"),

                    # run simulation model button
                    ui.input_action_button(id="run_sim",
                                           label="Run Simulation",
                                           class_="btn-primary"),
                ),
                # Main panel content
                ui.output_ui("result_table_info"),
                ui.output_data_frame("result_table"),
                ui.div().add_style("height:20px;"),  # Blank space
                ui.output_ui("result_graph_info"),
                output_widget("histogram"),
            ),
        ),
        # Panel for the about page
        ui.nav_panel("About",
                     ui.card(
                         ui.markdown(MODELDESCRIPTION),
                         # Center and prevent resizing of image
                         ui.tags.div(
                            ui.tags.img(src="model_logic.png",
                                        style="max-width: 100%; height: auto;"),
                            style="text-align: center;"
                        )
                     ),
                     ui.card(ui.markdown(ABOUT)),
                     ui.card(ui.markdown(SIMSOFTWARE)),
                     ui.card(ui.markdown(DOCS_LINK)))
    ),

    # Blank space
    ui.div().add_style("height:80px;"),

    theme = shinyswatch.theme.journal()
)

# -----------------------------------------------------------------------------
# Server: define logic and behaviour of app
# e.g. reactivity, rendering outputs
# -----------------------------------------------------------------------------

def server(input: Inputs, output: Outputs, session: Session):

    # Display about modal when app is opened
    ui.modal_show(
        ui.modal(
            ui.markdown('This application has been developed as part of STARS:'),
            ui.tags.img(src="stars_banner.png", height="100px"),
            ui.div().add_style("height:20px;"),  # Blank space
            ui.markdown(MODAL),
            title="Ciw Urgent Care Call Centre Model"
        )
    )

    # reactive value for replication results.
    replication_results = reactive.Value()

    def run_simulation():
        '''
        Run the simulation model

        Returns:
        --------
        pd.DataFrame
            Pandas Dataframe containing replications by performance
            measures
        '''
        # create the experiment
        user_experiment = Experiment(n_operators=input.n_operators(),
                                     n_nurses=input.n_nurses(),
                                     chance_callback=input.chance_callback())
        
        # run multiple replications
        results = multiple_replications(user_experiment, n_reps=input.n_reps())

        # Renaming metrics
        metrics = {
            '01_mean_waiting_time': 'Time waiting for operator (mins)',
            '02_operator_util': 'Operator utilisation (%)',
            '03_mean_nurse_waiting_time': 'Time waiting for nurse (mins)',
            '04_nurse_util': 'Nurse utilisation (%)'
        }
        results.columns = results.columns.map(metrics)

        return results

    def summary_results(replications):
        '''
        Convert the replication results into a summary table
        
        Returns:
        -------
        pd.DataFrame
        '''
        summary = replications.describe().round(2).T

        # Set index as a column
        summary = summary.reset_index() 
        summary = summary.rename(columns={'index': 'metric'})

        # Drop count, as that is implicit from chosen number of replications
        summary = summary.drop('count', axis=1)

        return summary
    
    def create_user_filtered_hist(results):
        '''
        Create a plotly histogram that includes a drop down list that allows a user
        to select which key performance indicator (KPI) is displayed as a histogram
        
        Params:
        -------
        results: pd.Dataframe
            rows = replications, cols = KPIs
            
        Returns:
        -------
        plotly.figure
        
        Sources:
        ------
        The code in this function was partly adapted from two sources:
        1. https://stackoverflow.com/questions/59406167/plotly-how-to-filter-a-pandas-dataframe-using-a-dropdown-menu
        
        Thanks and credit to `vestland` the author of the reponse.
        
        2. https://plotly.com/python/dropdowns/
        '''
        # Create figure with first metric column by default
        fig = go.Figure(data=[go.Histogram(
            x=results[results.columns[0]],
            # Label when hover over bar, with <extra></extra> preventing it
            # from appending "trace 0" to the end
            hovertemplate='Result of %{x} was found in %{y} replications<extra></extra>')])
        
        # Create dropdown menu to choose between metric columns to plot
        buttons = []
        for col in results.columns:
            buttons.append(
                dict(
                    method='update',
                    label=col,
                    args=[
                        {'x': [results[col]], 'type': 'histogram'},  # Update x data
                        {'xaxis.title.text': col}  # Update the x-axis title
                    ]
                )
            )

        # Update the figure...
        fig.update_layout(

            # Add the dropdown menu to the layout
            updatemenus=[{
                'buttons': buttons,   # List of buttons created above
                'direction': 'down',  # Direction of dropdown
                'showactive': True,   # Keep the selected button highlighted
                'x': 0.25,            # X position of the menu
                'y': 1.1,             # Y position of the menu
                'xanchor': 'right',   # X anchor point
                'yanchor': 'bottom',  # Y anchor point
            }],

            # Hide the legend
            showlegend=False,
   
            xaxis=dict(
                # Add a X axis label
                title=results.columns[0]),  # Initially set to first metric

            yaxis=dict(
                # Ensure ticks are evenly spaced and step of 1
                tickmode='linear', dtick=1,
                # Add a Y axis label
                title='Number of replications'),

            # Alter the displayed plotly toolbar
            modebar={'remove': ['zoom', 'pan', 'lasso', 'zoomIn2d', 'zoomOut2d',
                                'reset', 'select', 'autoscale']}
        )

        return fig

    @render.text
    def rep_error():
        '''
        If number of replications is set below 1, display error message
        '''
        if input.n_reps() < 1:
            return ui.HTML(REP_ERROR)

    @render.text
    @reactive.event(input.run_sim)
    def result_table_info():
        '''
        Reactive event to when the run simulation button is clicked.
        Produces title and paragraph of information about the results table.
        '''
        # Heading
        title = ui.markdown(TABLE_TITLE)
        # Icon with tooltip
        info_icon = ui.tooltip(
            # Class ms-2 adds a margin to the left of the icon
            icon_svg("circle-info").add_class("ms-2"),
            TABLE_TOOLTIP
        )
        return ui.div(title, info_icon, class_="d-flex align-items-center")

    @render.data_frame
    def result_table():
        '''
        Reactive event to when the run simulation button is clicked.
        Produces a summary table of results (mean, median, std, etc.)
        '''
        return summary_results(replication_results())
    
    @render.text
    @reactive.event(input.run_sim)
    def result_graph_info():
        '''
        Reactive event to when the run simulation button is clicked.
        Produces title and paragraph of information about the histogram.
        '''
        # Heading
        title = ui.markdown(GRAPH_TITLE)
        # Icon with tooltip
        info_icon = ui.tooltip(
            # Class ms-2 adds a margin to the left of the icon
            icon_svg("circle-info").add_class("ms-2"),
            GRAPH_TOOLTIP
        )
        # Additional sentence before figure (but remove margin)
        text = ui.HTML(f'<p style="margin: 0;">{GRAPH_INFO}</p>')

        # Combine to return from function
        content = ui.span(
            ui.div(title, info_icon, class_="d-flex align-items-center"),
            text
        )
        return content

    @render_widget
    def histogram():
        '''
        Updates the interactive histogram

        Returns:
        -------
        plotly.figure
        '''
        return create_user_filtered_hist(replication_results())

    @reactive.Effect
    @reactive.event(input.run_sim)
    async def _():
        '''
        Runs simulation model when button is clicked.
        This is a reactive effect. Once replication_results
        is set it invalidates results_table and histogram.  
        These are rerun by Shiny
        '''
        # set to empty - forces shiny to dim output widgets
        # helps with the feeling of waiting for simulation to complete
        replication_results.set([])
        ui.notification_show("Simulation running. Please wait", type='warning')
        replication_results.set(run_simulation())
        ui.notification_show("Simulation complete.", type='message')

    @reactive.Effect
    def _():
        '''
        Reactive effect to enable/disable the button based on n_reps input.
        '''
        # Disable button if n_reps is below 1, otherwise enable it
        if input.n_reps() < 1:
            ui.update_action_button("run_sim", disabled=True)
        else:
            ui.update_action_button("run_sim", disabled=False)

# -----------------------------------------------------------------------------
# Combine ui and server to create app
# -----------------------------------------------------------------------------

www_dir = Path(__file__).parent / "www"
app = App(app_ui, server, static_assets=www_dir)