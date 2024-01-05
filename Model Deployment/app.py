# import numpy as np
import joblib
import pandas as pd
from flask import Flask, jsonify, render_template, request

label_encoded_collumns = [
    "position_level",
    "gender_requirement",
    "work_type",
    "degree_requirement",
    "experience_requirement",
    "company_size",
    "primary_industry",
    "related_industry_1",
    "related_industry_2",
    "recruiting_area",
]


app = Flask(__name__)

# Tải mô hình
model = joblib.load("../models/Extra Trees.pkl")

# Tải Label Encoders
label_encoders = {
    col: joblib.load(f"../models/{col}_label_encoder.pkl")
    for col in label_encoded_collumns
}


@app.route("/")
# Trang chủ của ứng dụng
def index():
    input_collumns = [
        "position_level",
        "gender_requirement",
        "work_type",
        "degree_requirement",
        "experience_requirement",
        "company_size",
        "primary_industry",
        "related_industry_1",
        "related_industry_2",
        "recruiting_area",
        "probation_period",
        "min_age",
        "max_age",
    ]

    label_encoded_collumns = [
        "position_level",
        "gender_requirement",
        "work_type",
        "degree_requirement",
        "experience_requirement",
        "company_size",
        "primary_industry",
        "related_industry_1",
        "related_industry_2",
        "recruiting_area",
    ]

    column_translations = {
        "position_level": "Vị trí công việc công ty muốn tuyển là gì? ",
        "gender_requirement": "Yêu cầu giới tính của công ty như thế nào?",
        "work_type": "Công ty tuyển nhân viên của hình thức làm việc nào?",
        "degree_requirement": "Yêu cầu bằng cấp của công ty như thế nào?",
        "experience_requirement": "Yêu cầu kinh nghiệp của công như thế nào",
        "company_size": "Quy mô công ty như thế nào?",
        "primary_industry": "Vị trí cần tuyển có ngành nghề chính là gì ?",
        "related_industry_1": "Ngành nghề liên quan 1",
        "related_industry_2": "Ngành nghề liên quan 2",
        "recruiting_area": "Công ty muốn tuyển nhân viên làm việc ở đâu ?",
        "probation_period": "Nhân viên sẽ thử việc trong bao lâu ?",
        "min_age": "Tuổi tối thiểu công ty bạn yêu cầu là bao nhiêu ?",
        "max_age": (
            "Tuổi tối da đối với nhân viên công ty bạn yêu cầu "
            "là bao nhiêu ?"
        ),
    }
    return render_template(
        "index.html",
        input_collumns=input_collumns,
        label_encoded_collumns=label_encoded_collumns,
        column_translations=column_translations,
    )


@app.route("/get-dropdown-options")
# Lấy các lựa chọn cho các dropdown
def get_dropdown_options():
    options = {}
    for col in label_encoded_collumns:
        # Lấy các lớp mà label encoder đã học
        le_classes = label_encoders[col].classes_.tolist()
        options[col] = le_classes
    return jsonify(options)


@app.route("/predict", methods=["POST"])
# Dự đoán với những đầu vào đã chọn
def predict():
    try:
        # Nhận dữ liệu JSON từ request
        data = request.json
        # Nhận về một dictionary
        # print(data)

        # Tạo DataFrame từ dữ liệu đầu vào
        input_data = pd.DataFrame([data])
        print(input_data)
        # Áp dụng Label Encoding cho các cột phân loại
        for col in label_encoded_collumns:
            input_data[col] = label_encoders[col].transform(input_data[col])

        # Dự đoán
        prediction = model.predict(input_data)

        # Trả về kết quả
        return jsonify({"prediction": list(prediction)})

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)
