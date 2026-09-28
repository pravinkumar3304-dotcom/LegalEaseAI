import streamlit as st
import requests

st.set_page_config(
    page_title="LegalEase AI",
    page_icon="⚖️"
)

st.title("⚖️ LegalEase AI")
st.write("AI-powered Legal Document Generator")

st.subheader("Generate Legal Document")

document_type = st.selectbox(
    "Document Type",
    [
        "Rental Agreement",
        "Employment Agreement",
        "Non-Disclosure Agreement",
        "Legal Notice"
    ]
)

jurisdiction = st.text_input(
    "Jurisdiction",
    "Tamil Nadu, India"
)

parties = st.text_input(
    "Parties",
    "Landlord and Tenant"
)

terms = st.text_area(
    "Terms",
    "Monthly rent is Rs. 10000. Security deposit is Rs. 30000. Agreement duration is 11 months."
)

effective_date = st.date_input(
    "Effective Date"
)

language = st.selectbox(
    "Language",
    ["English", "Tamil"]
)

if st.button("Generate Document"):

    data = {
        "document_type": document_type,
        "jurisdiction": jurisdiction,
        "parties": parties,
        "terms": terms,
        "effective_date": str(effective_date),
        "language": language
    }

    try:
        response = requests.post(
            "http://127.0.0.1:8000/generate",
            json=data
        )

        if response.status_code == 200:
            result = response.json()

            st.success("Document generated successfully!")

            st.json(result)

        else:
            st.error(
                f"API Error: {response.status_code}"
            )

            st.write(response.text)

    except Exception as error:
        st.error(f"Connection failed: {error}")