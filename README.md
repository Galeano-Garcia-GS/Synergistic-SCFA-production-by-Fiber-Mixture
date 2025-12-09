# Synergistic SCFA Production by Fiber Mixture

## Overview

This repository contains the analysis pipeline and data for investigating synergistic boosts in short-chain fatty acid (SCFA) production across various health conditions induced by a fiber mixture. The project examines how different fiber types interact to enhance bacterial SCFA production beyond what would be expected from individual components alone.

## Authors

G. S. Galeano-Garcia¹,², T. Chen³, P. A. Engen⁴, A. Keshavarzian⁴,⁵,⁶,⁷, B. R. Hamaker¹,², T. M. Cantu-Jungles¹,²*

## Contents

- **Metadata.xlsx** - Sample metadata including individual characteristics, fiber types, observed and expected SCFA concentrations, and synergy calculations
- **feature-table-species-level.tsv** - Microbial community composition data at the species level (OTU/ASV table)
- **New_insights_into_synergistic_boosts_in_SCFA_production_across_health_conditions_induced_by_a_fiber_mixture.ipynb** - Complete analysis notebook with all figures and statistical analyses

## Key Analyses

The notebook includes the following major analyses:

### 1. Synergy Calculation (Figures 1, 2, S1)
Quantifies synergistic effects by comparing observed SCFA production to expected values based on individual fiber components. Includes gating rules for measurement error and detection limits.

### 2. Differential Abundance Analysis (Figure 3a)
ANCOM-BC analysis to identify taxa with significant differential abundance across synergy categories using QIIME2.

### 3. Community Structure Correlations (Figure 3b)
Pearson correlation heatmaps examining relationships between:
- Community structure metrics (Shannon entropy, observed features, Pielou's evenness)
- Changes in these metrics (∆ values)
- Synergy in different SCFAs (acetate, butyrate, propionate, total)

### 4. SCFA Production Correlations (Figure 3c)
Pearson correlation heatmaps correlating:
- Observed SCFA concentrations
- Synergy percentages across all SCFA types

### 5. Co-occurrence Network Analysis (Figure S2)
Builds microbial co-occurrence networks using correlation methods (SparCC or Spearman) and identifies network modules associated with synergy categories.

## Requirements

The analysis is designed to run in Google Colab, but can be adapted for local environments. Key dependencies include:

- Python 3.7+
- pandas
- openpyxl
- numpy
- matplotlib
- seaborn
- scipy
- statsmodels
- ipywidgets
- QIIME2 (for differential abundance and network analyses)
- biom-format

## Usage

### In Google Colab

1. Open the notebook in Google Colab
2. Follow the markdown instructions within each section
3. Adjust parameters in the code cells (marked with `#@param` comments) as needed
4. Run cells sequentially

### Key Parameters to Customize

- **Metadata file path**: Update `excel_file_path` to point to your data
- **Measurement error threshold**: Adjust `measurement_error` slider (default: 0.5)
- **Detection limit**: Set `minimal_detection_limit` (default: 1 mM)
- **Statistical corrections**: Choose p-value correction method (`fdr_bh`, `bonferroni`, `holm`, `sidak`)
- **Visualization options**: Customize figure sizes, font sizes, and colormaps

### For QIIME2 Analyses

The notebook includes commands for running ANCOM-BC and network analysis on a high-performance computing cluster. Update:

- `working_directory` - Path to your compute cluster workspace
- `qiime_working_directory` - QIIME2 working directory
- `filtering_formula` - Metadata filtering criteria
- `correlation_method` - Choose between "spearman" or "sparcc"

## Data Format

### Metadata (Metadata.xlsx)

Required columns:
- `Individual` - Sample identifier
- `Replicate` - Replicate number
- `Fiber` - Fiber type/mixture
- `Acetate_(mM)`, `Butyrate_(mM)`, `Propionate_(mM)`, `Total_SCFA_(mM)` - Observed concentrations
- `Expected_acetate_(mM)`, `Expected_butyrate_(mM)`, `Expected_propionate_(mM)`, `Expected_total_SCFA_(mM)` - Expected concentrations
- Community structure metrics (shannon_entropy, observed_features, pielou_evenness, etc.)
- Synergy categories (calculated automatically if not present)

### Feature Table (feature-table-species-level.tsv)

Tab-separated file with:
- Rows: Microbial taxa (species level)
- Columns: Sample IDs matching metadata
- Values: Abundance counts

## Outputs

The notebook generates:

- **Excel files** with filtered metadata and synergy calculations
- **Correlation matrices** (R values, raw p-values, adjusted p-values) as CSV files
- **Publication-quality figures** (PNG/SVG):
  - Correlation heatmaps
  - Network visualizations (from Cytoscape)

All outputs are saved to specified directories within the notebook.

## Statistical Methods

- **Synergy calculation**: ((Observed - Expected) / Expected) × 100
- **Multiple testing correction**: Benjamini-Hochberg FDR or alternative methods
- **Correlation analysis**: Pearson correlation with significance testing
- **Differential abundance**: ANCOM-BC (Analysis of Composition of Microbiomes with Bias Correction)
- **Co-occurrence networks**: SparCC (Sparse Correlation for Compositional data) or Spearman correlation

## Citation

[We will add citation information once the manuscript is published]

## Contact

For questions or issues, please contact: [ggaleano@purdue.edu]

## Troubleshooting

### Common Issues

1. **FileNotFoundError**: Ensure all file paths in the notebook match your directory structure
2. **Missing columns**: Verify all required columns are present in the metadata file with exact spelling
3. **QIIME2 errors**: Ensure the correct environment is activated and all dependencies are installed
4. **Memory issues**: If processing large datasets, reduce figure sizes or work with aggregated data

## References

- Galeano-Garcia et al. (Manuscript under review/published)
- QIIME2 documentation: https://docs.qiime2.org/
- SparCC: Friedman & Alm (2012) PLoS Comput Biol
- ANCOM-BC: Lin & Peddada (2020) Nat Commun

---

For more information about the research, methodology, or to report issues, please visit the [GitHub repository](https://github.com/Galeano-Garcia-GS/Synergistic-SCFA-production-by-Fiber-Mixture).
