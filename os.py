import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset (update with your dataset file path)
df = pd.read_csv('os.csv')  # Update with the correct file path

# Plot histogram for each feature to show the distribution
plt.figure(figsize=(12, 8))

# Select the columns of interest (e.g., 'Radiation', 'FIBRINOGEN', 'SOD_Activity')
columns = ['Radiation', 'FIBRINOGEN', 'SOD_Activity']  # Modify as needed
for i, column in enumerate(columns, 1):
    plt.subplot(2, 2, i)  # Adjust the subplot grid as necessary
    sns.histplot(df[column], kde=True, bins=20, color='skyblue')  # Histogram with KDE
    plt.title(f'Distribution of {column}')
    plt.xlabel(column)
    plt.ylabel('Frequency')

plt.tight_layout()
plt.show()


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from keras.models import Sequential
from keras.layers import Dense, Input
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, accuracy_score, classification_report
from sklearn.tree import DecisionTreeRegressor, plot_tree
import warnings
import tensorflow as tf

# Suppress PolynomialFeatures warning
warnings.filterwarnings('ignore', category=UserWarning, message="X does not have valid feature names")

# Load dataset and handle missing data
file_path = 'os.csv'   # Update with the correct path to your CSV fileds
df = pd.read_csv(file_path)
df.replace("", np.nan, inplace=True)
df.dropna(subset=['SOD_Activity', 'FIBRINOGEN', 'Radiation'], inplace=True)

# Convert columns to float for analysis
df['Radiation'] = df['Radiation'].astype(float)
df['SOD_Activity'] = df['SOD_Activity'].astype(float)
df['FIBRINOGEN'] = df['FIBRINOGEN'].astype(float)

# Generate heatmap for correlation matrix
plt.figure(figsize=(8, 6))
correlation_matrix = df.iloc[:, 1:].corr()  # Exclude the first column
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Heatmap')
plt.show()

# Prepare the input and target variables
X = df[['Radiation', 'FIBRINOGEN']]
y = df['SOD_Activity']

# Apply polynomial transformation for a more complex relationship
poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X)

# Standardize the data
scaler = StandardScaler()
X_poly_scaled = scaler.fit_transform(X_poly)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_poly_scaled, y, test_size=0.2, random_state=42)

# Build the neural network model
model = Sequential([
    Input(shape=(X_train.shape[1],)),
    Dense(64, activation='relu'),
    Dense(32, activation='relu'),
    Dense(1)  # Output layer for regression
])

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model with validation data
history = model.fit(X_train, y_train, epochs=100, batch_size=10, verbose=0, validation_data=(X_test, y_test))

# Decision Tree plotting
tree_model = DecisionTreeRegressor(max_depth=3)
tree_model.fit(X, y)

# Plot the decision tree
plt.figure(figsize=(12, 8))
plot_tree(tree_model, filled=True, feature_names=['Radiation', 'FIBRINOGEN'], rounded=True)
plt.title("Decision Tree for SOD Activity Prediction")
plt.show()
# Evaluate the model on test data
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)


print("Model Performance for SOD Prediction:")
print(f"Mean Absolute Error (MAE): {mae:.4f}")
print(f"Mean Squared Error (MSE): {mse:.4f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")


# Plotting the training and validation loss
plt.figure(figsize=(10, 5))
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Training and Validation Loss Over Epochs')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

sod_threshold = 3.5

# Function to calculate classification accuracy and generate classification report
def classify_and_evaluate(y_true, y_pred, threshold):
    # Convert predicted SOD activity and true values into binary classes based on the threshold
    y_pred_class = (y_pred > threshold).astype(int)
    y_true_class = (y_true > threshold).astype(int)

    # Calculate the accuracy
    accuracy = accuracy_score(y_true_class, y_pred_class)
    report = classification_report(y_true_class, y_pred_class, target_names=['Not Exposed', 'Exposed'])
    return accuracy, report

# Evaluate the model on the test set
test_accuracy, test_report = classify_and_evaluate(y_test, y_pred, sod_threshold)

# Print overall classification accuracy and report
print(f"\nTesting Accuracy: {test_accuracy * 100:.2f}%")
print("\nClassification Report for Test Set:")
print(test_report)

# Calculate validation accuracy (on validation data from training)
val_pred = model.predict(X_test)
val_accuracy, val_report = classify_and_evaluate(y_test, val_pred, sod_threshold)

print(f"\nValidation Accuracy: {val_accuracy * 100:.2f}%")

# Function to classify oxidative stress based on user input
def classify_oxidative_stress(radiation, fibrinogen):
    # Prepare the input data with polynomial transformation and scaling
    input_data = np.array([[radiation, fibrinogen]])
    input_data_poly = poly.transform(input_data)
    input_data_scaled = scaler.transform(input_data_poly)
    predicted_sod = model.predict(input_data_scaled)[0][0]

    # Classify based on threshold
    status = "Exposed to Oxidative Stress" if predicted_sod > sod_threshold else "Not Exposed to Oxidative Stress"
    return predicted_sod, status

# Get user input for Radiation and Fibrinogen
try:
    user_radiation = float(input("Enter Radiation level for prediction: "))
    user_fibrinogen = float(input("Enter Fibrinogen level for prediction: "))

    # Use the function to classify oxidative stress based on user input
    predicted_sod, exposure_status = classify_oxidative_stress(user_radiation, user_fibrinogen)

    # Display results
    print(f"\nPredicted SOD Activity: {predicted_sod:.2f}")
    print(f"Exposure Status: {exposure_status}")
    print(f"Threshold for Oxidative Stress (SOD): {sod_threshold}")

    # Visualization
    plt.figure(figsize=(6, 4))
    plt.bar(['Predicted SOD Activity'], [predicted_sod], color='blue')
    plt.axhline(sod_threshold, color='red', linestyle='--', label=f'SOD Threshold = {sod_threshold}')
    plt.text(0, predicted_sod + 0.1, f"{predicted_sod:.2f}", ha='center', color='black', fontsize=12)
    plt.title("User's SOD Activity Prediction and Oxidative Stress Threshold")
    plt.ylabel('SOD Activity')
    plt.legend()
    plt.show()

except ValueError:
    print("Please enter valid numerical values for Radiation and Fibrinogen.")


