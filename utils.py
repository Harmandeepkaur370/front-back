import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay, precision_score, recall_score, f1_score
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib import colors
import os
import datetime
import uuid
import random
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.graphics.shapes import Drawing, Rect, Line
from reportlab.graphics.barcode import qr

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
        textprops={'fontfamily': 'DejaVu Sans', 'fontsize': 11}
    )
    ax.set_title("Disease Risk Assessment", fontsize=13, fontweight='600', pad=14,
                 fontfamily='DejaVu Sans', color='#334155')
    return fig

def plot_cm(cm, title):
    fig, ax = plt.subplots(figsize=(4.5, 4), facecolor='none')
    ConfusionMatrixDisplay(cm).plot(ax=ax, colorbar=False)
    ax.set_title(title, fontsize=13, fontweight='600', pad=12,
                 fontfamily='DejaVu Sans', color='#334155')
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

    items = "".join(f"<li style='padding:8px 0;border-bottom:1px solid #F1F5F9;font-size:13px;color:#475569;display:flex;gap:12px;align-items:flex-start;'><span style='color:#2563EB;'>&rarr;</span><span>{t}</span></li>" for t in tips)
    return f"""<div style='font-family:Inter,sans-serif;background:white;border-radius:12px;padding:24px;border:1px solid #E2E8F0;margin-top:12px'>
      <h4 style='font-size:14px;font-weight:600;color:#0F172A;margin:0 0 12px 0;'>Clinical Recommendations</h4>
      <ul style='list-style:none;padding:0;margin:0'>{items}</ul>
    </div>"""

CLINICAL_RANGES = {
    "Blood Pressure": {"range": "80-120", "unit": "mmHg"},
    "Cholesterol": {"range": "< 200", "unit": "mg/dL"},
    "Glucose": {"range": "70-140", "unit": "mg/dL"},
    "BMI": {"range": "18.5-24.9", "unit": "kg/m\u00b2"},
    "Insulin": {"range": "0-150", "unit": "uIU/mL"},
    "Max Heart Rate": {"range": "70-200", "unit": "bpm"},
    "Fasting Blood Sugar >120": {"range": "No (0)", "unit": ""},
    "Pregnancies": {"range": "0-5", "unit": ""},
    "Age": {"range": "18-100", "unit": "yr"},
    "Chest Pain": {"range": "Type 0", "unit": ""},
}

def get_precautions_text(disease, risk):
    if disease == "Heart Disease":
        if risk == "LOW":      return ["Regular aerobic exercise (30 min/day)", "Heart-healthy diet (fruits, vegetables, whole grains)", "Avoid smoking and second-hand smoke"]
        elif risk == "MODERATE": return ["Monitor blood pressure weekly", "Reduce cholesterol through diet", "Schedule doctor checkup within a month"]
        else:                  return ["Immediate cardiologist consultation", "Strict medication adherence", "ECG and stress test recommended"]
    else:
        if risk == "LOW":      return ["Balanced low-GI diet", "30-min daily exercise routine", "Maintain healthy body weight"]
        elif risk == "MODERATE": return ["Reduce sugar and refined carbs", "Monitor blood glucose bi-weekly", "Consult a nutritionist"]
        else:                  return ["Consult endocrinologist immediately", "Daily glucose monitoring required", "Insulin therapy evaluation"]

def get_doctor_info():
    names = ["Aravind Sharma", "Priya Nair", "Vikram Rathore", "Sanjay Gupta", "Ananya Verma"]
    return {
        "name": f"Dr. {random.choice(names)}",
        "reg": f"MC/REG/{random.randint(10000, 99999)}",
        "degree": "MBBS, MD - General Physician"
    }

def precautions_html(disease, risk):
    tips = get_precautions_text(disease, risk)
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
    html += precautions_html(disease, risk)
    return html, risk

def create_pdf(user, name, age, gender, disease, risk, measurements, prob):
    os.makedirs("reports", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename_ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join("reports", f"{user}_{name}_{disease}_{filename_ts}_report.pdf")
    patient_id = f"PAT-{str(uuid.uuid4())[:8].upper()}"

    PAGE_W, PAGE_H = A4  # 595.27 x 841.89 pts
    MARGIN_LR = 32
    MARGIN_TB = 28
    CONTENT_W = PAGE_W - 2 * MARGIN_LR  # ~531 pts

    doc = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        rightMargin=MARGIN_LR,
        leftMargin=MARGIN_LR,
        topMargin=MARGIN_TB,
        bottomMargin=MARGIN_TB,
    )
    elements = []
    styles = getSampleStyleSheet()

    # ── Custom Styles (compact) ──────────────────────────────────
    styles.add(ParagraphStyle(
        name='HospitalName', fontSize=16, fontName='Helvetica-Bold',
        textColor=colors.HexColor("#008080"), leading=18, spaceAfter=0))
    styles.add(ParagraphStyle(
        name='HospitalTagline', fontSize=7, fontName='Helvetica',
        textColor=colors.HexColor("#64748B"), leading=9, spaceAfter=0))
    styles.add(ParagraphStyle(
        name='ContactInfo', fontSize=7.5, fontName='Helvetica',
        textColor=colors.HexColor("#475569"), leading=10, alignment=TA_RIGHT))
    styles.add(ParagraphStyle(
        name='HospitalSub', fontSize=8.5, textColor=colors.grey,
        spaceAfter=4, spaceBefore=2))
    styles.add(ParagraphStyle(
        name='SectionHeader', fontSize=11, fontName='Helvetica-Bold',
        textColor=colors.HexColor("#334155"), spaceBefore=6, spaceAfter=3))
    styles.add(ParagraphStyle(
        name='Label', fontSize=8.5, fontName='Helvetica-Bold',
        textColor=colors.HexColor("#64748B"), leading=10))
    styles.add(ParagraphStyle(
        name='Value', fontSize=8.5, fontName='Helvetica', leading=11))
    styles.add(ParagraphStyle(
        name='RiskBox', fontSize=11, fontName='Helvetica-Bold',
        alignment=TA_CENTER, textColor=colors.white, leading=14))
    styles.add(ParagraphStyle(
        name='BulletTip', fontSize=8.5, fontName='Helvetica',
        leading=11, spaceBefore=1, spaceAfter=1))

    # ═══════════════════════════════════════════════════════════════
    # 1. HEADER — hospital name LEFT, contact info RIGHT, no overlap
    # ═══════════════════════════════════════════════════════════════
    left_cell = Paragraph(
        "AI MULTI-SPECIALITY HOSPITAL"
        "<br/><font size='7' color='#64748B'>Comprehensive Diagnostic &amp; Wellness Centre</font>",
        styles['HospitalName'])

    right_cell = Paragraph(
        "<b>Phone:</b> +91 98765 43210<br/>"
        "<b>Email:</b> reports@aihospital.com<br/>"
        "<b>Addr:</b> AI Innovation Hub, Tech City, 560001",
        styles['ContactInfo'])

    header_table = Table(
        [[left_cell, right_cell]],
        colWidths=[CONTENT_W * 0.58, CONTENT_W * 0.42])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 2))

    elements.append(Paragraph(
        "Comprehensive Medical Risk Assessment Report", styles['HospitalSub']))

    # Divider line
    d = Drawing(CONTENT_W, 1)
    d.add(Line(0, 0, CONTENT_W, 0, strokeColor=colors.HexColor("#CBD5E1"), strokeWidth=0.75))
    elements.append(d)
    elements.append(Spacer(1, 6))

    # ═══════════════════════════════════════════════════════════════
    # 2. PATIENT INFORMATION (compact 4-col grid)
    # ═══════════════════════════════════════════════════════════════
    cw = [CONTENT_W * 0.18, CONTENT_W * 0.32, CONTENT_W * 0.18, CONTENT_W * 0.32]
    patient_info = [
        [Paragraph("Patient Name", styles['Label']), Paragraph(name, styles['Value']),
         Paragraph("Patient ID", styles['Label']), Paragraph(patient_id, styles['Value'])],
        [Paragraph("Age / Gender", styles['Label']), Paragraph(f"{age} yr / {gender}", styles['Value']),
         Paragraph("Report Date", styles['Label']), Paragraph(timestamp, styles['Value'])],
        [Paragraph("Disease Assessed", styles['Label']), Paragraph(disease, styles['Value']), "", ""]
    ]
    pt_table = Table(patient_info, colWidths=cw)
    pt_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor("#F8FAFC")),
        ('BACKGROUND', (2, 0), (2, -1), colors.HexColor("#F8FAFC")),
        ('PADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(pt_table)
    elements.append(Spacer(1, 6))

    # ═══════════════════════════════════════════════════════════════
    # 3. CLINICAL PARAMETERS TABLE (compact)
    # ═══════════════════════════════════════════════════════════════
    elements.append(Paragraph("Clinical Parameters Analysis", styles['SectionHeader']))

    table_data = [["Parameter", "Observed Value", "Normal Range", "Status"]]
    status_style = ParagraphStyle('st', fontSize=8.5, leading=10)

    for k, v in measurements.items():
        display_k = k.replace("_", " ").title()
        ref = CLINICAL_RANGES.get(display_k, {"range": "N/A", "unit": ""})

        status = "Normal"
        status_color = colors.HexColor("#16A34A")
        try:
            val_num = float(str(v).split()[0])
            if display_k == "Blood Pressure" and val_num > 130:
                status = "Abnormal"; status_color = colors.HexColor("#DC2626")
            elif display_k == "Glucose" and val_num > 140:
                status = "Abnormal"; status_color = colors.HexColor("#DC2626")
            elif display_k == "Cholesterol" and val_num > 240:
                status = "Abnormal"; status_color = colors.HexColor("#DC2626")
            elif display_k == "Bmi" and (val_num < 18 or val_num > 30):
                status = "Abnormal"; status_color = colors.HexColor("#DC2626")
        except:
            pass

        table_data.append([
            display_k,
            f"{v} {ref['unit']}",
            f"{ref['range']} {ref['unit']}",
            Paragraph(f"<b>{status}</b>", ParagraphStyle('s', textColor=status_color, fontSize=8.5, leading=10))
        ])

    param_cw = [CONTENT_W * 0.30, CONTENT_W * 0.24, CONTENT_W * 0.26, CONTENT_W * 0.20]
    param_table = Table(table_data, colWidths=param_cw)
    param_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#008080")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8.5),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('PADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    elements.append(param_table)
    elements.append(Spacer(1, 6))

    # ═══════════════════════════════════════════════════════════════
    # 4. RISK ASSESSMENT (compact banner)
    # ═══════════════════════════════════════════════════════════════
    elements.append(Paragraph("Diagnostic Risk Assessment", styles['SectionHeader']))

    percent = int(prob * 100)
    risk_color = colors.HexColor("#16A34A")
    if risk == "MODERATE":
        risk_color = colors.HexColor("#EA580C")
    elif risk == "HIGH":
        risk_color = colors.HexColor("#DC2626")

    risk_data = [[Paragraph(f"RISK LEVEL: {risk} ({percent}%)", styles['RiskBox'])]]
    risk_table = Table(risk_data, colWidths=[CONTENT_W], rowHeights=[24])
    risk_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), risk_color),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROUNDEDCORNERS', [8, 8, 8, 8]),
    ]))
    elements.append(risk_table)
    elements.append(Spacer(1, 6))

    # ═══════════════════════════════════════════════════════════════
    # 5. DOCTOR'S REMARKS (compact)
    # ═══════════════════════════════════════════════════════════════
    elements.append(Paragraph("Doctor's Remarks", styles['SectionHeader']))
    remarks = (
        f"Based on the clinical analysis, the patient shows a <b>{risk}</b> risk of {disease}. "
        f"The observed parameters indicate {('minor' if risk == 'LOW' else 'significant')} deviations "
        f"from the standard baseline. Preventive measures and lifestyle modifications are strongly advised."
    )
    elements.append(Paragraph(remarks, styles['Value']))
    elements.append(Spacer(1, 4))

    # ═══════════════════════════════════════════════════════════════
    # 6. RECOMMENDATIONS (inline bullets)
    # ═══════════════════════════════════════════════════════════════
    elements.append(Paragraph("Clinical Recommendations", styles['SectionHeader']))
    for tip in get_precautions_text(disease, risk):
        elements.append(Paragraph(f"• {tip}", styles['BulletTip']))

    elements.append(Spacer(1, 14))

    # ═══════════════════════════════════════════════════════════════
    # 7. SIGNATURE BLOCK (compact, right-aligned)
    # ═══════════════════════════════════════════════════════════════
    doc_info = get_doctor_info()
    sig_data = [
        ["", "____________________________"],
        ["", Paragraph(f"<b>{doc_info['name']}</b>",
                       ParagraphStyle('doc', alignment=TA_CENTER, fontSize=9, leading=11))],
        ["", Paragraph(f"{doc_info['degree']}<br/>Reg No: {doc_info['reg']}",
                       ParagraphStyle('docinfo', alignment=TA_CENTER, fontSize=7, textColor=colors.grey, leading=9))]
    ]
    sig_table = Table(sig_data, colWidths=[CONTENT_W - 160, 160])
    sig_table.setStyle(TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 1),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
    ]))
    elements.append(sig_table)

    # Footer / Disclaimer
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(
        "<i>Note: This is an AI-generated assessment report and should be verified by a medical professional.</i>",
        ParagraphStyle('Footer', fontSize=7, textColor=colors.HexColor("#94A3B8"), alignment=TA_CENTER)))

    # ── Build PDF (single-page guard) ────────────────────────────
    doc.build(elements)
    return file_path
