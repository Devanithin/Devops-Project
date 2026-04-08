import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from geopy.distance import geodesic
import folium
from streamlit_folium import st_folium

# Configuration
BASE_URL = "http://127.0.0.1:8000"

# Page configuration
st.set_page_config(
    page_title="HemoLink - Blood Donor Management System",
    page_icon="🩸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #e74c3c;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
    }
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    .success-message {
        color: #27ae60;
        font-weight: bold;
        padding: 0.5rem;
        background-color: #d4edda;
        border-radius: 0.25rem;
        border: 1px solid #c3e6cb;
    }
    .error-message {
        color: #e74c3c;
        font-weight: bold;
        padding: 0.5rem;
        background-color: #f8d7da;
        border-radius: 0.25rem;
        border: 1px solid #f5c6cb;
    }
    .warning-message {
        color: #f39c12;
        font-weight: bold;
        padding: 0.5rem;
        background-color: #fff3cd;
        border-radius: 0.25rem;
        border: 1px solid #ffeaa7;
    }
</style>
""", unsafe_allow_html=True)

# API Client Functions with robust error handling
def safe_api_call(method: str, endpoint: str, data: Dict = None, params: Dict = None) -> Tuple[bool, Dict]:
    """Safe API call with comprehensive error handling"""
    try:
        url = f"{BASE_URL}{endpoint}"
        
        if method.upper() == "GET":
            response = requests.get(url, params=params, timeout=10)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, timeout=10)
        elif method.upper() == "PUT":
            response = requests.put(url, json=data, timeout=10)
        else:
            return False, {"error": "Unsupported method"}
        
        if response.status_code == 200:
            return True, response.json()
        elif response.status_code == 404:
            return False, {"error": "Resource not found"}
        elif response.status_code == 500:
            return False, {"error": "Server error"}
        else:
            return False, {"error": f"HTTP {response.status_code}: {response.text}"}
            
    except requests.exceptions.Timeout:
        return False, {"error": "Request timeout"}
    except requests.exceptions.ConnectionError:
        return False, {"error": "Connection failed - check if backend is running"}
    except requests.exceptions.RequestException as e:
        return False, {"error": f"Request failed: {str(e)}"}
    except Exception as e:
        return False, {"error": f"Unexpected error: {str(e)}"}

@st.cache_data(ttl=300)
def get_all_donors() -> List[Dict]:
    """Fetch all donors from the backend"""
    success, result = safe_api_call("GET", "/donors/all")
    if success and isinstance(result, list):
        return result
    return []

@st.cache_data(ttl=300)
def get_all_hospitals() -> List[Dict]:
    """Fetch all hospitals from the backend"""
    success, result = safe_api_call("GET", "/hospitals/all")
    if success and isinstance(result, list):
        return result
    return []

@st.cache_data(ttl=300)
def get_all_requests() -> List[Dict]:
    """Fetch all blood requests from the backend"""
    success, result = safe_api_call("GET", "/requests/all")
    if success and isinstance(result, list):
        return result
    return []

def get_donor_by_id(donor_id: str) -> Optional[Dict]:
    """Get specific donor by ID"""
    success, result = safe_api_call("GET", f"/donors/{donor_id}")
    if success and isinstance(result, dict):
        return result
    return None

def get_hospital_by_id(hospital_id: str) -> Optional[Dict]:
    """Get specific hospital by ID"""
    success, result = safe_api_call("GET", f"/hospitals/{hospital_id}")
    if success and isinstance(result, dict):
        return result
    return None

def get_request_by_id(request_id: str) -> Optional[Dict]:
    """Get specific request by ID"""
    success, result = safe_api_call("GET", f"/requests/{request_id}")
    if success and isinstance(result, dict):
        return result
    return None

def get_request_notifications(request_id: str) -> List[Dict]:
    """Get notified donors for a specific request"""
    success, result = safe_api_call("GET", f"/requests/{request_id}/donors")
    if success and isinstance(result, list):
        return result
    return []

def register_donor(donor_data: Dict) -> bool:
    """Register a new donor"""
    success, result = safe_api_call("POST", "/donors/register", donor_data)
    if success:
        st.success("✅ Donor registered successfully!")
        return True
    else:
        st.error(f"❌ Error registering donor: {result.get('error', 'Unknown error')}")
        return False

def update_donor(donor_id: str, donor_data: Dict) -> bool:
    """Update donor information"""
    success, result = safe_api_call("PUT", f"/donors/{donor_id}/update", donor_data)
    if success:
        st.success("✅ Donor updated successfully!")
        return True
    else:
        st.error(f"❌ Error updating donor: {result.get('error', 'Unknown error')}")
        return False

def register_hospital(hospital_data: Dict) -> bool:
    """Register a new hospital"""
    success, result = safe_api_call("POST", "/hospitals/register", hospital_data)
    if success:
        st.success("✅ Hospital registered successfully!")
        return True
    else:
        st.error(f"❌ Error registering hospital: {result.get('error', 'Unknown error')}")
        return False

def update_hospital_inventory(hospital_id: str, inventory_data: Dict) -> bool:
    """Update hospital blood inventory"""
    success, result = safe_api_call("POST", f"/hospitals/{hospital_id}/inventory", inventory_data)
    if success:
        st.success("✅ Inventory updated successfully!")
        return True
    else:
        st.error(f"❌ Error updating inventory: {result.get('error', 'Unknown error')}")
        return False

def create_blood_request(request_data: Dict) -> bool:
    """Create a new blood request"""
    success, result = safe_api_call("POST", "/requests/create", request_data)
    if success:
        st.success("✅ Blood request created successfully!")
        return True
    else:
        st.error(f"❌ Error creating blood request: {result.get('error', 'Unknown error')}")
        return False

def respond_to_request(request_id: str, donor_id: str, response_data: Dict) -> bool:
    """Respond to a blood request"""
    success, result = safe_api_call("POST", f"/requests/{request_id}/respond", response_data)
    if success:
        st.success("✅ Response submitted successfully!")
        return True
    else:
        st.error(f"❌ Error submitting response: {result.get('error', 'Unknown error')}")
        return False

# Utility functions
def get_nearest_hospital(acc_lat: float, acc_lon: float, hospitals: List[Dict]) -> Tuple[Optional[Dict], float]:
    """Find nearest hospital to accident location"""
    if None in (acc_lat, acc_lon):
        return None, float("inf")
    
    min_dist = float("inf")
    nearest = None
    
    for h in hospitals:
        lat = h.get("latitude")
        lon = h.get("longitude")
        
        if lat is None or lon is None:
            continue
        
        dist = geodesic((acc_lat, acc_lon), (lat, lon)).km
        
        if dist < min_dist:
            min_dist = dist
            nearest = h
    
    return nearest, min_dist

def style_requests(row):
    """Style function for request dataframe - FIXED VERSION"""
    if row.get("status") == "pending":
        return ["background-color: #ff4b4b"] * len(row)
    elif row.get("status") == "accepted":
        return ["background-color: #4CAF50"] * len(row)
    elif row.get("status") == "fulfilled":
        return ["background-color: #4CAF50"] * len(row)
    return [""] * len(row)

def format_datetime(date_str: str) -> str:
    """Format datetime string for display"""
    try:
        if not date_str:
            return "N/A"
        
        formats = ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f"]
        
        for fmt in formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.strftime("%Y-%m-%d %H:%M")
            except ValueError:
                continue
        
        return date_str
    except Exception:
        return "N/A"

# Page Functions
def show_dashboard():
    """Display professional dashboard with metrics and recent data"""
    st.markdown('<h1 class="main-header">🩸 HemoLink Dashboard</h1>', unsafe_allow_html=True)
    
    # Refresh button
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        if st.button("🔄 Refresh Data", type="primary", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    
    st.markdown("---")
    
    # Fetch data with loading
    with st.spinner("🔄 Loading dashboard data..."):
        donors = get_all_donors()
        hospitals = get_all_hospitals()
        requests = get_all_requests()
    
    # Calculate metrics
    total_donors = len(donors)
    total_hospitals = len(hospitals)
    total_requests = len(requests)
    pending_requests = len([r for r in requests if r.get('status') == 'pending'])
    
    # Display professional metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{total_donors}</div>
            <div class="metric-label">👥 Total Donors</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{total_hospitals}</div>
            <div class="metric-label">🏥 Total Hospitals</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{total_requests}</div>
            <div class="metric-label">📋 Total Requests</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{pending_requests}</div>
            <div class="metric-label">⏳ Pending Requests</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Recent data tables
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-header">👥 Recent Donors</div>', unsafe_allow_html=True)
        if donors:
            recent_donors = donors[:5]
            donor_df = pd.DataFrame(recent_donors)
            
            # Select safe columns
            display_cols = []
            if 'name' in donor_df.columns:
                display_cols.append('name')
            if 'blood_type' in donor_df.columns:
                display_cols.append('blood_type')
            if 'city' in donor_df.columns:
                display_cols.append('city')
            if 'phone' in donor_df.columns:
                display_cols.append('phone')
            
            if display_cols:
                donor_df = donor_df[display_cols]
                donor_df.columns = ['Name', 'Blood Type', 'City', 'Phone'][:len(display_cols)]
                st.dataframe(donor_df, use_container_width=True)
        else:
            st.info("ℹ️ No donors found")
    
    with col2:
        st.markdown('<div class="section-header">📋 Recent Requests</div>', unsafe_allow_html=True)
        if requests:
            recent_requests = requests[:5]
            request_df = pd.DataFrame(recent_requests)
            
            # Select safe columns
            display_cols = []
            if 'blood_type' in request_df.columns:
                display_cols.append('blood_type')
            if 'units_needed' in request_df.columns:
                display_cols.append('units_needed')
            if 'status' in request_df.columns:
                display_cols.append('status')
            if 'created_at' in request_df.columns:
                display_cols.append('created_at')
            
            if display_cols:
                request_df = request_df[display_cols]
                
                # Format created_at if present
                if 'created_at' in request_df.columns:
                    request_df['created_at'] = request_df['created_at'].apply(format_datetime)
                
                request_df.columns = ['Blood Type', 'Units Needed', 'Status', 'Created At'][:len(display_cols)]
                st.dataframe(request_df, use_container_width=True)
        else:
            st.info("ℹ️ No requests found")

def show_donors():
    """Display professional donors management page"""
    st.markdown('<h1 class="main-header">👥 Donor Management</h1>', unsafe_allow_html=True)
    
    # Tabs for different operations
    tab1, tab2, tab3 = st.tabs(["📋 All Donors", "➕ Register Donor", "✏️ Update Donor"])
    
    with tab1:
        st.markdown('<div class="section-header">📋 All Registered Donors</div>', unsafe_allow_html=True)
        
        # Filters and search
        col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
        with col1:
            blood_type_filter = st.selectbox("🩸 Filter by Blood Type", ["All", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        with col2:
            city_filter = st.text_input("🏙️ Filter by City", placeholder="Enter city name")
        with col3:
            availability_filter = st.selectbox("✅ Filter by Availability", ["All", "Available", "Not Available"])
        with col4:
            if st.button("🔄 Refresh", use_container_width=True):
                st.cache_data.clear()
                st.rerun()
        
        # Fetch and display donors
        with st.spinner("🔄 Loading donors..."):
            donors = get_all_donors()
        
        if donors:
            # Apply filters
            filtered_donors = donors.copy()
            if blood_type_filter != "All":
                filtered_donors = [d for d in filtered_donors if d.get('blood_type') == blood_type_filter]
            if city_filter:
                filtered_donors = [d for d in filtered_donors if city_filter.lower() in d.get('city', '').lower()]
            if availability_filter != "All":
                is_available = availability_filter == "Available"
                filtered_donors = [d for d in filtered_donors if d.get('availability') == is_available]
            
            if filtered_donors:
                donor_df = pd.DataFrame(filtered_donors)
                
                # Select safe columns to display
                display_columns = []
                column_mapping = {}
                
                if 'name' in donor_df.columns:
                    display_columns.append('name')
                    column_mapping['name'] = 'Name'
                if 'blood_type' in donor_df.columns:
                    display_columns.append('blood_type')
                    column_mapping['blood_type'] = 'Blood Type'
                if 'city' in donor_df.columns:
                    display_columns.append('city')
                    column_mapping['city'] = 'City'
                if 'phone' in donor_df.columns:
                    display_columns.append('phone')
                    column_mapping['phone'] = 'Phone'
                if 'email' in donor_df.columns:
                    display_columns.append('email')
                    column_mapping['email'] = 'Email'
                if 'availability' in donor_df.columns:
                    display_columns.append('availability')
                    column_mapping['availability'] = 'Available'
                
                if display_columns:
                    donor_df = donor_df[display_columns]
                    donor_df.columns = [column_mapping[col] for col in display_columns]
                    
                    # Format availability
                    if 'Available' in donor_df.columns:
                        donor_df['Available'] = donor_df['Available'].apply(lambda x: "✅ Yes" if x else "❌ No")
                    
                    st.dataframe(donor_df, use_container_width=True)
                    
                    # Show statistics
                    st.markdown("---")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Donors", len(filtered_donors))
                    with col2:
                        unique_cities = len(set(d.get('city', '') for d in filtered_donors))
                        st.metric("Unique Cities", unique_cities)
                    with col3:
                        available_count = len([d for d in filtered_donors if d.get('availability')])
                        st.metric("Available Now", available_count)
            else:
                st.info("ℹ️ No donors match the selected filters")
        else:
            st.info("ℹ️ No donors found")
    
    with tab2:
        st.markdown('<div class="section-header">➕ Register New Donor</div>', unsafe_allow_html=True)
        
        with st.form("register_donor_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("👤 Full Name *", placeholder="Enter donor's full name")
                phone = st.text_input("📞 Phone Number *", placeholder="Enter phone number")
                email = st.text_input("📧 Email Address", placeholder="Enter email address")
                blood_type = st.selectbox("🩸 Blood Type *", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
            
            with col2:
                city = st.text_input("🏙️ City *", placeholder="Enter city name")
                latitude = st.text_input("📍 Latitude", placeholder="Enter latitude coordinates")
                longitude = st.text_input("📍 Longitude", placeholder="Enter longitude coordinates")
                availability = st.selectbox("✅ Availability", ["Available", "Not Available"])
            
            submitted = st.form_submit_button("🚀 Register Donor", type="primary")
            
            if submitted:
                if name and phone and blood_type and city:
                    donor_data = {
                        "name": name.strip(),
                        "phone": phone.strip(),
                        "email": email.strip() if email else None,
                        "blood_type": blood_type,
                        "city": city.strip(),
                        "latitude": float(latitude) if latitude else None,
                        "longitude": float(longitude) if longitude else None,
                        "availability": availability == "Available"
                    }
                    
                    if register_donor(donor_data):
                        st.rerun()
                else:
                    st.error("❌ Please fill in all required fields (marked with *)")
    
    with tab3:
        st.markdown('<div class="section-header">✏️ Update Donor Information</div>', unsafe_allow_html=True)
        
        # Fetch donors for selection
        with st.spinner("🔄 Loading donors..."):
            donors = get_all_donors()
        
        if donors:
            # Create safe donor options
            donor_options = {}
            for d in donors:
                name = d.get('name', 'Unknown')
                blood_type = d.get('blood_type', 'Unknown')
                city = d.get('city', 'Unknown')
                donor_id = d.get('id', 'unknown')
                donor_options[f"{name} ({blood_type}) - {city}"] = donor_id
            
            selected_donor = st.selectbox("👤 Select Donor to Update", list(donor_options.keys()))
            
            if selected_donor:
                donor_id = donor_options[selected_donor]
                
                # Get current donor details
                current_donor = get_donor_by_id(donor_id)
                
                with st.form("update_donor_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        update_phone = st.text_input("📞 Update Phone", 
                                                    value=current_donor.get('phone', '') if current_donor else '',
                                                    placeholder="Enter new phone number")
                        update_email = st.text_input("📧 Update Email", 
                                                    value=current_donor.get('email', '') if current_donor else '',
                                                    placeholder="Enter new email address")
                    
                    with col2:
                        update_city = st.text_input("🏙️ Update City", 
                                                   value=current_donor.get('city', '') if current_donor else '',
                                                   placeholder="Enter new city")
                        update_blood_type = st.selectbox("🩸 Update Blood Type", 
                                                         ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
                                                         index=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"].index(current_donor.get('blood_type', 'A+')) if current_donor else 0)
                        update_availability = st.selectbox("✅ Update Availability", 
                                                          ["Available", "Not Available"],
                                                          index=0 if current_donor and current_donor.get('availability', True) else 1)
                    
                    update_submitted = st.form_submit_button("💾 Update Donor", type="primary")
                    
                    if update_submitted:
                        update_data = {}
                        if update_phone and update_phone != current_donor.get('phone', ''):
                            update_data['phone'] = update_phone.strip()
                        if update_email and update_email != current_donor.get('email', ''):
                            update_data['email'] = update_email.strip()
                        if update_city and update_city != current_donor.get('city', ''):
                            update_data['city'] = update_city.strip()
                        if update_blood_type != current_donor.get('blood_type', ''):
                            update_data['blood_type'] = update_blood_type
                        
                        update_data['availability'] = update_availability == "Available"
                        
                        if update_data:
                            if update_donor(donor_id, update_data):
                                st.rerun()
                        else:
                            st.warning("⚠️ No changes detected")
        else:
            st.info("ℹ️ No donors available for update")

def show_hospitals():
    """Display professional hospitals management page"""
    st.markdown('<h1 class="main-header">🏥 Hospital Management</h1>', unsafe_allow_html=True)
    
    # Tabs for different operations
    tab1, tab2, tab3 = st.tabs(["📋 All Hospitals", "➕ Register Hospital", "📦 Update Inventory"])
    
    with tab1:
        st.markdown('<div class="section-header">📋 All Registered Hospitals</div>', unsafe_allow_html=True)
        
        # Search and filter
        col1, col2 = st.columns([3, 1])
        with col1:
            search_hospital = st.text_input("🔍 Search hospitals", placeholder="Search by name or city")
        with col2:
            if st.button("🔄 Refresh", use_container_width=True):
                st.cache_data.clear()
                st.rerun()
        
        with st.spinner("🔄 Loading hospitals..."):
            hospitals = get_all_hospitals()
        
        if hospitals:
            # Apply search filter
            if search_hospital:
                search_term = search_hospital.lower()
                hospitals = [h for h in hospitals if 
                           search_term in h.get('name', '').lower() or 
                           search_term in h.get('city', '').lower()]
            
            hospital_df = pd.DataFrame(hospitals)
            
            # Select safe columns to display
            display_columns = []
            column_mapping = {}
            
            if 'name' in hospital_df.columns:
                display_columns.append('name')
                column_mapping['name'] = 'Name'
            if 'city' in hospital_df.columns:
                display_columns.append('city')
                column_mapping['city'] = 'City'
            if 'phone' in hospital_df.columns:
                display_columns.append('phone')
                column_mapping['phone'] = 'Phone'
            if 'email' in hospital_df.columns:
                display_columns.append('email')
                column_mapping['email'] = 'Email'
            if 'address' in hospital_df.columns:
                display_columns.append('address')
                column_mapping['address'] = 'Address'
            
            if display_columns:
                hospital_df = hospital_df[display_columns]
                hospital_df.columns = [column_mapping[col] for col in display_columns]
                st.dataframe(hospital_df, use_container_width=True)
                
                # Show statistics
                st.markdown("---")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Hospitals", len(hospitals))
                with col2:
                    unique_cities = len(set(h.get('city', '') for h in hospitals))
                    st.metric("Cities Covered", unique_cities)
                with col3:
                    st.metric("Avg per City", f"{len(hospitals)/max(unique_cities, 1):.1f}")
        else:
            st.info("ℹ️ No hospitals found")
    
    with tab2:
        st.markdown('<div class="section-header">➕ Register New Hospital</div>', unsafe_allow_html=True)
        
        with st.form("register_hospital_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("🏥 Hospital Name *", placeholder="Enter hospital name")
                phone = st.text_input("📞 Phone Number *", placeholder="Enter phone number")
                email = st.text_input("📧 Email Address", placeholder="Enter email address")
            
            with col2:
                city = st.text_input("🏙️ City *", placeholder="Enter city name")
                address = st.text_input("📍 Address", placeholder="Enter full address")
                latitude = st.text_input("📍 Latitude", placeholder="Enter latitude coordinates")
                longitude = st.text_input("📍 Longitude", placeholder="Enter longitude coordinates")
            
            submitted = st.form_submit_button("🚀 Register Hospital", type="primary")
            
            if submitted:
                if name and phone and city:
                    hospital_data = {
                        "name": name.strip(),
                        "phone": phone.strip(),
                        "email": email.strip() if email else None,
                        "city": city.strip(),
                        "address": address.strip() if address else None,
                        "latitude": float(latitude) if latitude else None,
                        "longitude": float(longitude) if longitude else None
                    }
                    
                    if register_hospital(hospital_data):
                        st.rerun()
                else:
                    st.error("❌ Please fill in all required fields (marked with *)")
    
    with tab3:
        st.markdown('<div class="section-header">📦 Update Blood Inventory</div>', unsafe_allow_html=True)
        
        # Fetch hospitals for selection
        with st.spinner("🔄 Loading hospitals..."):
            hospitals = get_all_hospitals()
        
        if hospitals:
            # Create safe hospital options
            hospital_options = {}
            for h in hospitals:
                name = h.get('name', 'Unknown')
                city = h.get('city', 'Unknown')
                hospital_id = h.get('id', 'unknown')
                hospital_options[f"{name} - {city}"] = hospital_id
            
            col1, col2 = st.columns([2, 1])
            with col1:
                selected_hospital = st.selectbox("🏥 Select Hospital", list(hospital_options.keys()))
            with col2:
                if st.button("🔄 Refresh Inventory", use_container_width=True):
                    st.cache_data.clear()
                    st.rerun()
            
            if selected_hospital:
                hospital_id = hospital_options[selected_hospital]
                
                # Get current hospital inventory
                current_inventory = None
                try:
                    success, result = safe_api_call("GET", f"/hospitals/{hospital_id}/inventory")
                    if success and isinstance(result, list):
                        current_inventory = result
                except Exception:
                    pass
                
                # Show current inventory if available
                if current_inventory:
                    st.subheader("📊 Current Inventory")
                    inv_df = pd.DataFrame(current_inventory)
                    if not inv_df.empty:
                        display_cols = ['blood_type', 'units_available']
                        available_cols = [col for col in display_cols if col in inv_df.columns]
                        if available_cols:
                            inv_df = inv_df[available_cols]
                            inv_df.columns = ['Blood Type', 'Units Available'][:len(available_cols)]
                            st.dataframe(inv_df, use_container_width=True)
                
                st.markdown("---")
                st.subheader("📝 Update Inventory")
                
                with st.form("update_inventory_form"):
                    col1, col2 = st.columns(2)
                    with col1:
                        blood_type = st.selectbox("🩸 Blood Type", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
                    with col2:
                        units_available = st.number_input("📦 Units Available", min_value=0, value=1)
                    
                    operation = st.radio("🔄 Operation", ["Add Units", "Set Exact Amount"])
                    
                    submitted = st.form_submit_button("💾 Update Inventory", type="primary")
                    
                    if submitted:
                        inventory_data = {
                            "blood_type": blood_type,
                            "units_available": units_available,
                            "operation": "add" if operation == "Add Units" else "set"
                        }
                        
                        if update_hospital_inventory(hospital_id, inventory_data):
                            st.rerun()
        else:
            st.info("ℹ️ No hospitals available for inventory update")

def show_requests():
    """Display professional blood requests management page"""
    st.markdown('<h1 class="main-header">📋 Blood Request Management</h1>', unsafe_allow_html=True)
    
    # Tabs for different operations
    tab1, tab2, tab3 = st.tabs(["📋 All Requests", "➕ Create Request", "🔍 Request Details"])
    
    with tab1:
        st.markdown('<div class="section-header">📋 All Blood Requests</div>', unsafe_allow_html=True)
        
        # Filters
        col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
        with col1:
            status_filter = st.selectbox("📊 Filter by Status", ["All", "pending", "accepted", "fulfilled", "cancelled"])
        with col2:
            blood_type_filter = st.selectbox("🩸 Filter by Blood Type", ["All", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        with col3:
            urgency_filter = st.selectbox("⚡ Filter by Urgency", ["All", "Critical (>5 units)", "Normal (1-5 units)"])
        with col4:
            if st.button("🔄 Refresh", use_container_width=True):
                st.cache_data.clear()
                st.rerun()
        
        with st.spinner("🔄 Loading requests..."):
            requests = get_all_requests()
        
        if requests:
            # Apply filters
            filtered_requests = requests.copy()
            if status_filter != "All":
                filtered_requests = [r for r in filtered_requests if r.get('status') == status_filter]
            if blood_type_filter != "All":
                filtered_requests = [r for r in filtered_requests if r.get('blood_type') == blood_type_filter]
            if urgency_filter != "All":
                if urgency_filter == "Critical (>5 units)":
                    filtered_requests = [r for r in filtered_requests if r.get('units_needed', 0) > 5]
                else:
                    filtered_requests = [r for r in filtered_requests if 1 <= r.get('units_needed', 0) <= 5]
            
            if filtered_requests:
                request_df = pd.DataFrame(filtered_requests)
                
                # Select safe columns to display
                display_columns = []
                column_mapping = {}
                
                if 'id' in request_df.columns:
                    display_columns.append('id')
                    column_mapping['id'] = 'ID'
                if 'blood_type' in request_df.columns:
                    display_columns.append('blood_type')
                    column_mapping['blood_type'] = 'Blood Type'
                if 'units_needed' in request_df.columns:
                    display_columns.append('units_needed')
                    column_mapping['units_needed'] = 'Units Needed'
                if 'status' in request_df.columns:
                    display_columns.append('status')
                    column_mapping['status'] = 'Status'
                if 'created_at' in request_df.columns:
                    display_columns.append('created_at')
                    column_mapping['created_at'] = 'Created At'
                if 'patient_name' in request_df.columns:
                    display_columns.append('patient_name')
                    column_mapping['patient_name'] = 'Patient'
                
                if display_columns:
                    request_df = request_df[display_columns]
                    
                    # Format created_at if present
                    if 'created_at' in request_df.columns:
                        request_df['created_at'] = request_df['created_at'].apply(format_datetime)
                    
                    request_df.columns = [column_mapping[col] for col in display_columns]
                    
                    # Apply styling - FIXED VERSION
                    try:
                        styled_df = request_df.style.apply(style_requests, axis=1)
                        st.dataframe(styled_df, use_container_width=True)
                    except Exception as e:
                        st.warning(f"⚠️ Styling error: {e}")
                        st.dataframe(request_df, use_container_width=True)
                    
                    # Show statistics
                    st.markdown("---")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        pending = len([r for r in filtered_requests if r.get('status') == 'pending'])
                        st.metric("⏳ Pending", pending)
                    with col2:
                        accepted = len([r for r in filtered_requests if r.get('status') in ['accepted', 'fulfilled']])
                        st.metric("✅ Accepted", accepted)
                    with col3:
                        critical = len([r for r in filtered_requests if r.get('units_needed', 0) > 5])
                        st.metric("🚨 Critical", critical)
                    with col4:
                        total_units = sum(r.get('units_needed', 0) for r in filtered_requests)
                        st.metric("📦 Total Units", total_units)
            else:
                st.info("ℹ️ No requests match the selected filters")
        else:
            st.info("ℹ️ No blood requests found")
    
    with tab2:
        st.markdown('<div class="section-header">➕ Create New Blood Request</div>', unsafe_allow_html=True)
        
        # Fetch hospitals for selection
        with st.spinner("🔄 Loading hospitals..."):
            hospitals = get_all_hospitals()
        
        if hospitals:
            with st.form("create_request_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    # Create safe hospital options
                    hospital_options = {}
                    for h in hospitals:
                        name = h.get('name', 'Unknown')
                        city = h.get('city', 'Unknown')
                        hospital_id = h.get('id', 'unknown')
                        hospital_options[f"{name} - {city}"] = hospital_id
                    
                    selected_hospital = st.selectbox("🏥 Select Hospital *", list(hospital_options.keys()))
                    blood_type = st.selectbox("🩸 Blood Type *", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
                    units_needed = st.number_input("📦 Units Needed *", min_value=1, value=1)
                    urgency_level = st.selectbox("⚡ Urgency Level", ["Normal", "Urgent", "Critical"])
                
                with col2:
                    patient_name = st.text_input("👤 Patient Name *", placeholder="Enter patient name")
                    patient_age = st.number_input("🎂 Patient Age", min_value=0, max_value=150, value=30)
                    accident_latitude = st.text_input("📍 Accident Latitude", placeholder="Enter latitude")
                    accident_longitude = st.text_input("📍 Accident Longitude", placeholder="Enter longitude")
                    medical_notes = st.text_area("📝 Medical Notes", placeholder="Enter any relevant medical information")
                
                submitted = st.form_submit_button("🚀 Create Blood Request", type="primary")
                
                if submitted:
                    if selected_hospital and blood_type and units_needed and patient_name:
                        request_data = {
                            "hospital_id": hospital_options[selected_hospital],
                            "blood_type": blood_type,
                            "units_needed": units_needed,
                            "patient_name": patient_name.strip(),
                            "patient_age": patient_age,
                            "urgency_level": urgency_level,
                            "accident_latitude": float(accident_latitude) if accident_latitude else None,
                            "accident_longitude": float(accident_longitude) if accident_longitude else None,
                            "medical_notes": medical_notes.strip() if medical_notes else None
                        }
                        
                        if create_blood_request(request_data):
                            # Show nearest hospital and map if coordinates provided
                            if accident_latitude and accident_longitude:
                                acc_lat = float(accident_latitude)
                                acc_lon = float(accident_longitude)
                                
                                nearest_hospital, distance = get_nearest_hospital(acc_lat, acc_lon, hospitals)
                                
                                st.markdown("---")
                                st.subheader("🗺️ Nearest Hospital Analysis")
                                
                                if nearest_hospital:
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        st.success(f"🏥 **Nearest Hospital:** {nearest_hospital.get('name', 'Unknown')}")
                                        st.success(f"📍 **Distance:** {distance:.2f} km")
                                        st.success(f"📞 **Contact:** {nearest_hospital.get('phone', 'N/A')}")
                                    
                                    with col2:
                                        # Create and display map
                                        try:
                                            m = folium.Map(location=[acc_lat, acc_lon], zoom_start=12)
                                            
                                            folium.Marker(
                                                [acc_lat, acc_lon],
                                                tooltip="Accident",
                                                icon=folium.Icon(color="red")
                                            ).add_to(m)
                                            
                                            folium.Marker(
                                                [nearest_hospital.get("latitude"), nearest_hospital.get("longitude")],
                                                tooltip=nearest_hospital.get("name"),
                                                icon=folium.Icon(color="green")
                                            ).add_to(m)
                                            
                                            st_folium(m, width=700)
                                        except Exception as e:
                                            st.error(f"⚠️ Map error: {e}")
                                else:
                                    st.warning("⚠️ No hospitals with valid coordinates found")
                            
                            st.rerun()
                    else:
                        st.error("❌ Please fill in all required fields (marked with *)")
        else:
            st.info("ℹ️ No hospitals available. Please register a hospital first.")
    
    with tab3:
        st.markdown('<div class="section-header">🔍 Request Details and Donor Responses</div>', unsafe_allow_html=True)
        
        # Fetch requests for selection
        with st.spinner("🔄 Loading requests..."):
            requests = get_all_requests()
        
        if requests:
            # Create safe request options
            request_options = {}
            for r in requests:
                req_id = r.get('id', 'unknown')
                blood_type = r.get('blood_type', 'Unknown')
                status = r.get('status', 'Unknown')
                units = r.get('units_needed', 0)
                request_options[f"Request {req_id} - {blood_type} ({units} units) - {status}"] = req_id
            
            col1, col2 = st.columns([3, 1])
            with col1:
                selected_request = st.selectbox("📋 Select Request", list(request_options.keys()))
            with col2:
                if st.button("🔄 Refresh Details", use_container_width=True):
                    st.cache_data.clear()
                    st.rerun()
            
            if selected_request:
                request_id = request_options[selected_request]
                
                # Get detailed request information
                request_details = get_request_by_id(request_id)
                
                if request_details:
                    # Request Information
                    st.subheader("📋 Request Information")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**🩸 Blood Type:** {request_details.get('blood_type', 'N/A')}")
                        st.write(f"**📦 Units Needed:** {request_details.get('units_needed', 'N/A')}")
                        st.write(f"**📊 Status:** {request_details.get('status', 'N/A')}")
                    
                    with col2:
                        st.write(f"**👤 Patient Name:** {request_details.get('patient_name', 'N/A')}")
                        st.write(f"**⚡ Urgency:** {request_details.get('urgency_level', 'N/A')}")
                        st.write(f"**🏥 Hospital ID:** {request_details.get('hospital_id', 'N/A')}")
                    
                    with col3:
                        st.write(f"**📅 Created:** {format_datetime(request_details.get('created_at', ''))}")
                        
                        # Get hospital name if possible
                        hospital_id = request_details.get('hospital_id')
                        if hospital_id:
                            hospital_info = get_hospital_by_id(hospital_id)
                            if hospital_info:
                                st.write(f"**🏥 Hospital:** {hospital_info.get('name', 'Unknown')}")
                    
                    # Medical notes if available
                    if request_details.get('medical_notes'):
                        st.markdown("---")
                        st.subheader("📝 Medical Notes")
                        st.info(request_details.get('medical_notes'))
                
                # Notified Donors Section
                st.markdown("---")
                st.subheader("👥 Notified Donors")
                
                with st.spinner("🔄 Loading notified donors..."):
                    notifications = get_request_notifications(request_id)
                
                if notifications:
                    # Get detailed donor information for each notification - CRITICAL FIX
                    donor_details_list = []
                    
                    for notification in notifications:
                        donor_id = notification.get('donor_id')
                        if donor_id:
                            # Fetch donor details separately
                            donor_info = get_donor_by_id(donor_id)
                            if donor_info:
                                donor_details = {
                                    'donor_id': donor_id,
                                    'name': donor_info.get('name', 'Unknown'),
                                    'blood_type': donor_info.get('blood_type', 'Unknown'),
                                    'city': donor_info.get('city', 'Unknown'),
                                    'phone': donor_info.get('phone', 'Unknown'),
                                    'notification_status': notification.get('status', 'Unknown'),
                                    'donor_response': notification.get('donor_response', 'No response'),
                                    'notified_at': notification.get('created_at', '')
                                }
                                donor_details_list.append(donor_details)
                    
                    if donor_details_list:
                        donor_df = pd.DataFrame(donor_details_list)
                        
                        # Select columns to display
                        display_cols = ['name', 'blood_type', 'city', 'phone', 'donor_response', 'notification_status']
                        available_cols = [col for col in display_cols if col in donor_df.columns]
                        
                        if available_cols:
                            donor_df = donor_df[available_cols]
                            donor_df.columns = ['Name', 'Blood Type', 'City', 'Phone', 'Response', 'Notification Status'][:len(available_cols)]
                            st.dataframe(donor_df, use_container_width=True)
                        
                        # Donor Response Simulation
                        st.markdown("---")
                        st.subheader("💬 Simulate Donor Response")
                        
                        # Create donor options for response simulation
                        response_options = {}
                        for donor in donor_details_list:
                            name = donor.get('name', 'Unknown')
                            blood_type = donor.get('blood_type', 'Unknown')
                            donor_id = donor.get('donor_id', 'unknown')
                            response_options[f"{name} ({blood_type})"] = donor_id
                        
                        if response_options:
                            col1, col2, col3 = st.columns([2, 1, 1])
                            with col1:
                                selected_donor = st.selectbox("👤 Select Donor for Response", list(response_options.keys()))
                            with col2:
                                if st.button("✅ Accept", type="primary", use_container_width=True):
                                    donor_id = response_options[selected_donor]
                                    response_data = {
                                        "donor_id": donor_id,
                                        "response": "accept"
                                    }
                                    if respond_to_request(request_id, donor_id, response_data):
                                        st.rerun()
                            with col3:
                                if st.button("❌ Reject", use_container_width=True):
                                    donor_id = response_options[selected_donor]
                                    response_data = {
                                        "donor_id": donor_id,
                                        "response": "reject"
                                    }
                                    if respond_to_request(request_id, donor_id, response_data):
                                        st.rerun()
                    else:
                        st.warning("⚠️ Unable to fetch donor details for notifications")
                else:
                    st.info("ℹ️ No donors have been notified for this request yet")
        else:
            st.info("ℹ️ No blood requests available")

# Main application
def main():
    """Main Streamlit application with professional navigation"""
    # Sidebar navigation
    with st.sidebar:
        st.markdown("# 🩸 HemoLink")
        st.markdown("**Blood Donor Management System**")
        st.markdown("---")
        
        # Navigation menu with icons
        page = st.radio(
            "📍 Navigate to:",
            [
                "📊 Dashboard",
                "👥 Donors", 
                "🏥 Hospitals",
                "📋 Requests"
            ]
        )
        
        st.markdown("---")
        
        # System status
        st.markdown("### 🔧 System Status")
        
        # Check backend connectivity
        try:
            success, _ = safe_api_call("GET", "/")
            if success:
                st.success("✅ Backend Online")
            else:
                st.error("❌ Backend Offline")
        except Exception:
            st.error("❌ Backend Error")
        
        st.markdown(f"**🌐 Backend URL:** `{BASE_URL}`")
        st.markdown(f"**🕒 Last Sync:** {datetime.now().strftime('%H:%M:%S')}")
        
        st.markdown("---")
        
        # Quick stats
        st.markdown("### 📈 Quick Stats")
        
        # Quick fetch of stats
        donors = get_all_donors()
        hospitals = get_all_hospitals()
        requests = get_all_requests()
        
        st.metric("👥 Donors", len(donors))
        st.metric("🏥 Hospitals", len(hospitals))
        st.metric("📋 Requests", len(requests))
        
        st.markdown("---")
        
        # Footer
        st.markdown("### ℹ️ About")
        st.markdown("**Version:** 2.0.0")
        st.markdown("**Built with:** Streamlit + FastAPI")
        st.markdown("**Features:** Maps, Geolocation, Analytics")
    
    # Display selected page
    if page == "📊 Dashboard":
        show_dashboard()
    elif page == "👥 Donors":
        show_donors()
    elif page == "🏥 Hospitals":
        show_hospitals()
    elif page == "📋 Requests":
        show_requests()

# Run the application
if __name__ == "__main__":
    main()
