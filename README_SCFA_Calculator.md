# SCFA Expected Value Calculator

This tool calculates expected Short-Chain Fatty Acid (SCFA) production values for fiber mixtures based on weighted averages of individual fiber data at 100% concentration.

## Overview

The calculator:
1. Collects SCFA production data (acetate, propionate, butyrate) for individual fibers at 100% concentration
2. Reads fiber mixture combinations from a CSV file
3. Calculates expected SCFA production using weighted averages based on fiber ratios
4. Outputs results with expected values for each combination

## Available Versions

### 1. Interactive Python Script (`scfa_calculator.py`)

**Best for:** Command-line use, automated pipelines, flexible fiber configurations

**Features:**
- Fully interactive - asks for all inputs
- Works with any number of fibers
- Works with any number of replicates per fiber
- No hardcoded values
- Can be run locally or on a server

**Usage:**

```bash
python3 scfa_calculator.py
```

The script will prompt you for:
1. Number of fibers to analyze
2. Name of each fiber
3. Number of replicates for each fiber
4. SCFA values (acetate, propionate, butyrate) for each fiber/replicate
5. Path to your CSV file with combinations

**Output:**
- `scfa_expected_values.csv` - Complete results with expected SCFA values

---

### 2. Google Colab Version (`scfa_calculator_colab.py`)

**Best for:** Google Colab notebooks, quick analysis, pre-configured setups

**Features:**
- Designed for Google Colab with `@param` widgets
- Step-by-step execution with visual feedback
- Includes data visualization
- Pre-configured for common use cases
- Easy to modify values in the interface

**Usage:**

1. Open Google Colab: https://colab.research.google.com/
2. Create a new notebook
3. Copy the contents of `scfa_calculator_colab.py`
4. Run each cell in order
5. Modify values using the form widgets
6. Upload your CSV file or specify the path

**Output:**
- `scfa_expected_values.csv` - Complete results
- `scfa_expected_values_distribution.png` - Visualization

---

## CSV Format Requirements

Your CSV file with combinations should have the following structure:

```csv
Substrate,Replicate,FIBER1,FIBER2,FIBER3,...
FIBER1_100%,1,1.00,0.00,0.00
FIBER1_100%,2,1.00,0.00,0.00
FIBER1_50%-FIBER2_50%,1,0.50,0.50,0.00
FIBER1_50%-FIBER2_50%,2,0.50,0.50,0.00
...
```

**Required columns:**
- `Replicate`: Integer (1, 2, 3, ...)
- One column per fiber with numeric ratios (0.00 to 1.00)

**Optional columns:**
- `Substrate`: Name/description of the mixture
- Any other metadata columns

**Important:**
- Fiber ratios should sum to 1.00 (or close to it) for each row
- Use the same fiber names in the CSV as you entered in the script
- Replicates in CSV should match replicates collected for each fiber

---

## Example Workflow

### Using the Interactive Script:

```bash
$ python3 scfa_calculator.py

============================================================
  SCFA EXPECTED VALUE CALCULATOR
============================================================

How many fibers do you want to analyze? 4

--- Fiber 1/4 ---
Enter the name of fiber 1: AXOS
How many replicates for AXOS? 2

  Replicate 1/2 for AXOS (100% concentration)
    Acetate production: 26.44
    Propionate production: 12.95
    Butyrate production: 2.76

  Replicate 2/2 for AXOS (100% concentration)
    Acetate production: 25.66
    Propionate production: 12.58
    Butyrate production: 2.69

--- Fiber 2/4 ---
Enter the name of fiber 2: BRS
...

Enter the path to your CSV file: combinations.csv

✓ Calculating expected values...
✓ Results saved to: scfa_expected_values.csv
```

### Output Format:

The output CSV (`scfa_expected_values.csv`) will contain:

| Replicate | AXOS | BRS | CG | KGLUCO | expected_acetate | expected_propionate | expected_butyrate | expected_total_scfa |
|-----------|------|-----|-------|---------|------------------|---------------------|-------------------|---------------------|
| 1 | 1.00 | 0.00 | 0.00 | 0.00 | 26.44 | 12.95 | 2.76 | 42.15 |
| 2 | 1.00 | 0.00 | 0.00 | 0.00 | 25.66 | 12.58 | 2.69 | 40.93 |
| 1 | 0.26 | 0.74 | 0.00 | 0.00 | 32.72 | 7.48 | 5.95 | 46.15 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

---

## Calculation Method

For each fiber mixture combination, expected SCFA production is calculated as:

```
Expected_SCFA = Σ (Ratio_i × SCFA_100%_i)
```

Where:
- `Ratio_i` = proportion of fiber i in the mixture (from CSV)
- `SCFA_100%_i` = SCFA production at 100% concentration for fiber i (from input data)
- Calculation is done separately for acetate, propionate, and butyrate

**Example:**

For a mixture with 26% AXOS and 74% BRS (Replicate 1):

```
Expected Acetate = (0.26 × 26.44) + (0.74 × 34.93) = 6.87 + 25.85 = 32.72
Expected Propionate = (0.26 × 12.95) + (0.74 × 5.56) = 3.37 + 4.11 = 7.48
Expected Butyrate = (0.26 × 2.76) + (0.74 × 7.07) = 0.72 + 5.23 = 5.95
```

---

## Tips

1. **Fiber Names:** Use consistent naming (e.g., all uppercase) to avoid mismatches
2. **Replicates:** Ensure replicate numbers in your CSV match those you collected
3. **CSV Path:** Use absolute paths or ensure the CSV is in the same directory
4. **Data Validation:** Check that fiber ratios sum to ~1.00 in your CSV
5. **Missing Data:** If a replicate is missing, the script will use replicate 1 as fallback

---

## Troubleshooting

**Problem:** "Replicate X not found for FIBER_Y"
- **Solution:** Either add the missing replicate data or adjust your CSV to use available replicates

**Problem:** "Fiber column not found in CSV"
- **Solution:** Ensure fiber names in CSV exactly match those entered in the script (case-sensitive)

**Problem:** Results seem incorrect
- **Solution:** Verify that:
  - Fiber ratios in CSV sum to 1.00
  - Input data is for 100% concentration
  - Replicate numbers match between input data and CSV

---

## Citation

If you use this calculator in your research, please cite the relevant publication or repository.

---

## Support

For issues, questions, or contributions, please refer to the main repository documentation.
