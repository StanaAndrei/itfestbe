import tensorflow as tf
import numpy as np
import json
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt

print(tf.__version__ + "-----------------------------------")

# Citirea datelor din fisierul JSON
with open("products.json") as json_file:
    data = json.load(json_file)

# Extrage datele de nutrienți și scorurile de sănătate în liste separate
nutrients = [entry['nutrients'] for entry in data]
health_scores = [entry['health_score'] for entry in data]

# Convertirea listelor de dicționare în array-uri NumPy
nutrients_array = np.array([[nutrient[key] for key in nutrient] for nutrient in nutrients])
health_scores_array = np.array(health_scores)

# Setarea random seed
tf.random.set_seed(42)

# Setarea pentru callback pentru model
callback = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=8)

## NORMALIZAREA DATELOR

scaler = MinMaxScaler()
health_score_scaler = MinMaxScaler()

# Aplică scalarea asupra datelor de nutrienți
nutrients_scaled = scaler.fit_transform(nutrients_array)

# Normalizarea datelor de scoruri de sănătate
health_scores_scaled = health_score_scaler.fit_transform(health_scores_array.reshape(-1, 1))

# Împărțirea datelor în seturile de antrenare și de testare
x_train, x_test, y_train, y_test = train_test_split(nutrients_scaled, health_scores_scaled, test_size=0.2, random_state=42)

# x_train, x_test, y_train, y_test = train_test_split(nutrients_array, health_scores_array, test_size=0.2, random_state=42)

# Convert back to tensors for TensorFlow
x_train_tensor = tf.constant(x_train, dtype=tf.float32)
x_test_tensor = tf.constant(x_test, dtype=tf.float32)
y_train_tensor = tf.constant(y_train, dtype=tf.float32)
y_test_tensor = tf.constant(y_test, dtype=tf.float32)

#MODEL-------------------------------------------

#1 Crearea modelului
model_1 = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(8,)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1, activation='linear')

])

#2 Compilarea modelului
model_1.compile(optimizer='adam',
              loss='mean_squared_error',
              metrics=['mae'])


#3 Model fit
model_1.fit(x_train_tensor, y_train_tensor, validation_split=0.2, epochs=1600, callbacks=[tf.keras.callbacks.EarlyStopping(patience=8)])

#4 Evaluate the model 
print("EVALUATE THE MODEL")
print(model_1.evaluate(x_test, y_test))

# Hardcodează setul de date de intrare
input_data = np.array([[1740,9.6,72,13,8.7,1.5,3.9,1.3]])

# Normalizează datele de intrare folosind scalerul salvat
input_data_scaled = scaler.transform(input_data)

# Fă predicția folosind modelul
prediction_scaled = model_1.predict(input_data_scaled)

# Denormalizează predicția pentru a obține valoarea în intervalul original
prediction = health_score_scaler.inverse_transform(prediction_scaled)


# Afișează predicția denormalizată
print("Predicția (denormalizată):", prediction.flatten()[0])

model_1.save('model_1')

