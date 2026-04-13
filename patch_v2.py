import os

with open('app.py', 'r', encoding='utf-8') as f:
    orig = f.read()

parts = orig.split('# ============================================================\n# GRADIO UI\n# ============================================================')
if len(parts) < 2:
    parts = orig.split('# GRADIO UI')

new_css_and_ui = """
css = '''
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

:root {
  --app-bg: linear-gradient(135deg, #09090E 0%, #15112F 100%);
  --sidebar-bg: rgba(255, 255, 255, 0.02);
  --card-bg: rgba(255, 255, 255, 0.05);
  --glass-border: rgba(255, 255, 255, 0.08);
  --glass-highlight: rgba(255, 255, 255, 0.12);
  --text-primary: #FFFFFF;
  --text-secondary: #9BA1B6;
  --primary-color: #8B5CF6;
  --primary-gradient: linear-gradient(135deg, #6D28D9 0%, #3B82F6 100%);
  --success: #10B981;
  --danger: #EF4444;
}

body, .gradio-container {
    font-family: 'Outfit', sans-serif !important;
    background: var(--app-bg) !important;
    background-attachment: fixed !important;
    margin: 0 !important;
    padding: 0 !important;
    color: var(--text-primary) !important;
}

.gradio-container {
    max-width: 100% !important;
    width: 100% !important;
}

footer, .built-with { display: none !important; }

/* --- Login --- */
.login-bg {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 24px;
}
.login-card {
    background: var(--card-bg) !important;
    backdrop-filter: blur(24px) !important;
    -webkit-backdrop-filter: blur(24px) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 32px !important;
    padding: 48px !important;
    width: 100% !important;
    max-width: 440px !important;
    box-shadow: 0 32px 64px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.1) !important;
}
.login-card label, .login-card span { color: var(--text-secondary) !important; }
.login-card input {
    background: rgba(0,0,0,0.2) !important;
    color: white !important;
    border: 1px solid var(--glass-border) !important;
}

/* --- App Layout --- */
.app-layout {
    display: flex;
    min-height: 100vh;
    width: 100%;
}

/* --- Sidebar --- */
.sidebar {
    background: var(--sidebar-bg) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    min-height: 100vh;
    padding: 32px 24px !important;
    display: flex;
    flex-direction: column;
    border-right: 1px solid var(--glass-border);
    z-index: 100;
}
.sidebar-logo {
    display: flex;
    align-items: center;
    gap: 14px;
    color: white;
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 48px;
}
.sidebar-logo-icon {
    background: var(--primary-gradient);
    width: 44px; height: 44px;
    border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 4px 16px rgba(109, 40, 217, 0.4);
    font-size: 20px;
}

/* Navigation Buttons */
.nav-btn.secondary, .nav-btn.primary {
    justify-content: flex-start !important;
    padding: 16px 20px !important;
    border-radius: 16px !important;
    font-size: 15px !important;
    font-weight: 500 !important;
    border: 1px solid transparent !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    margin-bottom: 12px !important;
    width: 100% !important;
    text-align: left !important;
    box-shadow: none !important;
}
.nav-btn.secondary {
    background: transparent !important;
    color: var(--text-secondary) !important;
}
.nav-btn.secondary:hover {
    background: var(--glass-highlight) !important;
    color: white !important;
    border: 1px solid var(--glass-border) !important;
    transform: translateX(4px);
}
.nav-btn.primary {
    background: var(--glass-highlight) !important;
    border: 1px solid var(--primary-color) !important;
    color: white !important;
    box-shadow: 0 8px 24px rgba(0,0,0,0.2), inset 0 0 12px rgba(139,92,246,0.2) !important;
}

.logout-btn {
    margin-top: auto !important;
    color: var(--danger) !important;
}
.logout-btn:hover {
    background: rgba(239, 68, 68, 0.1) !important;
    border-color: rgba(239, 68, 68, 0.3) !important;
}

/* --- Content Area --- */
.content-area {
    flex-grow: 1;
    padding: 40px 56px !important;
    height: 100vh;
    overflow-y: auto;
}

/* Top Header */
.top-header {
    background: var(--card-bg);
    backdrop-filter: blur(16px);
    border: 1px solid var(--glass-border);
    border-radius: 24px;
    padding: 24px 32px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 40px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.2);
}

/* Glass Cards */
.glass-card {
    background: var(--card-bg) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 24px !important;
    padding: 32px !important;
    box-shadow: 0 12px 40px rgba(0,0,0,0.2) !important;
    margin-bottom: 24px !important;
    transition: all 0.3s ease;
}
.glass-card:hover { border-color: rgba(255,255,255,0.15) !important; }

/* Dashboard Grids */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 24px;
    margin-bottom: 40px;
}
.stat-card-custom {
    background: var(--card-bg);
    backdrop-filter: blur(12px);
    border: 1px solid var(--glass-border);
    border-radius: 24px;
    padding: 24px;
    display: flex;
    align-items: center;
    gap: 20px;
    transition: transform 0.3s ease, border-color 0.3s;
}
.stat-card-custom:hover {
    transform: translateY(-5px);
    border-color: rgba(255,255,255,0.2);
}
.stat-val { font-size: 32px; font-weight: 700; color: white; line-height: 1.1; }
.stat-label { font-size: 14px; color: var(--text-secondary); margin-top: 4px; }
.stat-icon-wrap {
    width: 56px; height: 56px;
    border-radius: 16px;
    display: flex; align-items: center; justify-content: center;
    font-size: 24px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.05);
}

/* Dataframe glass table */
.gradio-container .gr-dataframe {
    background: transparent !important;
    border: none !important;
    border-radius: 16px !important;
    overflow: hidden !important;
}
.gradio-container .gr-dataframe th {
    background: rgba(255,255,255,0.08) !important;
    color: white !important;
    font-weight: 600 !important;
    border-bottom: 1px solid rgba(255,255,255,0.1) !important;
    padding: 16px !important;
}
.gradio-container .gr-dataframe td {
    background: rgba(255,255,255,0.02) !important;
    color: var(--text-secondary) !important;
    border-bottom: 1px solid rgba(255,255,255,0.05) !important;
    padding: 16px !important;
}
.gradio-container .gr-dataframe tr:hover td { background: rgba(255,255,255,0.05) !important; }

/* Base Inputs & Controls */
.gradio-container input[type="text"],
.gradio-container input[type="number"],
.gradio-container textarea,
.gradio-container select,
.gr-textbox input,
.gr-box, .file-preview {
    border-radius: 14px !important;
    border: 1px solid var(--glass-border) !important;
    background: rgba(0,0,0,0.2) !important;
    padding: 14px 18px !important;
    color: white !important;
    font-size: 14px !important;
    box-shadow: none !important;
    backdrop-filter: blur(8px) !important;
}
.gradio-container input:focus, .gr-textbox input:focus {
    border-color: var(--primary-color) !important;
    box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.15) !important;
    outline: none !important;
}
.gradio-container label, .gradio-container span {
    font-weight: 500 !important;
    color: var(--text-secondary) !important;
    font-size: 13px !important;
}

/* Buttons */
.btn-predict {
    background: var(--primary-gradient) !important;
    color: white !important;
    border-radius: 16px !important;
    padding: 16px 28px !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    box-shadow: 0 8px 32px rgba(109, 40, 217, 0.4) !important;
    transition: all 0.3s ease !important;
}
.btn-predict:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 40px rgba(109, 40, 217, 0.6) !important;
}

/* Typography styles */
h2 { color: white !important; font-size: 28px !important; font-weight: 700 !important; margin: 0 0 8px 0 !important; }
p.desc { color: var(--text-secondary) !important; margin-bottom: 32px !important; font-size: 15px !important; }

/* Radio Checkboxes */
.gr-radio, .gr-checkboxgroup label {
    background: rgba(0,0,0,0.2) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 12px !important;
}
'''

# Update Dashboard HTML
def dashboard_stats_html():
    return f"""
    <div class='stats-grid'>
        <div class='stat-card-custom'>
            <div class='stat-icon-wrap' style='color:#3B82F6'>👤</div>
            <div>
                <div class='stat-val'>System Active</div>
                <div class='stat-label'>Database Status</div>
            </div>
        </div>
        <div class='stat-card-custom'>
            <div class='stat-icon-wrap' style='color:#EF4444'>❤️</div>
            <div>
                <div class='stat-val'>{heart_acc*100:.1f}%</div>
                <div class='stat-label'>Heart ML Accuracy</div>
            </div>
        </div>
        <div class='stat-card-custom'>
            <div class='stat-icon-wrap' style='color:#8B5CF6'>🩸</div>
            <div>
                <div class='stat-val'>{diabetes_acc*100:.1f}%</div>
                <div class='stat-label'>Diabetes ML Accuracy</div>
            </div>
        </div>
        <div class='stat-card-custom'>
            <div class='stat-icon-wrap' style='color:#10B981'>🧠</div>
            <div>
                <div class='stat-val'>Analytics</div>
                <div class='stat-label'>Real-time Process</div>
            </div>
        </div>
    </div>
    """

with gr.Blocks(css=css, theme=gr.themes.Base(), fill_width=True) as app:
    user_state = gr.State()
    nav_state = gr.State("dashboard")

    # ── LOGIN PAGE ──
    with gr.Column(visible=True, elem_classes="login-bg") as login_page:
        with gr.Column(elem_classes="login-card"):
            gr.HTML('''
            <div style="text-align:center;margin-bottom:32px">
                <div style="width:72px;height:72px;border-radius:20px;background:linear-gradient(135deg,#6D28D9,#3B82F6);display:inline-flex;align-items:center;justify-content:center;font-size:32px;color:white;box-shadow:0 8px 32px rgba(109,40,217,0.4);margin-bottom:20px">🏥</div>
                <div style="font-size:32px;font-weight:700;color:white;margin-bottom:8px;letter-spacing:-0.5px">Nexus Health</div>
                <div style="color:#9BA1B6;font-size:15px">Intelligent Clinical Predictions</div>
            </div>
            ''')
            username_input = gr.Textbox(label="👤 Operator ID", placeholder="Enter username")
            password_input = gr.Textbox(label="🔒 Security Key", placeholder="Enter password", type="password")
            login_msg      = gr.Textbox(label="", interactive=False, show_label=False)
            login_btn  = gr.Button("Authenticate", elem_classes="btn-predict")
            signup_btn = gr.Button("Register New Operator")

    # ── APP FRAME ──
    with gr.Column(visible=False) as dashboard:
        with gr.Row(elem_classes="app-layout"):
            
            # SIDEBAR
            with gr.Column(scale=0, min_width=280, elem_classes="sidebar"):
                gr.HTML('''
                <div class="sidebar-logo">
                    <div class="sidebar-logo-icon">🏥</div>
                    <div>
                        <div style="font-size:22px;line-height:1">Nexus Health</div>
                        <div style="font-size:11px;color:#9BA1B6;font-weight:400;margin-top:4px;letter-spacing:1px;text-transform:uppercase">Secure System</div>
                    </div>
                </div>
                ''')
                
                nav_btn_dash = gr.Button("📊 Control Center", elem_classes="nav-btn", variant="primary")
                nav_btn_heart = gr.Button("❤️ Heart Assessment", elem_classes="nav-btn", variant="secondary")
                nav_btn_diabetes = gr.Button("🩸 Metabolic Analysis", elem_classes="nav-btn", variant="secondary")
                nav_btn_symptom = gr.Button("🧠 Symptom Intelligence", elem_classes="nav-btn", variant="secondary")
                nav_btn_history = gr.Button("📜 Report History", elem_classes="nav-btn", variant="secondary")
                
                gr.HTML("<div style='flex-grow:1; min-height: 50vh;'></div>")
                
                gr.HTML('''
                <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.05);border-radius:16px;padding:16px;margin-bottom:16px;text-align:center">
                    <div style="font-size:12px;color:#9BA1B6;margin-bottom:8px">System Status</div>
                    <div style="color:#10B981;font-weight:600;font-size:14px;display:flex;align-items:center;justify-content:center;gap:6px">
                        <span style="width:8px;height:8px;background:#10B981;border-radius:50%;box-shadow:0 0 10px #10B981"></span> Online & Secure
                    </div>
                </div>
                ''')
                logout_btn = gr.Button("🚪 Terminate Session", elem_classes=["nav-btn", "logout-btn"])

            # MAIN CONTENT
            with gr.Column(scale=1, elem_classes="content-area"):
                
                gr.HTML('''
                <div class="top-header">
                    <div>
                        <div style="font-size:24px;font-weight:700;color:white">Command Interface</div>
                        <div style="color:#9BA1B6;font-size:14px">Real-time clinical intelligence platform</div>
                    </div>
                    <div style="display:flex;align-items:center;gap:12px;background:rgba(255,255,255,0.05);padding:8px 16px;border-radius:100px;border:1px solid rgba(255,255,255,0.1)">
                        <span style="width:32px;height:32px;background:linear-gradient(135deg,#6D28D9,#3B82F6);border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:600;color:white;font-size:14px">OP</span>
                        <span style="color:white;font-weight:500;font-size:14px">Active Operator</span>
                    </div>
                </div>
                ''')
                
                # PAGE: DASHBOARD
                with gr.Column(visible=True) as page_dashboard:
                    gr.HTML(dashboard_stats_html())
                    with gr.Row():
                        with gr.Column(elem_classes="glass-card"):
                            gr.HTML("<h3 style='color:white;margin:0 0 16px 0'>❤️ Heart Model Performance</h3>")
                            gr.Plot(value=plot_cm(heart_cm, "Heart Disease Confusion Matrix"))
                        with gr.Column(elem_classes="glass-card"):
                            gr.HTML("<h3 style='color:white;margin:0 0 16px 0'>🩸 Diabetes Model Performance</h3>")
                            gr.Plot(value=plot_cm(diabetes_cm, "Diabetes Confusion Matrix"))

                # PAGE: HEART
                with gr.Column(visible=False) as page_heart:
                    gr.HTML("<h2>❤️ Heart Disease Risk Assessment</h2><p class='desc'>Input clinical biometrics to compute probabilistic cardiovascular risk using Random Forest architecture.</p>")
                    with gr.Column(elem_classes="glass-card"):
                        with gr.Row():
                            patient_name   = gr.Textbox(label="Patient Key/Name")
                            patient_age    = gr.Slider(18, 100, value=45, label="Age (years)")
                            patient_sex    = gr.Radio(["Male","Female"], label="Biological Sex", value="Male")
                        with gr.Row():
                            cp      = gr.Slider(0, 3, step=1, value=1, label="Chest Pain Index (0–3)")
                            bp      = gr.Slider(80, 200, value=120, label="Resting BP (mmHg)")
                            chol    = gr.Slider(100, 400, value=200, label="Serum Cholesterol (mg/dL)")
                        with gr.Row():
                            fbs     = gr.Radio([0, 1], label="Fasting Sugar > 120", value=0)
                            thalach = gr.Slider(70, 210, value=150, label="Max Heart Rate Achieved")
                        
                        gr.HTML("<h4 style='color:white;margin:24px 0 16px;border-bottom:1px solid rgba(255,255,255,0.1);padding-bottom:8px'>Lifestyle Metadata</h4>")
                        
                        with gr.Row():
                            patient_smoking  = gr.Radio([0,1], label="Tobacco Use", value=0)
                            patient_exercise = gr.Radio([0,1], label="Physical Activity", value=1)
                            patient_diet     = gr.Radio([0,1], label="Regimented Diet", value=1)
                            patient_family   = gr.Radio([0,1], label="Family History", value=0)
                        
                        gr.HTML("<br>")
                        heart_btn = gr.Button("⚡ Initialize ML Prediction", elem_classes="btn-predict")
                        
                    with gr.Column(elem_classes="glass-card"):
                        gr.HTML("<h3 style='color:white;margin-top:0'>Prediction Core Output</h3>")
                        heart_out     = gr.HTML()
                        heart_pdf     = gr.File(label="📥 Export Encrypted PDF Report")
                        with gr.Row():
                            heart_chart   = gr.Plot(label="Risk Distribution")
                            heart_cm_plot = gr.Plot(label="Diagnostic Mapping")
                        heart_metrics = gr.HTML()

                # PAGE: DIABETES
                with gr.Column(visible=False) as page_diabetes:
                    gr.HTML("<h2>🩸 Metabolic Risk Analysis (Diabetes)</h2><p class='desc'>Assess probability factors for metabolic syndromes and indicators.</p>")
                    with gr.Column(elem_classes="glass-card"):
                        with gr.Row():
                            d_name = gr.Textbox(label="Patient Key/Name")
                            d_age  = gr.Slider(18, 100, value=40, label="Age (years)")
                        with gr.Row():
                            preg    = gr.Slider(0, 15, step=1, value=2, label="Pregnancies")
                            glucose = gr.Slider(70, 250, value=110, label="Plasma Glucose Level")
                            dbp     = gr.Slider(40, 140, value=72, label="Diastolic Blood Pressure")
                        with gr.Row():
                            bmi     = gr.Slider(15, 60, value=25, label="Body Mass Index")
                            insulin = gr.Slider(0, 600, value=80, label="Serum Insulin")
                        
                        gr.HTML("<h4 style='color:white;margin:24px 0 16px;border-bottom:1px solid rgba(255,255,255,0.1);padding-bottom:8px'>Lifestyle Metadata</h4>")
                        
                        with gr.Row():
                            d_smoking  = gr.Radio([0,1], label="Tobacco Use", value=0)
                            d_exercise = gr.Radio([0,1], label="Physical Activity", value=1)
                            d_diet     = gr.Radio([0,1], label="Regimented Diet", value=1)
                            d_family   = gr.Radio([0,1], label="Family History", value=0)

                        gr.HTML("<br>")
                        diabetes_btn = gr.Button("⚡ Initialize ML Prediction", elem_classes="btn-predict")
                        
                    with gr.Column(elem_classes="glass-card"):
                        gr.HTML("<h3 style='color:white;margin-top:0'>Prediction Core Output</h3>")
                        diabetes_out     = gr.HTML()
                        diabetes_pdf     = gr.File(label="📥 Export Encrypted PDF Report")
                        with gr.Row():
                            diabetes_chart   = gr.Plot(label="Risk Distribution")
                            diabetes_cm_plot = gr.Plot(label="Diagnostic Mapping")
                        diabetes_metrics = gr.HTML()

                # PAGE: SYMPTOM
                with gr.Column(visible=False) as page_symptom:
                    gr.HTML("<h2>🧠 Symptom Intelligence Engine</h2><p class='desc'>Cross-reference observable patient symptoms against differential databases.</p>")
                    with gr.Column(elem_classes="glass-card"):
                        symptoms = gr.CheckboxGroup(
                            choices=["chest pain","shortness of breath","fatigue","dizziness","palpitations","frequent urination","weight loss","blurred vision","increased hunger","headache","fever","body ache","pale skin"],
                            label="Select Observable Symptoms",
                            elem_classes="gr-checkboxgroup"
                        )
                        symptom_btn = gr.Button("⚡ Execute Pattern Match", elem_classes="btn-predict")
                        
                    with gr.Column(elem_classes="glass-card"):
                        gr.HTML("<h3 style='color:white;margin:0 0 16px'>Match Results</h3>")
                        symptom_output = gr.HTML()

                # PAGE: REPORT HISTORY
                with gr.Column(visible=False) as page_history:
                    gr.HTML("<h2>📜 Master Report History</h2><p class='desc'>Chronological log of unified clinical predictions mapped to operators.</p>")
                    with gr.Column(elem_classes="glass-card"):
                        history_btn   = gr.Button("🔄 Sync Database", elem_classes="btn-predict")
                        gr.HTML("<br>")
                        history_table = gr.Dataframe(headers=["Patient Name","Age","Disease Category","Computed Risk Level"], wrap=True)

    # ── LOGIC ──
    # Page Navigation Mapping
    def render_page(p_name):
        return [
            gr.update(visible=(p_name=="dashboard")),
            gr.update(visible=(p_name=="heart")),
            gr.update(visible=(p_name=="diabetes")),
            gr.update(visible=(p_name=="symptom")),
            gr.update(visible=(p_name=="history")),
            gr.update(variant="primary" if p_name=="dashboard" else "secondary"),
            gr.update(variant="primary" if p_name=="heart" else "secondary"),
            gr.update(variant="primary" if p_name=="diabetes" else "secondary"),
            gr.update(variant="primary" if p_name=="symptom" else "secondary"),
            gr.update(variant="primary" if p_name=="history" else "secondary")
        ]
        
    nav_outputs = [page_dashboard, page_heart, page_diabetes, page_symptom, page_history, nav_btn_dash, nav_btn_heart, nav_btn_diabetes, nav_btn_symptom, nav_btn_history]

    nav_btn_dash.click(lambda: "dashboard", outputs=nav_state).then(render_page, inputs=nav_state, outputs=nav_outputs)
    nav_btn_heart.click(lambda: "heart", outputs=nav_state).then(render_page, inputs=nav_state, outputs=nav_outputs)
    nav_btn_diabetes.click(lambda: "diabetes", outputs=nav_state).then(render_page, inputs=nav_state, outputs=nav_outputs)
    nav_btn_symptom.click(lambda: "symptom", outputs=nav_state).then(render_page, inputs=nav_state, outputs=nav_outputs)
    nav_btn_history.click(lambda: "history", outputs=nav_state).then(render_page, inputs=nav_state, outputs=nav_outputs)

    # Core Action Logic
    login_btn.click(login, inputs=[username_input, password_input], outputs=[dashboard, login_page, login_msg, user_state])
    signup_btn.click(signup, inputs=[username_input, password_input], outputs=[login_msg])
    logout_btn.click(logout, outputs=[dashboard, login_page])
    
    heart_btn.click(heart_predict, inputs=[user_state, patient_name, patient_age, patient_sex, cp, bp, chol, fbs, thalach, patient_smoking, patient_exercise, patient_diet, patient_family], outputs=[heart_out, heart_pdf, heart_chart, heart_cm_plot, heart_metrics])
    
    diabetes_btn.click(diabetes_predict, inputs=[user_state, d_name, d_age, preg, glucose, dbp, bmi, insulin, d_smoking, d_exercise, d_diet, d_family], outputs=[diabetes_out, diabetes_pdf, diabetes_chart, diabetes_cm_plot, diabetes_metrics])
    
    symptom_btn.click(symptom_checker, inputs=[symptoms], outputs=[symptom_output])
    history_btn.click(show_history, inputs=[user_state], outputs=[history_table])

app.launch(server_name="127.0.0.1")
"""

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(parts[0] + '# ============================================================\n# GRADIO UI\n# ============================================================\n' + new_css_and_ui)

print("Patching V2 Complete.")
