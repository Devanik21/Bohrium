# Bohrium

![Language](https://img.shields.io/badge/Language-Python-3776AB?style=flat-square) ![Stars](https://img.shields.io/github/stars/Devanik21/Bohrium?style=flat-square&color=yellow) ![Forks](https://img.shields.io/github/forks/Devanik21/Bohrium?style=flat-square&color=blue) ![Author](https://img.shields.io/badge/Author-Devanik21-black?style=flat-square&logo=github) ![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

> Bohrium — AI-accelerated computational chemistry for materials and molecular property prediction at the intersection of quantum mechanics and machine learning.

---

**Topics:** `academic-search` · `active-inference` · `cognitive-architecture` · `generative-models` · `knowledge-graph` · `latent-diffusion` · `neuromorphic-computing` · `paper-recommendation` · `scholar-network`

## Overview

Bohrium (named after element 107, Bh) is a computational chemistry platform that applies machine
learning to accelerate quantum chemical calculations — a field known as QML (Quantum Machine Learning
for Chemistry) or MLPotentials. It implements and benchmarks ML potential energy surfaces (ML-PES)
that learn to predict molecular energies and forces at DFT accuracy from atomistic fingerprints,
with inference speed orders of magnitude faster than ab initio calculations.

The core workflow follows the standard QML pipeline: generate a training dataset of molecular
geometries with DFT-computed energies, forces, and dipole moments (or query an existing dataset
like QM9, ANI-1, or COMP6); featurise each molecule using MBTR, SOAP, or SchNet-style graph
representations; train an energy model (Gaussian Process Regression, kernel ridge regression,
or a message-passing neural network); evaluate on held-out test sets using MAE in kcal/mol
(energy) and kcal/mol/Å (forces); and deploy for molecular dynamics or property screening.

The platform also includes Δ-ML (delta machine learning) — training an ML model to predict the
correction from a cheap low-level method (PM7 semi-empirical) to an expensive high-level method
(CCSD(T)), enabling near-coupled-cluster accuracy at semi-empirical cost. This is one of the most
practically powerful ideas in computational chemistry, and Bohrium provides a clean implementation
and benchmark against QM9 reference data.

---

## Motivation

DFT calculations that take hours per molecule create a fundamental bottleneck in drug discovery,
materials design, and atmospheric chemistry. ML-accelerated potentials that achieve DFT accuracy
in milliseconds per molecule have the potential to transform computational chemistry from a tool
used on hundreds of candidates to one applied to millions. Bohrium was built to make those ML
potential methodologies accessible, reproducible, and benchmarkable.

---

## Architecture

```
Molecular Structure (xyz / SMILES / InChI)
        │
  Preprocessing (ase: geometry + neighbour list)
        │
  Featurisation:
  ├── SOAP (Smooth Overlap of Atomic Positions)
  ├── MBTR (Many-Body Tensor Representation)
  └── SchNet graph (atom types + distances + angles)
        │
  Energy Predictor:
  ├── GPR (Gaussian Process Regression, exact/sparse)
  ├── KRR (Kernel Ridge Regression, Matern/RBF)
  └── SchNet / DimeNet / PaiNN (MPNN architectures)
        │
  Energy E(R) + Forces F = -∇E
        │
  Δ-ML: E_HL ≈ E_LL + E_ML(R)
```

---

## Features

### ML Potential Energy Surface Training
Train energy models on DFT datasets with GPR, KRR, or MPNN architectures — producing models that predict energies and forces at DFT accuracy in milliseconds per evaluation.

### SOAP and MBTR Featurisation
dscribe-based SOAP and MBTR descriptor computation with configurable hyperparameters, supporting elements from H to Rn and periodic/non-periodic systems.

### SchNet / PaiNN MPNN Models
Message-passing neural network implementations for end-to-end energy prediction directly from atomic numbers and positions, with equivariant force computation via automatic differentiation.

### Δ-ML Implementation
Delta machine learning pipeline: compute PM7 energies, train correction model to DFT, and evaluate near-DFT accuracy at PM7 cost — benchmarked against QM9 and ANI-1 datasets.

### QM9 and ANI-1 Benchmarks
Pre-configured benchmark pipelines for the QM9 (134,000 small organic molecules, 13 DFT properties) and ANI-1 (20M off-equilibrium configurations) datasets with reference MAE values.

### Molecular Dynamics Integration
ML potential deployment in ASE MD engine: NVE/NVT/NPT molecular dynamics at ML-potential speed, with energy conservation monitoring and trajectory analysis tools.

### Property Prediction Dashboard
Streamlit interface for predicting multiple molecular properties (dipole moment, polarisability, HOMO-LUMO gap, heat capacity) from SMILES or xyz input with the trained models.

### Active Learning Loop
Uncertainty-guided active learning: identify structures where the ML model is uncertain, queue for DFT calculation, add to training set, retrain — iteratively improving model with minimum DFT cost.

---

## Tech Stack

| Library / Tool | Role | Why This Choice |
|---|---|---|
| **ASE** | Atomic simulation | Structure I/O, MD engine, calculator interface |
| **dscribe** | Featurisation | SOAP, MBTR, Coulomb Matrix descriptors |
| **PyTorch Geometric** | MPNN models | SchNet, PaiNN graph neural network training |
| **scikit-learn** | Classical ML models | GPR, KRR with precomputed kernel matrices |
| **RDKit** | SMILES processing | Molecular structure generation and manipulation |
| **pandas / NumPy** | Dataset management | QM9/ANI dataset loading and preprocessing |
| **Streamlit** | Property predictor UI | Interactive molecular property prediction interface |

---

## Getting Started

### Prerequisites

- Python 3.9+ (or Node.js 18+ for TypeScript/JavaScript projects)
- A virtual environment manager (`venv`, `conda`, or equivalent)
- API keys as listed in the Configuration section

### Installation

```bash
git clone https://github.com/Devanik21/Bohrium.git
cd Bohrium
python -m venv venv && source venv/bin/activate
pip install ase dscribe torch torch-geometric scikit-learn rdkit pandas numpy streamlit
# Optional: GPyTorch for exact/sparse GP regression
# pip install gpytorch

# Download QM9 dataset
python download_qm9.py --output data/qm9/

# Train energy model
python train.py --dataset qm9 --model schnet --target dipole_moment --epochs 100

# Launch property predictor
streamlit run app.py
```

---

## Usage

```bash
# Train SchNet on QM9 HOMO-LUMO gap
python train.py --dataset qm9 --model schnet --target gap --epochs 100

# Predict property for a molecule
python predict.py --smiles 'c1ccccc1' --property gap --model checkpoints/best.pt

# Run molecular dynamics
python md_simulation.py --structure benzene.xyz --potential ml_potential.pt \
  --ensemble NVT --temperature 300 --steps 10000

# Δ-ML training
python delta_ml.py --low_level pm7 --high_level dft --dataset qm9 --target energy
```

---

## Configuration

| Variable | Default | Description |
|---|---|---|
| `MODEL` | `schnet` | ML potential model: gpr, krr, schnet, painn |
| `DATASET` | `qm9` | Training dataset: qm9, ani1, custom |
| `TARGET_PROPERTY` | `energy` | Prediction target: energy, forces, dipole, gap |
| `LEARNING_RATE` | `0.001` | Neural model learning rate |
| `CUTOFF_RADIUS` | `6.0` | Atomic neighbour cutoff in Angstroms |

> Copy `.env.example` to `.env` and populate required values before running.

---

## Project Structure

```
Bohrium/
├── README.md
├── requirements.txt
├── ReSeArcH.py
└── ...
```

---

## Roadmap

- [ ] NequIP and MACE equivariant MPNN implementation for force accuracy improvement
- [ ] Transfer learning from pre-trained universal potentials (MACE-MP-0, CHGNet) for new chemistries
- [ ] Reaction path optimisation: transition state search using ML potential for barrier height prediction
- [ ] Crystal structure prediction: evolutionary algorithm using ML potential for free energy minimisation
- [ ] Cloud deployment: REST API for on-demand molecular property prediction

---

## Contributing

Contributions, issues, and suggestions are welcome.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-idea`
3. Commit your changes: `git commit -m 'feat: add your idea'`
4. Push to your branch: `git push origin feature/your-idea`
5. Open a Pull Request with a clear description

Please follow conventional commit messages and add documentation for new features.

---

## Notes

ML potentials trained on QM9 are valid only for small organic molecules containing C, H, O, N, F up to 9 heavy atoms. Extrapolation to larger molecules or different chemistries requires retraining or fine-tuning. Forces computed via automatic differentiation (backprop through the energy model) are exact gradients of the energy — not finite differences.

---

## Author

**Devanik Debnath**  
B.Tech, Electronics & Communication Engineering  
National Institute of Technology Agartala

[![GitHub](https://img.shields.io/badge/GitHub-Devanik21-black?style=flat-square&logo=github)](https://github.com/Devanik21)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-devanik-blue?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/devanik/)

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

*Built with curiosity, depth, and care — because good projects deserve good documentation.*
