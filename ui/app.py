import streamlit as st
import requests
import time

# Configuration
API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Gen-Bio Insight",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for scientific look
st.markdown("""
<style>
    .reportview-container {
        background: #f8f9fa;
    }
    h1 {
        color: #2c3e50;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 10px;
        border-radius: 5px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/dna-helix.png", width=80)
    st.title("Research Hub")
    st.markdown("---")
    
    st.subheader("🧪 Drug Discovery")
    target_protein = st.text_input("Target Protein (e.g., EGFR)", "EGFR")
    smiles_input = st.text_area("SMILES String", "CC(=O)OC1=CC=CC=C1C(=O)O") # Aspirin
    
    if st.button("Predict Interaction"):
        with st.spinner("Running Molecular Simulation..."):
            try:
                response = requests.post(f"{API_URL}/analyze-molecule", json={"smiles": smiles_input, "target_protein": target_protein})
                if response.status_code == 200:
                    st.session_state.molecule_data = response.json()
                    st.success("Analysis Complete!")
                else:
                    st.error("Prediction Failed.")
            except Exception as e:
                st.error(f"Connection Error: {e}")

    st.markdown("---")
    st.info("💡 **Tip:** Use canonical SMILES for best results.")

# Main Interface
st.title("🧬 Gen-Bio Insight Platform")
st.markdown("### Accelerating Drug Discovery with Generative AI")

tab1, tab2 = st.tabs(["💊 Molecule Analyzer", "📚 Literature RAG"])

with tab1:
    if "molecule_data" in st.session_state:
        data = st.session_state.molecule_data
        mol_props = data["molecule"]
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Predicted Affinity (pKd)", f"{data['predicted_affinity_pKd']}", "+0.4")
        col2.metric("Molecular Weight", f"{mol_props['molecular_weight']} Da")
        col3.metric("LogP (Lipophilicity)", f"{mol_props['logP']}")
        col4.metric("Lipinski Rule of 5", "Pass" if mol_props['lipinski_compliant'] else "Fail")
        
        st.subheader("3D Structure Visualization")
        # Simulate 3D viewer with an image for now (real implementation uses stmol)
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Aspirin-3D-balls.png/320px-Aspirin-3D-balls.png", caption="3D Conformation (Simulated for Aspirin)", width=300)
        
        with st.expander("Detailed Properties"):
            st.json(mol_props)
    else:
        st.info("Enter a SMILES string in the sidebar to begin analysis.")

with tab2:
    st.subheader("Biomedical Literature Search")
    query = st.text_input("Search PubMed / BioRxiv", placeholder="Enter disease, target, or mechanism...")
    
    if query:
        with st.spinner("Searching Knowledge Graph..."):
            try:
                res = requests.post(f"{API_URL}/search-literature", json={"query": query})
                if res.status_code == 200:
                    papers = res.json()["papers"]
                    for paper in papers:
                        with st.container():
                            st.markdown(f"### 📄 {paper['title']}")
                            st.caption(f"**Authors:** {paper['authors']} | **Year:** {paper['year']}")
                            st.write(paper['summary'])
                            st.markdown(f"[Read Full Paper via DOI](https://doi.org/{paper['doi']})")
                            st.divider()
            except Exception as e:
                st.error(f"Search Service Unavailable: {e}")