import os
from datetime import datetime, timedelta, timezone

import pandas as pd
import plotly.express as px
import streamlit as st

# Optional cloud connection
try:
    from supabase import create_client, Client
except ImportError:
    create_client = None
    Client = None

st.set_page_config(
    page_title="AMRIT AGASTYA",
    page_icon="💧",
    layout="wide",
)


st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(59,130,246,.10), transparent 28%),
        radial-gradient(circle at 90% 20%, rgba(16,185,129,.10), transparent 30%),
        linear-gradient(135deg, #f8fbff 0%, #eef7ff 50%, #f5fffb 100%);
}
.block-container { padding-top: 1.5rem; }
h1 {
    font-weight: 800 !important;
    letter-spacing: .5px;
    text-shadow: 0 3px 18px rgba(37,99,235,.15);
}
.filter-card {
    min-height: 235px;
    padding: 16px 10px;
    border-radius: 22px;
    text-align: center;
    background: rgba(255,255,255,.88);
    border: 1px solid rgba(148,163,184,.25);
    box-shadow: 0 10px 30px rgba(15,23,42,.08);
    transition: transform .25s ease, box-shadow .25s ease;
    animation: floatIn .7s ease both, filterPulse 3.2s ease-in-out infinite;
}
.filter-card:hover {
    transform: translateY(-7px) scale(1.02);
    box-shadow: 0 18px 38px rgba(15,23,42,.14);
}
.filter-icon {
    width: 54px;
    height: 105px;
    margin: 0 auto 10px;
    position: relative;
    filter: drop-shadow(0 7px 8px rgba(15,23,42,.12));
}
.filter-cap {
    position:absolute; top:0; left:7px; right:7px; height:13px;
    border-radius:8px 8px 3px 3px; background:var(--filter-color);
}
.filter-body {
    position:absolute; top:11px; left:12px; right:12px; bottom:13px;
    border:3px solid var(--filter-color);
    border-radius:8px 8px 14px 14px;
    background:linear-gradient(180deg, rgba(255,255,255,.8), rgba(226,232,240,.65));
}
.filter-body:after {
    content:"";
    position:absolute; left:7px; right:7px; top:16px; height:4px;
    border-radius:4px; background:var(--filter-color);
    box-shadow:0 17px 0 var(--filter-color), 0 34px 0 var(--filter-color);
    opacity:.28;
}
.filter-foot {
    position:absolute; bottom:0; left:2px; right:2px; height:14px;
    border-radius:3px 3px 8px 8px; background:var(--filter-color);
}
.filter-name { font-weight:800; font-size:16px; }
.filter-desc { font-size:11px; color:#64748b; min-height:30px; }
.filter-health { font-size:24px; font-weight:900; margin-top:7px; }
.filter-status {
    color:white; display:inline-block; padding:3px 10px;
    border-radius:999px; font-size:10px; font-weight:800;
}
@keyframes floatIn {
    from { opacity:0; transform:translateY(15px); }
    to { opacity:1; transform:translateY(0); }
}
@keyframes filterPulse { 0%,100% { box-shadow:0 10px 30px rgba(15,23,42,.08); } 50% { box-shadow:0 16px 38px rgba(0,150,190,.16); } }
.filter-card:hover .filter-icon { animation: filterFloat .8s ease-in-out infinite alternate; }
@keyframes filterFloat { from { transform:translateY(0) rotate(-1deg); } to { transform:translateY(-5px) rotate(1deg); } }
.filter-body:after { animation: waterFlow 1.8s linear infinite; }
@keyframes waterFlow { 0% { opacity:.18; transform:translateY(-3px); } 50% { opacity:.48; transform:translateY(3px); } 100% { opacity:.18; transform:translateY(-3px); } }
</style>

<style>
[data-testid="stAppViewContainer"]{
background:radial-gradient(circle at 8% 5%,rgba(0,188,212,.13),transparent 25%),radial-gradient(circle at 92% 8%,rgba(33,150,243,.10),transparent 25%),linear-gradient(135deg,#f7fcff,#eef8fc 50%,#fbfeff);
}
[data-testid="stHeader"]{background:rgba(255,255,255,.72);backdrop-filter:blur(12px)}
.block-container{max-width:1500px;padding-top:1rem}




50%{transform:translate(-10px,12px)}}
.filter-wrap{background:rgba(255,255,255,.82);border:1px solid rgba(0,150,199,.14);border-radius:20px;padding:14px;box-shadow:0 8px 26px rgba(20,90,120,.08)}
.filter-icon{height:58px;border-radius:15px;display:flex;align-items:center;justify-content:center;font-size:28px;position:relative;overflow:hidden;background:linear-gradient(135deg,rgba(0,188,212,.12),rgba(255,255,255,.95))}
.filter-icon:after{content:"";position:absolute;left:-45%;width:42%;height:100%;background:linear-gradient(90deg,transparent,rgba(255,255,255,.8),transparent);transform:skewX(-20deg);animation:shine 3s infinite}
@keyframes shine{0%{left:-45%}55%,100%{left:125%}}
.unit-banner{padding:12px 18px;border-radius:16px;margin:18px 0 10px;background:linear-gradient(90deg,rgba(0,119,182,.11),rgba(0,188,212,.06));border-left:5px solid #008cc2;color:#16465a;font-weight:800;box-shadow:0 6px 20px rgba(20,90,120,.06)}
.chart-card{background:rgba(255,255,255,.76);border:1px solid rgba(0,132,180,.10);border-radius:18px;padding:6px;box-shadow:0 7px 23px rgba(20,80,110,.06);margin-bottom:12px}
div[data-testid="stMetric"]{background:rgba(255,255,255,.86);border:1px solid rgba(0,132,180,.12);padding:10px 14px;border-radius:16px;box-shadow:0 6px 19px rgba(20,80,110,.07)}
.stButton>button{border-radius:12px;font-weight:700;transition:all .2s ease}
.stButton>button:hover{transform:translateY(-2px);box-shadow:0 7px 18px rgba(0,120,170,.16)}
[data-testid="stDataFrame"]{border-radius:16px;overflow:hidden}
footer{visibility:hidden}
</style>

""", unsafe_allow_html=True)
st.title("💧 AMRIT AGASTYA")
st.caption("Temperature • TDS • pH • Turbidity • Machine Control")


# ================= ALERT SYSTEM + FEEDBACK =================
def amrit_beep():
    """Short browser beep. Browser may require one prior user interaction."""
    st.components.v1.html("""
    <script>
    try {
      const Ctx = window.AudioContext || window.webkitAudioContext;
      if (Ctx) {
        const ctx = new Ctx(); const osc = ctx.createOscillator(); const gain = ctx.createGain();
        osc.type = "sine"; osc.frequency.value = 880; gain.gain.value = 0.16;
        osc.connect(gain); gain.connect(ctx.destination); osc.start();
        setTimeout(() => { osc.stop(); ctx.close(); }, 420);
      }
    } catch(e) {}
    </script>
    """, height=1)

def show_alert_system(latest_reading, filter_data):
    alerts=[]
    for name, _desc, health in filter_data:
        if safe_float(health, 100) < 35:
            alerts.append(f"🔴 {name} health is {safe_float(health):.0f}% — below 35%.")
    if latest_reading is not None:
        ph=safe_float(latest_reading.get("ph")); tds=safe_float(latest_reading.get("tds")); turb=safe_float(latest_reading.get("turbidity"))
        bad=[]
        if not (6.5 <= ph <= 7.0): bad.append(f"pH {ph:.2f}")
        if tds > 500: bad.append(f"TDS {tds:.0f} ppm")
        if turb > 5: bad.append(f"Turbidity {turb:.2f} NTU")
        if bad: alerts.append("🟠 Drinking Water Quality mismatch: " + ", ".join(bad) + ".")
    st.subheader("🚨 Alert System")
    if alerts:
        st.error("ALERTS SYSTEM")
        for a in alerts: st.warning(a)
        amrit_beep()
    else:
        st.success("✅ No active filter-health or drinking-water quality alerts.")

def feedback_section():
    st.subheader("💬 Feedback")
    st.caption("Tell us what you think. Maximum 100 words.")
    feedback=st.text_area("Your feedback", max_chars=700, height=120, placeholder="Write your feedback here...", key="amrit_feedback")
    words=len(feedback.split()) if feedback.strip() else 0
    st.caption(f"{words}/100 words")
    if words > 100: st.warning("Please keep your feedback within 100 words.")
    if st.button("📨 Submit Feedback", key="amrit_feedback_submit"):
        if not feedback.strip(): st.warning("Please enter feedback first.")
        elif words > 100: st.warning("Please reduce your feedback to 100 words or fewer.")
        else: st.success("✅ Thank you! Your feedback has been recorded for this session.")

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

@st.cache_resource
def get_supabase():
    if not SUPABASE_URL or not SUPABASE_KEY or create_client is None:
        return None
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_supabase()

def demo_data():
    now = datetime.now(timezone.utc)
    rows = []
    for i in range(60):
        t = now - timedelta(minutes=59-i)
        for unit in ["1", "2"]:
            rows.append({
                "created_at": t.isoformat(),
                "temperature": round(27.0 + (i % 8) * 0.22 + (0.2 if unit == "2" else 0), 2),
                "tds": int(300 + (i % 11) * 4 + (15 if unit == "2" else 0)),
                "ph": round(7.0 + ((i % 7) - 3) * 0.05, 2),
                "turbidity": round(3.0 + (i % 6) * 0.5, 2),
                "flow_rate": round(5.0 + (i % 5) * 0.4, 2),
                "water_level": round(70 + (i % 8) * 2, 1),
                "location": unit,
            })
    return pd.DataFrame(rows)

def load_readings():
    if supabase is None:
        return demo_data(), "DEMO MODE"
    try:
        result = (
            supabase.table("sensor_readings")
            .select("created_at,temperature,tds,ph,turbidity,flow_rate,water_level,location")
            .order("created_at", desc=True)
            .limit(200)
            .execute()
        )
        df = pd.DataFrame(result.data)
        for c, default in {
            "flow_rate": 0.0,
            "water_level": 0.0,
            "location": "1",
        }.items():
            if c not in df.columns:
                df[c] = default
        if df.empty:
            return demo_data(), "CLOUD CONNECTED • NO DATA YET"
        df["created_at"] = pd.to_datetime(df["created_at"], utc=True)
        for c in ["temperature", "tds", "ph", "turbidity", "flow_rate", "water_level"]:
            df[c] = pd.to_numeric(df[c], errors="coerce")
        return df.sort_values("created_at"), "CLOUD CONNECTED"
    except Exception as e:
        st.warning(f"Cloud read failed: {e}")
        return demo_data(), "DEMO MODE • CLOUD READ ERROR"

def get_machine_status():
    """Safely return machine state as a dictionary."""
    default = {"pump": False, "valve": False}

    if supabase is None:
        return default.copy()

    try:
        result = (
            supabase.table("machine_state")
            .select("pump,valve")
            .eq("device_id", "esp32-01")
            .limit(1)
            .execute()
        )

        data = getattr(result, "data", None)

        # Supabase can return a dict, a list of rows, None, or an unexpected value.
        if isinstance(data, list):
            data = data[0] if data and isinstance(data[0], dict) else None

        if not isinstance(data, dict):
            return default.copy()

        return {
            "pump": bool(data.get("pump", False)),
            "valve": bool(data.get("valve", False)),
        }

    except Exception as e:
        st.sidebar.warning(f"Machine status unavailable: {e}")
        return default.copy()

def send_command(device_id, command, value):
    if supabase is None:
        st.info(f"DEMO: command queued → {device_id}: {command}={value}")
        return
    try:
        supabase.table("control_commands").insert({
            "device_id": device_id,
            "command": command,
            "value": str(value),
            "status": "pending",
        }).execute()
        st.success(f"Command sent: {command} = {value}")
    except Exception as e:
        st.error(f"Command failed: {e}")


# ================= DRINKING WATER QUALITY =================
def safe_float(value, default=0.0):
    try:
        number = float(value)
        return default if pd.isna(number) else number
    except (TypeError, ValueError):
        return default


def drinking_water_quality(reading):
    ph = safe_float(reading.get("ph", 0))
    tds = safe_float(reading.get("tds", 0))
    turbidity = safe_float(reading.get("turbidity", 0))

    passed = sum([
        6.5 <= ph <= 8.5,
        tds <= 500,
        turbidity <= 5
    ])

    if passed == 3:
        return "GOOD", "#16a34a", "All monitored parameters are within the dashboard limits."
    if passed == 2:
        return "ATTENTION", "#f59e0b", "One monitored parameter needs attention."
    return "POOR", "#dc2626", "Multiple monitored parameters need attention."


# ================= FILTER ROW =================
def filter_health_row(name, health, description):
    if health >= 80:
        color, status = "#16a34a", "GOOD"
    elif health >= 50:
        color, status = "#f59e0b", "WARNING"
    else:
        color, status = "#dc2626", "BAD"

    filter_visual = f"""
    <div style="width:90px;height:150px;position:relative;margin:auto;">
        <div style="position:absolute;left:28px;top:2px;width:34px;height:12px;
                    background:{color};border-radius:7px 7px 3px 3px;"></div>
        <div style="position:absolute;left:12px;top:13px;width:66px;height:112px;
                    background:white;border:5px solid {color};border-radius:13px;"></div>
        <div style="position:absolute;left:21px;top:43px;width:48px;height:66px;
                    background:{color}22;border-radius:7px;"></div>
        <div style="position:absolute;left:27px;top:58px;width:36px;height:4px;
                    background:{color};border-radius:4px;"></div>
        <div style="position:absolute;left:31px;top:75px;width:28px;height:4px;
                    background:{color};border-radius:4px;"></div>
        <div style="position:absolute;left:25px;top:92px;width:38px;height:4px;
                    background:{color};border-radius:4px;"></div>
        <div style="position:absolute;left:29px;top:125px;width:32px;height:18px;
                    background:{color};border-radius:0 0 7px 7px;"></div>
    </div>
    """

    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:20px;
                border:2px solid {color};border-radius:15px;
                padding:10px 18px;margin:8px 0;background:{color}0d;">
        <div style="width:120px;text-align:center;">{filter_visual}</div>
        <div style="flex:1;">
            <div style="font-size:19px;font-weight:800;">{name}</div>
            <div style="font-size:13px;color:#666;">{description}</div>
        </div>
        <div style="min-width:105px;text-align:center;">
            <div style="font-size:26px;font-weight:800;color:{color};">{health}%</div>
            <div style="display:inline-block;padding:5px 13px;border-radius:18px;
                        background:{color};color:white;font-weight:700;font-size:12px;">
                {status}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

df, connection = load_readings()
machine_status = get_machine_status()

st.sidebar.success(connection)
st.sidebar.write("Device: **esp32-01**")
st.sidebar.write("Cloud: **Supabase**")

# ================= SENSOR UNIT 1 & SENSOR UNIT 2 =================
if "location" not in df.columns:
    df["location"] = "1"

def normalize_unit(value):
    text = str(value).strip().upper()
    return "2" if ("2" in text or "POINT 2" in text or "UNIT 2" in text) else "1"

df["unit"] = df["location"].apply(normalize_unit)

unit1_df = df[df["unit"] == "1"].sort_values("created_at")
unit2_df = df[df["unit"] == "2"].sort_values("created_at")

latest1 = unit1_df.iloc[-1] if not unit1_df.empty else None
latest2 = unit2_df.iloc[-1] if not unit2_df.empty else None

def show_sensor_unit(unit_name, reading):
    st.subheader(f"📡 Sensor Unit {unit_name}")

    if reading is None:
        st.info("No data available for this sensor unit.")
        return

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("🌡 Temperature", f"{safe_float(reading.get('temperature', 0)):.2f} °C")
    c2.metric("💧 TDS", f"{safe_float(reading.get('tds', 0)):.0f} ppm")
    c3.metric("🧪 pH", f"{safe_float(reading.get('ph', 0)):.2f}")
    c4.metric("🌫 Turbidity", f"{safe_float(reading.get('turbidity', 0)):.2f} NTU")
    c5.metric("💦 Flow", f"{safe_float(reading.get('flow_rate', 0)):.2f} L/min")
    c6.metric("🛢 Water Level", f"{safe_float(reading.get('water_level', 0)):.1f}%")

show_sensor_unit("1", latest1)
st.divider()
show_sensor_unit("2", latest2)

latest = latest1 if latest1 is not None else latest2
location_df = unit1_df if latest1 is not None else unit2_df
st.divider()

# ================= DRINKING WATER QUALITY =================
st.subheader("🥤 Drinking Water Quality")

if latest is not None:
    quality, qcolor, qmessage = drinking_water_quality(latest)
    icon = "🟢" if quality == "GOOD" else ("🟡" if quality == "ATTENTION" else "🔴")

    st.markdown(f"""
    <div style="border:2px solid {qcolor};border-radius:14px;
                padding:14px 18px;background:{qcolor}0d;
                display:flex;justify-content:space-between;align-items:center;">
        <div>
            <div style="font-size:23px;font-weight:800;color:{qcolor};">
                {icon} {quality}
            </div>
            <div style="font-size:14px;">{qmessage}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.caption("Screening indicator based on monitored pH, TDS and turbidity. It does not replace laboratory testing.")

st.divider()

# ================= FIVE FILTERS =================
st.subheader("🧰 Filter Health")
st.caption("Live-style visual status of the five filtration stages")

filter_data = [
    ("Filter 1", "Sediment / Pre-filter", 95),
    ("Filter 2", "Activated Carbon", 88),
    ("Filter 3", "Mineral / Conditioning", 72),
    ("Filter 4", "Fine Filtration", 55),
    ("Filter 5", "Final Disinfection", 35),
]

cols = st.columns(5)

for col, (name, desc, health) in zip(cols, filter_data):
    if health >= 80:
        color = "#16a34a"
        status = "GOOD"
    elif health >= 50:
        color = "#f59e0b"
        status = "WARNING"
    else:
        color = "#dc2626"
        status = "LOW"

    with col:
        st.markdown(
            f"""
            <div class="filter-card" style="--filter-color:{color};">
                <div class="filter-icon">
                    <div class="filter-cap"></div>
                    <div class="filter-body"></div>
                    <div class="filter-foot"></div>
                </div>
                <div class="filter-name">{name}</div>
                <div class="filter-desc">{desc}</div>
                <div class="filter-health" style="color:{color};">{health}%</div>
                <div class="filter-status" style="background:{color};">{status}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.divider()

show_alert_system(latest, filter_data)

st.divider()

left, right = st.columns([2, 1])

with left:
    st.subheader("📈 Sensor History")

    def show_history(unit_name, unit_df):
        st.markdown(f"#### 📡 Sensor Unit {unit_name}")
        if unit_df.empty:
            st.info("No history available.")
            return

        chart_params = [
            ("temperature", "Temperature (°C)"),
            ("tds", "TDS (ppm)"),
            ("ph", "pH"),
            ("turbidity", "Turbidity (NTU)"),
            ("flow_rate", "Flow Rate (L/min)"),
            ("water_level", "Water Level (%)"),
        ]

        # Six graphs are arranged automatically in 2 rows × 3 columns.
        for row_start in range(0, len(chart_params), 3):
            cols = st.columns(3)
            for col, (metric, label) in zip(cols, chart_params[row_start:row_start + 3]):
                with col:
                    fig = px.line(
                        unit_df,
                        x="created_at",
                        y=metric,
                        markers=True,
                        title=label,
                    )
                    fig.update_layout(
                        height=270,
                        margin=dict(l=10, r=10, t=45, b=15),
                        hovermode="x unified",
                    )
                    st.plotly_chart(
                        fig,
                        use_container_width=True,
                        key=f"history_chart_{unit_name}_{metric}",
                    )

    show_history("1", unit1_df)
    st.divider()
    show_history("2", unit2_df)

with right:
    st.subheader("📊 Flow & Water Level")

    if latest is not None:
        st.metric("💦 Flow Rate", f"{safe_float(latest.get('flow_rate', 0)):.2f} L/min")
        level = safe_float(latest.get("water_level", 0))
        level_status = "🟢 NORMAL" if level >= 60 else ("🟡 LOW" if level >= 30 else "🔴 CRITICAL")
        st.metric("🛢 Water Level", f"{level:.1f}%")
        st.write(f"Status: **{level_status}**")

    st.subheader("⚙️ Remote Control")
    st.write("Machine: **ESP32-01**")

    pump = bool(machine_status.get("pump", False))
    valve = bool(machine_status.get("valve", False))

    st.write(f"Pump status: {'🟢 ON' if pump else '🔴 OFF'}")
    if st.button("🔴 Turn Pump OFF", use_container_width=True):
        send_command("esp32-01", "pump", "OFF")
    if st.button("🟢 Turn Pump ON", use_container_width=True):
        send_command("esp32-01", "pump", "ON")

    st.write(f"Valve status: {'🟢 OPEN' if valve else '🔴 CLOSED'}")
    if st.button("🔴 Close Valve", use_container_width=True):
        send_command("esp32-01", "valve", "CLOSE")
    if st.button("🟢 Open Valve", use_container_width=True):
        send_command("esp32-01", "valve", "OPEN")

st.divider()

st.subheader("🗄️ Recent Cloud Data")

st.markdown("#### 📡 Sensor Unit 1")
st.dataframe(
    unit1_df.tail(10).sort_values("created_at", ascending=False),
    use_container_width=True,
    hide_index=True
)

st.markdown("#### 📡 Sensor Unit 2")
st.dataframe(
    unit2_df.tail(10).sort_values("created_at", ascending=False),
    use_container_width=True,
    hide_index=True
)

feedback_section()

st.caption(
    "Safety note: add authentication, device authorization, command validation, "
    "and a fail-safe state before connecting real motors, pumps or valves."
)
