import streamlit as st
import pandas as pd
import os

# Load your dataset (update the path to your CSV file)
csv_file = r"C:\Users\abilp\movies_with_ratings.csv"  # Replace with the path to your CSV file
image_folder = r"C:\Users\abilp\Desktop\archive\Multi_Label_dataset\Images"  # Replace with your image folder path

# Read the dataset
try:
    df = pd.read_csv(csv_file)
except FileNotFoundError:
    st.error(f"File not found: {csv_file}")
    st.stop()

# Ensure required columns exist and update column names
required_columns = ["Id", "Genre", "Ratings"]
if not all(col in df.columns for col in required_columns):
    st.error(f"CSV file must contain the following columns: {required_columns}")
    st.stop()

# Convert 'Genre' from string representation to list if necessary
if isinstance(df["Genre"].iloc[0], str) and df["Genre"].iloc[0].startswith("["):
    df["Genre"] = df["Genre"].apply(eval)

# Streamlit app
st.title("Movie Recommendation App")

# Extract unique genres for selection
all_genres = set(g for genres in df["Genre"] for g in genres)
selected_genre = st.selectbox("Select Genre:", sorted(all_genres))

# Add a slider for filtering by ratings
min_rating = st.slider("Select Minimum Rating:", min_value=1, max_value=10, value=5)

# Filter movies by the selected genre and minimum rating
filtered_movies = df[(df["Genre"].apply(lambda x: selected_genre in x)) & (df["Ratings"] >= min_rating)]

# Display filtered movies
st.subheader(f"Recommended Movies for Genre: {selected_genre} with chosen Ratings {min_rating}")

if filtered_movies.empty:
    st.write("No movies found for this genre and rating.")
else:
    # Group movies into rows of three
    rows = [filtered_movies.iloc[i:i+3] for i in range(0, len(filtered_movies), 3)]

    for row in rows:
        cols = st.columns(3)  # Create three columns
        for col, (_, movie) in zip(cols, row.iterrows()):
            movie_id = movie["Id"]
            rating = movie["Ratings"]
            # Construct the image file path
            image_path = os.path.join(image_folder, f"{movie_id}.jpg")

            with col:
                if os.path.exists(image_path):
                    st.image(image_path, caption=f"Rating: {rating}/10", use_container_width=True)
                else:
                    st.write(f"Image not found for Movie ID: {movie_id}")
                st.write(f"**Genres:** {', '.join(movie['Genre'])}")
