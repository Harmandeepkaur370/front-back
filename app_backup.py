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
# GRADIO UI
# ============================================================
css = """
.gradio-container {
    max-width: 100% !important;
    width: 100% !important;
    padding: 0 !important;
}

.main {
    max-width: 100% !important;
}

footer {display: none !important;}
"""
# with gr.Blocks(css=css, theme=gr.themes.Base()) as app:
with gr.Blocks(css=css, theme=gr.themes.Base(), fill_width=True) as app:
    
    user_state = gr.State()

    # ── LOGIN PAGE ──────────────────────────────────────────
    with gr.Column(visible=True, elem_id="login_page") as login_page:
        # gr.HTML("""
        # <div style='
        #   min-height:100vh;
        #   display:flex;
        #   align-items:center;
        #   justify-content:center;
        #   padding:40px 16px;
        #   background: radial-gradient(ellipse 800px 600px at 75% 25%, rgba(96,165,250,.15) 0%, transparent 70%),
        #               radial-gradient(ellipse 600px 500px at 15% 75%, rgba(167,139,250,.14) 0%, transparent 70%),
        #               linear-gradient(150deg, #EFF6FF 0%, #F5F3FF 50%, #F0FDF4 100%);
        # '>
        # </div>
        # """)
        with gr.Column(elem_id="login_container"):
            gr.HTML("""
            <div style='
              max-width:440px;
              margin:0 auto;
              background:rgba(255,255,255,0.82);
              backdrop-filter:blur(24px);
              border:1px solid rgba(255,255,255,0.9);
              border-radius:28px;
              box-shadow: 0 20px 60px rgba(0,0,0,.12), inset 0 1px 0 rgba(255,255,255,0.9);
              padding:48px 44px 40px;
              animation: slideUp .5s cubic-bezier(.34,1.56,.64,1) both;
            '>
              <div style='text-align:center;margin-bottom:32px'>
                <div style='
                  width:68px;height:68px;border-radius:50%;
                  background:linear-gradient(135deg,#3B82F6,#8B5CF6);
                  display:inline-flex;align-items:center;justify-content:center;
                  font-size:28px;color:white;
                  box-shadow:0 8px 24px rgba(59,130,246,.38);
                  margin-bottom:14px;
                '>🏥</div>
                <h1 style='font-family:Playfair Display,serif;font-size:21px;font-weight:700;color:#1E293B;margin:0;line-height:1.3'>
                  Integrated Medical<br>Intelligence System
                </h1>
                <p style='font-size:13px;color:#94A3B8;margin-top:6px;font-weight:400'>Secure clinical portal — please authenticate</p>
              </div>
            </div>
            """)

            with gr.Column(elem_classes="login-card"):
                username_input = gr.Textbox(label="👤 Username", placeholder="Enter your username")
                password_input = gr.Textbox(label="🔒 Password", placeholder="Enter your password", type="password")
                login_msg      = gr.Textbox(label="", interactive=False, show_label=False, elem_classes="status-msg")
                login_btn  = gr.Button("Sign In →", elem_classes="btn-primary")
                signup_btn = gr.Button("Create Account", elem_classes="btn-secondary")

    # ── DASHBOARD ───────────────────────────────────────────
    with gr.Column(visible=False) as dashboard:

        # ── Top header bar ──
        with gr.Row():
            gr.HTML("""
            <div style='
              width:100%;
              background:rgba(255,255,255,0.9);
              backdrop-filter:blur(16px);
              border-bottom:1px solid #E2E8F0;
              padding:14px 32px;
              display:flex;
              align-items:center;
              justify-content:space-between;
              font-family:DM Sans,sans-serif;
              position:sticky;top:0;z-index:200;
            '>
              <div style='display:flex;align-items:center;gap:12px'>
                <div style='
                  width:36px;height:36px;border-radius:9px;
                  background:linear-gradient(135deg,#3B82F6,#8B5CF6);
                  display:flex;align-items:center;justify-content:center;
                  color:white;font-size:16px;
                  box-shadow:0 4px 12px rgba(59,130,246,.30);
                '>🏥</div>
                <div>
                  <div style='font-family:Playfair Display,serif;font-size:15px;font-weight:700;color:#1E293B'>IMIS</div>
                  <div style='font-size:10px;color:#94A3B8;letter-spacing:.04em;text-transform:uppercase'>Medical Intelligence</div>
                </div>
              </div>
              <div style='font-size:13px;color:#64748B'>Integrated Medical Intelligence System &nbsp;·&nbsp; v2.0</div>
            </div>
            """)

        with gr.Row():
            # ── Sidebar ──
            with gr.Column(scale=0, min_width=220):
                gr.HTML("""
                <div style='
                  background:rgba(255,255,255,0.88);
                  backdrop-filter:blur(20px);
                  border-right:1px solid #F1F5F9;
                  min-height:calc(100vh - 64px);
                  padding:20px 12px;
                  display:flex;
                  flex-direction:column;
                  gap:2px;
                  font-family:DM Sans,sans-serif;
                  box-shadow:4px 0 20px rgba(0,0,0,.04);
                '>
                  <div style='font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:.08em;color:#94A3B8;padding:4px 12px 8px'>Navigation</div>
                  <div class='nav-item active' style='display:flex;align-items:center;gap:10px;padding:10px 12px;border-radius:8px;background:linear-gradient(135deg,#EFF6FF,#F5F3FF);color:#2563EB;font-weight:600;font-size:14px;box-shadow:inset 3px 0 0 #3B82F6'>
                    <div style='width:30px;height:30px;border-radius:8px;background:linear-gradient(135deg,#3B82F6,#8B5CF6);display:flex;align-items:center;justify-content:center;color:white;font-size:13px;flex-shrink:0'>📊</div>
                    <span>Dashboard</span>
                  </div>
                  <div style='margin:8px 0;height:1px;background:#F1F5F9'></div>
                  <div style='font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:.08em;color:#94A3B8;padding:4px 12px 6px'>Predictions</div>
                  <div style='display:flex;align-items:center;gap:10px;padding:10px 12px;border-radius:8px;color:#475569;font-size:14px;font-weight:500;cursor:pointer;transition:.2s'>
                    <div style='width:30px;height:30px;border-radius:8px;background:#FFF1F2;display:flex;align-items:center;justify-content:center;font-size:13px;flex-shrink:0'>❤️</div>
                    <span>Heart Disease</span>
                  </div>
                  <div style='display:flex;align-items:center;gap:10px;padding:10px 12px;border-radius:8px;color:#475569;font-size:14px;font-weight:500;cursor:pointer'>
                    <div style='width:30px;height:30px;border-radius:8px;background:#EDE9FE;display:flex;align-items:center;justify-content:center;font-size:13px;flex-shrink:0'>🩸</div>
                    <span>Diabetes</span>
                  </div>
                  <div style='margin:8px 0;height:1px;background:#F1F5F9'></div>
                  <div style='font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:.08em;color:#94A3B8;padding:4px 12px 6px'>Tools</div>
                  <div style='display:flex;align-items:center;gap:10px;padding:10px 12px;border-radius:8px;color:#475569;font-size:14px;font-weight:500;cursor:pointer'>
                    <div style='width:30px;height:30px;border-radius:8px;background:#DCFCE7;display:flex;align-items:center;justify-content:center;font-size:13px;flex-shrink:0'>🧠</div>
                    <span>Symptom Checker</span>
                  </div>
                  <div style='display:flex;align-items:center;gap:10px;padding:10px 12px;border-radius:8px;color:#475569;font-size:14px;font-weight:500;cursor:pointer'>
                    <div style='width:30px;height:30px;border-radius:8px;background:#DBEAFE;display:flex;align-items:center;justify-content:center;font-size:13px;flex-shrink:0'>📄</div>
                    <span>Reports</span>
                  </div>
                  <div style='display:flex;align-items:center;gap:10px;padding:10px 12px;border-radius:8px;color:#475569;font-size:14px;font-weight:500;cursor:pointer'>
                    <div style='width:30px;height:30px;border-radius:8px;background:#FEF3C7;display:flex;align-items:center;justify-content:center;font-size:13px;flex-shrink:0'>📜</div>
                    <span>History</span>
                  </div>
                </div>
                """)

            # ── Main Content ──
            with gr.Column(scale=4):
                with gr.Tabs():

                    # ── TAB: Dashboard Overview ──
                    with gr.Tab("📊 Overview"):
                        gr.HTML(dashboard_stats_html())
                        with gr.Row():
                            with gr.Column():
                                gr.Markdown("### ❤️ Heart Model — Confusion Matrix")
                                gr.Plot(value=plot_cm(heart_cm, "Heart Disease Confusion Matrix"))
                            with gr.Column():
                                gr.Markdown("### 🩸 Diabetes Model — Confusion Matrix")
                                gr.Plot(value=plot_cm(diabetes_cm, "Diabetes Confusion Matrix"))

                    # ── TAB: Heart Prediction ──
                    with gr.Tab("❤️ Heart Disease"):
                        gr.HTML("""
                        <div style='font-family:DM Sans,sans-serif;background:linear-gradient(135deg,#FFF1F2,#FFE4E6);border-radius:14px;padding:18px 22px;border:1px solid #FECDD3;margin-bottom:20px'>
                          <h2 style='font-size:18px;font-weight:700;color:#1E293B;margin:0 0 4px'>❤️ Heart Disease Risk Prediction</h2>
                          <p style='font-size:13px;color:#64748B;margin:0'>Enter patient clinical parameters to assess cardiovascular risk using Random Forest AI.</p>
                        </div>
                        """)
                        with gr.Row():
                            patient_name   = gr.Textbox(label="Patient Full Name", placeholder="e.g. John Smith")
                            patient_age    = gr.Slider(18, 100, value=45, label="Age (years)")
                            patient_sex    = gr.Radio(["Male","Female"], label="Biological Sex", value="Male")

                        with gr.Row():
                            cp      = gr.Slider(0, 3, step=1, value=1, label="Chest Pain Type (0–3)")
                            bp      = gr.Slider(80, 200, value=120, label="Resting Blood Pressure (mmHg)")
                            chol    = gr.Slider(100, 400, value=200, label="Serum Cholesterol (mg/dL)")

                        with gr.Row():
                            fbs     = gr.Radio([0, 1], label="Fasting Blood Sugar > 120 mg/dL", value=0)
                            thalach = gr.Slider(70, 210, value=150, label="Max Heart Rate Achieved")

                        gr.HTML("<div style='font-family:DM Sans,sans-serif;font-size:13px;font-weight:600;color:#475569;padding:8px 0 4px;border-top:1px solid #F1F5F9;margin-top:8px'>⚕️ Lifestyle Risk Factors</div>")
                        with gr.Row():
                            patient_smoking  = gr.Radio([0,1], label="Smoking (1=Yes)", value=0)
                            patient_exercise = gr.Radio([0,1], label="Regular Exercise (1=Yes)", value=1)
                            patient_diet     = gr.Radio([0,1], label="Healthy Diet (1=Yes)", value=1)
                            patient_family   = gr.Radio([0,1], label="Family History (1=Yes)", value=0)

                        heart_btn = gr.Button("🔍 Predict Heart Disease Risk", elem_classes="btn-predict")

                        heart_out     = gr.HTML()
                        heart_pdf     = gr.File(label="📥 Download PDF Report")
                        with gr.Row():
                            heart_chart   = gr.Plot(label="Risk Assessment Chart")
                            heart_cm_plot = gr.Plot(label="Confusion Matrix")
                        heart_metrics = gr.HTML()

                    # ── TAB: Diabetes Prediction ──
                    with gr.Tab("🩸 Diabetes"):
                        gr.HTML("""
                        <div style='font-family:DM Sans,sans-serif;background:linear-gradient(135deg,#F5F3FF,#EDE9FE);border-radius:14px;padding:18px 22px;border:1px solid #DDD6FE;margin-bottom:20px'>
                          <h2 style='font-size:18px;font-weight:700;color:#1E293B;margin:0 0 4px'>🩸 Diabetes Risk Prediction</h2>
                          <p style='font-size:13px;color:#64748B;margin:0'>Assess patient diabetes risk using metabolic and lifestyle parameters.</p>
                        </div>
                        """)
                        with gr.Row():
                            d_name = gr.Textbox(label="Patient Full Name", placeholder="e.g. Sarah Johnson")
                            d_age  = gr.Slider(18, 100, value=40, label="Age (years)")

                        with gr.Row():
                            preg    = gr.Slider(0, 15, step=1, value=2, label="Number of Pregnancies")
                            glucose = gr.Slider(70, 250, value=110, label="Plasma Glucose Level (mg/dL)")
                            dbp     = gr.Slider(40, 140, value=72, label="Diastolic Blood Pressure")

                        with gr.Row():
                            bmi     = gr.Slider(15, 60, value=25, label="Body Mass Index (BMI)")
                            insulin = gr.Slider(0, 600, value=80, label="Serum Insulin (μU/mL)")

                        gr.HTML("<div style='font-family:DM Sans,sans-serif;font-size:13px;font-weight:600;color:#475569;padding:8px 0 4px;border-top:1px solid #F1F5F9;margin-top:8px'>⚕️ Lifestyle Risk Factors</div>")
                        with gr.Row():
                            d_smoking  = gr.Radio([0,1], label="Smoking (1=Yes)", value=0)
                            d_exercise = gr.Radio([0,1], label="Regular Exercise (1=Yes)", value=1)
                            d_diet     = gr.Radio([0,1], label="Healthy Diet (1=Yes)", value=1)
                            d_family   = gr.Radio([0,1], label="Family History (1=Yes)", value=0)

                        diabetes_btn = gr.Button("🔍 Predict Diabetes Risk", elem_classes="btn-predict")

                        diabetes_out     = gr.HTML()
                        diabetes_pdf     = gr.File(label="📥 Download PDF Report")
                        with gr.Row():
                            diabetes_chart   = gr.Plot(label="Risk Assessment Chart")
                            diabetes_cm_plot = gr.Plot(label="Confusion Matrix")
                        diabetes_metrics = gr.HTML()

                    # ── TAB: Symptom Checker ──
                    with gr.Tab("🧠 Symptom Checker"):
                        gr.HTML("""
                        <div style='font-family:DM Sans,sans-serif;background:linear-gradient(135deg,#F0FDF4,#DCFCE7);border-radius:14px;padding:18px 22px;border:1px solid #BBF7D0;margin-bottom:20px'>
                          <h2 style='font-size:18px;font-weight:700;color:#1E293B;margin:0 0 4px'>🧠 AI Symptom Checker</h2>
                          <p style='font-size:13px;color:#64748B;margin:0'>Select all symptoms the patient is experiencing. The AI will match them to possible conditions.</p>
                        </div>
                        """)
                        symptoms = gr.CheckboxGroup(
                            choices=["chest pain","shortness of breath","fatigue","dizziness","palpitations",
                                     "frequent urination","weight loss","blurred vision","increased hunger",
                                     "headache","fever","body ache","pale skin"],
                            label="Select Symptoms"
                        )
                        symptom_btn    = gr.Button("🔍 Analyse Symptoms", elem_classes="btn-predict")
                        symptom_output = gr.HTML()

                    # ── TAB: Reports ──
                    with gr.Tab("📄 Reports"):
                        gr.HTML("""
                        <div style='font-family:DM Sans,sans-serif'>
                          <div style='background:linear-gradient(135deg,#EFF6FF,#DBEAFE);border-radius:14px;padding:22px;border:1px solid #BFDBFE;margin-bottom:20px'>
                            <h2 style='font-size:18px;font-weight:700;color:#1E293B;margin:0 0 6px'>📄 Medical Reports</h2>
                            <p style='font-size:13px;color:#64748B;margin:0'>PDF reports are automatically generated after each prediction. Use the Heart Disease or Diabetes tabs to run a prediction and download the report below.</p>
                          </div>
                          <div style='display:grid;grid-template-columns:1fr 1fr;gap:16px'>
                            <div style='background:white;border-radius:14px;padding:22px;border:1.5px dashed #BFDBFE;text-align:center'>
                              <div style='font-size:36px;margin-bottom:10px'>❤️</div>
                              <h3 style='font-size:15px;font-weight:600;color:#1E293B;margin-bottom:6px'>Heart Disease Report</h3>
                              <p style='font-size:12px;color:#94A3B8'>Run a Heart prediction to generate the PDF report. The download link will appear in the Heart Disease tab.</p>
                            </div>
                            <div style='background:white;border-radius:14px;padding:22px;border:1.5px dashed #DDD6FE;text-align:center'>
                              <div style='font-size:36px;margin-bottom:10px'>🩸</div>
                              <h3 style='font-size:15px;font-weight:600;color:#1E293B;margin-bottom:6px'>Diabetes Report</h3>
                              <p style='font-size:12px;color:#94A3B8'>Run a Diabetes prediction to generate the PDF report. The download link will appear in the Diabetes tab.</p>
                            </div>
                          </div>
                          <div style='background:#FFFBEB;border-radius:12px;padding:14px 18px;border:1px solid #FEF3C7;margin-top:16px'>
                            <p style='font-size:13px;color:#92400E;margin:0;font-weight:500'>📋 Reports include: Patient details · Risk score · Measured parameters · Personalized precautions · Model metadata</p>
                          </div>
                        </div>
                        """)

                    # ── TAB: History ──
                    with gr.Tab("📜 History"):
                        gr.HTML("""
                        <div style='font-family:DM Sans,sans-serif;background:linear-gradient(135deg,#FFFBEB,#FEF3C7);border-radius:14px;padding:18px 22px;border:1px solid #FDE68A;margin-bottom:20px'>
                          <h2 style='font-size:18px;font-weight:700;color:#1E293B;margin:0 0 4px'>📜 Patient History</h2>
                          <p style='font-size:13px;color:#64748B;margin:0'>View all past predictions for your account. Sorted by most recent.</p>
                        </div>
                        """)
                        history_btn   = gr.Button("🔄 Refresh History", elem_classes="btn-predict")
                        history_table = gr.Dataframe(
                            headers=["Patient Name","Age","Disease","Risk Level"],
                            wrap=True
                        )

                # Logout outside tabs
                gr.HTML("<div style='height:24px'></div>")
                logout_btn = gr.Button("🚪 Sign Out", elem_classes="btn-logout")

    # ============================================================
    # BUTTON LOGIC
    # ============================================================

    login_btn.click(
        login,
        inputs=[username_input, password_input],
        outputs=[dashboard, login_page, login_msg, user_state]
    )
    signup_btn.click(
        signup,
        inputs=[username_input, password_input],
        outputs=[login_msg]
    )
    logout_btn.click(
        logout,
        outputs=[dashboard, login_page]
    )
    heart_btn.click(
        heart_predict,
        inputs=[user_state, patient_name, patient_age, patient_sex,
                cp, bp, chol, fbs, thalach,
                patient_smoking, patient_exercise, patient_diet, patient_family],
        outputs=[heart_out, heart_pdf, heart_chart, heart_cm_plot, heart_metrics]
    )
    diabetes_btn.click(
        diabetes_predict,
        inputs=[user_state, d_name, d_age,
                preg, glucose, dbp, bmi, insulin,
                d_smoking, d_exercise, d_diet, d_family],
        outputs=[diabetes_out, diabetes_pdf, diabetes_chart, diabetes_cm_plot, diabetes_metrics]
    )
    symptom_btn.click(
        symptom_checker,
        inputs=[symptoms],
        outputs=[symptom_output]
    )
    history_btn.click(
        show_history,
        inputs=[user_state],
        outputs=[history_table]
    )

# ============================================================
# LAUNCH
# ============================================================
app.launch()



