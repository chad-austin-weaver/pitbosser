import streamlit as st
from constraint import *

import casino
import constraintfunction
import pandas as pd
import testgen
import visualizations

# TODO: 3. Bar charts of test data from hypothesis-based experiments.
# TODO: Implement streamlit.io .CSV creator/exporter.

# TODO: Set dealer IDs for comparisons speed-up.
# TODO: Clean-up visuals (condense/merge (table, r-table), crap tables on schedule, color/sort pie chart wedges)

def relief_constraint(*assignments):
    #Count times each dealer assigned
    dealer_count = {dealer: assignments.count(dealer.getName()) for dealer in testCasino.getDealers()}

    #Ensure no dealer is assigned more than n positions
    return all(count <= testCasino.getMaxReliefTables() for dealer, count in dealer_count.items())

error_message = "Error! Check your input file.\nNot sure what's wrong? Check the Quickstart Guide."

st.title("Pitbosser")
st.markdown("***")
upload_file = st.file_uploader("Upload .csv file")
st.markdown("***")

if upload_file:    
    testCasino = casino.Casino()
    problem = Problem()
    problem.setSolver(RecursiveBacktrackingSolver())
    try:
        testCasino.import_casino_from_upload_file(upload_file)
        testCasino.set_table_variables(problem)
        problem.addConstraint(AllDifferentConstraint(), testCasino.tableVars)
        constraintfunction.disjoint_sets(problem, testCasino.tableVars, testCasino.reliefVars)
        problem.addConstraint(relief_constraint, testCasino.reliefVars)
        solution = problem.getSolution()
        
    #TODO: Add link to Quickstart Guide.
    except TypeError:
        st.write(error_message)
    except KeyError:
        st.write(error_message)
    except IndexError:
        st.write(error_message)
    except ValueError:
        st.write(error_message)
    if solution:
        schedule = visualizations.generate_schedule(solution)

        strip_game_mix = {
            "blackjack": 0.4841,
            "craps": 0.0781,
            "roulette": 0.1217,
            "3-card poker": 0.0377,
            "baccarat": 0.1608,
            "mini-baccarat": 0.0260,
            "let it ride": 0.0076,
            "pai gow": 0.0058,
            "pai gow poker": 0.0395,
            "other": 0.0386
        }
    
        st.markdown(schedule.style.hide(axis="index").to_html(), unsafe_allow_html=True)

        strip_averages = {game_type: strip_game_mix.get(game_type) for game_type in testCasino.getGameTypes()}
        strip_games_pie = visualizations.generate_game_mix_chart(strip_averages)
        actual_games_pie = visualizations.generate_game_mix_chart(testCasino.getTablesOfType())
        st.markdown("***")
        col1, col2 = st.columns(2)
        with col1:
            st.header("[Strip game mix:](https://gaming.library.unlv.edu/reports/strip_game_mix.pdf)")
            st.pyplot(strip_games_pie)
        with col2:
            st.header("Actual game mix:")
            st.pyplot(actual_games_pie)
        st.markdown("***")
    else:
        st.write("No solution found!")
