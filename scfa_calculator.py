#!/usr/bin/env python3
"""
SCFA Expected Value Calculator

This script collects 100% SCFA production data for individual fibers
and calculates expected values for fiber mixtures based on weighted averages.
"""

import pandas as pd
import sys

def get_positive_int(prompt):
    """Get a positive integer from user input."""
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid integer.")

def get_positive_float(prompt):
    """Get a positive float from user input."""
    while True:
        try:
            value = float(input(prompt))
            if value >= 0:
                return value
            print("Please enter a non-negative number.")
        except ValueError:
            print("Please enter a valid number.")

def collect_fiber_data():
    """
    Interactively collect fiber names, replicates, and SCFA production data.

    Returns:
        dict: Nested dictionary with structure:
              {fiber_name: {replicate_num: {scfa_type: value}}}
        list: List of fiber names in order entered
    """
    print("\n" + "="*60)
    print("SCFA PRODUCTION DATA COLLECTION")
    print("="*60 + "\n")

    # Get number of fibers
    num_fibers = get_positive_int("How many fibers do you want to analyze? ")

    fiber_data = {}
    fiber_names = []

    # For each fiber
    for i in range(num_fibers):
        print(f"\n--- Fiber {i+1}/{num_fibers} ---")

        # Get fiber name
        fiber_name = input(f"Enter the name of fiber {i+1}: ").strip().upper()
        while not fiber_name:
            print("Fiber name cannot be empty.")
            fiber_name = input(f"Enter the name of fiber {i+1}: ").strip().upper()

        fiber_names.append(fiber_name)
        fiber_data[fiber_name] = {}

        # Get number of replicates for this fiber
        num_replicates = get_positive_int(f"How many replicates for {fiber_name}? ")

        # For each replicate
        for rep in range(1, num_replicates + 1):
            print(f"\n  Replicate {rep}/{num_replicates} for {fiber_name} (100% concentration)")

            acetate = get_positive_float(f"    Acetate production: ")
            propionate = get_positive_float(f"    Propionate production: ")
            butyrate = get_positive_float(f"    Butyrate production: ")

            fiber_data[fiber_name][rep] = {
                "acetate": acetate,
                "propionate": propionate,
                "butyrate": butyrate
            }

    print(f"\n{'='*60}")
    print("Data collection complete!")
    print(f"{'='*60}\n")

    return fiber_data, fiber_names

def display_collected_data(fiber_data):
    """Display the collected fiber data in a readable format."""
    print("\n" + "="*60)
    print("COLLECTED SCFA PRODUCTION DATA (100% concentration)")
    print("="*60 + "\n")

    for fiber, replicates in fiber_data.items():
        print(f"{fiber}:")
        for rep, scfa_values in replicates.items():
            print(f"  Replicate {rep}:")
            print(f"    Acetate:    {scfa_values['acetate']:.2f}")
            print(f"    Propionate: {scfa_values['propionate']:.2f}")
            print(f"    Butyrate:   {scfa_values['butyrate']:.2f}")
        print()

def load_combinations_csv(fiber_names):
    """
    Load the CSV file containing fiber mixture combinations.

    Args:
        fiber_names: List of expected fiber column names

    Returns:
        pd.DataFrame: DataFrame with combinations
    """
    print("\n" + "="*60)
    print("LOAD COMBINATION DATA")
    print("="*60 + "\n")

    while True:
        csv_path = input("Enter the path to your CSV file with combinations: ").strip()

        try:
            # Try reading the CSV
            df = pd.read_csv(csv_path)

            # Clean column names
            df.columns = [c.strip() for c in df.columns]

            # Check if required columns exist
            if 'Replicate' not in df.columns:
                print("Error: CSV must contain a 'Replicate' column.")
                continue

            # Check if all fiber columns exist
            missing_fibers = [f for f in fiber_names if f not in df.columns]
            if missing_fibers:
                print(f"Warning: The following fibers are missing from CSV: {', '.join(missing_fibers)}")
                print("Available columns:", ', '.join(df.columns))
                add_cols = input("Do you want to continue anyway? (yes/no): ").strip().lower()
                if add_cols != 'yes':
                    continue

            # Convert numeric columns
            df['Replicate'] = pd.to_numeric(df['Replicate'], errors='coerce')
            for fiber in fiber_names:
                if fiber in df.columns:
                    df[fiber] = pd.to_numeric(df[fiber], errors='coerce').fillna(0)

            # Drop rows with invalid replicates
            df = df.dropna(subset=['Replicate'])
            df['Replicate'] = df['Replicate'].astype(int)

            print(f"\nSuccessfully loaded {len(df)} combinations from CSV.")
            print(f"Replicates found: {sorted(df['Replicate'].unique())}")

            return df

        except FileNotFoundError:
            print(f"Error: File '{csv_path}' not found. Please try again.")
        except Exception as e:
            print(f"Error reading CSV: {e}")
            print("Please try again.")

def calculate_expected_values(fiber_data, combinations_df, fiber_names):
    """
    Calculate expected SCFA production for each combination.

    Args:
        fiber_data: Dictionary with 100% SCFA data
        combinations_df: DataFrame with mixture ratios
        fiber_names: List of fiber names

    Returns:
        pd.DataFrame: DataFrame with expected values
    """
    print("\n" + "="*60)
    print("CALCULATING EXPECTED VALUES")
    print("="*60 + "\n")

    scfa_types = ["acetate", "propionate", "butyrate"]
    results = []

    for idx, row in combinations_df.iterrows():
        replicate = int(row['Replicate'])

        # Initialize SCFA totals
        expected = {scfa: 0.0 for scfa in scfa_types}

        # For each fiber in the combination
        for fiber in fiber_names:
            if fiber not in combinations_df.columns:
                continue

            ratio = row[fiber]

            # Skip if ratio is 0 or fiber not in our data
            if ratio == 0 or fiber not in fiber_data:
                continue

            # Check if this replicate exists for this fiber
            if replicate not in fiber_data[fiber]:
                print(f"Warning: Replicate {replicate} not found for {fiber}. Using replicate 1 as fallback.")
                use_rep = 1
            else:
                use_rep = replicate

            # Add weighted contribution
            for scfa in scfa_types:
                expected[scfa] += ratio * fiber_data[fiber][use_rep][scfa]

        # Calculate total SCFA
        total_scfa = sum(expected.values())

        # Build result record
        result = {
            'Replicate': replicate,
            **{fiber: row.get(fiber, 0) for fiber in fiber_names},
            'expected_acetate': round(expected['acetate'], 2),
            'expected_propionate': round(expected['propionate'], 2),
            'expected_butyrate': round(expected['butyrate'], 2),
            'expected_total_scfa': round(total_scfa, 2)
        }

        # Add substrate column if it exists
        if 'Substrate' in row:
            result = {'Substrate': row['Substrate'], **result}

        results.append(result)

    results_df = pd.DataFrame(results)
    print(f"Calculated expected values for {len(results_df)} combinations.")

    return results_df

def save_results(results_df):
    """Save results to CSV file."""
    output_file = "scfa_expected_values.csv"
    results_df.to_csv(output_file, index=False)
    print(f"\n{'='*60}")
    print(f"Results saved to: {output_file}")
    print(f"{'='*60}\n")

    return output_file

def display_summary(results_df):
    """Display summary statistics of the results."""
    print("\n" + "="*60)
    print("SUMMARY OF EXPECTED VALUES")
    print("="*60 + "\n")

    print("First 10 rows:")
    print(results_df.head(10).to_string(index=False))

    print("\n\nDescriptive Statistics:")
    scfa_cols = [c for c in results_df.columns if c.startswith('expected_')]
    if scfa_cols:
        print(results_df[scfa_cols].describe().round(2))

def main():
    """Main function to run the SCFA calculator."""
    print("\n" + "="*60)
    print("  SCFA EXPECTED VALUE CALCULATOR")
    print("="*60)
    print("\nThis script will:")
    print("1. Collect 100% SCFA production data for each fiber")
    print("2. Load your CSV file with fiber mixture combinations")
    print("3. Calculate expected SCFA values based on weighted averages")
    print("4. Save results to a CSV file")
    print("\n" + "="*60 + "\n")

    # Step 1: Collect fiber data
    fiber_data, fiber_names = collect_fiber_data()

    # Step 2: Display collected data
    display_collected_data(fiber_data)

    # Step 3: Load combinations CSV
    combinations_df = load_combinations_csv(fiber_names)

    # Step 4: Calculate expected values
    results_df = calculate_expected_values(fiber_data, combinations_df, fiber_names)

    # Step 5: Display summary
    display_summary(results_df)

    # Step 6: Save results
    output_file = save_results(results_df)

    print("\nDone! You can now use the expected values for your analysis.")
    print(f"Output file: {output_file}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nAn error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
