'''import streamlit as st
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import StandardScaler,LabelEncoder,OneHotEncoder
import pickle
import warnings
import keras
import h5py
import json
warnings.filterwarnings('ignore')


with h5py.File("model.h5", "r+") as f:
    config = json.loads(f.attrs["model_config"])

    for layer in config["config"]["layers"]:
        if "config" in layer:
            layer["config"].pop("quantization_config", None)

    f.attrs["model_config"] = json.dumps(config).encode("utf-8")


#Load the model
model=keras.models.load_model('model.h5')

#Load the encoders and scalers
#label encoder
with open('label_encoder_gender.pkl','rb') as file:
    label_encoder_gender=pickle.load(file)


#OneHotEncoder
with open('onehot_encoder_geo.pkl','rb') as file:
    onehot_encoder_geo=pickle.load(file)


#loadthe scaler file
with open('scaler.pkl','rb') as file:
    scaler=pickle.load(file)


#Creating the Streamlit app
st.title("Customer Churn Prediction")
st.markdown("---")


#User input
print(onehot_encoder_geo.categories_[0])
geography=st.selectbox("Geography",onehot_encoder_geo.categories_[0])

gender=st.selectbox("Gender",label_encoder_gender.classes_)

age=st.slider("Age",18,92)

balance=st.number_input("Balance",min_value=1000)

credit_score=st.number_input("Credit Score")

estimated_salary=st.number_input("Estimated Salary")

tenure=st.slider("Tenure",0,10)

num_of_products=st.slider("Number of Products",1,4)

has_cr_card=st.selectbox("Has credit card",[0,1])

is_active_members= st.selectbox("Is active member",[0,1])


#Creating one DataFrame w.r.t the input data

print(label_encoder_gender.transform([gender]))

input_data =pd.DataFrame({

    'CreditScore':[credit_score],
    'Gender':[label_encoder_gender.transform([gender])[0]],
    'Age':[age],
    'Tenure':[tenure],
    'Balance':[balance],
    'NumOfProducts':[num_of_products],
    'HasCrCard':[has_cr_card],
    'IsActiveMember':[is_active_members],
    'EstimatedSalary':[estimated_salary]


}
)

#One-hot encode Geography
geo_encoded=onehot_encoder_geo.transform([[geography]]).toarray()
print(geo_encoded)
geo_encoded_df =pd.DataFrame(geo_encoded,columns=onehot_encoder_geo.get_feature_names_out(['Geography']))
print(geo_encoded_df)



#   DataFrame-1          DataFrame-2

#0   data-1              3  data-1

#1   data-2               4  data-2

#2    data-3              5  data-3




#Combine one-hot encoded columns with  input data
input_data=pd.concat([input_data.reset_index(drop=True),geo_encoded_df],axis=1)
print(input_data)


#Scalized the input data
input_data_scaled=scaler.transform(input_data)
print(input_data_scaled)


#Prediction Operation

predict=model.predict(input_data_scaled)
print(predict)
pred_prob=predict[0][0]

st.write(f"The probability is {pred_prob:.3f}")

if pred_prob >=0.5:
    st.write("Customer's bank account will not be terminated")
else:
    st.write("Customer's bank account will be terminated")
    '''

import streamlit as st
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
import pickle
import warnings
import keras
import h5py
import json
import matplotlib.pyplot as plt
from tensorflow.keras import Model

warnings.filterwarnings('ignore')

# ---------------- FIX MODEL FILE ----------------
with h5py.File("model.h5", "r+") as f:
    config = json.loads(f.attrs["model_config"])

    for layer in config["config"]["layers"]:
        if "config" in layer:
            layer["config"].pop("quantization_config", None)

    f.attrs["model_config"] = json.dumps(config).encode("utf-8")

# ---------------- LOAD MODEL ----------------
model = keras.models.load_model('model.h5')

# ---------------- LOAD ENCODERS ----------------
with open('label_encoder_gender.pkl','rb') as file:
    label_encoder_gender = pickle.load(file)

with open('onehot_encoder_geo.pkl','rb') as file:
    onehot_encoder_geo = pickle.load(file)

with open('scaler.pkl','rb') as file:
    scaler = pickle.load(file)

# ---------------- UI DESIGN ----------------
st.set_page_config(page_title="Churn Predictor", layout="centered")

st.markdown("""
<style>
.main {background-color: #f4f6f9;}
.title {text-align:center; font-size:40px; font-weight:bold; color:#2c3e50;}
.card {
    padding:20px; border-radius:15px; background:white;
    box-shadow:0px 4px 12px rgba(0,0,0,0.1); margin-bottom:20px;
}
.result-box {
    padding:15px; border-radius:10px; text-align:center;
    font-size:20px; font-weight:bold;
}
.success {background-color:#d4edda; color:#155724;}
.danger {background-color:#f8d7da; color:#721c24;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">💳 Customer Churn Prediction</div>', unsafe_allow_html=True)

# ---------------- INPUT SECTION ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)

geography = st.selectbox("Geography", onehot_encoder_geo.categories_[0])
gender = st.selectbox("Gender", label_encoder_gender.classes_)
age = st.slider("Age", 18, 92)
balance = st.number_input("Balance", min_value=1000)
credit_score = st.number_input("Credit Score")
estimated_salary = st.number_input("Estimated Salary")
tenure = st.slider("Tenure", 0, 10)
num_of_products = st.slider("Number of Products", 1, 4)
has_cr_card = st.selectbox("Has Credit Card", [0,1])
is_active_members = st.selectbox("Is Active Member", [0,1])

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- DATA PROCESSING ----------------
input_data = pd.DataFrame({
    'CreditScore':[credit_score],
    'Gender':[label_encoder_gender.transform([gender])[0]],
    'Age':[age],
    'Tenure':[tenure],
    'Balance':[balance],
    'NumOfProducts':[num_of_products],
    'HasCrCard':[has_cr_card],
    'IsActiveMember':[is_active_members],
    'EstimatedSalary':[estimated_salary]
})

# One-hot encoding
geo_encoded = onehot_encoder_geo.transform([[geography]]).toarray()
geo_encoded_df = pd.DataFrame(
    geo_encoded,
    columns=onehot_encoder_geo.get_feature_names_out(['Geography'])
)

# Combine
input_data = pd.concat([input_data.reset_index(drop=True), geo_encoded_df], axis=1)

# Scale
input_data_scaled = scaler.transform(input_data)

# ---------------- PREDICTION ----------------
predict = model.predict(input_data_scaled)
pred_prob = predict[0][0]

# ---------------- RESULT ----------------
if pred_prob >= 0.5:
    st.markdown(f'<div class="result-box danger">⚠️ High Risk of Churn ({pred_prob:.2f})</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="result-box success">✅ Customer Safe ({pred_prob:.2f})</div>', unsafe_allow_html=True)

# ---------------- ANN VISUALIZATION ----------------
st.markdown("### 🧠 ANN Structure Visualization")

def plot_ann():
    fig, ax = plt.subplots(figsize=(6,4))
    layers = [12, 8, 6, 1]

    for i, layer_size in enumerate(layers):
        for j in range(layer_size):
            ax.scatter(i, j, s=100)

    for i in range(len(layers)-1):
        for j in range(layers[i]):
            for k in range(layers[i+1]):
                ax.plot([i, i+1], [j, k], linewidth=0.3)

    ax.set_title("ANN Structure")
    ax.axis('off')
    st.pyplot(fig)

plot_ann()

# ---------------- SHOW SCALED INPUT ----------------
st.markdown("### 🔢 Scaled Input Features")
st.write(pd.DataFrame(input_data_scaled, columns=input_data.columns))

