import gradio as gr
import backend

# -----------------------------
# Login function
# -----------------------------
def login(username, password):
    user = backend.verify_user(username, password)
    if user:
        return "Login Successful"
    else:
        return "Login Failed"

# -----------------------------
# Add patient function
# -----------------------------
def add_patient(name, age, gender, disease_type, predicted_positive):
    return backend.add_patient(name, age, gender, disease_type, predicted_positive)

# -----------------------------
# Show analytics function
# -----------------------------
def show_analytics():
    data = backend.get_analytics()
    return f"Total Patients: {data['total_patients']}\nHeart Positives: {data['heart_positive']}\nDiabetes Positives: {data['diabetes_positive']}"

# -----------------------------
# Gradio Interface
# -----------------------------
with gr.Blocks() as demo:

    with gr.Tab("Login"):
        username = gr.Textbox(label="Username")
        password = gr.Textbox(label="Password", type="password")
        login_output = gr.Textbox()
        login_btn = gr.Button("Login")
        login_btn.click(login, [username, password], login_output)

    with gr.Tab("Add Patient"):
        name = gr.Textbox(label="Name")
        age = gr.Number(label="Age")
        gender = gr.Radio(["Male", "Female"], label="Gender")
        disease_type = gr.Radio(["heart", "diabetes"], label="Disease Type")
        predicted = gr.Checkbox(label="Predicted Positive?")
        add_output = gr.Textbox()
        add_btn = gr.Button("Add Patient")
        add_btn.click(add_patient, [name, age, gender, disease_type, predicted], add_output)

    with gr.Tab("Analytics"):
        analytics_output = gr.Textbox()
        analytics_btn = gr.Button("Show Analytics")
        analytics_btn.click(show_analytics, [], analytics_output)

demo.launch()