# Fabian E. Ortega
# Human Computer Interaction - Project 1
# 5/25/2025

import streamlit as st
import pandas as pd
import time
import os

# Create a folder called data in the main project folder
DATA_FOLDER = "data"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

# Define CSV file paths for each part of the usability testing
CONSENT_CSV = os.path.join(DATA_FOLDER, "consent_data.csv")
DEMOGRAPHIC_CSV = os.path.join(DATA_FOLDER, "demographic_data.csv")
TASK_CSV = os.path.join(DATA_FOLDER, "task_data.csv")
EXIT_CSV = os.path.join(DATA_FOLDER, "exit_data.csv")


def save_to_csv(data_dict, csv_file):
    # Convert dict to DataFrame with a single row
    df_new = pd.DataFrame([data_dict])
    if not os.path.isfile(csv_file):
        # If CSV doesn't exist, write with headers
        df_new.to_csv(csv_file, mode='w', header=True, index=False)
    else:
        # Else, we need to append without writing the header!
        df_new.to_csv(csv_file, mode='a', header=False, index=False)


def load_from_csv(csv_file):
    if os.path.isfile(csv_file):
        return pd.read_csv(csv_file)
    else:
        return pd.DataFrame()


def main():
    st.title("Usability Testing Tool")

    home, consent, demographics, tasks, exit, report = st.tabs(
        ["Home", "Consent", "Demographics", "Task", "Exit Questionnaire", "Report"])

    with home:
        st.header("Introduction")
        st.write("""
        Welcome to the Usability Testing Tool for HCI.

        In this app, you will:
        1. Provide consent for data collection.
        2. Fill out a short demographic questionnaire.
        3. Perform a specific task (or tasks).
        4. Answer an exit questionnaire about your experience.
        5. View a summary report (for demonstration purposes).
        """)

    with consent:
        st.header("Consent Form")
        st.write("Please read the consent bellow  and agree to the agreement.")
        st.write("**Consent Agreement:**")
        st.write("""
                By participating, you agree to allow your responses and feedback 
                during the questionare to be recorded and used for research purposes only. 
                No personal information will be shared to the public.
                """)
        st.write("- I aknowleged my data will be used for research purposes.")
        st.write("- I aknowleged my information will not be shared to the public")
        consent_given = st.checkbox("I agree to the consent above")

        if st.button("Submit Consent"):
            if not consent_given:
                st.error("You must agree to the consent terms before proceeding.")

            else:
                # Save the consent acceptance time
                data_dict = {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "consent_given": consent_given
                }
                save_to_csv(data_dict, CONSENT_CSV)
                # when submitted, display sucess message
                st.success("Consent submitted")

    with demographics:
        st.header("Demographic Questionnaire")

        with st.form("demographic_form"):
            name = st.text_input("Enter full name", placeholder="First name and last name")
            age = st.number_input("Enter age", min_value=18, max_value=60, step=1)
            occupation = st.text_input("Enter occupation")
            familiarity = st.selectbox("Enter familiarity", options =
                                   ["", "Not Familar", "Familar", "Somewhat Familar"])
            submitted = st.form_submit_button("Submit")

            # created a F value holder
            missing = False

            #Add error message if boxes are missing
            if  age and name and occupation and familiarity:
                missing = True

            if submitted and missing:
                st.success("Demographic questionnaire submitted")
                data_dict = {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "name": name,
                    "age": age,
                    "occupation": occupation,
                    "familiarity": familiarity
                }
                save_to_csv(data_dict, DEMOGRAPHIC_CSV)

                #Error Message if missing
            if submitted and missing == False:
                st.error("Please fill out the form, make sure all fields are completed")

    with tasks:

        st.header("Task Page")

        st.write("Please select a task and record your experience completing it.")

        # For this template, we assume there's only one task, in project 3, we will have to include the actual tasks
        selected_task = st.selectbox("Select Task", ["Task 1: Example Task"])
        st.write("Task Description: Perform the example task in our system...")

        # Track success, completion time, etc.
        start_button = st.button("Start Task Timer")
        if start_button:
            st.session_state["start_time"] = time.time()
            st.success("Task Timer started")

        stop_button = st.button("Stop Task Timer")
        if stop_button and "start_time" in st.session_state:
            duration = time.time() - st.session_state["start_time"]
            st.session_state["task_duration"] = duration

            # display timer total
            st.warning(f"Task Timer stopped. Completed in {duration:.2f} seconds.")

        success = st.radio("Was the task completed successfully?", ["Yes", "No", "Partial"])
        notes = st.text_area("Observer Notes", placeholder="Write your feedback here")

        submitted2 = st.button("Save Task Results")

        # place horder for fill entire page
        notFilled = False

        if  notes:
            notFilled = True


        if submitted2 and notFilled:
            st.success("Task results saved")
            duration_val = st.session_state.get("task_duration", None)

            data_dict = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "task_name": selected_task,
                "success": success,
                "duration_seconds": duration_val if duration_val else "",
                "notes": notes
            }
            save_to_csv(data_dict, TASK_CSV)

            # Error message if not filled
        if submitted2 and notFilled == False:
            st.error("Please fill out the form, make sure all fields are completed")

            # Reset any stored time in session_state if you'd like
            if "start_time" in st.session_state:
                del st.session_state["start_time"]
            if "task_duration" in st.session_state:
                del st.session_state["task_duration"]



    with exit:
        st.header("Exit Questionnaire")

        with st.form("exit_form"):
            satisfaction = st.slider("How satisfied is the exit questionnaire? (1=very low, 10=very high)", min_value=1, max_value=10)
            difficulty = st.slider("How difficulty is the exit questionnaire? (1=very low, 10=very high)", min_value=1, max_value=10)
            open_feedback = st.text_area("Open Feedback", placeholder="Write additional feedback here (optional)")


            submitted_exit = st.form_submit_button("Submit Exit Questionnaire")
            if submitted_exit:
                data_dict = {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),

                    "satisfaction": satisfaction,
                    "difficulty": difficulty,
                    "open_feedback": open_feedback
                }
                save_to_csv(data_dict, EXIT_CSV)
                st.success("Exit questionnaire data saved.")




    with report:
        st.header("Usability Report - Aggregated Results")

        st.write("**Consent Data**")
        consent_df = load_from_csv(CONSENT_CSV)
        if not consent_df.empty:
            st.dataframe(consent_df)
        else:
            st.info("No consent data available yet.")

        st.write("**Demographic Data**")
        demographic_df = load_from_csv(DEMOGRAPHIC_CSV)
        if not demographic_df.empty:
            st.dataframe(demographic_df)
        else:
            st.info("No demographic data available yet.")

        st.write("**Task Performance Data**")
        task_df = load_from_csv(TASK_CSV)
        if not task_df.empty:
            st.dataframe(task_df)
        else:
            st.info("No task data available yet.")

        st.write("**Exit Questionnaire Data**")
        exit_df = load_from_csv(EXIT_CSV)
        if not exit_df.empty:
            st.dataframe(exit_df)
        else:
            st.info("No exit questionnaire data available yet.")

        # Example of aggregated stats (for demonstration only)
        if not exit_df.empty:
            st.subheader("Exit Questionnaire Averages")
            avg_satisfaction = exit_df["satisfaction"].mean()
            avg_difficulty = exit_df["difficulty"].mean()
            st.write(f"**Average Satisfaction**: {avg_satisfaction:.2f}")
            st.write(f"**Average Difficulty**: {avg_difficulty:.2f}")


if __name__ == "__main__":
    main()