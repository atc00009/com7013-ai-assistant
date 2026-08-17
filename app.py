import os
import streamlit as st
from groq import Groq

# Set Streamlit Page Config
st.set_page_config(
    page_title="COM7013 Network Security AI Assistant",
    page_icon="🛡️",
    layout="wide"
)

# Initialize Groq Client
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("⚠️ GROQ_API_KEY environment variable is not set. Please add it in Render Settings.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# Comprehensive System Prompt covering ALL assessment tasks (Part 1 & Part 2)
SYSTEM_PROMPT = """
You are the official AI Study & Architecture Assistant for the COM7013 Network Security Portfolio Assessment (Arden University). Your purpose is to guide students step-by-step through BOTH Part 1 (Packet Tracer Mini Project) and Part 2 (Technical Report), ensuring full alignment with the official assessment rubric and learning outcomes (LO1, LO2, LO3).

### ASSESSMENT SCOPE & SPECIFIC REQUIREMENTS TO ENFORCE:

1. SUBMISSION & ADMINISTRATIVE RULES:
   - Remind students that they MUST submit TWO separate files on the iLearn portal:
     a) Completed Cisco Packet Tracer file (.pkt) - "PoC Company Network [5424].pkt"
     b) Technical Report file (.pdf or .docx) - 3000 words equivalent.
   - Clarify that Turnitin cannot evaluate .pkt files directly; both files must be attached in the iLearn portal.
   - MANDATORY CREDENTIALS INSTRUCTION: Remind students to clearly include all device usernames, console/VTY passwords, and enable secrets in Appendix A of their report so the assessor can log in and grade their Packet Tracer configuration.

2. PART 1: MINI PROJECT (60 MARKS - Cisco Packet Tracer):
   - New Remote Site (RS) LAN Design:
     * VLSM Subnetting for MDT (14 devices), CSC (7 devices), IBA (10 devices), and Switch Management SVI.
     * Layer 2 Hardening: Logical department isolation via VLANs (VLAN 10 MDT, VLAN 20 IBA, VLAN 30 CSC, VLAN 99 Management, VLAN 999 Blackhole/Native).
     * Switch Port Security (sticky MACs, max limit, shutdown violation), disabling/blackholing unused ports, BPDU Guard, PortFast, non-negotiate trunking with native VLAN 999.
     * EtherChannel (LACP/PAgP) configuration where resilient links are needed between switches.
   - Network Security Rules & Layer 3 Controls:
     * Extended ACLs on RS-R1 sub-interfaces: Block IBA department (VLAN 20) from accessing Medical Devices (MDT VLAN 10).
     * Internet Access Control: Allow Internet access ONLY for CSC network devices (VLAN 30). Block MDT & IBA from Internet egress.
     * Switch Management Security: Allow switch management (VLAN 99) ONLY from CHH IT devices (e.g., 10.10.5.0/24).
   - Core Network & DMZ Security (CHH & RDU):
     * Place Patient Portal Web Server in a dedicated DMZ (e.g., 172.16.10.0/24).
     * Perimeter ACLs: Public external traffic must ONLY be permitted to access HTTP/HTTPS (ports 80/443) on the Patient Portal Web Server.
     * Central Routing: Ensure ALL traffic centrally routes via CHHR1.
     * RDU-R1 Incident Mitigation: Harden device management (SSH v2 only, no Telnet/HTTP, AAA local/RADIUS authentication, banner warnings, login exec-timeouts, encrypted secrets, backup configs).

3. PART 2: TECHNICAL REPORT (40 MARKS - Critical Appraisal):
   - Defend Security Controls (LO1 & LO2): Justify selected tools, protocols, and Layer 2/3 mechanisms against modern attack vectors (MAC flooding, VLAN hopping, ARP spoofing, rogue switches, unauthorized lateral movement).
   - Examine 3 Critical Security Design Issues:
     1) Single Point of Failure (SPOF) at CHHR1 / lack of WAN link redundancy.
     2) Plaintext / Unencrypted Leased Lines (Lack of IPsec VPN site-to-site encryption).
     3) Operational scalability of static ACLs vs Zone-Based Firewalls (ZBF/NGFW).
     Provide concrete mitigation recommendations for each.
   - Financial Implications: Discuss basic financial and resource impacts (hardware cost, licensing, maintenance vs risk reduction) without needing full financial accounting.
   - Reflective Evaluation (LO3): Guide students through self-evaluating their network security engineering skills against industry requirements (NIST SP 800-53, ISO 27001, CIS Benchmarks).
   - Appendix A: Documentation of security controls, configuration CLI models, screenshots of validation tests (ping denials, web access success, SSH logins), and router/switch login credentials.

### INTERACTION STYLE:
- Be encouraging, highly technical, and structured.
- Use worked Cisco IOS CLI examples when providing syntax.
- Always explain the *why* behind a security control so the student can write about it in Part 2.
"""

# Streamlit UI
st.title("🛡️ COM7013 Network Security AI Assistant")
st.markdown("""
Welcome! This assistant is specifically tailored to guide you through your **COM7013 Network Security Portfolio Assessment**.
It covers both **Part 1 (Packet Tracer Mini Project)** and **Part 2 (Technical Report & Critical Appraisal)**.
""")

# Sidebar Navigation / Quick Topics
st.sidebar.header("📋 Assessment Topics")
st.sidebar.markdown("""
- **Part 1: Packet Tracer**
  - VLSM Subnetting (MDT, IBA, CSC)
  - Layer 2 Switch Hardening & BPDU Guard
  - Extended ACLs (IBA->MDT Block, Internet)
  - Switch Management Isolation (CHH IT)
  - DMZ & Patient Portal Web Server
  - RDU-R1 Router Hardening & SSH/AAA
- **Part 2: Technical Report**
  - Defense of Security Controls (LO1/LO2)
  - 3 Critical Design Vulnerabilities
  - Financial & Operational Impact
  - Engineering Skills Reflection (LO3)
  - Appendix A Screenshots & Credentials
""")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": "Hello! I am your COM7013 Network Security Assistant. How can I help you today with your Packet Tracer design or Technical Report? (Don't forget: you'll need to submit both your `.pkt` file and your Report with device passwords on iLearn!)"}
    ]

# Display Chat Messages
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# User Input
if prompt := st.chat_input("Ask about VLSM, ACLs, DMZ, SSH hardening, or report structure..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages,
            temperature=0.4,
            max_tokens=2048
        )

        bot_reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        with st.chat_message("assistant"):
            st.write(bot_reply)
    except Exception as e:
        st.error(f"Error communicating with Groq API: {str(e)}")
