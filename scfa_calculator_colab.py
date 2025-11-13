"""
SCFA Expected Value Calculator - Google Colab Version

This notebook collects 100% SCFA production data for individual fibers
and calculates expected values for fiber mixtures based on weighted averages.

Instructions:
1. Run all cells in order
2. Input your fiber data when prompted
3. Upload or specify path to your CSV file with combinations
4. View and download the results
"""

import pandas as pd
import numpy as np
from IPython.display import display, HTML

#@title Step 1: Configure Number of Fibers and Replicates
#@markdown Specify how many fibers you want to analyze and how many replicates per fiber

num_fibers = 5  #@param {type:"integer"}
num_replicates_per_fiber = 2  #@param {type:"integer"}

print(f"✓ Configuration set: {num_fibers} fibers, {num_replicates_per_fiber} replicates each")

#@title Step 2: Enter Fiber Names
#@markdown Enter the names of your fibers (one per line, will be converted to uppercase)

fiber_names_input = """AXOS
BRS
CG
KGLUCO
GOS"""  #@param {type:"string"}

# Process fiber names
fiber_names = [name.strip().upper() for name in fiber_names_input.strip().split('\n') if name.strip()]

# Validate
if len(fiber_names) != num_fibers:
    print(f"⚠️ Warning: You specified {num_fibers} fibers but entered {len(fiber_names)} names.")
    print(f"Using {len(fiber_names)} fibers: {', '.join(fiber_names)}")
    num_fibers = len(fiber_names)
else:
    print(f"✓ Fiber names loaded: {', '.join(fiber_names)}")

#@title Step 3: Enter 100% SCFA Production Data
#@markdown Enter SCFA production values for each fiber at 100% concentration.
#@markdown Values are organized by fiber and replicate.

# AXOS
#@markdown ### AXOS
axos_rep1_acetate = 26.44  #@param {type:"number"}
axos_rep1_propionate = 12.95  #@param {type:"number"}
axos_rep1_butyrate = 2.76  #@param {type:"number"}
axos_rep2_acetate = 25.66  #@param {type:"number"}
axos_rep2_propionate = 12.58  #@param {type:"number"}
axos_rep2_butyrate = 2.69  #@param {type:"number"}

# BRS
#@markdown ### BRS
brs_rep1_acetate = 34.93  #@param {type:"number"}
brs_rep1_propionate = 5.56  #@param {type:"number"}
brs_rep1_butyrate = 7.07  #@param {type:"number"}
brs_rep2_acetate = 34.30  #@param {type:"number"}
brs_rep2_propionate = 5.69  #@param {type:"number"}
brs_rep2_butyrate = 7.77  #@param {type:"number"}

# CG
#@markdown ### CG
cg_rep1_acetate = 9.19  #@param {type:"number"}
cg_rep1_propionate = 3.52  #@param {type:"number"}
cg_rep1_butyrate = 2.09  #@param {type:"number"}
cg_rep2_acetate = 9.38  #@param {type:"number"}
cg_rep2_propionate = 3.57  #@param {type:"number"}
cg_rep2_butyrate = 2.08  #@param {type:"number"}

# KGLUCO
#@markdown ### KGLUCO
kgluco_rep1_acetate = 39.06  #@param {type:"number"}
kgluco_rep1_propionate = 10.69  #@param {type:"number"}
kgluco_rep1_butyrate = 5.16  #@param {type:"number"}
kgluco_rep2_acetate = 46.08  #@param {type:"number"}
kgluco_rep2_propionate = 12.05  #@param {type:"number"}
kgluco_rep2_butyrate = 6.17  #@param {type:"number"}

# GOS
#@markdown ### GOS
gos_rep1_acetate = 57.82  #@param {type:"number"}
gos_rep1_propionate = 7.76  #@param {type:"number"}
gos_rep1_butyrate = 8.85  #@param {type:"number"}
gos_rep2_acetate = 51.27  #@param {type:"number"}
gos_rep2_propionate = 6.70  #@param {type:"number"}
gos_rep2_butyrate = 7.45  #@param {type:"number"}

# Build data structure
fiber_data = {
    "AXOS": {
        1: {"acetate": axos_rep1_acetate, "propionate": axos_rep1_propionate, "butyrate": axos_rep1_butyrate},
        2: {"acetate": axos_rep2_acetate, "propionate": axos_rep2_propionate, "butyrate": axos_rep2_butyrate}
    },
    "BRS": {
        1: {"acetate": brs_rep1_acetate, "propionate": brs_rep1_propionate, "butyrate": brs_rep1_butyrate},
        2: {"acetate": brs_rep2_acetate, "propionate": brs_rep2_propionate, "butyrate": brs_rep2_butyrate}
    },
    "CG": {
        1: {"acetate": cg_rep1_acetate, "propionate": cg_rep1_propionate, "butyrate": cg_rep1_butyrate},
        2: {"acetate": cg_rep2_acetate, "propionate": cg_rep2_propionate, "butyrate": cg_rep2_butyrate}
    },
    "KGLUCO": {
        1: {"acetate": kgluco_rep1_acetate, "propionate": kgluco_rep1_propionate, "butyrate": kgluco_rep1_butyrate},
        2: {"acetate": kgluco_rep2_acetate, "propionate": kgluco_rep2_propionate, "butyrate": kgluco_rep2_butyrate}
    },
    "GOS": {
        1: {"acetate": gos_rep1_acetate, "propionate": gos_rep1_propionate, "butyrate": gos_rep1_butyrate},
        2: {"acetate": gos_rep2_acetate, "propionate": gos_rep2_propionate, "butyrate": gos_rep2_butyrate}
    }
}

# Display summary
print("✓ SCFA production data loaded for:")
for fiber in fiber_data.keys():
    print(f"  • {fiber}: {len(fiber_data[fiber])} replicates")

#@title Step 4: Display Collected Data
#@markdown View the 100% SCFA production data you entered

print("="*70)
print("COLLECTED SCFA PRODUCTION DATA (100% concentration)")
print("="*70 + "\n")

for fiber, replicates in fiber_data.items():
    print(f"{fiber}:")
    for rep, scfa_values in replicates.items():
        total = scfa_values['acetate'] + scfa_values['propionate'] + scfa_values['butyrate']
        print(f"  Replicate {rep}:")
        print(f"    Acetate:    {scfa_values['acetate']:7.2f}")
        print(f"    Propionate: {scfa_values['propionate']:7.2f}")
        print(f"    Butyrate:   {scfa_values['butyrate']:7.2f}")
        print(f"    Total SCFA: {total:7.2f}")
    print()

#@title Step 5: Load Combination CSV File
#@markdown Specify the path to your CSV file containing fiber mixture combinations

csv_file_path = "/content/Cubic optimal design - Copy of Formulas ⚠️.csv"  #@param {type:"string"}

try:
    # Load CSV
    combinations_df = pd.read_csv(csv_file_path)

    # Clean column names
    combinations_df.columns = [c.strip() for c in combinations_df.columns]

    # Ensure required columns exist
    if 'Replicate' not in combinations_df.columns:
        raise ValueError("CSV must contain a 'Replicate' column")

    # Convert to numeric
    combinations_df['Replicate'] = pd.to_numeric(combinations_df['Replicate'], errors='coerce')

    # Process fiber columns
    for fiber in fiber_names:
        if fiber in combinations_df.columns:
            combinations_df[fiber] = pd.to_numeric(combinations_df[fiber], errors='coerce').fillna(0)
        else:
            print(f"⚠️ Warning: {fiber} not found in CSV, adding as 0")
            combinations_df[fiber] = 0

    # Drop invalid rows
    combinations_df = combinations_df.dropna(subset=['Replicate'])
    combinations_df['Replicate'] = combinations_df['Replicate'].astype(int)

    print(f"✓ Successfully loaded {len(combinations_df)} combinations")
    print(f"  Replicates: {sorted(combinations_df['Replicate'].unique())}")
    print(f"  Columns: {', '.join(combinations_df.columns)}")

    # Display first few rows
    print("\nFirst 10 combinations:")
    display(combinations_df.head(10))

except FileNotFoundError:
    print(f"❌ Error: File not found: {csv_file_path}")
    print("Please upload your CSV file to Colab or update the path.")
except Exception as e:
    print(f"❌ Error loading CSV: {e}")

#@title Step 6: Calculate Expected Values
#@markdown Calculate expected SCFA production for each combination based on weighted averages

scfa_types = ["acetate", "propionate", "butyrate"]
results = []

for idx, row in combinations_df.iterrows():
    replicate = int(row['Replicate'])

    # Initialize expected values
    expected = {scfa: 0.0 for scfa in scfa_types}

    # Calculate weighted sum for each SCFA
    for fiber in fiber_names:
        if fiber not in combinations_df.columns:
            continue

        ratio = row[fiber]

        if ratio == 0 or fiber not in fiber_data:
            continue

        # Use specified replicate, or fall back to replicate 1
        if replicate not in fiber_data[fiber]:
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
    }

    # Add substrate name if available
    if 'Substrate' in combinations_df.columns:
        result['Substrate'] = row['Substrate']

    # Add fiber ratios
    for fiber in fiber_names:
        result[fiber] = row.get(fiber, 0)

    # Add expected values
    result.update({
        'expected_acetate': round(expected['acetate'], 2),
        'expected_propionate': round(expected['propionate'], 2),
        'expected_butyrate': round(expected['butyrate'], 2),
        'expected_total_scfa': round(total_scfa, 2)
    })

    results.append(result)

# Create results DataFrame
results_df = pd.DataFrame(results)

print(f"✓ Calculated expected values for {len(results_df)} combinations")
print("\nFirst 10 results:")
display(results_df.head(10))

#@title Step 7: View Summary Statistics
#@markdown Summary statistics of expected SCFA values

print("="*70)
print("SUMMARY STATISTICS")
print("="*70 + "\n")

scfa_cols = [c for c in results_df.columns if c.startswith('expected_')]
summary_stats = results_df[scfa_cols].describe().round(2)

display(summary_stats)

print("\n" + "="*70)
print("EXPECTED VALUES BY SCFA TYPE")
print("="*70 + "\n")

for scfa_col in scfa_cols:
    scfa_name = scfa_col.replace('expected_', '').replace('_', ' ').title()
    print(f"{scfa_name}:")
    print(f"  Mean:   {results_df[scfa_col].mean():.2f}")
    print(f"  Median: {results_df[scfa_col].median():.2f}")
    print(f"  Min:    {results_df[scfa_col].min():.2f}")
    print(f"  Max:    {results_df[scfa_col].max():.2f}")
    print()

#@title Step 8: Save Results to CSV
#@markdown Save the results to a CSV file

output_filename = "scfa_expected_values.csv"  #@param {type:"string"}

results_df.to_csv(output_filename, index=False)

print(f"✓ Results saved to: {output_filename}")
print(f"  Total rows: {len(results_df)}")
print(f"  Total columns: {len(results_df.columns)}")
print("\nYou can download the file from the Files panel on the left.")

# Also display download link
from google.colab import files
print("\nTo download the file, run the following code:")
print(f"```python\nfrom google.colab import files\nfiles.download('{output_filename}')\n```")

#@title Step 9: Visualize Results (Optional)
#@markdown Create visualizations of expected SCFA values

import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 6)

# Create subplots
fig, axes = plt.subplots(1, 2, figsize=(15, 5))

# Plot 1: Distribution of expected values
scfa_data = results_df[['expected_acetate', 'expected_propionate', 'expected_butyrate']].melt(
    var_name='SCFA Type',
    value_name='Expected Production'
)
scfa_data['SCFA Type'] = scfa_data['SCFA Type'].str.replace('expected_', '').str.capitalize()

sns.boxplot(data=scfa_data, x='SCFA Type', y='Expected Production', ax=axes[0])
axes[0].set_title('Distribution of Expected SCFA Production', fontsize=14, fontweight='bold')
axes[0].set_ylabel('Expected Production (mM)', fontsize=12)
axes[0].set_xlabel('SCFA Type', fontsize=12)

# Plot 2: Total SCFA distribution
axes[1].hist(results_df['expected_total_scfa'], bins=20, edgecolor='black', alpha=0.7)
axes[1].set_title('Distribution of Total Expected SCFA', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Total SCFA Production (mM)', fontsize=12)
axes[1].set_ylabel('Frequency', fontsize=12)
axes[1].axvline(results_df['expected_total_scfa'].mean(), color='red', linestyle='--',
                linewidth=2, label=f'Mean: {results_df["expected_total_scfa"].mean():.2f}')
axes[1].legend()

plt.tight_layout()
plt.savefig('scfa_expected_values_distribution.png', dpi=300, bbox_inches='tight')
plt.show()

print("✓ Visualization saved as: scfa_expected_values_distribution.png")

print("\n" + "="*70)
print("ANALYSIS COMPLETE!")
print("="*70)
print("\nYour expected SCFA values have been calculated and saved.")
print("You can now use these values for synergy/antagonism analysis.")
