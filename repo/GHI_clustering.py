import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Directory containing JSON files
base_dir = r"D:\2025\json"

def clusterGHI(file_path):
    data = []
    with open(file_path, "r") as file:
        for line in file:
            data.append(eval(line.strip()))  # Convert each JSON object

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Extract relevant columns
    df = df[['irradiance', 'image_path']].rename(columns={'irradiance': 'GHI'})

    # Normalize GHI values
    scaler = StandardScaler()
    df['GHI_scaled'] = scaler.fit_transform(df[['GHI']])

    # Apply K-Means clustering
    k = 5  # Choose number of clusters (adjustable)
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    df['Cluster'] = kmeans.fit_predict(df[['GHI_scaled']])

    # Assign sky condition labels automatically
    centroids = np.argsort(kmeans.cluster_centers_.flatten())  # Sort clusters by GHI
    sky_labels = {
        centroids[0]: "Clear Sky (High Clear-Sky Index, Very Low Cloud Cover)",
        centroids[1]: "Overcast High Irradiance (Overirradiance Phenomenon)",
        centroids[2]: "Partly Cloudy (Linear Clear-Sky Index & Cloud Cover)",
        centroids[3]: "Partly Clear (Low Cloud Cover, Low Clear-Sky Index)", 
        centroids[4]: "Overcast (Very Low Clear-Sky Index, High Cloud Cover)",
    }
    df['Sky_Condition'] = df['Cluster'].map(sky_labels)

    # Display classified results
    print(df[['image_path', 'GHI', 'Sky_Condition']])

    # Save results to CSV
    df[['image_path', 'GHI', 'Sky_Condition']].to_csv("classified_sky_images.csv", index=False)

    # Visualize the classification
    plt.scatter(df.index, df['GHI'], c=df['Cluster'], cmap='viridis', alpha=0.7)
    plt.xlabel("Time")
    plt.ylabel("GHI (W/m²)")
    plt.title("Sky Classification Using K-Means on GHI")
    plt.colorbar(label="Cluster")
    plt.show()


# Loop through all JSON files in subdirectories
for month in os.listdir(base_dir):
    month_path = os.path.join(base_dir, month)
    if os.path.isdir(month_path):
        for date in os.listdir(month_path):
            date_path = os.path.join(month_path, date)
            if os.path.isfile(date_path) and date_path.endswith(".json"):
                clusterGHI(date_path)