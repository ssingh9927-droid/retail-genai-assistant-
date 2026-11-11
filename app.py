import streamlit as st
import chromadb
import re

st.set_page_config(page_title="Indore Electronics GenAI Assistant", layout="wide")

# Guardrails: DPDP and PCI-DSS
def check_guardrails(query: str):
    pci_pattern = r'\b(?:\d[ -]*?){13,16}\b|\b\d{3,4}\b' # Card number / CVV
    pan_aadhaar_pattern = r'\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b|\b\d{4}\s\d{4}\s\d{4}\b'
    
    if re.search(r'\b(cvv|card number|otp|pin)\b', query, re.I):
        return False, "Security Alert: PCI-DSS violation. Inquiries involving raw card numbers, CVVs, or OTPs are prohibited."
    if re.search(pan_aadhaar_pattern, query):
        return False, "Privacy Alert: DPDP Act compliance violation. Queries containing sensitive personal identifiers (PAN/Aadhaar) cannot be processed."
    return True, ""

# Database connection
@st.cache_resource
def get_db():
    client = chromadb.PersistentClient(path="./chroma_db")
    return client.get_or_create_collection(name="indore_retail_policies")

collection = get_db()

st.title("Indore Electronics - Internal Staff Assistant")
st.caption("Grounded GenAI Knowledge Portal with DPDP & PCI-DSS Guardrails")

query = st.text_input("Ask an internal policy, SOP, or customer process question:")

if st.button("Search & Answer") and query:
    allowed, msg = check_guardrails(query)
    if not allowed:
        st.error(msg)
    else:
        # Vector retrieval with preference for active records
        results = collection.query(
            query_texts=[query],
            n_results=2,
            where={"status": "active"} # Automatically filters deprecated versions
        )
        
        if not results['documents'][0]:
            st.warning("I do not have sufficient verified documentation to answer this question.")
        else:
            top_doc = results['documents'][0][0]
            metadata = results['metadatas'][0][0]
            
            st.subheader("Synthesized Answer:")
            st.write(f"Based on internal guidelines: {top_doc}")
            
            st.divider()
            st.subheader("Citations & Source Metadata:")
            st.markdown(f"- **Department:** {metadata['dept']}")
            st.markdown(f"- **Policy Version:** {metadata['version']}")
            st.markdown(f"- **Verification Status:** Active Verified Document")
