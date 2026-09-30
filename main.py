import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from langchain.messages import SystemMessage, HumanMessage
from system_prompts import extraction_system_prompt, verification_system_prompt
import streamlit as st
import pandas as pd
from cleaner import clean_transcripts
from validator import validate_action_items
from evaluation_data import (sample_transcripts,evaluation_data_list)
from evaluator import evaluate_action_items

load_dotenv()

api_key = st.secrets["GEMINI_API_KEY2"]

meeting_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash",google_api_key=api_key)

class TasksOwners(BaseModel):
    task: str = Field(description="what is the task that has to be performed?")
    owner: str | None = Field(description="Who is the person responsible for the task")
    deadline: str | None = Field(description="Task needs to be done by which day or date")
    status: str = Field(description="Whether the task has been already completed or pending or delayed")
    confidence: float = Field(description="How much confidence does LLM have on the specific details of a single task given by it, must be between 0 and 1")


class Action_items(BaseModel):
    tasks: list[TasksOwners] = Field(description="it is a list of all the tasks, their owners, deadlines, status and confidence")

extraction_model = meeting_model.with_structured_output(Action_items)
review_model = meeting_model.with_structured_output(Action_items)

if "transcript_text" not in st.session_state:
    st.session_state["transcript_text"] = ""

st.sidebar.title("Meeting Action Item Extractor")

st.sidebar.markdown("### Navigation")

page = st.sidebar.radio("Go to",["Extract Tasks","Evaluation"])

if page == "Extract Tasks":

    st.title("Turn conversation into follow-up work")
    st.subheader("Paste a meeting transcript to begin.")
    st.markdown("###### Don't have a transcript to test?")
    st.write("You can paste your own transcript or use one of the sample transcripts below.")
    sample_names = list(sample_transcripts.keys())
    col1, col2 = st.columns([3, 1])

    with col1:
        selected_sample = st.selectbox("Choose a sample transcript:",["None"] + sample_names,key="sample_selector")

    with col2:
        st.write("")
        use_sample = st.button("Use Sample",disabled=(selected_sample == "None"))

    if use_sample:

        st.session_state["transcript_text"] = (sample_transcripts[selected_sample])
        st.rerun()

    transcript = st.text_area("Your Transcript:",key="transcript_text",height=250)

    if st.button("Go",type="primary"):

        if not transcript.strip():
            st.warning("Please enter a meeting transcript first.")

        else:

            with st.spinner("Cleaning transcript..."):
                cleaned_transcript = (clean_transcripts(transcript))

            if (cleaned_transcript== transcript.strip()):
                st.success("Transcript is already clean.")

            else:
                st.success("Transcript cleaned successfully.")

            with st.expander("View cleaned transcript"):
                st.text(cleaned_transcript)

            with st.spinner("Extracting action items...\n\n""Hang on, it may take a little while..."):

                messages = [
                    SystemMessage(extraction_system_prompt),
                    HumanMessage(cleaned_transcript)
                    ]

                response2 = extraction_model.invoke(messages)

            st.success("Action items extracted successfully!")

            validation_issues = (validate_action_items(response2))

            if validation_issues:
                with st.expander("Validation checks"):
                    for issue in validation_issues:
                        st.warning(issue)

            else:
                st.success("Rule-based validation passed.")

            with st.spinner("Verifying and refining action items...\n\n""Hang on, it may take a little while..."):

                validation_input = f"""
ORIGINAL MEETING TRANSCRIPT:

{cleaned_transcript}


EXTRACTED ACTION ITEMS:

{response2.model_dump_json(indent=2)}


RULE-BASED VALIDATION FINDINGS:

{validation_issues}
"""


                validation_messages = [
                    SystemMessage(verification_system_prompt),
                    HumanMessage(validation_input)
                    ]


                final_response = (review_model.invoke(validation_messages))


            st.success("Action items verified successfully!")

            data = [
                {
                    "Task": task.task,
                    "Owner": task.owner,
                    "Deadline": task.deadline,
                    "Status": task.status,
                    "Confidence": task.confidence
                }
                for task in final_response.tasks
            ]

            df = pd.DataFrame(data)

            st.subheader("Final Action Items")
            st.dataframe(df,width="stretch")



elif page == "Evaluation":

    st.title("Model Evaluation")

    st.write("Evaluate the complete action-item extraction pipeline using manually annotated meeting transcripts.")
    st.info(f"Official evaluation dataset contains "f"{len(evaluation_data_list)} test transcripts.")

    if st.button("Run Evaluation",type="primary"):
        all_results = []
        progress_bar = st.progress(0)
        status_text = st.empty()

        for index, test_case in enumerate(evaluation_data_list):

            status_text.write(
                f"Running evaluation "
                f"{index + 1}/{len(evaluation_data_list)}: "
                f"{test_case['name']}"
            )

            transcript = test_case["transcript"]
            ground_truth = test_case["ground_truth"]

            cleaned_transcript = (clean_transcripts(transcript))

            messages = [
                SystemMessage(extraction_system_prompt),
                HumanMessage(cleaned_transcript)
            ]

            response2 = extraction_model.invoke(messages)

            validation_issues = (validate_action_items(response2))

            validation_input = f"""
ORIGINAL MEETING TRANSCRIPT:

{cleaned_transcript}


EXTRACTED ACTION ITEMS:

{response2.model_dump_json(indent=2)}


RULE-BASED VALIDATION FINDINGS:

{validation_issues}
"""


            validation_messages = [
                SystemMessage(verification_system_prompt),
                HumanMessage(validation_input)
            ]

            final_response = (review_model.invoke(validation_messages))
            result = evaluate_action_items(final_response,ground_truth)

            result["name"] = (test_case["name"])
            result["predicted_response"] = (final_response)
            result["ground_truth"] = (ground_truth)
            all_results.append(result)

            progress_bar.progress((index + 1)/ len(evaluation_data_list))

        status_text.success("Evaluation completed!")

        st.session_state["evaluation_results"] = all_results

    if "evaluation_results" in st.session_state:
        results = st.session_state["evaluation_results"]
        st.subheader("Overall Evaluation")

        metrics = ["precision","recall","f1_score","owner_accuracy","deadline_accuracy","status_accuracy"]
        averages = {}
        for metric in metrics:
            averages[metric] = (sum(result[metric]for result in results)/ len(results))

        col1, col2, col3 = st.columns(3)

        col1.metric("Precision",f"{averages['precision']:.2%}")
        col2.metric("Recall",f"{averages['recall']:.2%}")
        col3.metric("F1 Score",f"{averages['f1_score']:.2%}")

        col4, col5, col6 = st.columns(3)

        col4.metric("Owner Accuracy",f"{averages['owner_accuracy']:.2%}")
        col5.metric("Deadline Accuracy",f"{averages['deadline_accuracy']:.2%}")
        col6.metric("Status Accuracy",f"{averages['status_accuracy']:.2%}")

        st.subheader("Individual Test Results")

        for index, result in enumerate(results,start=1):

            with st.expander(f"Test Case {index}: "f"{result['name']}"):
                c1, c2, c3 = st.columns(3)

                c1.metric("Precision",f"{result['precision']:.2%}")
                c2.metric("Recall",f"{result['recall']:.2%}")
                c3.metric("F1 Score",f"{result['f1_score']:.2%}")

                c4, c5, c6 = st.columns(3)

                c4.metric("Owner Accuracy",f"{result['owner_accuracy']:.2%}")
                c5.metric("Deadline Accuracy",f"{result['deadline_accuracy']:.2%}")
                c6.metric("Status Accuracy",f"{result['status_accuracy']:.2%}")

                st.write(f"Ground Truth Tasks: "f"{result['total_ground_truth']}")
                st.write(f"Predicted Tasks: "f"{result['total_predicted']}")
                st.write(f"True Positives: "f"{result['true_positive']}")
                st.write(f"False Positives:"f"{result['false_positive']}")
                st.write(f"False Negatives:"f"{result['false_negative']}")

                st.markdown("##### Ground Truth")

                gt_df = pd.DataFrame(result["ground_truth"])
                st.dataframe(gt_df,width="stretch")

                st.markdown("##### Model Output")

                predicted_data = [
                    {
                        "Task": task.task,
                        "Owner": task.owner,
                        "Deadline": task.deadline,
                        "Status": task.status,
                        "Confidence": task.confidence
                    }
                    for task in result["predicted_response"].tasks
                ]

                predicted_df = pd.DataFrame(predicted_data)

                st.dataframe(predicted_df,width="stretch")

if page == "Evaluation":
    st.subheader("Run Your Own Evaluation")
    st.write("You can also evaluate the model using your own meeting transcript and manually prepared ground truth.")

    custom_transcript = st.text_area("Your Meeting Transcript:",key="custom_transcript",height=200)
    custom_ground_truth_text = st.text_area(
        "Ground Truth Action Items:",
        key="custom_ground_truth",
        height=200,
        placeholder=(
            "Enter one task per line:\n\n"
            "Task | Owner | Deadline | Status\n\n"
            "Example:\n"
            "Update pricing page | Sarah | Friday | pending\n"
            "Prepare presentation | Bob | Monday | pending\n"
            "Review report | Alice | None | pending"
        ))

    if st.button("Evaluate My Transcript"):
        if not custom_transcript.strip():
            st.warning("Please enter a meeting transcript.")

        elif not custom_ground_truth_text.strip():
            st.warning("Please enter the ground truth.")

        else:
            custom_ground_truth = []
            valid_ground_truth = True

            for line in (custom_ground_truth_text.splitlines()):
                line = line.strip()
                if not line:
                    continue
                parts = [part.strip()for part in line.split("|")]

                if len(parts) != 4:
                    st.error("Each ground truth line must have exactly 4 fields:\n\n Task | Owner | Deadline | Status")
                    valid_ground_truth = False
                    break

                task, owner, deadline, status = (parts)

                if deadline.lower() == "none":
                    deadline = None


                custom_ground_truth.append(
                    {
                        "task": task,
                        "owner": owner,
                        "deadline": deadline,
                        "status": status
                    }
                )

            if valid_ground_truth:

                with st.spinner("Running your evaluation...\n\n Hang on, it may take a little while..."):
                    cleaned = clean_transcripts(custom_transcript)
                    messages = [
                        SystemMessage(extraction_system_prompt),
                        HumanMessage(cleaned)
                    ]
                    extracted = extraction_model.invoke(messages)
                    issues = (validate_action_items(extracted))
                    validation_input = f"""
ORIGINAL MEETING TRANSCRIPT:

{cleaned}


EXTRACTED ACTION ITEMS:

{extracted.model_dump_json(indent=2)}


RULE-BASED VALIDATION FINDINGS:

{issues}
"""


                    validation_messages = [
                        SystemMessage(verification_system_prompt),
                        HumanMessage(validation_input)
                    ]

                    final_custom = (review_model.invoke(validation_messages))
                    custom_result = (evaluate_action_items(final_custom,custom_ground_truth))

                st.success("Custom evaluation completed!")
                st.subheader("Your Evaluation Results")

                c1, c2, c3 = st.columns(3)

                c1.metric("Precision",f"{custom_result['precision']:.2%}")
                c2.metric("Recall",f"{custom_result['recall']:.2%}")
                c3.metric("F1 Score",f"{custom_result['f1_score']:.2%}")

                c4, c5, c6 = st.columns(3)

                c4.metric("Owner Accuracy",f"{custom_result['owner_accuracy']:.2%}")
                c5.metric("Deadline Accuracy",f"{custom_result['deadline_accuracy']:.2%}")
                c6.metric("Status Accuracy",f"{custom_result['status_accuracy']:.2%}")

                st.write(f"Ground Truth Tasks: {custom_result['total_ground_truth']}")
                st.write(f"Predicted Tasks: {custom_result['total_predicted']}")
                st.write(f"True Positives: {custom_result['true_positive']}")
                st.write(f"False Positives: {custom_result['false_positive']}")
                st.write(f"False Negatives: {custom_result['false_negative']}")
                st.markdown("##### Model Output")

                custom_predicted_data = [
                    {
                        "Task": task.task,
                        "Owner": task.owner,
                        "Deadline": task.deadline,
                        "Status": task.status,
                        "Confidence": task.confidence
                    }
                    for task in final_custom.tasks
                ]

                custom_df = pd.DataFrame(custom_predicted_data)
                st.dataframe(custom_df,width="stretch")