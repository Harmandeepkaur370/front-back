with open('app_backup.py', 'r', encoding='utf-8') as f:
    orig = f.read()

# Cut at the UI section start
ui_start = orig.find('# GRADIO UI')
if ui_start == -1:
    ui_start = orig.find("with gr.Blocks")
while ui_start > 0 and orig[ui_start-1] != '\n':
    ui_start -= 1

kept = orig[:ui_start].rstrip()

new_ui = '''
# ============================================================
# GRADIO UI
# ============================================================
import datetime as _dt

css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* Kill ALL Gradio default spacing */
html, body { margin:0 !important; padding:0 !important; overflow:auto; height:100%; }
body, .gradio-container {
    font-family:'Inter',sans-serif !important;
    background:#F4F7FE !important;
    margin:0 !important; padding:0 !important;
}
.gradio-container { max-width:100% !important; width:100% !important; padding:0 !important; }
.gradio-container > .main { padding:0 !important; margin:0 !important; }
.gradio-container > .main > .wrap { padding:0 !important; margin:0 !important; }
footer,.built-with,.svelte-1lc7rdp { display:none !important; }

/* ── Login ── */
.login-bg {
    min-height:100vh; display:flex; align-items:center; justify-content:center;
    background:radial-gradient(circle at 50% 50%, #4318FF 0%, #0B1437 100%) !important;
    padding:24px;
}
.login-card {
    background:rgba(255,255,255,0.08) !important;
    backdrop-filter:blur(24px) !important;
    border:1px solid rgba(255,255,255,0.15) !important;
    border-radius:32px !important; padding:48px !important;
    width:100% !important; max-width:460px !important;
    box-shadow:0 32px 64px rgba(0,0,0,0.4) !important;
}
.login-title { font-size:28px; font-weight:700; margin-bottom:8px; text-align:center; color:white; }

/* ── App shell ── */
.app-layout {
    display:flex !important; min-height:100vh; width:100%;
    margin:0 !important; padding:0 !important; gap:0 !important;
}

/* ── Sidebar ── */
.sidebar {
    background:#0B1437 !important; min-height:100vh;
    width:260px; flex-shrink:0;
    padding:28px 16px !important; display:flex; flex-direction:column;
    box-shadow:4px 0 24px rgba(0,0,0,0.2); z-index:100;
}
.sidebar-logo {
    display:flex; align-items:center; gap:12px; color:white;
    font-size:20px; font-weight:800; margin-bottom:40px; padding-left:8px;
}
.sidebar-logo-icon {
    background:linear-gradient(135deg,#4318FF,#868CFF);
    width:40px; height:40px; border-radius:12px;
    display:flex; align-items:center; justify-content:center;
    box-shadow:0 4px 12px rgba(67,24,255,0.4);
}

.nav-btn.secondary button, .nav-btn.primary button {
    justify-content:flex-start !important; padding:13px 18px !important;
    border-radius:14px !important; font-size:14px !important; font-weight:600 !important;
    border:none !important; transition:all 0.25s ease !important;
    margin-bottom:6px !important; width:100% !important;
    box-shadow:none !important; text-align:left !important;
    font-family:'Inter',sans-serif !important;
}
.nav-btn.secondary button { background:transparent !important; color:#A3AED0 !important; }
.nav-btn.secondary button:hover { background:rgba(255,255,255,0.07) !important; color:white !important; }
.nav-btn.primary button {
    background:linear-gradient(135deg,#4318FF,#868CFF) !important;
    color:white !important; box-shadow:0 6px 18px rgba(67,24,255,0.35) !important;
}
.logout-btn button { color:#FF5B5B !important; margin-top:auto !important; }
.logout-btn button:hover { background:rgba(255,91,91,0.1) !important; }

/* ── Content ── */
.content-area {
    flex:1; flex-grow:1; padding:28px 36px !important;
    background:#F4F7FE !important; height:100vh; overflow-y:auto;
}

/* Glass cards */
.glass-card {
    background:rgba(255,255,255,0.88) !important;
    backdrop-filter:blur(16px) !important;
    border:1px solid rgba(255,255,255,0.95) !important;
    border-radius:18px !important; padding:24px !important;
    box-shadow:0 4px 20px rgba(0,0,0,0.05) !important;
    margin-bottom:20px !important; transition:all 0.25s ease;
}
.glass-card:hover { box-shadow:0 8px 32px rgba(0,0,0,0.09) !important; transform:translateY(-1px); }

/* Page header */
.page-header { margin-bottom:24px; }
.page-header h2 { font-size:20px; font-weight:700; color:#1a1f36; margin:0 0 4px; }
.page-header p  { font-size:13px; color:#6b7a9d; margin:0; }

/* Group heading inside card */
.group-title {
    font-size:12px; font-weight:700; text-transform:uppercase;
    letter-spacing:0.06em; color:#6b7a9d; margin-bottom:16px;
    padding-bottom:10px; border-bottom:1px solid #eef0f7;
}

/* Inputs */
.gradio-container input[type="text"], .gradio-container input[type="password"],
.gradio-container input[type="number"], .gradio-container textarea,
.gradio-container select {
    border:1.5px solid #E0E5F2 !important; border-radius:12px !important;
    padding:11px 15px !important; font-size:14px !important;
    font-family:'Inter',sans-serif !important;
    background:#ffffff !important; color:#1a1f36 !important;
    box-shadow:none !important; transition:border-color .2s, box-shadow .2s !important;
}
.gradio-container input:focus, .gradio-container textarea:focus {
    border-color:#4318FF !important;
    box-shadow:0 0 0 3px rgba(67,24,255,0.1) !important; outline:none !important;
}
.gradio-container .label-wrap span, .gradio-container label span {
    font-size:12.5px !important; font-weight:600 !important;
    color:#344563 !important; font-family:'Inter',sans-serif !important;
}
.gradio-container input[type="range"] { accent-color:#4318FF !important; }

/* Predict button */
.btn-predict button {
    background:linear-gradient(135deg,#4318FF,#868CFF) !important;
    color:white !important; border-radius:14px !important;
    padding:13px 28px !important; font-weight:700 !important;
    font-family:'Inter',sans-serif !important; font-size:14px !important;
    border:none !important; box-shadow:0 6px 20px rgba(67,24,255,0.32) !important;
    transition:all 0.25s ease !important; cursor:pointer !important;
}
.btn-predict button:hover {
    transform:translateY(-2px) !important;
    box-shadow:0 10px 28px rgba(67,24,255,0.42) !important;
}

/* Login button */
.btn-login button {
    background:linear-gradient(135deg,#4318FF,#868CFF) !important;
    color:white !important; border-radius:14px !important;
    padding:13px 28px !important; font-weight:700 !important;
    font-family:'Inter',sans-serif !important; width:100% !important;
    border:none !important; box-shadow:0 6px 20px rgba(67,24,255,0.32) !important;
    transition:all 0.25s ease !important;
}
.btn-login button:hover { transform:translateY(-1px) !important; }

/* Stats row */
.stats-row {
    display:grid; grid-template-columns:repeat(4,1fr); gap:16px; margin-bottom:20px;
}
.stat-card {
    background:white; border-radius:16px; padding:20px;
    border:1px solid #eef0f7; box-shadow:0 2px 12px rgba(0,0,0,0.04);
    transition:all .25s ease;
}
.stat-card:hover { transform:translateY(-2px); box-shadow:0 6px 20px rgba(0,0,0,0.08); }

/* Dataframe */
.gradio-container table { font-family:'Inter',sans-serif !important; font-size:13px !important; }
.gradio-container th {
    background:#F4F7FE !important; color:#6b7a9d !important;
    font-weight:700 !important; font-size:11px !important;
    text-transform:uppercase !important; letter-spacing:.06em !important;
    padding:10px 16px !important; border-bottom:2px solid #eef0f7 !important;
}
.gradio-container td { padding:12px 16px !important; border-bottom:1px solid #eef0f7 !important; }
.gradio-container tr:hover td { background:#F8FAFF !important; }
"""

def _get_reports():
    import datetime as _dt
    os.makedirs("reports", exist_ok=True)
    files = sorted([f for f in os.listdir("reports") if f.endswith('.pdf')],
                   key=lambda f: os.path.getmtime(os.path.join("reports",f)), reverse=True)
    rows  = [[f, _dt.datetime.fromtimestamp(os.path.getmtime(os.path.join("reports",f))).strftime("%Y-%m-%d %H:%M"),
              os.path.join("reports",f)] for f in files]
    paths = [r[2] for r in rows]
    return gr.update(value=rows), gr.update(choices=paths)

def _do_login(u, p):
    if not (u and p):
        return gr.update(visible=True), gr.update(visible=False), "⚠️ Enter username and password", None
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (u, p))
    if cursor.fetchone():
        return gr.update(visible=False), gr.update(visible=True), "✅ Login successful!", u
    return gr.update(visible=True), gr.update(visible=False), "❌ Invalid credentials", None

def _do_signup(u, p):
    try:
        cursor.execute("INSERT INTO users(username,password) VALUES (?,?)", (u, p))
        conn.commit()
        return "✅ Account created. You may now sign in."
    except:
        return "⚠️ Username already exists."

def _nav(target):
    pages = ["dash","heart","diab","symp","hist","prof"]
    pg_els = [_pg_dash, _pg_heart, _pg_diab, _pg_symp, _pg_hist, _pg_prof]
    btns   = [_nb_dash, _nb_heart, _nb_diab, _nb_symp, _nb_hist, _nb_prof]
    vis   = [gr.update(visible=(target==p)) for p in pages]
    varis = [gr.update(variant=("primary" if target==p else "secondary")) for p in pages]
    return vis + varis

def _dashboard_html():
    return f"""
<div style='font-family:Inter,sans-serif;margin-bottom:8px'>
  <h2 style='font-size:20px;font-weight:700;color:#1a1f36;margin:0 0 4px'>Welcome back 👋</h2>
  <p style='font-size:13px;color:#6b7a9d;margin:0 0 22px'>Clinical intelligence dashboard — real-time metrics</p>
  <div class='stats-row'>
    <div class='stat-card'>
      <div style='font-size:24px;margin-bottom:10px'>❤️</div>
      <div style='font-size:26px;font-weight:700;color:#1a1f36'>{heart_acc*100:.1f}%</div>
      <div style='font-size:12px;color:#6b7a9d;margin-top:3px'>Heart Accuracy</div>
      <span style='display:inline-block;margin-top:8px;background:#f0fdf4;color:#16a34a;font-size:10px;font-weight:700;padding:2px 8px;border-radius:20px'>RF · 200 trees</span>
    </div>
    <div class='stat-card'>
      <div style='font-size:24px;margin-bottom:10px'>🩸</div>
      <div style='font-size:26px;font-weight:700;color:#1a1f36'>{diabetes_acc*100:.1f}%</div>
      <div style='font-size:12px;color:#6b7a9d;margin-top:3px'>Diabetes Accuracy</div>
      <span style='display:inline-block;margin-top:8px;background:#f5f3ff;color:#7c3aed;font-size:10px;font-weight:700;padding:2px 8px;border-radius:20px'>RF · 200 trees</span>
    </div>
    <div class='stat-card'>
      <div style='font-size:24px;margin-bottom:10px'>🧠</div>
      <div style='font-size:26px;font-weight:700;color:#1a1f36'>5</div>
      <div style='font-size:12px;color:#6b7a9d;margin-top:3px'>Symptom Rules</div>
      <span style='display:inline-block;margin-top:8px;background:#eff6ff;color:#2563eb;font-size:10px;font-weight:700;padding:2px 8px;border-radius:20px'>Rule-based</span>
    </div>
    <div class='stat-card'>
      <div style='font-size:24px;margin-bottom:10px'>📋</div>
      <div style='font-size:26px;font-weight:700;color:#1a1f36'>PDF</div>
      <div style='font-size:12px;color:#6b7a9d;margin-top:3px'>Auto Reports</div>
      <span style='display:inline-block;margin-top:8px;background:#fff7ed;color:#c2410c;font-size:10px;font-weight:700;padding:2px 8px;border-radius:20px'>On Predict</span>
    </div>
  </div>
</div>"""

with gr.Blocks(fill_width=True) as app:
    user_state = gr.State(value=None)
    nav_state  = gr.State(value="dash")

    # ── LOGIN ──
    with gr.Column(visible=True, elem_classes="login-bg") as _login_pg:
        with gr.Column(elem_classes="login-card"):
            gr.HTML(\'\'\'
            <div style="text-align:center;margin-bottom:32px">
              <div style="width:64px;height:64px;border-radius:18px;background:linear-gradient(135deg,#4318FF,#868CFF);display:inline-flex;align-items:center;justify-content:center;font-size:32px;color:white;box-shadow:0 8px 24px rgba(67,24,255,0.4);margin-bottom:16px">🏥</div>
              <div style="font-size:26px;font-weight:800;color:white;margin-bottom:6px">AI Hospital System</div>
              <div style="font-size:13px;color:rgba(255,255,255,0.65)">Secure Clinical Intelligence Platform</div>
            </div>\'\'\')
            _u = gr.Textbox(label="Username", placeholder="Enter your staff ID")
            _p = gr.Textbox(label="Password",  placeholder="Enter password", type="password")
            _m = gr.Textbox(label="", interactive=False, show_label=False)
            _lb = gr.Button("Sign In →", elem_classes="btn-login")
            _sb = gr.Button("Create Account")

    # ── APP ──
    with gr.Column(visible=False) as _app_pg:
        with gr.Row(elem_classes="app-layout"):

            # SIDEBAR
            with gr.Column(scale=0, min_width=260, elem_classes="sidebar"):
                gr.HTML(\'\'\'
                <div class="sidebar-logo">
                  <div class="sidebar-logo-icon">🏥</div> IMIS
                </div>\'\'\')
                gr.HTML(\'<div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#4a5568;padding:0 8px 8px">Main Menu</div>\')
                _nb_dash  = gr.Button("📊  Dashboard",            variant="primary",   elem_classes="nav-btn")
                _nb_heart = gr.Button("❤️   Heart Prediction",    variant="secondary", elem_classes="nav-btn")
                _nb_diab  = gr.Button("🩸  Diabetes Prediction",  variant="secondary", elem_classes="nav-btn")
                _nb_symp  = gr.Button("🧠  Symptom Checker",      variant="secondary", elem_classes="nav-btn")
                gr.HTML(\'<div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#4a5568;padding:18px 8px 8px">Records</div>\')
                _nb_hist  = gr.Button("📂  Report History",       variant="secondary", elem_classes="nav-btn")
                _nb_prof  = gr.Button("👤  User Profile",         variant="secondary", elem_classes="nav-btn")
                gr.HTML(\'<div style="flex:1;min-height:60px"></div>\')
                _lo = gr.Button("🚪  Sign Out", elem_classes=["nav-btn","logout-btn"], variant="secondary")

            # MAIN CONTENT
            with gr.Column(elem_classes="content-area"):

                # DASHBOARD
                with gr.Column(visible=True) as _pg_dash:
                    gr.HTML(_dashboard_html())
                    with gr.Row():
                        with gr.Column(elem_classes="glass-card"):
                            gr.HTML(\'<div class="group-title">❤️ Heart Model — Confusion Matrix</div>\')
                            gr.Plot(value=plot_cm(heart_cm, "Heart Disease"))
                        with gr.Column(elem_classes="glass-card"):
                            gr.HTML(\'<div class="group-title">🩸 Diabetes Model — Confusion Matrix</div>\')
                            gr.Plot(value=plot_cm(diabetes_cm, "Diabetes"))

                # HEART
                with gr.Column(visible=False) as _pg_heart:
                    gr.HTML(\'<div class="page-header"><h2>❤️ Heart Disease Risk Assessment</h2><p>Cardiovascular risk prediction using Random Forest AI</p></div>\')
                    with gr.Column(elem_classes="glass-card"):
                        gr.HTML(\'<div class="group-title">Patient Information</div>\')
                        with gr.Row():
                            _ph_n = gr.Textbox(label="Full Name", placeholder="e.g. John Doe")
                            _ph_a = gr.Slider(18,100, value=45, step=1, label="Age (years)")
                            _ph_s = gr.Radio(["Male","Female"], label="Biological Sex", value="Male")
                    with gr.Column(elem_classes="glass-card"):
                        gr.HTML(\'<div class="group-title">Clinical Parameters</div>\')
                        with gr.Row():
                            _ph_cp   = gr.Slider(0,3, step=1, value=1, label="Chest Pain Type (0–3)")
                            _ph_bp   = gr.Slider(80,200, value=120, label="Blood Pressure (mmHg)")
                            _ph_chol = gr.Slider(100,400, value=200, label="Cholesterol (mg/dL)")
                        with gr.Row():
                            _ph_fbs  = gr.Radio([0,1], label="Fasting Blood Sugar >120", value=0)
                            _ph_thal = gr.Slider(70,210, value=150, label="Max Heart Rate")
                    with gr.Column(elem_classes="glass-card"):
                        gr.HTML(\'<div class="group-title">Lifestyle Risk Factors</div>\')
                        with gr.Row():
                            _ph_sm  = gr.Radio([0,1], label="Smoking",          value=0)
                            _ph_ex  = gr.Radio([0,1], label="Regular Exercise", value=1)
                            _ph_dt  = gr.Radio([0,1], label="Healthy Diet",     value=1)
                            _ph_fam = gr.Radio([0,1], label="Family History",   value=0)
                        _ph_btn = gr.Button("🔍 Run Assessment", elem_classes="btn-predict")
                    with gr.Column(elem_classes="glass-card"):
                        gr.HTML(\'<div class="group-title">Prediction Result</div>\')
                        _ph_out  = gr.HTML(\'<p style="color:#a0aec0;font-size:13px">Run assessment to see results.</p>\')
                        _ph_pdf  = gr.File(label="📥 Download PDF Report")
                        with gr.Row():
                            _ph_ch  = gr.Plot(label="Risk Distribution")
                            _ph_cm2 = gr.Plot(label="Confusion Matrix")
                        _ph_met = gr.HTML()

                # DIABETES
                with gr.Column(visible=False) as _pg_diab:
                    gr.HTML(\'<div class="page-header"><h2>🩸 Diabetes Risk Assessment</h2><p>Metabolic risk prediction using Random Forest AI</p></div>\')
                    with gr.Column(elem_classes="glass-card"):
                        gr.HTML(\'<div class="group-title">Patient Information</div>\')
                        with gr.Row():
                            _pd_n = gr.Textbox(label="Full Name", placeholder="e.g. Jane Doe")
                            _pd_a = gr.Slider(18,100, value=40, step=1, label="Age (years)")
                    with gr.Column(elem_classes="glass-card"):
                        gr.HTML(\'<div class="group-title">Metabolic Parameters</div>\')
                        with gr.Row():
                            _pd_pr = gr.Slider(0,15, step=1, value=2, label="Pregnancies")
                            _pd_gl = gr.Slider(70,250, value=110, label="Plasma Glucose")
                            _pd_bp = gr.Slider(40,140, value=72,  label="Diastolic BP")
                        with gr.Row():
                            _pd_bmi = gr.Slider(15,60, value=25, label="BMI")
                            _pd_ins = gr.Slider(0,600, value=80, label="Serum Insulin")
                    with gr.Column(elem_classes="glass-card"):
                        gr.HTML(\'<div class="group-title">Lifestyle Risk Factors</div>\')
                        with gr.Row():
                            _pd_sm  = gr.Radio([0,1], label="Smoking",          value=0)
                            _pd_ex  = gr.Radio([0,1], label="Regular Exercise", value=1)
                            _pd_dt  = gr.Radio([0,1], label="Healthy Diet",     value=1)
                            _pd_fam = gr.Radio([0,1], label="Family History",   value=0)
                        _pd_btn = gr.Button("🔍 Run Assessment", elem_classes="btn-predict")
                    with gr.Column(elem_classes="glass-card"):
                        gr.HTML(\'<div class="group-title">Prediction Result</div>\')
                        _pd_out  = gr.HTML(\'<p style="color:#a0aec0;font-size:13px">Run assessment to see results.</p>\')
                        _pd_pdf  = gr.File(label="📥 Download PDF Report")
                        with gr.Row():
                            _pd_ch  = gr.Plot(label="Risk Distribution")
                            _pd_cm2 = gr.Plot(label="Confusion Matrix")
                        _pd_met = gr.HTML()

                # SYMPTOM
                with gr.Column(visible=False) as _pg_symp:
                    gr.HTML(\'<div class="page-header"><h2>🧠 AI Symptom Checker</h2><p>Rule-based clinical symptom matching engine</p></div>\')
                    with gr.Column(elem_classes="glass-card"):
                        gr.HTML(\'<div class="group-title">Select Reported Symptoms</div>\')
                        _ps_chk = gr.CheckboxGroup(
                            choices=["chest pain","shortness of breath","fatigue","dizziness",
                                     "palpitations","frequent urination","weight loss","blurred vision",
                                     "increased hunger","headache","fever","body ache","pale skin"],
                            label="")
                        _ps_btn = gr.Button("🔍 Analyze Symptoms", elem_classes="btn-predict")
                    with gr.Column(elem_classes="glass-card"):
                        gr.HTML(\'<div class="group-title">Matched Conditions</div>\')
                        _ps_out = gr.HTML(\'<p style="color:#a0aec0;font-size:13px">Select symptoms and analyze.</p>\')

                # REPORT HISTORY
                with gr.Column(visible=False) as _pg_hist:
                    gr.HTML(\'<div class="page-header"><h2>📂 Report History</h2><p>All generated clinical PDF reports</p></div>\')
                    with gr.Column(elem_classes="glass-card"):
                        gr.HTML(\'<div class="group-title">Report Archive</div>\')
                        _hr_btn = gr.Button("🔄 Refresh", elem_classes="btn-predict")
                        _hr_tbl = gr.Dataframe(headers=["Filename","Created At","Path"], interactive=False, wrap=True)
                    with gr.Column(elem_classes="glass-card"):
                        gr.HTML(\'<div class="group-title">Download Report</div>\')
                        _hr_drp = gr.Dropdown(label="Select a report", choices=[])
                        _hr_fl  = gr.File(label="Selected Report")

                # USER PROFILE
                with gr.Column(visible=False) as _pg_prof:
                    gr.HTML(\'<div class="page-header"><h2>👤 Patient History</h2><p>Historical risk assessments from the clinical database</p></div>\')
                    with gr.Column(elem_classes="glass-card"):
                        gr.HTML(\'<div class="group-title">Assessment Log</div>\')
                        _up_btn = gr.Button("🔄 Load Records", elem_classes="btn-predict")
                        _up_tbl = gr.Dataframe(headers=["Patient Name","Age","Disease","Risk Level"], interactive=False, wrap=True)

    # ── WIRES ──
    _all = [_pg_dash,_pg_heart,_pg_diab,_pg_symp,_pg_hist,_pg_prof,
            _nb_dash,_nb_heart,_nb_diab,_nb_symp,_nb_hist,_nb_prof]

    _lb.click(_do_login,  inputs=[_u,_p], outputs=[_login_pg,_app_pg,_m,user_state])
    _sb.click(_do_signup, inputs=[_u,_p], outputs=[_m])
    _lo.click(lambda: (gr.update(visible=True), gr.update(visible=False), None),
              outputs=[_login_pg, _app_pg, user_state])

    _nb_dash.click( lambda:"dash",  outputs=nav_state).then(_nav, inputs=nav_state, outputs=_all)
    _nb_heart.click(lambda:"heart", outputs=nav_state).then(_nav, inputs=nav_state, outputs=_all)
    _nb_diab.click( lambda:"diab",  outputs=nav_state).then(_nav, inputs=nav_state, outputs=_all)
    _nb_symp.click( lambda:"symp",  outputs=nav_state).then(_nav, inputs=nav_state, outputs=_all)
    _nb_hist.click( lambda:"hist",  outputs=nav_state).then(_nav, inputs=nav_state, outputs=_all)
    _nb_prof.click( lambda:"prof",  outputs=nav_state).then(_nav, inputs=nav_state, outputs=_all)

    _ph_btn.click(heart_predict,
        inputs=[user_state,_ph_n,_ph_a,_ph_s,_ph_cp,_ph_bp,_ph_chol,_ph_fbs,_ph_thal,_ph_sm,_ph_ex,_ph_dt,_ph_fam],
        outputs=[_ph_out,_ph_pdf,_ph_ch,_ph_cm2,_ph_met])
    _pd_btn.click(diabetes_predict,
        inputs=[user_state,_pd_n,_pd_a,_pd_pr,_pd_gl,_pd_bp,_pd_bmi,_pd_ins,_pd_sm,_pd_ex,_pd_dt,_pd_fam],
        outputs=[_pd_out,_pd_pdf,_pd_ch,_pd_cm2,_pd_met])
    _ps_btn.click(symptom_checker, inputs=[_ps_chk], outputs=[_ps_out])
    _hr_btn.click(_get_reports, outputs=[_hr_tbl,_hr_drp])
    _hr_drp.change(lambda x:x, inputs=[_hr_drp], outputs=[_hr_fl])
    _up_btn.click(show_history, inputs=[user_state], outputs=[_up_tbl])

app.launch(server_name="127.0.0.1", css=css)
'''

result = kept + '\n' + new_ui

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(result)

print("Successfully written.")
