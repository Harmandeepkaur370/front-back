import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay, precision_score, recall_score, f1_score
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
import os
import datetime
from reportlab.lib.units import inch

# HELPERS
# ============================================================

def lifestyle_modifier(prob, smoking, exercise, diet, family):
    if smoking == 1:  prob += 0.08
    if exercise == 0: prob += 0.07
    if diet == 0:     prob += 0.05
    if family == 1:   prob += 0.10
    return min(prob, 1)

def risk_pie_chart(prob):
    risk_pct  = int(prob * 100)
    safe_pct  = 100 - risk_pct
    fig, ax = plt.subplots(figsize=(3.5, 3.5), facecolor='none')
    wedge_props = {'linewidth': 2, 'edgecolor': 'white'}
    ax.pie(
        [risk_pct, safe_pct],
        labels=[f"Risk {risk_pct}%", f"Safe {safe_pct}%"],
        colors=["#F43F5E", "#60A5FA"],
        autopct='%1.1f%%', startangle=90,
        wedgeprops=wedge_props,
        textprops={'fontfamily': 'DM Sans', 'fontsize': 11}
    )
    ax.set_title("Disease Risk Assessment", fontsize=13, fontweight='600', pad=14,
                 fontfamily='DM Sans', color='#334155')
    return fig

def plot_cm(cm, title):
    fig, ax = plt.subplots(figsize=(4.5, 4), facecolor='none')
    ConfusionMatrixDisplay(cm).plot(ax=ax, colorbar=False)
    ax.set_title(title, fontsize=13, fontweight='600', pad=12,
                 fontfamily='DM Sans', color='#334155')
    fig.patch.set_alpha(0)
    return fig

def cm_metrics(cm, y_true, y_pred):
    TP = cm[1,1]; TN = cm[0,0]; FP = cm[0,1]; FN = cm[1,0]
    precision    = precision_score(y_true, y_pred)
    recall       = recall_score(y_true, y_pred)
    f1           = f1_score(y_true, y_pred)
    accuracy     = accuracy_score(y_true, y_pred)
    specificity  = TN / (TN + FP) if (TN + FP) != 0 else 0
    npv          = TN / (TN + FN) if (TN + FN) != 0 else 0
    fpr          = FP / (FP + TN) if (FP + TN) != 0 else 0
    fnr          = FN / (FN + TP) if (FN + TP) != 0 else 0

    def row(label, val, note):
        return f"<tr><td style='padding:9px 14px;font-size:13px;color:#475569;font-weight:500'>{label}</td><td style='padding:9px 14px;font-size:13px;color:#1E293B;font-weight:600;text-align:right'>{val}</td><td style='padding:9px 14px;font-size:12px;color:#94A3B8;text-align:right'>{note}</td></tr>"

    html = """
    <div style='font-family:DM Sans,sans-serif;background:white;border-radius:14px;border:1px solid #E2E8F0;overflow:hidden;margin-top:8px'>
      <div style='padding:16px 20px;border-bottom:1px solid #F1F5F9;background:#F8FAFC'>
        <h3 style='font-size:15px;font-weight:600;color:#1E293B;margin:0'>Model Performance Metrics</h3>
        <p style='font-size:12px;color:#94A3B8;margin:2px 0 0'>Confusion matrix analysis</p>
      </div>
      <div style='padding:8px'>
        <div style='display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:12px'>
    """
    def kpi(label, val, color, icon):
        return f"""<div style='background:{color}20;border-radius:10px;padding:14px;border:1px solid {color}30'>
          <div style='font-size:22px;font-weight:700;color:{color};margin-bottom:3px'>{val}</div>
          <div style='font-size:12px;color:#64748B;font-weight:500'>{icon} {label}</div>
        </div>"""
    html += kpi("Accuracy",  f"{accuracy*100:.1f}%",   "#3B82F6", "🎯")
    html += kpi("Precision", f"{precision*100:.1f}%",  "#8B5CF6", "🔬")
    html += kpi("Recall",    f"{recall*100:.1f}%",     "#22C55E", "📡")
    html += kpi("F1-Score",  f"{f1*100:.1f}%",         "#F59E0B", "⚖️")
    html += "</div><table style='width:100%;border-collapse:collapse'>"
    html += row("True Positive (TP)",  TP,  "Correctly predicted positive")
    html += row("True Negative (TN)",  TN,  "Correctly predicted negative")
    html += row("False Positive (FP)", FP,  "Incorrectly predicted positive")
    html += row("False Negative (FN)", FN,  "Incorrectly predicted negative")
    html += row("Specificity",  f"{specificity*100:.1f}%", "Actual negatives identified")
    html += row("NPV",          f"{npv*100:.1f}%",          "Predicted negatives correct")
    html += row("FPR",          f"{fpr*100:.1f}%",          "Negatives predicted as positive")
    html += row("FNR",          f"{fnr*100:.1f}%",          "Positives missed")
    html += "</table></div></div>"
    return html

def precautions(disease, risk):
    if disease == "Heart Disease":
        if risk == "LOW":      tips = ["Regular aerobic exercise (30 min/day)", "Heart-healthy diet (fruits, vegetables, whole grains)", "Avoid smoking and second-hand smoke"]
        elif risk == "MODERATE": tips = ["Monitor blood pressure weekly", "Reduce cholesterol through diet", "Schedule doctor checkup within a month"]
        else:                  tips = ["Immediate cardiologist consultation", "Strict medication adherence", "ECG and stress test recommended"]
    else:
        if risk == "LOW":      tips = ["Balanced low-GI diet", "30-min daily exercise routine", "Maintain healthy body weight"]
        elif risk == "MODERATE": tips = ["Reduce sugar and refined carbs", "Monitor blood glucose bi-weekly", "Consult a nutritionist"]
        else:                  tips = ["Consult endocrinologist immediately", "Daily glucose monitoring required", "Insulin therapy evaluation"]

    items = "".join(f"<li style='padding:8px 0;border-bottom:1px solid #F1F5F9;font-size:13px;color:#475569;display:flex;gap:12px;align-items:flex-start;'><span style='color:#2563EB;'>&rarr;</span><span>{t}</span></li>" for t in tips)
    return f"""<div style='font-family:Inter,sans-serif;background:white;border-radius:12px;padding:24px;border:1px solid #E2E8F0;margin-top:12px'>
      <h4 style='font-size:14px;font-weight:600;color:#0F172A;margin:0 0 12px 0;'>Clinical Recommendations</h4>
      <ul style='list-style:none;padding:0;margin:0'>{items}</ul>
    </div>"""

def generate_report(prob, disease, name, age, measurements):
    percent = int(prob * 100)
    if percent < 30:   risk = "LOW";      color = "#16A34A"; bg = "#F0FDF4"; border = "#DCFCE7"
    elif percent < 70: risk = "MODERATE"; color = "#EA580C"; bg = "#FFF7ED"; border = "#FFEDD5"
    else:              risk = "HIGH";     color = "#DC2626"; bg = "#FEF2F2"; border = "#FEE2E2"

    badge = f"<span style='display:inline-block;background:{color}1A;color:{color};border:1px solid {color}33;border-radius:6px;padding:4px 12px;font-size:12px;font-weight:700'>{risk} RISK &bull; {percent}%</span>"

    rows = "".join(f"<tr><td style='padding:10px 16px;font-size:13px;color:#64748B;font-weight:500;border-bottom:1px solid #F1F5F9;'>{k}</td><td style='padding:10px 16px;font-size:13px;color:#0F172A;font-weight:600;border-bottom:1px solid #F1F5F9;text-align:right;'>{v}</td></tr>" for k,v in measurements.items())

    html = f"""
    <div style='font-family:Inter,sans-serif;background:white;border-radius:12px;border:1px solid {border};margin-bottom:24px;box-shadow:0 1px 3px rgba(0,0,0,0.05);overflow:hidden;'>
      <div style='background:{bg};padding:24px;border-bottom:1px solid {border};display:flex;justify-content:space-between;align-items:flex-start;'>
        <div>
          <h2 style='font-size:18px;font-weight:600;color:#0F172A;margin:0 0 4px 0;'>Diagnostic Result Card</h2>
          <p style='font-size:13px;color:#475569;margin:0;'>{disease} &bull; Patient: {name} ({age})</p>
        </div>
        <div>
          {badge}
        </div>
      </div>
      <div style='padding:0;'>
        <table style='width:100%;border-collapse:collapse;margin:0;'>
          {rows}
        </table>
      </div>
    </div>
    """
    html += precautions(disease, risk)
    return html, risk

def create_pdf(user, name, age, disease, risk, measurements, prob):
    os.makedirs("reports", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file = os.path.join("reports", f"{user}_{name}_{disease}_{timestamp}_report.pdf")
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(file, pagesize=(8.27*inch, 11.69*inch))
    elements = []
    elements.append(Paragraph("AI MULTI-SPECIALITY HOSPITAL", styles["Title"]))
    elements.append(Paragraph("Comprehensive Medical Risk Assessment Report",
                               ParagraphStyle("Center", alignment=TA_CENTER, fontSize=16, spaceAfter=10)))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(f"Patient Name: {name}", styles["Normal"]))
    elements.append(Paragraph(f"Age: {age}", styles["Normal"]))
    elements.append(Paragraph(f"Disease Assessed: {disease}", styles["Normal"]))
    elements.append(Spacer(1, 10))
    data = [["Factor","Value"]] + [[k, str(v)] for k,v in measurements.items()]
    table = Table(data, colWidths=[200, 200])
    table.setStyle(TableStyle([
        ("GRID",       (0,0),(-1,-1), 1, colors.grey),
        ("BACKGROUND", (0,0),(-1,0),   colors.lightblue),
        ("ALIGN",      (0,0),(-1,-1),  "CENTER")
    ]))
    elements.append(table)
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(f"Risk Assessment: {int(prob*100)}% ({risk})", styles["Normal"]))
    doc.build(elements)
    return file
