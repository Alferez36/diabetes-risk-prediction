import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Predicción Diabetes", layout="wide")

modelA = "Modelo A: Diagnóstico"
modelC = "Modelo C: Índice de Riesgo"

with st.sidebar:
    st.header("Elección del modelo")
    picked_model = st.radio(
        "Seleccione el modelo de predicción:",
        (modelA, modelC),
        help="El modelo A es una herramienta de diganóstico para los médicos y el Modelo C es una predicción en base a los hábitos"
    )
    
    st.divider()


@st.cache_resource
def load_assets(model_type):
    if model_type == modelA: 
        model = joblib.load("model_A_forest.joblib")
        preprocessor = joblib.load("preprocessor_A.joblib")
    else: 
        model = joblib.load("model_C_forest.joblib")
        preprocessor = joblib.load("preprocessor_C.joblib")
    return model, preprocessor

try:
    model, preprocessor = load_assets(picked_model)
except Exception as e:
    st.error(
        "Error al cargar los archivos del modelo. Los archivos .joblib deben estar presentes dentro de la misma carpeta."
    )
    st.stop()

st.title(f"Diagnóstico de Diabetes. {picked_model}")
if picked_model==modelA: 
    st.info(
        "Este modelo utiliza biomarcadores clínicos (Glucosa, HbA1c) para confirmar la presencia de diabetes."
    )
else: 
    st.info(
        "Este modelo no utiliza biomarcadores clínicos."
    )

tabs_list = ["Perfil", "Vitales y Lípidos", "Antecendentes y Estilo de vida"]
if picked_model == modelA:
    tabs_list.insert(1,"Biomarcadores") # se añade la página de glucosa al modelo A
    
tabs = st.tabs(tabs_list)

with st.form("clinical_form"):

    with tabs[0]:
        c_a, c_b = st.columns(2)
        age = c_a.number_input("Edad", 1, 120, 45)
        gender = c_a.selectbox("Género", ["Male", "Female", "Other"])
        ethnicity = c_a.selectbox(
            "Etnia", ["Asian", "Black", "Hispanic", "White", "Other"]
        )
        bmi = c_a.number_input("IMC (BMI)", 10.0, 60.0, 26.5)
        risk_score = c_b.slider("Diabetes Risk Score previo", 0.0, 1.0, 0.4)
        employment = c_b.selectbox(
            "Empleo", ["Employed", "Unemployed", "Student", "Retired"]
        )
        education = c_b.selectbox(
            "Educación", ["No formal", "Highschool", "Graduate", "Postgraduate"]
        )
        income = c_b.selectbox(
            "Ingresos", ["Low", "Lower-Middle", "Middle", "Upper-Middle", "High"]
        )

    if picked_model == modelA:
        with tabs[1]:
            st.subheader("Biomarcadores de Glucosa")
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                hba1c = st.number_input(
                    "HbA1c (%)", 4.0, 15.0, 5.4, help="Hemoglobina Glicosilada"
                )
            with c2:
                glu_fasting = st.number_input("Glucosa Basal (mg/dL)", 50, 400, 95)
            with c3:
                glu_post = st.number_input("Glucosa Postprandial (mg/dL)", 70, 500, 120)
            with c4:
                insulin = st.number_input("Nivel de Insulina (µU/mL)", 2.0, 100.0, 15.0)
        idx = 1
    else: 
        idx = 0
        
        
    with tabs[1+idx]:
        st.subheader("Signos Vitales y lípidos")
        c_v1, c_v2 = st.columns(2)
        sys_bp = c_v1.number_input("Sistólica", 80, 200, 120)
        dia_bp = c_v1.number_input("Diastólica", 50, 120, 80)
        heart_rate = c_v1.number_input("Frecuencia Cardíaca", 40, 150, 72)
        chol = c_v2.number_input("Colesterol Total", 100, 400, 200)
        tri = c_v2.number_input("Triglicéridos", 50, 500, 150)
        hdl = c_v2.number_input("HDL", 20, 100, 50)
        ldl = c_v2.number_input("LDL", 50, 300, 120)

    with tabs[2+idx]:
        st.subheader("Antecedentes y Estilo de Vida")
        c_e1, c_e2 = st.columns(2)
        fam_hist = c_e1.checkbox("Historia Familiar de Diabetes")
        hyp_hist = c_e1.checkbox("Historia de Hipertensión")
        cardio = c_e1.checkbox("Historia Cardiopatía")
        smoking = c_e1.selectbox("Fumador", ["Never", "Former", "Current"])

        activity = c_e2.number_input("Actividad Física (min/sem)", 0, 1000, 150)
        alcohol = c_e2.number_input("Alcohol (unidades/sem)", 0, 100, 2)
        diet = c_e2.slider("Calidad de Dieta (0-10)", 0, 10, 6)
        sleep = c_e2.number_input("Sueño (h/día)", 0, 24, 7)
        screen = c_e2.number_input("Tiempo en Pantalla (h/día)", 0, 24, 4)
        whr = c_e2.number_input("WHR (Cintura/Cadera)", 0.5, 1.5, 0.85)

    submit = st.form_submit_button("EJECUTAR DIAGNÓSTICO")

if submit:
    data_dict = {
        "age": [age],
        "gender": [gender],
        "ethnicity": [ethnicity],
        "education_level": [education],
        "income_level": [income],
        "employment_status": [employment],
        "alcohol_consumption_per_week": [alcohol],
        "physical_activity_minutes_per_week": [activity],
        "diet_score": [diet],
        "sleep_hours_per_day": [sleep],
        "screen_time_hours_per_day": [screen],
        "smoking_status": [smoking],
        "bmi": [bmi],
        "waist_to_hip_ratio": [whr],
        "systolic_bp": [sys_bp],
        "diastolic_bp": [dia_bp],
        "heart_rate": [heart_rate],
        "cholesterol_total": [chol],
        "hdl_cholesterol": [hdl],
        "ldl_cholesterol": [ldl],
        "triglycerides": [tri],
        "family_history_diabetes": [1 if fam_hist else 0],
        "hypertension_history": [1 if hyp_hist else 0],
        "cardiovascular_history": [1 if cardio else 0],
    }
    
    if picked_model == modelA:
        data_dict.update({
            "glucose_fasting": [glu_fasting],
            "glucose_postprandial": [glu_post],
            "insulin_level": [insulin],
            "hba1c": [hba1c],
            "diabetes_risk_score": [risk_score],
        })
    
    input_data = pd.DataFrame(data_dict)
        
    input_p = preprocessor.transform(input_data)
    prob = model.predict_proba(input_p)[0][1]

    # umbral sugerido : 0.3 (a partir de 30%)
    umbralA = 0.49
    umbralC = 0.49

    st.divider()
    col_res1, col_res2 = st.columns(2)

    with col_res1:
        st.metric(label="Probabilidad de Diabetes", value=f"{prob*100:.1f}%")

    if picked_model == modelC: 
        umbral = umbralC
    if picked_model == modelA: 
        umbral = umbralA
    
    with col_res2:
        if prob >= umbral:
            st.error("RESULTADO: POSITIVO PARA DIABETES")
            st.write("El modelo detecta patrones claros compatibles con diabetes.")
        else:
            st.success("RESULTADO: NEGATIVO")
            st.write(
                "Los valores se encuentran dentro de los rangos normales para el modelo."
            )

    st.warning("Nota: Esta herramienta no sustituye un diagnóstico médico profesional.")