import streamlit as st

st.set_page_config(page_title="Blood Donation System", layout="centered")

st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
    }
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stButton>button {
        width: 100%;
        background-color: #5a67d8;
        color: white;
        font-size: 18px;
        font-weight: bold;
        padding: 15px;
        border-radius: 12px;
        border: none;
        margin-top: 30px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton>button:hover {
        background-color: #4c51bf;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    h1 {
        color: white;
        text-align: center;
        font-size: 48px;
        margin-bottom: 10px;
        font-weight: bold;
    }
    h3 {
        color: #e0e7ff;
        text-align: center;
        font-weight: 300;
        margin-top: 0px;
        margin-bottom: 15px;
        font-size: 20px;
    }
    .donor-reg-title {
        color: white;
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        margin-top: 30px;
        margin-bottom: 30px;
    }
    .stTextInput>div>div>input, .stSelectbox>div>div>select {
        border-radius: 10px;
        border: 2px solid #4c51bf;
        padding: 12px;
        background-color: #2d3748;
        color: white;
        font-size: 16px;
    }
    .stTextInput>div>div>input::placeholder {
        color: #a0aec0;
    }
    .stRadio>div {
        background-color: transparent;
    }
    .stRadio>div>label>div {
        color: white;
        font-weight: 500;
    }
    label {
        color: white !important;
        font-weight: 500;
        font-size: 16px;
    }
    .stSelectbox>div>label {
        color: white !important;
    }
    .stTextInput>div>label {
        color: white !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #2d3748;
        border: 2px solid #4c51bf;
        border-radius: 10px;
    }
    .login-button {
        background-color: rgba(255, 255, 255, 0.2);
        color: white;
        padding: 10px 30px;
        border-radius: 25px;
        border: 2px solid white;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        float: right;
        margin-top: -60px;
        margin-right: 20px;
    }
    .login-button:hover {
        background-color: rgba(255, 255, 255, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <div style='text-align: right; padding: 20px;'>
        <button class='login-button'>LOGIN</button>
    </div>
    """, unsafe_allow_html=True)

st.title("🩸 Blood Donation System")
st.markdown("<h3>Save Lives, Become a Donor Today</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    st.markdown("<div class='donor-reg-title'>Donor Registration</div>", unsafe_allow_html=True)
    
    name = st.text_input("Full Name", placeholder="Enter your full name")
    
    col_gender, col_blood = st.columns(2)
    
    with col_gender:
        gender = st.selectbox("Gender", options=["Select Gender", "Male", "Female", "Other"])
    
    with col_blood:
        blood_group = st.selectbox(
            "Blood Group",
            options=["Select Blood Group", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
        )
    
    phone = st.text_input("Phone Number", placeholder="Enter your phone number")
    
    email = st.text_input("Email Address", placeholder="Enter your email address")
    
    if st.button("Register as Donor"):
        st.success("Registration form submitted successfully!")
        st.balloons()

st.markdown("<br><br>", unsafe_allow_html=True)
