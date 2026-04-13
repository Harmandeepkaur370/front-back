# 🏥 AI HOSPITAL MEDICAL INTELLIGENCE SYSTEM – FULL WORKING VERSION
# ============================================================
import backend
import gradio as gr
import pandas as pd
import numpy as np
import os
from auth import login, signup, logout
from models import *
from utils import *
import matplotlib.pyplot as plt
import sqlite3

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay, precision_score, recall_score, f1_score

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.lib.units import inch
# DATABASE CONNECTION
# ============================================================
conn = sqlite3.connect("hospital.db", check_same_thread=False)
cursor = conn.cursor()

# PREMIUM UI STYLE
# ============================================================

css = """
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css');

/* ── CSS Variables ── */
:root {
  --blue-50:  #EFF6FF;
  --blue-100: #DBEAFE;
  --blue-200: #BFDBFE;
  --blue-400: #60A5FA;
  --blue-500: #3B82F6;
  --blue-600: #2563EB;
  --blue-700: #1D4ED8;

  --lavender-50:  #F5F3FF;
  --lavender-100: #EDE9FE;
  --lavender-400: #A78BFA;
  --lavender-500: #8B5CF6;

  --mint-50:  #F0FDF4;
  --mint-100: #DCFCE7;
  --mint-400: #4ADE80;
  --mint-500: #22C55E;

  --rose-50:  #FFF1F2;
  --rose-400: #FB7185;
  --rose-500: #F43F5E;

  --amber-50:  #FFFBEB;
  --amber-400: #FBBF24;

  --gray-50:  #F8FAFC;
  --gray-100: #F1F5F9;
  --gray-200: #E2E8F0;
  --gray-300: #CBD5E1;
  --gray-400: #94A3B8;
  --gray-500: #64748B;
  --gray-600: #475569;
  --gray-700: #334155;
  --gray-800: #1E293B;
  --gray-900: #0F172A;

  --sidebar-w: 260px;
  --radius-sm: 8px;
  --radius-md: 14px;
  --radius-lg: 20px;
  --radius-xl: 28px;
  --shadow-sm: 0 1px 3px rgba(0,0,0,.06), 0 1px 2px rgba(0,0,0,.04);
  --shadow-md: 0 4px 16px rgba(0,0,0,.08), 0 2px 6px rgba(0,0,0,.05);
  --shadow-lg: 0 10px 40px rgba(0,0,0,.10), 0 4px 12px rgba(0,0,0,.06);
  --shadow-xl: 0 20px 60px rgba(0,0,0,.14);
  --transition: 0.22s cubic-bezier(.4,0,.2,1);
}

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body, .gradio-container {
  font-family: 'DM Sans', sans-serif !important;
  background: linear-gradient(135deg, #EFF6FF 0%, #F5F3FF 40%, #F0FDF4 100%) !important;
  min-height: 100vh;
  color: var(--gray-800) !important;
}

/* ── Hide default Gradio chrome ── */
footer, .footer, .built-with { display: none !important; }
.gradio-container { max-width: 100% !important; padding: 0 !important; }
.main { padding: 0 !important; }

/* ══════════════════════════════════
   LOGIN PAGE
══════════════════════════════════ */
.login-scene {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background:
    radial-gradient(ellipse 900px 600px at 80% 20%, rgba(96,165,250,.18) 0%, transparent 70%),
    radial-gradient(ellipse 700px 500px at 10% 80%, rgba(167,139,250,.16) 0%, transparent 70%),
    radial-gradient(ellipse 600px 400px at 60% 90%, rgba(74,222,128,.12) 0%, transparent 70%),
    linear-gradient(150deg, #EFF6FF 0%, #F5F3FF 50%, #F0FDF4 100%);
  padding: 32px 16px;
}

.login-card {
  width: 100%;
  max-width: 440px;
  background: rgba(255,255,255,0.72);
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  border: 1px solid rgba(255,255,255,0.85);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-xl), inset 0 1px 0 rgba(255,255,255,0.9);
  padding: 48px 44px;
  animation: slideUp .5s cubic-bezier(.34,1.56,.64,1) both;
}

@keyframes slideUp {
  from { opacity:0; transform:translateY(32px) scale(.97); }
  to   { opacity:1; transform:translateY(0) scale(1); }
}

.login-logo {
  text-align: center;
  margin-bottom: 32px;
}
.login-logo .logo-ring {
  width: 72px; height: 72px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--blue-500), var(--lavender-500));
  display: inline-flex; align-items: center; justify-content: center;
  font-size: 30px; color: white;
  box-shadow: 0 8px 24px rgba(59,130,246,.35);
  margin-bottom: 14px;
}
.login-logo h1 {
  font-family: 'Playfair Display', serif;
  font-size: 22px; font-weight: 700;
  color: var(--gray-800);
  line-height: 1.2;
}
.login-logo p {
  font-size: 13px; color: var(--gray-500); margin-top: 4px; font-weight: 400;
}

.login-tabs {
  display: flex; gap: 4px;
  background: var(--gray-100);
  border-radius: var(--radius-sm);
  padding: 4px;
  margin-bottom: 28px;
}
.login-tab {
  flex: 1; padding: 9px;
  border-radius: 6px; border: none;
  font-family: 'DM Sans', sans-serif;
  font-size: 14px; font-weight: 500;
  cursor: pointer; transition: var(--transition);
  background: transparent; color: var(--gray-500);
}
.login-tab.active {
  background: white;
  color: var(--blue-600);
  box-shadow: var(--shadow-sm);
}

/* ── Gradio input overrides inside login ── */
#login_page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
#login_page .gr-textbox input,
#login_page input[type="text"],
#login_page input[type="password"] {
  border: 1.5px solid var(--gray-200) !important;
  border-radius: var(--radius-md) !important;
  padding: 13px 16px !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 14px !important;
  background: white !important;
  transition: var(--transition) !important;
  box-shadow: none !important;
  outline: none !important;
}
#login_page .gr-textbox input:focus,
#login_page input:focus {
  border-color: var(--blue-400) !important;
  box-shadow: 0 0 0 3px rgba(96,165,250,.18) !important;
}

/* ── Primary button ── */
.btn-primary button, button.btn-primary {
  background: linear-gradient(135deg, var(--blue-500) 0%, var(--blue-600) 100%) !important;
  color: white !important;
  border: none !important;
  border-radius: var(--radius-md) !important;
  padding: 13px 28px !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 15px !important;
  font-weight: 600 !important;
  cursor: pointer !important;
  transition: var(--transition) !important;
  box-shadow: 0 4px 14px rgba(59,130,246,.40) !important;
  width: 100% !important;
}
.btn-primary button:hover, button.btn-primary:hover {
  transform: translateY(-1px) !important;
  box-shadow: 0 6px 20px rgba(59,130,246,.50) !important;
}

.btn-secondary button, button.btn-secondary {
  background: white !important;
  color: var(--blue-600) !important;
  border: 1.5px solid var(--blue-200) !important;
  border-radius: var(--radius-md) !important;
  padding: 11px 28px !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 14px !important;
  font-weight: 500 !important;
  cursor: pointer !important;
  transition: var(--transition) !important;
  width: 100% !important;
}
.btn-secondary button:hover { background: var(--blue-50) !important; }

/* ══════════════════════════════════
   DASHBOARD LAYOUT
══════════════════════════════════ */
.app-layout {
  display: flex;
  min-height: 100vh;
}

/* ── Sidebar ── */
.sidebar {
  width: var(--sidebar-w);
  min-height: 100vh;
  background: rgba(255,255,255,0.85);
  backdrop-filter: blur(20px);
  border-right: 1px solid var(--gray-100);
  box-shadow: 4px 0 20px rgba(0,0,0,.05);
  display: flex;
  flex-direction: column;
  padding: 0;
  position: sticky;
  top: 0;
  flex-shrink: 0;
  z-index: 100;
}

.sidebar-brand {
  padding: 28px 24px 20px;
  border-bottom: 1px solid var(--gray-100);
}
.sidebar-brand .brand-icon {
  width: 40px; height: 40px;
  border-radius: 10px;
  background: linear-gradient(135deg, var(--blue-500), var(--lavender-500));
  display: inline-flex; align-items: center; justify-content: center;
  font-size: 18px; color: white;
  box-shadow: 0 4px 12px rgba(59,130,246,.30);
  margin-bottom: 10px;
}
.sidebar-brand h2 {
  font-family: 'Playfair Display', serif;
  font-size: 15px; font-weight: 700;
  color: var(--gray-800);
  line-height: 1.3;
}
.sidebar-brand span {
  font-size: 11px; color: var(--gray-400); font-weight: 400;
}

.sidebar-nav {
  flex: 1;
  padding: 16px 12px;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.nav-section-label {
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--gray-400);
  padding: 12px 12px 6px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 11px 14px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: var(--transition);
  font-size: 14px;
  font-weight: 500;
  color: var(--gray-600);
  border: none;
  background: none;
  width: 100%;
  text-align: left;
  font-family: 'DM Sans', sans-serif;
}
.nav-item:hover {
  background: var(--blue-50);
  color: var(--blue-600);
}
.nav-item.active {
  background: linear-gradient(135deg, var(--blue-50), var(--lavender-50));
  color: var(--blue-600);
  font-weight: 600;
  box-shadow: inset 3px 0 0 var(--blue-500);
}
.nav-item .nav-icon {
  width: 32px; height: 32px;
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-size: 14px;
  background: var(--gray-100);
  transition: var(--transition);
  flex-shrink: 0;
}
.nav-item:hover .nav-icon,
.nav-item.active .nav-icon {
  background: linear-gradient(135deg, var(--blue-500), var(--lavender-500));
  color: white;
}
.nav-item.logout-btn {
  color: var(--rose-500);
  margin-top: auto;
}
.nav-item.logout-btn:hover {
  background: var(--rose-50);
  color: var(--rose-500);
}
.nav-item.logout-btn .nav-icon { background: var(--rose-50); color: var(--rose-400); }
.nav-item.logout-btn:hover .nav-icon { background: var(--rose-400); color: white; }

.sidebar-footer {
  padding: 16px 20px;
  border-top: 1px solid var(--gray-100);
}
.user-chip {
  display: flex; align-items: center; gap: 10px;
  padding: 10px;
  border-radius: var(--radius-sm);
  background: var(--gray-50);
}
.user-avatar {
  width: 34px; height: 34px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--blue-400), var(--lavender-400));
  display: flex; align-items: center; justify-content: center;
  color: white; font-size: 13px; font-weight: 600;
  flex-shrink: 0;
}
.user-chip .user-name { font-size: 13px; font-weight: 600; color: var(--gray-700); }
.user-chip .user-role { font-size: 11px; color: var(--gray-400); }

/* ── Main Content ── */
.main-content {
  flex: 1;
  padding: 32px 36px;
  overflow-y: auto;
}

.page-header {
  margin-bottom: 32px;
}
.page-header .greeting {
  font-size: 13px;
  color: var(--gray-400);
  font-weight: 400;
  margin-bottom: 4px;
}
.page-header h1 {
  font-family: 'Playfair Display', serif;
  font-size: 28px; font-weight: 700;
  color: var(--gray-800);
}
.page-header p {
  color: var(--gray-500);
  font-size: 14px;
  margin-top: 4px;
}

/* ── Stat Cards ── */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.stat-card {
  background: white;
  border-radius: var(--radius-lg);
  padding: 24px;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--gray-100);
  position: relative;
  overflow: hidden;
  transition: var(--transition);
}
.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}
.stat-card::before {
  content: '';
  position: absolute;
  top: 0; right: 0;
  width: 80px; height: 80px;
  border-radius: 0 var(--radius-lg) 0 80px;
  opacity: .07;
}
.stat-card.blue::before { background: var(--blue-500); }
.stat-card.lavender::before { background: var(--lavender-500); }
.stat-card.mint::before { background: var(--mint-500); }
.stat-card.amber::before { background: var(--amber-400); }

.stat-icon {
  width: 44px; height: 44px;
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  font-size: 18px; margin-bottom: 14px;
}
.stat-card.blue .stat-icon { background: var(--blue-50); color: var(--blue-500); }
.stat-card.lavender .stat-icon { background: var(--lavender-50); color: var(--lavender-500); }
.stat-card.mint .stat-icon { background: var(--mint-50); color: var(--mint-500); }
.stat-card.amber .stat-icon { background: var(--amber-50); color: var(--amber-400); }

.stat-value {
  font-family: 'Playfair Display', serif;
  font-size: 30px; font-weight: 700;
  color: var(--gray-800); line-height: 1;
  margin-bottom: 4px;
}
.stat-label { font-size: 13px; color: var(--gray-500); font-weight: 400; }
.stat-badge {
  display: inline-block;
  font-size: 11px; font-weight: 600;
  padding: 3px 8px;
  border-radius: 20px;
  margin-top: 8px;
}
.stat-badge.green { background: var(--mint-50); color: var(--mint-500); }
.stat-badge.blue  { background: var(--blue-50); color: var(--blue-500); }

/* ── Section Card ── */
.section-card {
  background: white;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  border: 1px solid var(--gray-100);
  margin-bottom: 24px;
  overflow: hidden;
  transition: var(--transition);
}
.section-card:hover { box-shadow: var(--shadow-lg); }

.section-header {
  padding: 20px 24px 16px;
  border-bottom: 1px solid var(--gray-100);
  display: flex;
  align-items: center;
  gap: 12px;
}
.section-header .sh-icon {
  width: 36px; height: 36px;
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 15px;
}
.section-header.heart .sh-icon { background: var(--rose-50); color: var(--rose-400); }
.section-header.diabetes .sh-icon { background: var(--lavender-50); color: var(--lavender-500); }
.section-header.symptom .sh-icon { background: var(--mint-50); color: var(--mint-500); }
.section-header.history .sh-icon { background: var(--amber-50); color: var(--amber-400); }
.section-header.report .sh-icon { background: var(--blue-50); color: var(--blue-500); }

.section-header h3 {
  font-size: 16px; font-weight: 600; color: var(--gray-800);
}
.section-header p { font-size: 12px; color: var(--gray-400); margin-top: 1px; }
.section-body { padding: 24px; }

/* ── Form Controls ── */
.form-grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}
.form-grid-3 {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 16px;
}

/* Override Gradio labels and inputs globally */
.gradio-container label,
.gradio-container .label-wrap span {
  font-family: 'DM Sans', sans-serif !important;
  font-size: 13px !important;
  font-weight: 500 !important;
  color: var(--gray-600) !important;
  margin-bottom: 4px !important;
}

.gradio-container input[type="text"],
.gradio-container input[type="number"],
.gradio-container textarea,
.gradio-container select,
.gradio-container .gr-textbox input {
  border: 1.5px solid var(--gray-200) !important;
  border-radius: var(--radius-sm) !important;
  padding: 10px 14px !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 14px !important;
  background: var(--gray-50) !important;
  transition: var(--transition) !important;
  color: var(--gray-800) !important;
}
.gradio-container input:focus,
.gradio-container textarea:focus {
  border-color: var(--blue-400) !important;
  background: white !important;
  box-shadow: 0 0 0 3px rgba(96,165,250,.15) !important;
  outline: none !important;
}

/* Slider */
.gradio-container input[type="range"] {
  accent-color: var(--blue-500) !important;
}

/* Radio */
.gradio-container .gr-radio-row,
.gradio-container .block.svelte-90oupt {
  gap: 8px !important;
}

/* Predict buttons */
.btn-predict button {
  background: linear-gradient(135deg, var(--blue-600) 0%, var(--lavender-500) 100%) !important;
  color: white !important;
  border: none !important;
  border-radius: var(--radius-md) !important;
  padding: 14px 32px !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 15px !important;
  font-weight: 600 !important;
  cursor: pointer !important;
  transition: var(--transition) !important;
  box-shadow: 0 4px 16px rgba(59,130,246,.35) !important;
  min-width: 200px !important;
}
.btn-predict button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 24px rgba(59,130,246,.45) !important;
}

/* ── Risk Result Badge styles (used in HTML output) ── */
.risk-card {
  border-radius: var(--radius-lg) !important;
  padding: 24px !important;
  margin-bottom: 16px !important;
}
.risk-HIGH  { background: linear-gradient(135deg,#FFF1F2,#FFE4E6); border-left: 5px solid #F43F5E; }
.risk-MODERATE { background: linear-gradient(135deg,#FFFBEB,#FEF3C7); border-left: 5px solid #F59E0B; }
.risk-LOW   { background: linear-gradient(135deg,#F0FDF4,#DCFCE7); border-left: 5px solid #22C55E; }

/* ── Metrics card ── */
.metrics-card {
  background: var(--gray-50) !important;
  border-radius: var(--radius-md) !important;
  padding: 20px !important;
  border: 1px solid var(--gray-100) !important;
}
.metrics-card h3 {
  font-family: 'Playfair Display', serif !important;
  font-size: 16px !important;
  color: var(--gray-800) !important;
  margin-bottom: 12px !important;
}
.metrics-card ul { list-style: none !important; }
.metrics-card li {
  padding: 8px 0 !important;
  border-bottom: 1px solid var(--gray-200) !important;
  font-size: 13px !important;
  color: var(--gray-700) !important;
  display: flex !important;
  justify-content: space-between !important;
}
.metrics-card li:last-child { border-bottom: none !important; }

/* ── History table ── */
.gradio-container .gr-dataframe table {
  font-family: 'DM Sans', sans-serif !important;
  border-collapse: collapse !important;
  width: 100% !important;
}
.gradio-container .gr-dataframe th {
  background: var(--gray-50) !important;
  color: var(--gray-600) !important;
  font-size: 12px !important;
  font-weight: 600 !important;
  text-transform: uppercase !important;
  letter-spacing: .04em !important;
  padding: 10px 16px !important;
  border-bottom: 2px solid var(--gray-100) !important;
}
.gradio-container .gr-dataframe td {
  font-size: 14px !important;
  padding: 12px 16px !important;
  border-bottom: 1px solid var(--gray-100) !important;
  color: var(--gray-700) !important;
}
.gradio-container .gr-dataframe tr:hover td {
  background: var(--blue-50) !important;
}

/* ── Status message ── */
.status-msg {
  background: var(--mint-50) !important;
  border: 1px solid var(--mint-100) !important;
  color: var(--mint-500) !important;
  border-radius: var(--radius-sm) !important;
  padding: 10px 14px !important;
  font-size: 13px !important;
  font-weight: 500 !important;
}

/* ── Logout button ── */
.btn-logout button {
  background: white !important;
  color: var(--rose-500) !important;
  border: 1.5px solid var(--rose-200) !important;
  border-radius: var(--radius-md) !important;
  padding: 10px 22px !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 14px !important;
  font-weight: 500 !important;
  cursor: pointer !important;
  transition: var(--transition) !important;
}
.btn-logout button:hover {
  background: var(--rose-50) !important;
}

/* ── Pill badge on nav ── */
.nav-badge {
  margin-left: auto;
  background: var(--blue-100);
  color: var(--blue-600);
  font-size: 10px;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: 20px;
}

/* ── Divider ── */
.nav-divider {
  height: 1px;
  background: var(--gray-100);
  margin: 8px 12px;
}

/* ── Tabs for pages ── */
.gradio-container .tab-nav button {
  font-family: 'DM Sans', sans-serif !important;
  font-size: 14px !important;
  font-weight: 500 !important;
  border-radius: var(--radius-sm) !important;
  transition: var(--transition) !important;
}
.gradio-container .tab-nav button.selected {
  background: var(--blue-500) !important;
  color: white !important;
  box-shadow: 0 2px 8px rgba(59,130,246,.30) !important;
}

/* ── Symptom Checker checkboxes ── */
.gradio-container .gr-check-radio {
  border-radius: var(--radius-sm) !important;
  border: 1.5px solid var(--gray-200) !important;
  padding: 8px 12px !important;
  font-size: 13px !important;
  transition: var(--transition) !important;
  cursor: pointer !important;
  background: white !important;
}
.gradio-container .gr-check-radio:hover {
  border-color: var(--blue-300) !important;
  background: var(--blue-50) !important;
}
.gradio-container .gr-check-radio input:checked + span {
  color: var(--blue-600) !important;
  font-weight: 500 !important;
}

/* ── File download button ── */
.gradio-container .file-preview {
  border-radius: var(--radius-md) !important;
  border: 1.5px dashed var(--gray-200) !important;
  background: var(--gray-50) !important;
}

/* ── Plot output ── */
.gradio-container .plot-container {
  border-radius: var(--radius-md) !important;
  overflow: hidden !important;
  border: 1px solid var(--gray-100) !important;
}

/* ══════════════════════════════════
   MOBILE RESPONSIVE
══════════════════════════════════ */
@media (max-width: 900px) {
  .sidebar { width: 64px; }
  .sidebar-brand h2, .sidebar-brand span,
  .nav-item span, .nav-section-label,
  .nav-badge, .sidebar-footer .user-chip .user-name,
  .sidebar-footer .user-chip .user-role { display: none; }
  .nav-item { justify-content: center; padding: 11px 0; }
  .nav-item .nav-icon { margin: 0; }
  .main-content { padding: 20px 16px; }
}
@media (max-width: 600px) {
  .form-grid-2, .form-grid-3 { grid-template-columns: 1fr; }
  .stats-grid { grid-template-columns: 1fr 1fr; }
}
"""

# ============================================================
# USER MANAGEMENT
# ============================================================

def signup(username, password):
    try:
        cursor.execute("INSERT INTO users(username,password) VALUES (?,?)", (username, password))
        conn.commit()
        return "✅ Signup successful! You can now log in."
    except sqlite3.IntegrityError:
        return "⚠️ Username already exists."

def login(username, password):
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    if cursor.fetchone():
        return (
            gr.update(visible=True),
            gr.update(visible=False),
            "✅ Login successful!",
            username
        )
    else:
        return (
            gr.update(visible=False),
            gr.update(visible=True),
            "❌ Invalid username or password",
            None
        )

def logout():
    return gr.update(visible=False), gr.update(visible=True)


# PREDICTION FUNCTIONS
# ============================================================

def heart_predict(user, name, age, sex, cp, bp, chol, fbs, thalach, smoking, exercise, diet, family):
    sex_val = 1 if sex == "Male" else 0
    arr = pd.DataFrame([[age,sex_val,cp,bp,chol,fbs,thalach]],
                       columns=["age","sex","cp","trestbps","chol","fbs","thalach"])
    arr = arr.reindex(columns=X_heart.columns, fill_value=0)
    prob = heart_model.predict_proba(arr)[0][1]
    prob = lifestyle_modifier(prob, smoking, exercise, diet, family)
    measurements = {"Age":age,"Gender":sex,"Chest Pain":cp,"Blood Pressure":bp,
                    "Cholesterol":chol,"Fasting Sugar":fbs,"Max Heart Rate":thalach,
                    "Smoking":smoking,"Exercise":exercise,"Diet":diet,"Family History":family}
    html, risk = generate_report(prob, "Heart Disease", name, age, measurements)
    chart      = risk_pie_chart(prob)
    cm_fig     = plot_cm(heart_cm, "Heart Disease — Confusion Matrix")
    metrics_html = cm_metrics(heart_cm, yh_test, heart_model.predict(Xh_test))
    backend.save_history(user, name, age, "Heart Disease", risk)
    pdf = create_pdf(name, age, "Heart Disease", risk, measurements, prob)
    return html, pdf, chart, cm_fig, metrics_html

def diabetes_predict(user, name, age, preg, glucose, bp, bmi, insulin, smoking, exercise, diet, family):
    arr = pd.DataFrame([[preg,glucose,bp,0,insulin,bmi,0,age]], columns=X_diabetes.columns)
    prob = diabetes_model.predict_proba(arr)[0][1]
    prob = lifestyle_modifier(prob, smoking, exercise, diet, family)
    measurements = {"Age":age,"Pregnancies":preg,"Glucose":glucose,"Blood Pressure":bp,
                    "BMI":bmi,"Insulin":insulin,"Smoking":smoking,"Exercise":exercise,
                    "Diet":diet,"Family History":family}
    html, risk = generate_report(prob, "Diabetes", name, age, measurements)
    chart      = risk_pie_chart(prob)
    cm_fig     = plot_cm(diabetes_cm, "Diabetes — Confusion Matrix")
    metrics_html = cm_metrics(diabetes_cm, yd_test, diabetes_model.predict(Xd_test))
    backend.save_history(user, name, age, "Diabetes Disease", risk)
    pdf = create_pdf(name, age, "Diabetes", risk, measurements, prob)
    return html, pdf, chart, cm_fig, metrics_html

def show_history(user):
    if not user:
        return [["Login Required","","",""]]
    data = backend.get_history(user)
    return data if data else [["No records found","","",""]]

def symptom_checker(symptoms):
    symptoms = set(symptoms)
    disease_map = {
        "Heart Disease":      {"symptoms":{"chest pain","shortness of breath","fatigue","dizziness","palpitations"},"advice":"Consult a cardiologist and monitor blood pressure"},
        "Diabetes":           {"symptoms":{"frequent urination","weight loss","fatigue","blurred vision","increased hunger"},"advice":"Check blood sugar levels and consult a doctor"},
        "Hypertension":       {"symptoms":{"headache","dizziness","blurred vision","chest pain"},"advice":"Monitor BP regularly and reduce salt intake"},
        "Anemia":             {"symptoms":{"fatigue","pale skin","shortness of breath","dizziness"},"advice":"Check hemoglobin levels and improve iron intake"},
        "Flu / Viral Infection":{"symptoms":{"fever","fatigue","body ache","headache"},"advice":"Take rest, stay hydrated, and use basic medication"},
    }
    results = sorted(
        [(d, len(symptoms & v["symptoms"]) / len(v["symptoms"]) * 100, v["advice"])
         for d,v in disease_map.items() if len(symptoms & v["symptoms"]) > 0],
        key=lambda x: x[1], reverse=True
    )
    if not results:
        return "<div style='font-family:DM Sans,sans-serif;background:#F8FAFC;border-radius:14px;padding:24px;border:1px solid #E2E8F0;text-align:center;color:#64748B'>No significant disease pattern detected from selected symptoms.</div>"

    html = "<div style='font-family:DM Sans,sans-serif;display:flex;flex-direction:column;gap:12px'>"
    for disease, conf, advice in results:
        if conf < 40:   c = "#22C55E"; bg = "#F0FDF4"; bd = "#DCFCE7"
        elif conf < 70: c = "#F59E0B"; bg = "#FFFBEB"; bd = "#FEF3C7"
        else:           c = "#F43F5E"; bg = "#FFF1F2"; bd = "#FFE4E6"
        bar = min(int(conf), 100)
        html += f"""
        <div style='background:{bg};border-radius:12px;padding:16px 20px;border:1px solid {bd}'>
          <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:8px'>
            <span style='font-size:15px;font-weight:600;color:#1E293B'>{disease}</span>
            <span style='font-size:13px;font-weight:700;color:{c};background:white;padding:3px 10px;border-radius:20px;border:1px solid {bd}'>{conf:.0f}% match</span>
          </div>
          <div style='background:white;border-radius:100px;height:6px;overflow:hidden;margin-bottom:10px'>
            <div style='height:100%;width:{bar}%;background:{c};border-radius:100px;transition:.5s ease'></div>
          </div>
          <p style='font-size:12px;color:#64748B;margin:0'>💡 {advice}</p>
        </div>"""
    html += "</div>"
    return html

# ============================================================
# DASHBOARD STAT CARDS HTML
# ============================================================

def dashboard_stats_html():
    return f"""
    <div style='font-family:DM Sans,sans-serif'>
      <div style='margin-bottom:28px'>
        <p style='font-size:13px;color:#94A3B8;margin-bottom:4px'>AI-Powered Clinical Intelligence</p>
        <h1 style='font-family:Playfair Display,serif;font-size:26px;font-weight:700;color:#1E293B;margin:0'>Welcome to your Dashboard</h1>
        <p style='font-size:14px;color:#64748B;margin-top:4px'>Real-time model metrics and patient insights</p>
      </div>
      <div style='display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:18px;margin-bottom:28px'>
        <div style='background:white;border-radius:16px;padding:22px;box-shadow:0 4px 16px rgba(0,0,0,.07);border:1px solid #F1F5F9;position:relative;overflow:hidden'>
          <div style='width:40px;height:40px;border-radius:10px;background:#FFF1F2;display:flex;align-items:center;justify-content:center;font-size:18px;margin-bottom:12px'>❤️</div>
          <div style='font-family:Playfair Display,serif;font-size:28px;font-weight:700;color:#1E293B'>{heart_acc*100:.1f}%</div>
          <div style='font-size:13px;color:#64748B;margin-top:2px'>Heart Disease Accuracy</div>
          <div style='display:inline-block;background:#F0FDF4;color:#22C55E;font-size:11px;font-weight:600;padding:3px 8px;border-radius:20px;margin-top:8px'>Random Forest · 200 trees</div>
        </div>
        <div style='background:white;border-radius:16px;padding:22px;box-shadow:0 4px 16px rgba(0,0,0,.07);border:1px solid #F1F5F9'>
          <div style='width:40px;height:40px;border-radius:10px;background:#EDE9FE;display:flex;align-items:center;justify-content:center;font-size:18px;margin-bottom:12px'>🩸</div>
          <div style='font-family:Playfair Display,serif;font-size:28px;font-weight:700;color:#1E293B'>{diabetes_acc*100:.1f}%</div>
          <div style='font-size:13px;color:#64748B;margin-top:2px'>Diabetes Accuracy</div>
          <div style='display:inline-block;background:#EDE9FE;color:#8B5CF6;font-size:11px;font-weight:600;padding:3px 8px;border-radius:20px;margin-top:8px'>Random Forest · 200 trees</div>
        </div>
        <div style='background:white;border-radius:16px;padding:22px;box-shadow:0 4px 16px rgba(0,0,0,.07);border:1px solid #F1F5F9'>
          <div style='width:40px;height:40px;border-radius:10px;background:#DBEAFE;display:flex;align-items:center;justify-content:center;font-size:18px;margin-bottom:12px'>🧠</div>
          <div style='font-family:Playfair Display,serif;font-size:28px;font-weight:700;color:#1E293B'>5</div>
          <div style='font-size:13px;color:#64748B;margin-top:2px'>Diseases in Symptom DB</div>
          <div style='display:inline-block;background:#DBEAFE;color:#3B82F6;font-size:11px;font-weight:600;padding:3px 8px;border-radius:20px;margin-top:8px'>Rule-based matching</div>
        </div>
        <div style='background:white;border-radius:16px;padding:22px;box-shadow:0 4px 16px rgba(0,0,0,.07);border:1px solid #F1F5F9'>
          <div style='width:40px;height:40px;border-radius:10px;background:#FEF3C7;display:flex;align-items:center;justify-content:center;font-size:18px;margin-bottom:12px'>📄</div>
          <div style='font-family:Playfair Display,serif;font-size:28px;font-weight:700;color:#1E293B'>PDF</div>
          <div style='font-size:13px;color:#64748B;margin-top:2px'>Report Generation</div>
          <div style='display:inline-block;background:#FEF3C7;color:#F59E0B;font-size:11px;font-weight:600;padding:3px 8px;border-radius:20px;margin-top:8px'>Auto-generated on predict</div>
        </div>
      </div>
      <div style='background:linear-gradient(135deg,#EFF6FF,#F5F3FF);border-radius:14px;padding:18px 22px;border:1px solid #DBEAFE'>
        <p style='font-size:13px;color:#3B82F6;font-weight:500;margin:0'>ℹ️ Select a prediction module from the tabs above to get started. Fill in patient parameters and receive an instant AI-powered risk assessment.</p>
      </div>
    </div>
    """

# ============================================================

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
    display:none; display:flex; align-items:center; justify-content:center;
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
            gr.HTML('''
            <div style="text-align:center;margin-bottom:32px">
              <div style="width:64px;height:64px;border-radius:18px;background:linear-gradient(135deg,#4318FF,#868CFF);display:inline-flex;align-items:center;justify-content:center;font-size:32px;color:white;box-shadow:0 8px 24px rgba(67,24,255,0.4);margin-bottom:16px">🏥</div>
              <div style="font-size:26px;font-weight:800;color:white;margin-bottom:6px">Integrated Medical Intelligence System</div>
              <div style="font-size:13px;color:rgba(255,255,255,0.65)">Secure Clinical Platform</div>
            </div>''')
            _u = gr.Textbox(label="Username", placeholder="Enter your ID")
            _p = gr.Textbox(label="Password",  placeholder="Enter password", type="password")
            _m = gr.Textbox(label="", interactive=False, show_label=False)
            _lb = gr.Button("Sign In →", elem_classes="btn-login")
            _sb = gr.Button("Create Account")

    # ── APP ──
    with gr.Column(visible=False) as _app_pg:
        with gr.Row(elem_classes="app-layout"):

            # SIDEBAR
            with gr.Column(scale=0, min_width=260, elem_classes="sidebar"):
                gr.HTML('''
                <div class="sidebar-logo">
                  <div class="sidebar-logo-icon">🏥</div> IMIS
                </div>''')
                gr.HTML('<div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#4a5568;padding:0 8px 8px">Main Menu</div>')
                _nb_dash  = gr.Button("📊  Dashboard",            variant="primary",   elem_classes="nav-btn")
                _nb_heart = gr.Button("❤️   Heart Prediction",    variant="secondary", elem_classes="nav-btn")
                _nb_diab  = gr.Button("🩸  Diabetes Prediction",  variant="secondary", elem_classes="nav-btn")
                _nb_symp  = gr.Button("🧠  Symptom Checker",      variant="secondary", elem_classes="nav-btn")
                gr.HTML('<div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#4a5568;padding:18px 8px 8px">Records</div>')
                _nb_hist  = gr.Button("📂  Report History",       variant="secondary", elem_classes="nav-btn")
                _nb_prof  = gr.Button("👤  User Profile",         variant="secondary", elem_classes="nav-btn")
                gr.HTML('<div style="flex:1;min-height:60px"></div>')
                _lo = gr.Button("🚪  Sign Out", elem_classes=["nav-btn","logout-btn"], variant="secondary")

            # MAIN CONTENT
            with gr.Column(elem_classes="content-area"):

                # DASHBOARD
                with gr.Column(visible=True) as _pg_dash:
                    gr.HTML(_dashboard_html())
                    with gr.Row():
                        with gr.Column(elem_classes="glass-card"):
                            gr.HTML('<div class="group-title">❤️ Heart Model — Confusion Matrix</div>')
                            gr.Plot(value=plot_cm(heart_cm, "Heart Disease"))
                        with gr.Column(elem_classes="glass-card"):
                            gr.HTML('<div class="group-title">🩸 Diabetes Model — Confusion Matrix</div>')
                            gr.Plot(value=plot_cm(diabetes_cm, "Diabetes"))

                # HEART
                with gr.Column(visible=False) as _pg_heart:
                    gr.HTML('<div class="page-header"><h2>❤️ Heart Disease Risk Assessment</h2><p>Cardiovascular risk prediction using Random Forest AI</p></div>')
                    with gr.Column(elem_classes="glass-card"):
                        gr.HTML('<div class="group-title">Patient Information</div>')
                        with gr.Row():
                            _ph_n = gr.Textbox(label="Full Name", placeholder="e.g. John Doe")
                            _ph_a = gr.Slider(18,100, value=45, step=1, label="Age (years)")
                            _ph_s = gr.Radio(["Male","Female"], label="Biological Sex", value="Male")
                    with gr.Column(elem_classes="glass-card"):
                        gr.HTML('<div class="group-title">Clinical Parameters</div>')
                        with gr.Row():
                            _ph_cp   = gr.Slider(0,3, step=1, value=1, label="Chest Pain Type (0–3)")
                            _ph_bp   = gr.Slider(80,200, value=120, label="Blood Pressure (mmHg)")
                            _ph_chol = gr.Slider(100,400, value=200, label="Cholesterol (mg/dL)")
                        with gr.Row():
                            _ph_fbs  = gr.Radio(choices=[("No", 0), ("Yes", 1)], label="Fasting Blood Sugar >120", value=0)
                            _ph_thal = gr.Slider(70,210, value=150, label="Max Heart Rate")
                    with gr.Column(elem_classes="glass-card"):
                        gr.HTML('<div class="group-title">Lifestyle Risk Factors</div>')
                        with gr.Row():
                            _ph_sm  = gr.Radio(  choices=[("No", 0), ("Yes", 1)], label="Smoking",          value=0)
                            _ph_ex  = gr.Radio(  choices=[("No", 0), ("Yes", 1)], label="Regular Exercise", value=1)
                            _ph_dt  = gr.Radio(  choices=[("No", 0), ("Yes", 1)], label="Healthy Diet",     value=1)
                            _ph_fam = gr.Radio(  choices=[("No", 0), ("Yes", 1)], label="Family History",   value=0)
                        _ph_btn = gr.Button("🔍 Run Assessment", elem_classes="btn-predict")
                    with gr.Column(elem_classes="glass-card"):
                        gr.HTML('<div class="group-title">Prediction Result</div>')
                        _ph_out  = gr.HTML('<p style="color:#a0aec0;font-size:13px">Run assessment to see results.</p>')
                        _ph_pdf  = gr.File(label="📥 Download PDF Report")
                        with gr.Row():
                            _ph_ch  = gr.Plot(label="Risk Distribution")
                            _ph_cm2 = gr.Plot(label="Confusion Matrix")
                        _ph_met = gr.HTML()

                # DIABETES
                with gr.Column(visible=False) as _pg_diab:
                    gr.HTML('<div class="page-header"><h2>🩸 Diabetes Risk Assessment</h2><p>Metabolic risk prediction using Random Forest AI</p></div>')
                    with gr.Column(elem_classes="glass-card"):
                        gr.HTML('<div class="group-title">Patient Information</div>')
                        with gr.Row():
                            _pd_n = gr.Textbox(label="Full Name", placeholder="e.g. Jane Doe")
                            _pd_a = gr.Slider(18,100, value=40, step=1, label="Age (years)")
                    with gr.Column(elem_classes="glass-card"):
                        gr.HTML('<div class="group-title">Metabolic Parameters</div>')
                        with gr.Row():
                            _pd_pr = gr.Slider(0,15, step=1, value=2, label="Pregnancies")
                            _pd_gl = gr.Slider(70,250, value=110, label="Plasma Glucose")
                            _pd_bp = gr.Slider(40,140, value=72,  label="Diastolic BP")
                        with gr.Row():
                            _pd_bmi = gr.Slider(15,60, value=25, label="BMI")
                            _pd_ins = gr.Slider(0,600, value=80, label="Serum Insulin")
                    with gr.Column(elem_classes="glass-card"):
                        gr.HTML('<div class="group-title">Lifestyle Risk Factors</div>')
                        with gr.Row():
                            _pd_sm  = gr.Radio(  choices=[("No", 0), ("Yes", 1)], label="Smoking",          value=0)
                            _pd_ex  = gr.Radio(  choices=[("No", 0), ("Yes", 1)], label="Regular Exercise", value=1)
                            _pd_dt  = gr.Radio(  choices=[("No", 0), ("Yes", 1)], label="Healthy Diet",     value=1)
                            _pd_fam = gr.Radio(  choices=[("No", 0), ("Yes", 1)], label="Family History",   value=0)
                        _pd_btn = gr.Button("🔍 Run Assessment", elem_classes="btn-predict")
                    with gr.Column(elem_classes="glass-card"):
                        gr.HTML('<div class="group-title">Prediction Result</div>')
                        _pd_out  = gr.HTML('<p style="color:#a0aec0;font-size:13px">Run assessment to see results.</p>')
                        _pd_pdf  = gr.File(label="📥 Download PDF Report")
                        with gr.Row():
                            _pd_ch  = gr.Plot(label="Risk Distribution")
                            _pd_cm2 = gr.Plot(label="Confusion Matrix")
                        _pd_met = gr.HTML()

                # SYMPTOM
                with gr.Column(visible=False) as _pg_symp:
                    gr.HTML('<div class="page-header"><h2>🧠 AI Symptom Checker</h2><p>Rule-based clinical symptom matching engine</p></div>')
                    with gr.Column(elem_classes="glass-card"):
                        gr.HTML('<div class="group-title">Select Reported Symptoms</div>')
                        _ps_chk = gr.CheckboxGroup(
                            choices=["chest pain","shortness of breath","fatigue","dizziness",
                                     "palpitations","frequent urination","weight loss","blurred vision",
                                     "increased hunger","headache","fever","body ache","pale skin"],
                            label="Symptoms")
                        _ps_btn = gr.Button("🔍 Analyze Symptoms", elem_classes="btn-predict")
                    with gr.Column(elem_classes="glass-card"):
                        gr.HTML('<div class="group-title">Matched Conditions</div>')
                        _ps_out = gr.HTML('<p style="color:#a0aec0;font-size:13px">Select symptoms and analyze.</p>')

                # REPORT HISTORY
                with gr.Column(visible=False) as _pg_hist:
                    gr.HTML('<div class="page-header"><h2>📂 Report History</h2><p>All generated clinical PDF reports</p></div>')
                    with gr.Column(elem_classes="glass-card"):
                        gr.HTML('<div class="group-title">Report Archive</div>')
                        _hr_btn = gr.Button("🔄 Refresh", elem_classes="btn-predict")
                        _hr_tbl = gr.Dataframe(headers=["Filename","Created At","Path"], interactive=False, wrap=True)
                    with gr.Column(elem_classes="glass-card"):
                        gr.HTML('<div class="group-title">Download Report</div>')
                        _hr_drp = gr.Dropdown(label="Select a report", choices=[])
                        _hr_fl  = gr.File(label="Selected Report")

                # USER PROFILE
                with gr.Column(visible=False) as _pg_prof:
                    gr.HTML('<div class="page-header"><h2>👤 Patient History</h2><p>Historical risk assessments from the clinical database</p></div>')
                    with gr.Column(elem_classes="glass-card"):
                        gr.HTML('<div class="group-title">Assessment Log</div>')
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
