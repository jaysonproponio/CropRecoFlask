import csv
import random

# Crop labels
crop_labels = [
    "rice", "maize", "chickpea", "kidneybeans", "pigeonpeas",
    "mothbeans", "mungbean", "blackgram", "lentil", "pomegranate",
    "banana", "mango", "grapes", "watermelon", "muskmelon",
    "apple", "orange", "papaya", "coconut", "cotton",
    "jute", "coffee"
]

# Number of rows you want
num_rows = 1000

with open("crop_recommendation.csv", "w", newline="") as file:
    writer = csv.writer(file)
    
    # Header
    writer.writerow(["N", "P", "K", "temperature", "humidity", "ph", "rainfall", "label"])
    
    for _ in range(num_rows):
        N = random.randint(0, 140)
        P = random.randint(5, 145)
        K = random.randint(5, 205)
        temperature = round(random.uniform(8.0, 43.0), 2)
        humidity = round(random.uniform(14.0, 100.0), 2)
        ph = round(random.uniform(3.5, 9.5), 2)
        rainfall = round(random.uniform(20.0, 300.0), 2)
        label = random.choice(crop_labels)

        writer.writerow([N, P, K, temperature, humidity, ph, rainfall, label])

print("crop_recommendation.csv has been created successfully.")