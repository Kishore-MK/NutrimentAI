import streamlit as st
import cv2
import numpy as np
from PIL import Image
from roboflow import Roboflow
import json
import tempfile
import os
import streamlit as st
# 99dfeee62adec0ce99ba5bc5b559352
from py_edamam import Edamam
from bmi import calculate_bmr,calculate_tdee
rf = Roboflow(api_key="2uZE1vKgi52zC8NJG5eW")
project = rf.workspace().project("-food-detection")
model = project.version(1).model

# infer on a local image
def detect_image(image):
    result=(model.predict(image, confidence=40, overlap=30).json())

    return result['predictions'][0]['class']


def getcalories(food_item):
     
    e = Edamam(nutrition_appid='2d7c855d',
            nutrition_appkey='3cb57ad0fb6b9cbf1f8623747575e942',
            )
            
    data= e.search_nutrient("1"+str(food_item))
    return data['calories'],data['dietLabels'],data['totalWeight']


def main():
    st.title("Nutriment AI")
    
    st.write("Please enter the following information:")

    # Input fields
    height = st.number_input("Height (m)", min_value=0.0, step=0.1, format="%.1f")
    weight = st.number_input("Weight (kg)", min_value=0.0, step=0.1, format="%.1f")
    age = st.number_input("Age (years)", min_value=0, step=1)
    gender = st.selectbox("Gender", options=["Male", "Female"])
    activity_level = st.selectbox("Activity Level", options=["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])

    if st.button("Calculate"):
        # Process inputs and perform calculations here
        st.write("BMI:",weight / (height ** 2))
        bmr=calculate_bmr(weight,height,age,gender)
        st.write("BMR: "+str(bmr))
        tdee=calculate_tdee(float(calculate_bmr(weight,height,age,gender)),activity_level)
        st.write("TDEE: "+str(tdee))



    # Create an image upload widget
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

    if uploaded_image is not None:
        # Display the uploaded image
        image = Image.open(uploaded_image)
        st.image(image, caption='Uploaded Image', use_column_width=True)
        if uploaded_image:
            temp_dir = tempfile.mkdtemp()
            path = os.path.join(temp_dir, uploaded_image.name)
            with open(path, "wb") as f:
                    f.write(uploaded_image.getvalue())
        # Perform object detection when 'Detect' button is clicked
        if st.button("Detect"):
            # Call object detection function
            detected_image = detect_image(path)
            calories = getcalories(detected_image)
            # Display the detected image
            str(st.text("Food Item: "+ detected_image))
            # print(type(st.text(calories)))
            st.text("Calories: "+str(calories[0]))
            st.text("Diet: "+str(calories[1]))
            st.text("Weight: "+str(calories[2])+' g')
            st.text("Remaining calory intake: "+str(calculate_tdee(float(calculate_bmr(weight,height,age,gender)),activity_level)-calories[0]))

if __name__ == '__main__':
    main()
