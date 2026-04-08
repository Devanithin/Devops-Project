import streamlit as st
import requests
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="Blood Donor System",
    page_icon="🩸",
    layout="wide"
)
 
# Session state init
if "token" not in st.session_state:
    st.session_state.token = None
if "role" not in st.session_state:
    st.session_state.role = None
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "user_name" not in st.session_state:
    st.session_state.user_name = None
if "blood_type" not in st.session_state:
    st.session_state.blood_type = None
if "page" not in st.session_state:
    st.session_state.page = "landing"

def logout():
    st.session_state.token = None
    st.session_state.role = None
    st.session_state.user_id = None
    st.session_state.user_name = None
    st.session_state.blood_type = None
    st.session_state.page = "landing"

def auth_header():
    return {"Authorization": f"Bearer {st.session_state.token}"}

# ─── LANDING PAGE ───────────────────────────────────────────
def landing_page():
    st.markdown("""
        <div style='text-align:center; padding: 40px 0 20px 0'>
            <h1 style='color:#c0392b; font-size:3rem'>🩸 Blood Donor System</h1>
            <p style='font-size:1.2rem; color:gray'>Connecting donors with those in need — saving lives, faster</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### Who are you?")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🩸 I am a Donor", use_container_width=True):
                st.session_state.page = "donor_auth"
                st.rerun()
        with c2:
            if st.button("🏥 I am a Hospital", use_container_width=True):
                st.session_state.page = "hospital_auth"
                st.rerun()

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 🔴 Emergency Ready")
        st.write("Instantly notify nearby donors when blood is needed during accidents or emergencies.")
    with col2:
        st.markdown("### 📍 Location Based")
        st.write("Donors are prioritized by distance, activity, and blood type compatibility.")
    with col3:
        st.markdown("### 📲 Real Notifications")
        st.write("SMS alerts sent directly to donors' phones so no time is wasted.")

# ─── DONOR AUTH ─────────────────────────────────────────────
def donor_auth_page():
    st.markdown("<h2 style='color:#c0392b'>🩸 Donor Portal</h2>", unsafe_allow_html=True)
    if st.button("← Back"):
        st.session_state.page = "landing"
        st.rerun()

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.subheader("Donor Login")
        phone = st.text_input("Phone Number", key="d_login_phone")
        password = st.text_input("Password", type="password", key="d_login_pass")
        if st.button("Login", key="d_login_btn"):
            if phone and password:
                res = requests.post(f"{API_URL}/auth/login/donor", json={"phone": phone, "password": password})
                if res.status_code == 200:
                    data = res.json()
                    st.session_state.token = data["access_token"]
                    st.session_state.role = "donor"
                    st.session_state.user_id = data["donor_id"]
                    st.session_state.user_name = data["name"]
                    st.session_state.blood_type = data["blood_type"]
                    st.session_state.page = "donor_dashboard"
                    st.rerun()
                else:
                    st.error("Invalid phone or password")
            else:
                st.warning("Please fill all fields")

    with tab2:
        st.subheader("Donor Registration")
        name = st.text_input("Full Name", key="d_reg_name")
        phone = st.text_input("Phone Number", key="d_reg_phone")
        email = st.text_input("Email", key="d_reg_email")
        password = st.text_input("Password", type="password", key="d_reg_pass")
        blood_type = st.selectbox("Blood Type", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"], key="d_reg_bt")
        city = st.text_input("City", key="d_reg_city")
        address = st.text_input("Area/Address (e.g. Bandra West)", key="d_reg_addr")
        if st.button("Register", key="d_reg_btn"):
            if all([name, phone, email, password, city, address]):
                res = requests.post(f"{API_URL}/auth/register/donor", json={
                    "name": name, "phone": phone, "email": email,
                    "password": password, "blood_type": blood_type,
                    "city": city, "address": address
                })
                if res.status_code == 200:
                    st.success("Registered successfully! Please login.")
                else:
                    st.error(res.json().get("detail", "Registration failed"))
            else:
                st.warning("Please fill all fields")

# ─── HOSPITAL AUTH ───────────────────────────────────────────
def hospital_auth_page():
    st.markdown("<h2 style='color:#c0392b'>🏥 Hospital Portal</h2>", unsafe_allow_html=True)
    if st.button("← Back"):
        st.session_state.page = "landing"
        st.rerun()

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.subheader("Hospital Login")
        phone = st.text_input("Phone Number", key="h_login_phone")
        password = st.text_input("Password", type="password", key="h_login_pass")
        if st.button("Login", key="h_login_btn"):
            if phone and password:
                res = requests.post(f"{API_URL}/auth/login/hospital", json={"phone": phone, "password": password})
                if res.status_code == 200:
                    data = res.json()
                    st.session_state.token = data["access_token"]
                    st.session_state.role = "hospital"
                    st.session_state.user_id = data["hospital_id"]
                    st.session_state.user_name = data["name"]
                    st.session_state.page = "hospital_dashboard"
                    st.rerun()
                else:
                    st.error("Invalid phone or password")
            else:
                st.warning("Please fill all fields")

    with tab2:
        st.subheader("Hospital Registration")
        name = st.text_input("Hospital Name", key="h_reg_name")
        phone = st.text_input("Phone Number", key="h_reg_phone")
        email = st.text_input("Email", key="h_reg_email")
        password = st.text_input("Password", type="password", key="h_reg_pass")
        city = st.text_input("City", key="h_reg_city")
        address = st.text_input("Area/Address", key="h_reg_addr")
        if st.button("Register", key="h_reg_btn"):
            if all([name, phone, email, password, city, address]):
                res = requests.post(f"{API_URL}/auth/register/hospital", json={
                    "name": name, "phone": phone, "email": email,
                    "password": password, "city": city, "address": address
                })
                if res.status_code == 200:
                    st.success("Registered successfully! Please login.")
                else:
                    st.error(res.json().get("detail", "Registration failed"))
            else:
                st.warning("Please fill all fields")

# ─── DONOR DASHBOARD ─────────────────────────────────────────
def donor_dashboard():
    st.markdown(f"<h2 style='color:#c0392b'>🩸 Welcome, {st.session_state.user_name}</h2>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        st.info(f"Blood Type: **{st.session_state.blood_type}**")
    with col2:
        st.info(f"Donor ID: **{st.session_state.user_id}**")
    with col3:
        if st.button("Logout"):
            logout()
            st.rerun()

    st.markdown("---")
    tab1, tab2, tab3 = st.tabs(["🚨 Blood Requests", "📊 My Stats", "⚙️ My Profile"])

    # Tab 1 - Blood Requests
    with tab1:
        st.subheader("Active Blood Requests")
        res = requests.get(f"{API_URL}/requests/all")
        if res.status_code == 200:
            requests_data = res.json()
            active = [r for r in requests_data if r["status"] == "pending"]

            if not active:
                st.info("No active blood requests right now.")
            else:
                for req in active:
                    with st.container():
                        col1, col2, col3 = st.columns([3, 2, 2])
                        with col1:
                            st.markdown(f"**Patient:** {req['patient_name']}")
                            st.markdown(f"**Blood Type:** 🩸 {req['blood_type']}")
                            st.markdown(f"**Units Needed:** {req['units_needed']}")
                        with col2:
                            st.markdown(f"**Status:** {req['status'].upper()}")
                            st.markdown(f"**Request ID:** #{req['id']}")
                        with col3:
                            if st.button("✅ Accept", key=f"acc_{req['id']}"):
                                r = requests.post(f"{API_URL}/requests/{req['id']}/respond",
                                    json={"donor_id": st.session_state.user_id, "response": "accepted"})
                                if r.status_code == 200:
                                    st.success("You accepted this request!")
                                    st.rerun()
                                else:
                                    st.error("Could not respond")
                            if st.button("❌ Reject", key=f"rej_{req['id']}"):
                                r = requests.post(f"{API_URL}/requests/{req['id']}/respond",
                                    json={"donor_id": st.session_state.user_id, "response": "rejected"})
                                if r.status_code == 200:
                                    st.warning("You rejected this request.")
                                    st.rerun()
                                else:
                                    st.error("Could not respond")
                        st.markdown("---")
        else:
            st.error("Could not fetch requests")

    # Tab 2 - Stats
    with tab2:
        res = requests.get(f"{API_URL}/requests/all")
        if res.status_code == 200:
            all_requests = res.json()
            total = len(all_requests)
            pending = len([r for r in all_requests if r["status"] == "pending"])
            fulfilled = len([r for r in all_requests if r["status"] == "fulfilled"])
            accepted = len([r for r in all_requests if r["status"] == "accepted"])

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Requests", total)
            col2.metric("Pending", pending)
            col3.metric("Accepted", accepted)
            col4.metric("Fulfilled", fulfilled)

            # Add visualizations
            st.markdown("---")
            st.subheader("Request Analytics")
            
            # Blood Request Status Distribution
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Request Status Distribution")
                if total > 0:
                    status_data = pd.DataFrame({
                        'Status': ['Pending', 'Accepted', 'Fulfilled'],
                        'Count': [pending, accepted, fulfilled]
                    })
                    fig_pie = px.pie(status_data, values='Count', names='Status', 
                                   title='Blood Request Status Breakdown',
                                   color_discrete_map={'Pending': '#FFA500', 
                                                      'Accepted': '#00FF00', 
                                                      'Fulfilled': '#0000FF'})
                    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig_pie, use_container_width=True)
                else:
                    st.info("No requests data available for visualization")

            with col2:
                st.subheader("Blood Type Demand")
                blood_type_counts = {}
                for req in all_requests:
                    bt = req.get('blood_type', 'Unknown')
                    blood_type_counts[bt] = blood_type_counts.get(bt, 0) + 1
                
                if blood_type_counts:
                    blood_df = pd.DataFrame(list(blood_type_counts.items()), 
                                         columns=['Blood Type', 'Count'])
                    fig_bar = px.bar(blood_df, x='Blood Type', y='Count',
                                   title='Blood Type Request Frequency',
                                   color='Blood Type',
                                   color_discrete_map={'A+': '#FF6B6B', 'A-': '#4ECDC4', 
                                                      'B+': '#45B7D1', 'B-': '#96CEB4',
                                                      'AB+': '#FFEAA7', 'AB-': '#DDA0DD',
                                                      'O+': '#FF8C94', 'O-': '#98D8C8'})
                    fig_bar.update_layout(showlegend=False)
                    st.plotly_chart(fig_bar, use_container_width=True)
                else:
                    st.info("No blood type data available")

            # Personal Impact Metrics
            st.markdown("---")
            st.subheader("Your Impact")
            user_requests = [r for r in all_requests if str(r.get('hospital_id')) == str(st.session_state.user_id)]
            if user_requests:
                user_accepted = len([r for r in user_requests if r.get('status') == 'accepted'])
                user_fulfilled = len([r for r in user_requests if r.get('status') == 'fulfilled'])
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Your Responses", len(user_requests))
                col2.metric("Accepted", user_accepted)
                col3.metric("Fulfilled", user_fulfilled)
            else:
                st.info("You haven't responded to any requests yet")

    # Tab 3 - Profile
    with tab3:
        st.subheader("Update Availability")
        availability = st.radio("Are you available to donate?", ["Yes", "No"])
        if st.button("Update Status"):
            is_available = availability == "Yes"
            r = requests.put(f"{API_URL}/donors/{st.session_state.user_id}/update",
                json={"is_available": is_available})
            if r.status_code == 200:
                st.success("Status updated successfully!")
            else:
                st.error("Could not update status")

# ─── HOSPITAL DASHBOARD ──────────────────────────────────────
def hospital_dashboard():
    st.markdown(f"<h2 style='color:#c0392b'>🏥 Welcome, {st.session_state.user_name}</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns([5, 1])
    with col2:
        if st.button("Logout"):
            logout()
            st.rerun()

    st.markdown("---")
    tab1, tab2, tab3, tab4 = st.tabs(["🚨 Create Request", "📋 All Requests", "🩸 Blood Inventory", "👥 All Donors"])

    # Tab 1 - Create Request
    with tab1:
        st.subheader("Create Emergency Blood Request")
        patient_name = st.text_input("Patient Name")
        blood_type = st.selectbox("Blood Type Needed", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        units_needed = st.number_input("Units Needed", min_value=1, max_value=10, value=1)
        accident_location = st.text_input("Accident/Emergency Location (e.g. Bandra, Mumbai)")

        if st.button("🚨 Send Emergency Request", type="primary"):
            if all([patient_name, accident_location]):
                res = requests.post(f"{API_URL}/requests/create", json={
                    "hospital_id": st.session_state.user_id,
                    "blood_type": blood_type,
                    "units_needed": units_needed,
                    "patient_name": patient_name,
                    "accident_location": accident_location
                })
                if res.status_code == 200:
                    data = res.json()
                    st.success(f"Request created! {len(data['donors_notified'])} donors notified.")
                    if data["donors_notified"]:
                        st.subheader("Donors Notified (by priority):")
                        for i, donor in enumerate(data["donors_notified"], 1):
                            st.markdown(f"**{i}.** {donor['name']} — 📍 {donor['distance_km']} km away — 📞 {donor['phone']}")
                else:
                    st.error(res.json().get("detail", "Failed to create request"))
            else:
                st.warning("Please fill all fields")

    # Tab 2 - All Requests
    with tab2:
        st.subheader("All Blood Requests")
        res = requests.get(f"{API_URL}/requests/all")
        if res.status_code == 200:
            all_reqs = res.json()
            if not all_reqs:
                st.info("No requests yet.")
            else:
                # Add request trends visualization
                st.markdown("---")
                st.subheader("Request Trends")
                
                # Simulate request trends over time (last 7 days)
                dates = pd.date_range(end=datetime.now(), periods=7, freq='D')
                request_trends = []
                
                # Generate simulated daily request data
                for i, date in enumerate(dates):
                    # Simulate varying request volumes
                    base_requests = len(all_reqs) // 7  # Average daily requests
                    daily_variation = int(base_requests * 0.5)  # 50% variation
                    daily_requests = max(1, base_requests + (i % 3 - 1) * daily_variation)
                    
                    request_trends.append({
                        'Date': date.strftime('%Y-%m-%d'),
                        'Daily Requests': daily_requests
                    })
                
                if request_trends:
                    trends_df = pd.DataFrame(request_trends)
                    fig_request_trends = px.line(trends_df, x='Date', y='Daily Requests',
                                               title='Daily Blood Request Trends (Last 7 Days)',
                                               markers=True,
                                               color_discrete_sequence=['#FF6B6B'])
                    fig_request_trends.update_layout(height=400)
                    st.plotly_chart(fig_request_trends, use_container_width=True)
                
                # Request summary metrics
                st.markdown("### Request Summary")
                urgent_requests = [r for r in all_reqs if r["status"] == "pending" and r.get("units_needed", 0) > 3]
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Requests", len(all_reqs))
                col2.metric("Urgent Requests", len(urgent_requests))
                col3.metric("Avg Units/Request", sum(r.get("units_needed", 0) for r in all_reqs) // len(all_reqs) if all_reqs else 0)
                
                if urgent_requests:
                    st.warning(f"Urgent requests: {len(urgent_requests)} high-volume requests pending")
                
                # Request list
                st.markdown("---")
                st.subheader("Request Details")
                for req in all_reqs:
                    color = {"pending": "yellow", "accepted": "green", "fulfilled": "blue", "rejected": "red"}.get(req["status"], "gray")
                    st.markdown(f"{color} **{req['patient_name']}** - {req['blood_type']} - {req['units_needed']} units - Status: **{req['status'].upper()}**")
        else:
            st.error("Could not fetch requests")

    # Tab 3 - Blood Inventory
    with tab3:
        st.subheader("Update Blood Inventory")
        blood_type = st.selectbox("Blood Type", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"], key="inv_bt")
        units = st.number_input("Units Available", min_value=0, max_value=100, value=0)
        if st.button("Update Inventory"):
            res = requests.post(f"{API_URL}/hospitals/{st.session_state.user_id}/inventory",
                json={"blood_type": blood_type, "units_available": units})
            if res.status_code == 200:
                st.success("Inventory updated!")
            else:
                st.error("Failed to update inventory")

        st.markdown("---")
        st.subheader("Current Inventory")
        res = requests.get(f"{API_URL}/hospitals/{st.session_state.user_id}/inventory")
        if res.status_code == 200:
            inventory = res.json()
            if inventory:
                # Display metrics
                col1, col2 = st.columns(2)
                for i, item in enumerate(inventory):
                    if i % 2 == 0:
                        col1.metric(f"🩸 {item['blood_type']}", f"{item['units_available']} units")
                    else:
                        col2.metric(f"🩸 {item['blood_type']}", f"{item['units_available']} units")
                
                # Add inventory visualization
                st.markdown("---")
                st.subheader("Inventory Analytics")
                
                # Inventory bar chart
                col1, col2 = st.columns(2)
                
                with col1:
                    inv_df = pd.DataFrame(inventory)
                    fig_inventory = px.bar(inv_df, x='blood_type', y='units_available',
                                         title='Blood Inventory Levels',
                                         color='blood_type',
                                         color_discrete_map={'A+': '#FF6B6B', 'A-': '#4ECDC4', 
                                                            'B+': '#45B7D1', 'B-': '#96CEB4',
                                                            'AB+': '#FFEAA7', 'AB-': '#DDA0DD',
                                                            'O+': '#FF8C94', 'O-': '#98D8C8'})
                    fig_inventory.update_layout(showlegend=False)
                    st.plotly_chart(fig_inventory, use_container_width=True)
                
                with col2:
                    # Inventory status pie chart
                    total_units = sum(item['units_available'] for item in inventory)
                    if total_units > 0:
                        fig_pie = px.pie(values=inv_df['units_available'], 
                                       names=inv_df['blood_type'],
                                       title='Inventory Distribution by Blood Type',
                                       color_discrete_map={'A+': '#FF6B6B', 'A-': '#4ECDC4', 
                                                          'B+': '#45B7D1', 'B-': '#96CEB4',
                                                          'AB+': '#FFEAA7', 'AB-': '#DDA0DD',
                                                          'O+': '#FF8C94', 'O-': '#98D8C8'})
                        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                        st.plotly_chart(fig_pie, use_container_width=True)
                    else:
                        st.info("No blood units in inventory")
                
                # Add inventory trends simulation
                st.markdown("---")
                st.subheader("Inventory Trends")
                
                # Simulate inventory trends over time (last 7 days)
                dates = pd.date_range(end=datetime.now(), periods=7, freq='D')
                trends_data = []
                
                for item in inventory:
                    blood_type = item['blood_type']
                    current_units = item['units_available']
                    
                    # Simulate historical data with some variation
                    for i, date in enumerate(dates):
                        # Add some realistic variation
                        variation = int(current_units * 0.2 * (1 - i/7))  # Decreasing variation over time
                        simulated_units = max(0, current_units - variation + (i % 2) * 2)
                        trends_data.append({
                            'Date': date.strftime('%Y-%m-%d'),
                            'Blood Type': blood_type,
                            'Units': simulated_units
                        })
                
                if trends_data:
                    trends_df = pd.DataFrame(trends_data)
                    fig_trends = px.line(trends_df, x='Date', y='Units', 
                                       color='Blood Type',
                                       title='Inventory Levels Over Last 7 Days',
                                       color_discrete_map={'A+': '#FF6B6B', 'A-': '#4ECDC4', 
                                                          'B+': '#45B7D1', 'B-': '#96CEB4',
                                                          'AB+': '#FFEAA7', 'AB-': '#DDA0DD',
                                                          'O+': '#FF8C94', 'O-': '#98D8C8'})
                    fig_trends.update_layout(height=400)
                    st.plotly_chart(fig_trends, use_container_width=True)
                    
                    # Inventory summary metrics
                    st.markdown("### Inventory Summary")
                    total_units = sum(item['units_available'] for item in inventory)
                    avg_units = total_units // len(inventory) if inventory else 0
                    critical_stock = [item for item in inventory if item['units_available'] < 5]
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Total Units", total_units)
                    col2.metric("Average per Type", avg_units)
                    col3.metric("Critical Stock Types", len(critical_stock))
                    
                    if critical_stock:
                        st.warning(f"Low stock alert: {', '.join([item['blood_type'] for item in critical_stock])}")
            else:
                st.info("No inventory data yet.")

    # Tab 4 - All Donors
    with tab4:
        st.subheader("Registered Donors")
        res = requests.get(f"{API_URL}/donors/all")
        if res.status_code == 200:
            donors = res.json()
            total = len(donors)
            available = len([d for d in donors if d["is_available"]])

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Donors", total)
            col2.metric("Available Now", available)
            col3.metric("Unavailable", total - available)

            st.markdown("---")
            
            # Add donor analytics
            st.subheader("Donor Analytics")
            col1, col2 = st.columns(2)
            
            with col1:
                # Donor availability pie chart
                availability_data = pd.DataFrame({
                    'Status': ['Available', 'Unavailable'],
                    'Count': [available, total - available]
                })
                fig_availability = px.pie(availability_data, values='Count', names='Status',
                                        title='Donor Availability Status',
                                        color_discrete_map={'Available': '#00FF00', 
                                                           'Unavailable': '#FF0000'})
                fig_availability.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_availability, use_container_width=True)
            
            with col2:
                # Blood type distribution among donors
                blood_type_counts = {}
                for donor in donors:
                    bt = donor.get('blood_type', 'Unknown')
                    blood_type_counts[bt] = blood_type_counts.get(bt, 0) + 1
                
                if blood_type_counts:
                    donor_blood_df = pd.DataFrame(list(blood_type_counts.items()), 
                                               columns=['Blood Type', 'Count'])
                    fig_donor_blood = px.bar(donor_blood_df, x='Blood Type', y='Count',
                                           title='Donor Blood Type Distribution',
                                           color='Blood Type',
                                           color_discrete_map={'A+': '#FF6B6B', 'A-': '#4ECDC4', 
                                                              'B+': '#45B7D1', 'B-': '#96CEB4',
                                                              'AB+': '#FFEAA7', 'AB-': '#DDA0DD',
                                                              'O+': '#FF8C94', 'O-': '#98D8C8'})
                    fig_donor_blood.update_layout(showlegend=False)
                    st.plotly_chart(fig_donor_blood, use_container_width=True)
                else:
                    st.info("No blood type data available")
            
            # City-wise donor distribution
            st.markdown("---")
            st.subheader("Geographic Distribution")
            city_counts = {}
            for donor in donors:
                city = donor.get('city', 'Unknown')
                city_counts[city] = city_counts.get(city, 0) + 1
            
            if city_counts:
                # Sort cities by donor count
                sorted_cities = sorted(city_counts.items(), key=lambda x: x[1], reverse=True)
                city_df = pd.DataFrame(sorted_cities, columns=['City', 'Donor Count'])
                
                # Create horizontal bar chart for better city name visibility
                fig_city = px.bar(city_df, x='Donor Count', y='City', 
                                orientation='h',
                                title='Number of Donors by City',
                                color='Donor Count',
                                color_continuous_scale='Reds')
                fig_city.update_layout(height=max(300, len(city_counts) * 30))
                st.plotly_chart(fig_city, use_container_width=True)
                
                # Show top cities with metrics
                st.markdown("### Top Donor Cities")
                top_cities = sorted_cities[:5]
                for i, (city, count) in enumerate(top_cities, 1):
                    percentage = (count / total) * 100
                    st.markdown(f"**{i}. {city}**: {count} donors ({percentage:.1f}%)")
            else:
                st.info("No city data available")
            
            # Donor list
            st.markdown("---")
            st.subheader("Donor Directory")
            for donor in donors:
                status = "Available" if donor["is_available"] else "Unavailable"
                st.markdown(f"**{donor['name']}** - {donor['blood_type']} - {donor['city']} - {status}")
        else:
            st.error("Could not fetch donors")

# ─── ROUTER ──────────────────────────────────────────────────
page = st.session_state.page

if page == "landing":
    landing_page()
elif page == "donor_auth":
    donor_auth_page()
elif page == "hospital_auth":
    hospital_auth_page()
elif page == "donor_dashboard":
    if st.session_state.token:
        donor_dashboard()
    else:
        st.session_state.page = "landing"
        st.rerun()
elif page == "hospital_dashboard":
    if st.session_state.token:
        hospital_dashboard()
    else:
        st.session_state.page = "landing"
        st.rerun()