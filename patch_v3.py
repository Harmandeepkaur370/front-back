with open('app.py', 'r', encoding='utf-8') as f:
    orig = f.read()

parts = orig.split('# ============================================================\n# GRADIO UI\n# ============================================================')
if len(parts) < 2:
    parts = orig.split('# GRADIO UI')

with open('new_ui.txt', 'r', encoding='utf-8') as f:
    new_ui = f.read()

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(parts[0] + '# ============================================================\n# GRADIO UI\n# ============================================================\n' + new_ui)

print("Patching V3 Complete.")
