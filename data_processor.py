import pandas as pd
import glob
import os

def load_and_process_csvs(directory_path="data_files"):
    """
    Loads all CSV files from the specified directory using glob and processes them.

    Assumes all CSV files have a standard structure needed for analysis.
    Returns a list of DataFrames, one for each successfully loaded file.
    """
    search_pattern = os.path.join(directory_path, "*.csv")
    all_files = glob.glob(search_pattern)

    if not all_files:
        print(f"⚠️ Warning: No CSV files found in the directory: {directory_path}")
        return []

    df_list = []
    for filename in all_files:
        try:
            # Read the CSV file
            df = pd.read_csv(filename)
            print(f"✅ Successfully loaded {filename} with shape: {df.shape}")
            df_list.append(df)
        except pd.errors.EmptyDataError:
            print(f"❌ Warning: Skipping empty file: {filename}")
        except pd.errors.ParserError:
            print(f"❌ Error parsing CSV content in file: {filename}. Check delimiters or format.")
        except FileNotFoundError:
            print(f"❌ Error: File not found at path: {filename}")
        except Exception as e:
            print(f"❌ An unexpected error occurred while processing {filename}: {e}")

    return df_list

def analyze_dataframes(df_list):
    """
    Placeholder for the actual analysis logic.
    This function takes a list of DataFrames and performs specific steps.
    The user must customize this function based on their analytical goal 
    (e.g., merging, statistical aggregation, feature engineering).
    """
    if not df_list:
        print("🛑 Cannot perform analysis: No dataframes were loaded.")
        return None

    # --- EXAMPLE ANALYSIS STAGE 1: CONCATENATE AND CLEAN ---
    try:
        # Concatenate all loaded DataFrames into one master DataFrame
        master_df = pd.concat(df_list, ignore_index=True)
        print(f"✨ Master DataFrame created with total shape: {master_df.shape}")

        # Example cleaning step: Drop rows where 'ID' (assuming this column exists in all files) is null
        if 'ID' in master_df.columns:
            original_count = len(master_df)
            master_df.dropna(subset=['ID'], inplace=True) # Requires an ID column
            print(f"🧹 Dropped {original_count - len(master_df)} rows with missing 'ID'.")
        else:
             print("⚠️ Skipping ID-based cleaning: 'ID' column not found.")

    except Exception as e:
        print(f"🚨 Error during data concatenation/cleaning: {e}")
        return None


    # --- EXAMPLE ANALYSIS STAGE 2: AGGREGATION (CUSTOMIZE THIS) ---
    print("\\n--- Starting Custom Analysis Stage ---")
    final_result = None

    # **IMPORTANT:** Replace the logic below with your actual business logic.
    '''
    Example: Group by 'Category' and calculate the average of 'Value'.
    if 'Category' in master_df.columns and 'Value' in master_df.columns:
        final_result = master_df.groupby('Category')['Value'].mean().reset_index()
        print("\\n📊 Successfully calculated the mean value per category.")
    '''

    # For now, we will simply return the cleaned master DataFrame as a placeholder output
    final_result = master_df
    return final_result


if __name__ == "__main__":
    # 1. Load Data
    dataframes = load_and_process_csvs()

    # 2. Analyze Data
    final_output_df = analyze_dataframes(dataframes)

    # 3. Output Results
    if final_output_df is not None:
        print("\\n==============================")
        print("✅ Analysis Complete.")
        print("The final resulting DataFrame structure:")
        print(final_output_df.head()) 

        # Save the result to a new CSV file
        output_path = "processed_and_analyzed_output.csv"
        try:
            final_output_df.to_csv(output_path, index=False)
            print(f"🎉 Success! Results saved to {output_path}")
        except Exception as e:
            print(f"🚨 Could not save output file. Error: {e}")

# Remember to create a 'data_files' directory and place your CSVs inside before running this script.