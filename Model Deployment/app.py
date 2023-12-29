import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import joblib


input_collumns = ['position_level', 'gender_requirement', 'work_type',
       'degree_requirement', 'experience_requirement', 'company_size',
       'primary_industry', 'related_industry_1', 'related_industry_2',
       'recruiting_area', 'probation_period', 'min_age', 'max_age']

label_encoded_collumns = ['position_level', 'gender_requirement', 'work_type', 
                          'degree_requirement', 'experience_requirement', 'company_size', 
                          'primary_industry', 'related_industry_1', 'related_industry_2', 'recruiting_area']

app = Flask(__name__)

# Tải mô hình
model = joblib.load('../models/Extra Trees.pkl')

# Tải Label Encoders
label_encoders = {col: joblib.load(f'../models/{col}_label_encoder.pkl') 
                  for col in label_encoded_collumns}
@app.route('/')
def index():
    return render_template('index.html', 
                           input_collumns=input_collumns, 
                           label_encoded_collumns=label_encoded_collumns)

@app.route('/get-dropdown-options')
def get_dropdown_options():
    options = {}
    for col in label_encoded_collumns:
        # Lấy các lớp mà label encoder đã học
        le_classes = label_encoders[col].classes_.tolist()
        options[col] = le_classes
    return jsonify(options)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Nhận dữ liệu JSON từ request
        data = request.json

        # Tạo DataFrame từ dữ liệu đầu vào
        input_data = pd.DataFrame([data])

        # Áp dụng Label Encoding cho các cột phân loại
        for col in label_encoded_collumns:
            input_data[col] = label_encoders[col].transform(input_data[col])

        # Dự đoán
        prediction = model.predict(input_data)

        # Trả về kết quả
        return jsonify({'prediction': list(prediction)})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
