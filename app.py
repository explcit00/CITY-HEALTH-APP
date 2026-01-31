# These libraries are essential to how the program runs and how users interact with it.
# Streamlit makes the app interactive and usable in a web browser, while pandas handles 
# data organization and processing to ensure accurate results.base64 enables files and images 
# to be embedded or downloaded within the app. Together, they make the program efficient, reliable, and user-friendly.

import streamlit as st
import pandas as pd
import io
import re
import base64


# --- Barangay Reference Lists and Mapping
# --- This section defines the official barangay list of Cagayan de Oro and maps smaller areas (sitios/subdivisions) to their correct mother barangay.


CDO_BARANGAYS = [
    "AGUSAN", "BAIKINGON", "BALUBAL", "BALULANG", "BAYABAS", "BAYANGA", "BESIGAN", 
    "BONBON", "BUGO", "BUHUAWEN", "BULUA", "CAMAMAN-AN", "CANITOAN", "CARMEN", 
    "CONSOLACION", "CUGMAN", "DANSOLIHON", "F.S. CATANICO", "GUSA", "INDAHAG", 
    "IPONAN", "KAUSWAGAN", "LAPASAN", "LUMBAMBIA", "LUMBIA", "MACABALAN", 
    "MACASANDIG", "MAGSAYSAY", "MAMBUAYA", "NAZARETH", "PAGALUNGAN", "PAGATPAT", 
    "PATAG", "PIGSAG-AN", "PUERTO", "PUNTOD", "SAN SIMON", "TABLON", "TAGLIMAO", 
    "TAGPANGI", "TIGNAPOLOAN", "TUBURAN", "TUMPAGON"
]
for i in range(1, 41):
    CDO_BARANGAYS.append(f"BARANGAY {i}")

SUB_BRGY_MAP = {
    "CALAANAN": "CANITOAN",
    "PASIL": "KAUSWAGAN",
    "AGORA": "LAPASAN",
    "MACANHAN": "CARMEN",
    "ORO HABITAT": "CANITOAN"
}


# --- Address Standardization Function
# --- This function checks the Address and Specific Address columns, searches for a matching barangay, and standardizes the result.


def process_strict_address(row):
    addr_val = str(row.get('ADDRESS', '')).upper().strip()
    spec_val = str(row.get('SPECIFIC ADDRESS', '')).upper().strip()
    if addr_val in ["NAN", "NONE"]: addr_val = ""
    if spec_val in ["NAN", "NONE"]: spec_val = ""
    full_text = f"{addr_val} {spec_val}".strip()
    found_brgy = None
    for sitio, parent_brgy in SUB_BRGY_MAP.items():
        if re.search(r'\b' + re.escape(sitio) + r'\b', full_text):
            found_brgy = parent_brgy
            break
    if not found_brgy:
        for brgy in CDO_BARANGAYS:
            if re.search(r'\b' + re.escape(brgy) + r'\b', full_text):
                found_brgy = brgy
                break
    if not found_brgy:
        return "TRANSIENT" if full_text != "" else "MISSING"
    return found_brgy


# --- Streamlit Page Configuration
st.set_page_config(page_title="CHO Records Standardizer", layout="wide")


# --- Image Encoding Function
# --- This converts images into Base64 format so they can be displayed in Streamlit without separate hosting.


def get_image_base64(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return ""

# 1. Encode the background image (CITY-HEALTH-OFFICE-DOCTORS.png)
def get_image_base64(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return ""

bg_img_b64 = get_image_base64("CITY-HEALTH-OFFICE-DOCTORS.png")
img_b64 = get_image_base64("images.png") # Your logo file



# --- Custom CSS Styling and Header Design
# --- This section styles the app background image, centered container, header bar, fonts, table colors, and buttons.

st.markdown(f"""
    <style>
    /* 1. Background image for the app - Updated for movement/zoom */
    [data-testid="stApp"] {{
        background-image: url("data:image/jpeg;base64,{bg_img_b64}");
        
        /* 'cover' ensures the image stretches to fill the space without gaps */
        background-size: cover;
        
        /* 'center' ensures the zoom originates from the middle of the image */
        background-position: center center;
        
        /* 'fixed' keeps the image in place while content scrolls over it */
        background-attachment: fixed;
        
        background-repeat: no-repeat;
    }}

    /* Hide default Streamlit header */
    [data-testid="stHeader"] {{
        visibility: hidden;
    }}

    /* 2. Main container (Centered) */
    [data-testid="stAppViewBlockContainer"] {{
        width: 95%; /* Ensures it doesn't hit screen edges when zoomed */
        max-width: 850px;
        margin-left: auto;
        margin-right: auto;
        padding-top: 12rem;
        padding-bottom: 5rem;
        
        /* Box background */
        background-color: rgba(255, 255, 255, 0.9); 
        padding-left: 40px;
        padding-right: 40px;
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
        margin-top: 50px;
        margin-bottom: 50px;
        
        color: black !important;
    }}

    /* Target all headers, labels, and standard text to be BLACK */
    h1, h2, h3, p, label, .stMarkdown, [data-testid="stMarkdownContainer"] p {{
        color: black !important;
    }}

    /* 3. Top corner header styling */
    .top-header {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 70px;
        background-color: white;
        display: flex;
        align-items: center;
        padding: 0 40px;
        border-bottom: 3px solid #87b97b;
        z-index: 9999;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }}

    .logo-img {{
        height: 45px;
        margin-right: 20px;
    }}

    .header-label {{
        font-weight: bold;
        color: black !important;
        font-family: 'Segoe UI', sans-serif;
        font-size: 1.2rem;
    }}

    .main-title {{ 
        font-size: 28px; 
        font-weight: bold; 
        color: black !important; 
        text-align: center; 
        margin-bottom: 30px; 
    }}
    
    .stFileUploader {{
        text-align: center;
        color: black !important;
    }}

    [data-testid="stFileUploadDropzone"] div {{
        color: black !important;
    }}

    /* Table styling */
    th {{
        background-color: #1E3A8A !important;
        color: white !important; 
        font-weight: bold !important;
        text-align: center !important;
    }}
    
    td {{
        color: black !important;
    }}
    
    /* Button styling */
    .stButton>button {{ 
        background-color: #1E3A8A; 
        color: white !important; 
        border-radius: 10px; 
        font-weight: bold; 
    }}
    </style>

    <div class="top-header">
        <img src="data:image/png;base64,{img_b64}" class="logo-img">
        <div class="header-label">City Health Office | Records Standardizer</div>
    </div>
    """, unsafe_allow_html=True)



# --- File Upload and Data Cleaning Logic
# --- Handles file upload, cleans the data, standardizes fields, removes unnecessary columns, and prepares the final dataset.


uploaded_file = st.file_uploader("Upload the raw CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, encoding='latin1')
        else:
            df = pd.read_excel(uploaded_file)

        df.columns = [re.sub(' +', ' ', str(c).strip().upper()) for c in df.columns]

        if 'ADDRESS' in df.columns:
            if 'SPECIFIC ADDRESS' not in df.columns:
                df['SPECIFIC ADDRESS'] = ""
            df['ADDRESS'] = df.apply(process_strict_address, axis=1)

        if 'ATTENDANT' in df.columns:
            df['ATTENDANT'] = df['ATTENDANT'].astype(str).str.upper().replace({
                'MIDWIFE': 'RHM',
                'PHYSICIAN': 'MD'
            })

        cols_to_drop = ["NAME", "MOTHER'S NAME", "SPECIFIC ADDRESS"]
        unnamed_cols = [col for col in df.columns if "UNNAMED" in col]
        cols_to_drop.extend(unnamed_cols)
        
        existing_drops = [c for c in cols_to_drop if c in df.columns]
        df_final = df.drop(columns=existing_drops)

        st.success("Standards Applied: RHM/MD updated, Names removed, and Columns segregated.")
        
        st.markdown("### Preview of Cleaned Data")
        st.dataframe(df_final.head(15), use_container_width=True)

        import io

        # 1. Create a buffer to hold the excel data
        buffer = io.BytesIO()

        # 2. Write the dataframe to the buffer using the 'xlsxwriter' or 'openpyxl' engine
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df_final.to_excel(writer, index=False, sheet_name='Birth Records')

        # 3. Seek to the beginning of the buffer so Streamlit can read it
        download_data = buffer.getvalue()

        # 4. Update the download button
        st.download_button(
            label="DOWNLOAD FINAL ORGANIZED FILE",
            data=download_data,
            file_name="OFFICIAL_CHO_BIRTH_RECORDS.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
            st.error(f"Error: {e}")