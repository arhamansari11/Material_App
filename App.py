import streamlit as st
from mp_api.client import MPRester
from pymatgen.core import Composition

# Streamlit app setting
st.set_page_config(page_title="🔬 Material Property Explorer", layout="centered")
st.title("🔬 Material Property Explorer")
st.markdown("Enter a material formula or symbol to fetch basic properties from the Materials Project database.")

# Input fiel
material = st.text_input("Material formula (e.g., Li, Mg, CrTe2):")

# API Key
API_KEY = "pvoS51pKX4Yy80JlJL4SnnfkoAuULzsn"

if material:
    try:
        comp = Composition(material)
        with MPRester(API_KEY) as mpr:
            results = mpr.summary.search(formula=material, num_chunks=1)

        if results:
            summary = results[0]
            st.subheader(f"🔍 Properties for: {summary.formula_pretty}")
            st.markdown(f"**Material ID:** `{summary.material_id}`")
            st.markdown(f"**Band Gap:** `{summary.band_gap} eV`")
            st.markdown(f"**Density:** `{summary.density:.2f} g/cm³`")
            st.markdown(f"**Energy Above Hull:** `{summary.energy_above_hull:.3f} eV/atom`")
            st.markdown(f"**Formation Energy per Atom:** `{summary.formation_energy_per_atom:.3f} eV`")
            st.markdown(f"**Volume:** `{summary.volume:.2f} Å³`")
            st.markdown(f"**Number of Sites:** `{summary.nsites}`")
            st.markdown(f"**Is Metal:** `{summary.is_metal}`")
            st.markdown(f"**Is Theoretical:** `{summary.theoretical}`")

            # Extract symmetry info safely     
            try:
                st.markdown(f"**Crystal System:** `{summary.symmetry.crystal_system}`")
                st.markdown(f"**Space Group Symbol:** `{summary.symmetry.symbol}`")
                st.markdown(f"**Space Group Number:** `{summary.symmetry.number}`")
            except Exception as symm_error:
                st.warning(f"ℹ️ Symmetry data not available: {symm_error}")

        else:
            st.warning("⚠️ No results found for the entered formula.")
    except Exception as e:
        st.error(f"❌ Error fetching data: {e}")
