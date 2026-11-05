
import streamlit as st
from groq import Groq
from theme import apply_light_theme

st.set_page_config(
    page_title="IncomeAI Assistant",
    page_icon="💬",
    layout="wide"
)

apply_light_theme()

st.title("💬 IncomeAI Assistant")
st.caption(
    "Ask questions about your Employee Income Category "
    "Predictor, Python, machine learning, or other topics."
)

# Load Groq API key
try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    api_key = None

if not api_key:
    st.error(
        "Groq API key not found. Add GROQ_API_KEY "
        "to .streamlit/secrets.toml."
    )
    st.stop()

# Create Groq client
client = Groq(api_key=api_key)

SYSTEM_INSTRUCTION = """
You are IncomeAI, a helpful AI assistant in a student project
called Employee Income Category Predictor.

Explain concepts clearly in beginner-friendly language suitable
for a fifth-semester student.

The project uses the UCI Adult Census Income dataset to classify
historical census records into income categories such as <=50K
and >50K.

Candidate algorithms include Logistic Regression, Decision Tree,
and Linear SVM.

Never invent model scores or claim a model is best without actual
evaluation results.

Help with Python, Streamlit, preprocessing, visualisations,
model evaluation, project workflow, presentations and reports.

Explain that census income categories do not guarantee a person's
actual salary. Discuss dataset limitations and fairness when relevant.

Answer the user's actual question directly. If unsure, say so.
"""

if "incomeai_history" not in st.session_state:
    st.session_state.incomeai_history = []

# Show previous messages
for message in st.session_state.incomeai_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
question = st.chat_input("Type your question here...")

if question:
    with st.chat_message("user"):
        st.markdown(question)

    # Add current question to conversation history
    st.session_state.incomeai_history.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("assistant"):
        with st.spinner("IncomeAI is thinking..."):
            try:
                messages = [
                    {
                        "role": "system",
                        "content": SYSTEM_INSTRUCTION
                    }
                ]

                messages.extend(
                    st.session_state.incomeai_history
                )

                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=messages,
                    temperature=0.5,
                    max_tokens=1000
                )

                answer = response.choices[0].message.content

                if not answer:
                    answer = "I couldn't generate an answer. Please try again."

                st.markdown(answer)

                st.session_state.incomeai_history.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as error:
                error_text = str(error)

                if "429" in error_text or "rate_limit" in error_text.lower():
                    st.warning(
                        "The free AI usage limit may have been reached. "
                        "Please wait or check your Groq usage limits."
                    )
                elif any(code in error_text for code in ["500", "502", "503", "504"]):
                    st.warning(
                        "The AI service is temporarily unavailable. "
                        "Please try again shortly."
                    )
                else:
                    st.error(
                        "IncomeAI couldn't answer this question. "
                        "Check your API key, internet connection, "
                        "and model access."
                    )
                    st.caption(f"Technical details: {error}")

# Clear chat
if st.button("Clear conversation"):
    st.session_state.incomeai_history = []
    st.rerun()
