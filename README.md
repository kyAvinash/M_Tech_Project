# M_Tech_Project

# Diabetes Prediction System

![Project Logo](https://via.placeholder.com/150x50.png?text=Diabetes+Predictor)  
**Live Demo:** [https://kyavinash.pythonanywhere.com/](https://kyavinash.pythonanywhere.com/)

## 📌 Overview

A web-based diabetes risk assessment system that uses machine learning to predict the likelihood of diabetes based on health metrics, lifestyle factors, and personal information. The system implements a two-stage machine learning framework with Random Forest (ROC-AUC: 0.815) for accurate predictions.

## ✨ Features

- **Comprehensive Risk Assessment**:
  - Personal health metrics analysis
  - Lifestyle factors evaluation
  - Family history consideration

- **Advanced ML Integration**:
  - Random Forest classifier
  - Two-stage prediction framework
  - Probability scoring with confidence levels

- **User-Friendly Interface**:
  - Interactive forms with validation
  - Detailed results visualization
  - Actionable recommendations

- **Additional Tools**:
  - BMI calculator
  - Glucose impact estimator
  - Health data tracking

## 🛠️ Technology Stack

### Backend
- **Python** (3.8+)
- **Flask** (Web framework)
- **Scikit-learn** (Machine learning)
- **SQLite** (Database)

### Frontend
- **HTML5**, **CSS3**
- **Bootstrap 5** (Responsive design)
- **Font Awesome** (Icons)

### Deployment
- **PythonAnywhere** (Hosting)
- **Git** (Version control)

## 🚀 How to Use

1. **Access the Application**:
   Visit [https://kyavinash.pythonanywhere.com/](https://kyavinash.pythonanywhere.com/)

2. **Navigate to Prediction Page**:
   - Click on "Diabetes Risk Assessment" in the menu
   - Or go directly to: [https://kyavinash.pythonanywhere.com/predict](https://kyavinash.pythonanywhere.com/predict)

3. **Fill the Form**:
   - Enter your personal information
   - Provide health metrics
   - Describe your lifestyle habits

4. **Get Results**:
   - Receive immediate risk assessment
   - View detailed health analysis
   - Get personalized recommendations

## 📊 System Architecture

```mermaid
graph TD
    A[User Interface] --> B[Flask Application]
    B --> C[Random Forest Model]
    B --> D[Database]
    C --> E[Prediction Results]
    E --> F[Recommendation Engine]
