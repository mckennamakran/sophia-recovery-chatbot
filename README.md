# Sophia: Relapse Chatbot
**By McKenna Makran**  
**Language:** Python  
**Environment:** PyCharm  




## Rundown
Sophia is an **empathetic, conversational AI chatbot** designed to support people in addiction recovery. It helps users:

- Reflect on their past experiences and health  
- Identify triggers and cravings  
- Classify their current relapse phase  
- Predict the probability of relapse  
- Offer emotionally intelligent advice and resources  

This project is more than just code; it’s an exploration into the psychology of addiction and human behavior, intertwined with practical machine learning solutions.



## Purpose & Psychological Insights
Not having any substance addictions myself, this project challenged me to **step into someone else’s experience**, learn deeply about relapse cycles, and confront **inner conflicts** around empathy, responsibility, and human fragility.  

Sophia is built to be **supportive, nonjudgmental, and educational**, combining technical prediction with psychological guidance. Every question, trigger, and craving assessment is designed to **promote self-reflection**, awareness, and informed action.



## Features
- Interactive, conversational user interface  
- Personal data collection: name, age, gender, addiction type  
- Triggers & cravings assessment  
- Health, stress, and self-esteem evaluation  
- Support system and life stressors tracking  
- Predictive relapse classification (Low / Medium / High)  
- Probability of relapse calculation (0–100%)  
- Personalized, psychologically-informed advice  


## How It Works
1. **User Input** – Sophia collects detailed information about the user’s experiences, health, and support system.  
2. **Data Cleaning & Encoding** – Categorical inputs are encoded using `OneHotEncoder` for machine learning compatibility.  
3. **Model Prediction** – Random Forest Classifier predicts the relapse phase; Random Forest Regressor predicts relapse probability.  
4. **Output & Guidance** – Users receive an overview of their data, risk assessment, and empathetic advice.  

It’s a **blend of human-centered design and technical rigor**, where machine learning supports psychological insight.


## Tech Stack
- **Python 3.11+** – Core programming language  
- **PyCharm IDE** – Development environment  
- **Pandas** – Data manipulation and preprocessing  
- **Scikit-learn** – Machine learning models (Random Forest Classifier & Regressor)  
- **CSV Module** – Data storage and retrieval  
- **OneHotEncoder** – Encoding categorical data for models  

