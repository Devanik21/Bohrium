import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
import random
import json
from enum import Enum
import time
import math

# Page configuration
st.set_page_config(page_title="Universe Sandbox AI", layout="wide", initial_sidebar_state="expanded")

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 1rem;
    }
    .stat-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .organism-card {
        border: 2px solid #667eea;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        background: rgba(102, 126, 234, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Enums for different life types
class LifeType(Enum):
    CARBON_BASED = "Carbon-Based"
    SILICON_BASED = "Silicon-Based"
    NITROGEN_BASED = "Nitrogen-Based"
    SULFUR_BASED = "Sulfur-Based"
    PHOSPHORUS_BASED = "Phosphorus-Based"
    METALLIC = "Metallic Life"
    PLASMA_BASED = "Plasma-Based"
    CRYSTALLINE = "Crystalline"
    QUANTUM = "Quantum Entity"
    HYBRID = "Hybrid Organism"
    MACHINE = "Machine Life"
    ENERGY_BEING = "Pure Energy"

class ComplexityLevel(Enum):
    PRIMORDIAL = 0
    SINGLE_CELL = 1
    MULTI_CELL = 2
    SIMPLE_ORGANISM = 3
    COMPLEX_ORGANISM = 4
    INTELLIGENT = 5
    ADVANCED = 6
    TRANSCENDENT = 7
    COSMIC = 8
    OMNIPOTENT = 9

# Data classes for organisms
@dataclass
class Genome:
    dna_length: int
    mutation_rate: float
    genes: Dict[str, float]
    epigenetic_factors: Dict[str, float]
    horizontal_transfer_rate: float
    
@dataclass
class Organism:
    id: int
    name: str
    life_type: LifeType
    complexity: ComplexityLevel
    genome: Genome
    traits: Dict[str, float]
    age: int
    generation: int
    population: int
    energy: float
    intelligence: float
    adaptability: float
    reproductive_rate: float
    mutation_history: List[str]
    ancestors: List[int]
    environment_fitness: float
    technological_level: float
    consciousness_level: float
    
    # Physical characteristics
    size: float
    mass: float
    structure_complexity: int
    
    # Behavioral traits
    aggression: float
    cooperation: float
    exploration_drive: float
    
    # Advanced traits
    telepathic_ability: float
    dimensional_awareness: float
    quantum_coherence: float
    
    # Resource management
    energy_efficiency: float
    resource_gathering: float
    
    # Environmental interaction
    temperature_tolerance: Tuple[float, float]
    pressure_tolerance: Tuple[float, float]
    radiation_resistance: float

@dataclass
class Environment:
    temperature: float
    pressure: float
    radiation_level: float
    oxygen_level: float
    water_availability: float
    mineral_richness: float
    gravity: float
    magnetic_field: float
    atmospheric_composition: Dict[str, float]
    geological_activity: float
    stellar_type: str
    cosmic_ray_flux: float
    time_dilation_factor: float

@dataclass
class UniverseState:
    age: int
    organisms: List[Organism]
    environment: Environment
    extinction_events: int
    evolutionary_leaps: int
    dominant_species: Optional[str]
    total_biomass: float
    technological_artifacts: int
    dimensional_breaches: int
    
# Initialize session state
if 'universe' not in st.session_state:
    st.session_state.universe = None
    st.session_state.running = False
    st.session_state.speed = 1
    st.session_state.history = []
    st.session_state.generation = 0
    st.session_state.advanced_mode = False

# Sidebar controls
st.sidebar.markdown("# 🌌 Universe Sandbox AI")
st.sidebar.markdown("### Control Panel")

# Main control section
st.sidebar.markdown("## 🎮 Simulation Controls")
if st.sidebar.button("🌟 Initialize Universe", use_container_width=True):
    st.session_state.running = False
    st.session_state.generation = 0
    st.session_state.history = []

col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("▶️ Start", use_container_width=True):
        st.session_state.running = True
with col2:
    if st.button("⏸️ Pause", use_container_width=True):
        st.session_state.running = False

if st.sidebar.button("⏭️ Step Forward", use_container_width=True):
    st.session_state.generation += 1

if st.sidebar.button("🔄 Reset Universe", use_container_width=True):
    st.session_state.universe = None
    st.session_state.history = []
    st.session_state.generation = 0
    st.session_state.running = False

st.session_state.speed = st.sidebar.slider("⚡ Simulation Speed", 1, 100, 10)

# Advanced mode toggle
st.session_state.advanced_mode = st.sidebar.checkbox("🔬 Advanced Mode", value=st.session_state.advanced_mode)

# === FUNDAMENTAL PHYSICS PARAMETERS ===
st.sidebar.markdown("---")
st.sidebar.markdown("## ⚛️ Fundamental Physics")

with st.sidebar.expander("🌟 Universal Constants", expanded=False):
    st.markdown("### Core Constants")
    speed_of_light = st.slider("Speed of Light (c)", 1e8, 5e8, 3e8, format="%.2e")
    planck_constant = st.slider("Planck Constant (h)", 1e-35, 1e-33, 6.626e-34, format="%.3e")
    gravitational_constant = st.slider("Gravitational Constant (G)", 1e-12, 1e-10, 6.674e-11, format="%.3e")
    fine_structure_constant = st.slider("Fine Structure Constant (α)", 0.001, 0.01, 0.00729)
    cosmological_constant = st.slider("Dark Energy Density", -1.0, 1.0, 0.7)
    
    st.markdown("### Forces")
    strong_force = st.slider("Strong Nuclear Force", 0.1, 2.0, 1.0)
    weak_force = st.slider("Weak Nuclear Force", 0.1, 2.0, 1.0)
    electromagnetic_force = st.slider("Electromagnetic Force", 0.1, 2.0, 1.0)
    gravity_strength = st.slider("Gravity Strength", 0.1, 2.0, 1.0)
    
    st.markdown("### Particle Properties")
    electron_mass = st.slider("Electron Mass Ratio", 0.5, 1.5, 1.0)
    proton_mass = st.slider("Proton Mass Ratio", 0.5, 1.5, 1.0)
    neutron_mass = st.slider("Neutron Mass Ratio", 0.5, 1.5, 1.0)
    higgs_field = st.slider("Higgs Field Strength", 0.5, 1.5, 1.0)

with st.sidebar.expander("🌌 Cosmological Parameters", expanded=False):
    universe_age = st.slider("Universe Age (billions of years)", 1.0, 50.0, 13.8)
    universe_expansion_rate = st.slider("Expansion Rate (Hubble)", 0.5, 2.0, 1.0)
    matter_density = st.slider("Matter Density", 0.1, 2.0, 0.3)
    dark_matter_ratio = st.slider("Dark Matter %", 0.0, 50.0, 26.8)
    dark_energy_ratio = st.slider("Dark Energy %", 0.0, 80.0, 68.3)
    
    spatial_dimensions = st.slider("Spatial Dimensions", 3, 11, 3)
    time_dimensions = st.slider("Time Dimensions", 1, 3, 1)
    curvature = st.slider("Space-Time Curvature", -1.0, 1.0, 0.0)
    topology_type = st.selectbox("Universe Topology", ["Flat", "Spherical", "Hyperbolic", "Toroidal", "Mobius"])

with st.sidebar.expander("🔥 Thermodynamics", expanded=False):
    entropy_increase_rate = st.slider("Entropy Increase Rate", 0.1, 2.0, 1.0)
    heat_death_progress = st.slider("Heat Death Progress %", 0.0, 100.0, 0.1)
    temperature_variance = st.slider("Temperature Variance", 0.0, 100.0, 50.0)
    thermal_equilibrium_tendency = st.slider("Equilibrium Tendency", 0.0, 1.0, 0.5)
    
    energy_conservation = st.slider("Energy Conservation", 0.9, 1.0, 0.999)
    reversibility_factor = st.slider("Time Reversibility", 0.0, 0.1, 0.001)

with st.sidebar.expander("⚡ Quantum Mechanics", expanded=False):
    quantum_uncertainty = st.slider("Heisenberg Uncertainty", 0.5, 2.0, 1.0)
    wave_particle_duality = st.slider("Wave-Particle Duality", 0.0, 1.0, 0.5)
    quantum_entanglement = st.slider("Entanglement Strength", 0.0, 1.0, 0.8)
    superposition_stability = st.slider("Superposition Stability", 0.0, 1.0, 0.5)
    decoherence_rate = st.slider("Quantum Decoherence", 0.0, 1.0, 0.3)
    
    quantum_tunneling = st.slider("Tunneling Probability", 0.0, 1.0, 0.1)
    vacuum_energy = st.slider("Vacuum Energy Density", 0.0, 2.0, 1.0)
    zero_point_energy = st.slider("Zero Point Energy", 0.0, 2.0, 1.0)

# === ENVIRONMENTAL PARAMETERS ===
st.sidebar.markdown("---")
st.sidebar.markdown("## 🌍 Environmental Conditions")

with st.sidebar.expander("🌡️ Planetary Environment", expanded=False):
    base_temperature = st.slider("Base Temperature (K)", 0.0, 1000.0, 288.0)
    temperature_fluctuation = st.slider("Temperature Fluctuation", 0.0, 100.0, 20.0)
    atmospheric_pressure = st.slider("Atmospheric Pressure (atm)", 0.0, 10.0, 1.0)
    gravity_strength_local = st.slider("Surface Gravity (g)", 0.1, 5.0, 1.0)
    
    water_coverage = st.slider("Water Coverage %", 0.0, 100.0, 70.0)
    land_coverage = st.slider("Land Coverage %", 0.0, 100.0, 30.0)
    ice_coverage = st.slider("Ice Coverage %", 0.0, 100.0, 3.0)
    
    day_length = st.slider("Day Length (hours)", 1.0, 100.0, 24.0)
    year_length = st.slider("Year Length (days)", 10.0, 1000.0, 365.0)
    axial_tilt = st.slider("Axial Tilt (degrees)", 0.0, 90.0, 23.5)
    orbital_eccentricity = st.slider("Orbital Eccentricity", 0.0, 0.5, 0.017)

with st.sidebar.expander("🌊 Atmospheric Composition", expanded=False):
    nitrogen_level = st.slider("Nitrogen %", 0.0, 100.0, 78.0)
    oxygen_level = st.slider("Oxygen %", 0.0, 50.0, 21.0)
    carbon_dioxide = st.slider("CO2 %", 0.0, 10.0, 0.04)
    argon_level = st.slider("Argon %", 0.0, 5.0, 0.93)
    methane_level = st.slider("Methane %", 0.0, 10.0, 0.0002)
    ammonia_level = st.slider("Ammonia %", 0.0, 10.0, 0.0)
    hydrogen_level = st.slider("Hydrogen %", 0.0, 50.0, 0.00005)
    helium_level = st.slider("Helium %", 0.0, 30.0, 0.0005)
    ozone_level = st.slider("Ozone Layer Strength", 0.0, 1.0, 0.8)

with st.sidebar.expander("☢️ Radiation & Energy", expanded=False):
    solar_radiation = st.slider("Solar Radiation", 0.0, 2.0, 1.0)
    cosmic_radiation = st.slider("Cosmic Radiation", 0.0, 2.0, 0.3)
    background_radiation = st.slider("Background Radiation", 0.0, 1.0, 0.1)
    magnetic_field_strength = st.slider("Magnetic Field Strength", 0.0, 2.0, 1.0)
    
    uv_radiation = st.slider("UV Radiation", 0.0, 2.0, 1.0)
    infrared_radiation = st.slider("IR Radiation", 0.0, 2.0, 1.0)
    gamma_radiation = st.slider("Gamma Radiation", 0.0, 1.0, 0.01)
    
    geothermal_energy = st.slider("Geothermal Activity", 0.0, 2.0, 1.0)
    tidal_forces = st.slider("Tidal Forces", 0.0, 2.0, 1.0)

with st.sidebar.expander("🏔️ Geological Activity", expanded=False):
    volcanic_activity = st.slider("Volcanic Activity", 0.0, 2.0, 1.0)
    tectonic_activity = st.slider("Tectonic Activity", 0.0, 2.0, 1.0)
    erosion_rate = st.slider("Erosion Rate", 0.0, 2.0, 1.0)
    sedimentation_rate = st.slider("Sedimentation Rate", 0.0, 2.0, 1.0)
    
    mountain_formation = st.slider("Mountain Formation", 0.0, 1.0, 0.5)
    ocean_trench_activity = st.slider("Ocean Trench Activity", 0.0, 1.0, 0.5)
    continental_drift = st.slider("Continental Drift Speed", 0.0, 2.0, 1.0)

# === CHEMICAL PARAMETERS ===
st.sidebar.markdown("---")
st.sidebar.markdown("## 🧪 Chemical Properties")

with st.sidebar.expander("⚗️ Elemental Abundance", expanded=False):
    hydrogen_abundance = st.slider("Hydrogen Abundance", 0.0, 100.0, 73.9)
    carbon_abundance = st.slider("Carbon Abundance", 0.0, 10.0, 0.5)
    nitrogen_abundance = st.slider("Nitrogen Abundance", 0.0, 10.0, 0.1)
    oxygen_abundance = st.slider("Oxygen Abundance", 0.0, 10.0, 1.0)
    silicon_abundance = st.slider("Silicon Abundance", 0.0, 5.0, 0.07)
    phosphorus_abundance = st.slider("Phosphorus Abundance", 0.0, 1.0, 0.001)
    sulfur_abundance = st.slider("Sulfur Abundance", 0.0, 1.0, 0.05)
    iron_abundance = st.slider("Iron Abundance", 0.0, 5.0, 0.11)
    
    rare_earth_elements = st.slider("Rare Earth Elements", 0.0, 1.0, 0.1)
    heavy_metals = st.slider("Heavy Metals", 0.0, 1.0, 0.2)
    noble_gases = st.slider("Noble Gases", 0.0, 1.0, 0.05)

with st.sidebar.expander("🔗 Chemical Bonding", expanded=False):
    ionic_bond_strength = st.slider("Ionic Bond Strength", 0.5, 2.0, 1.0)
    covalent_bond_strength = st.slider("Covalent Bond Strength", 0.5, 2.0, 1.0)
    metallic_bond_strength = st.slider("Metallic Bond Strength", 0.5, 2.0, 1.0)
    hydrogen_bond_strength = st.slider("Hydrogen Bond Strength", 0.5, 2.0, 1.0)
    van_der_waals_force = st.slider("Van der Waals Force", 0.5, 2.0, 1.0)
    
    bond_formation_rate = st.slider("Bond Formation Rate", 0.1, 2.0, 1.0)
    bond_breaking_rate = st.slider("Bond Breaking Rate", 0.1, 2.0, 1.0)
    catalytic_efficiency = st.slider("Catalytic Efficiency", 0.5, 2.0, 1.0)

with st.sidebar.expander("💧 Water Properties", expanded=False):
    water_polarity = st.slider("Water Polarity", 0.5, 2.0, 1.0)
    water_density_anomaly = st.slider("Density Anomaly", 0.5, 2.0, 1.0)
    surface_tension = st.slider("Surface Tension", 0.5, 2.0, 1.0)
    viscosity = st.slider("Viscosity", 0.5, 2.0, 1.0)
    
    freezing_point = st.slider("Freezing Point (C)", -50.0, 50.0, 0.0)
    boiling_point = st.slider("Boiling Point (C)", 50.0, 200.0, 100.0)
    heat_capacity = st.slider("Heat Capacity", 0.5, 2.0, 1.0)

# === BIOLOGICAL PARAMETERS ===
st.sidebar.markdown("---")
st.sidebar.markdown("## 🧬 Biological Mechanisms")

with st.sidebar.expander("🧬 Genetic Systems", expanded=False):
    dna_stability = st.slider("DNA Stability", 0.5, 1.5, 1.0)
    rna_efficiency = st.slider("RNA Efficiency", 0.5, 1.5, 1.0)
    protein_folding_accuracy = st.slider("Protein Folding Accuracy", 0.5, 1.0, 0.99)
    
    base_mutation_rate = st.slider("Base Mutation Rate", 0.0, 0.1, 0.001)
    beneficial_mutation_chance = st.slider("Beneficial Mutation %", 0.0, 50.0, 10.0)
    neutral_mutation_chance = st.slider("Neutral Mutation %", 0.0, 80.0, 70.0)
    harmful_mutation_chance = st.slider("Harmful Mutation %", 0.0, 50.0, 20.0)
    
    horizontal_gene_transfer = st.slider("Horizontal Gene Transfer", 0.0, 1.0, 0.1)
    genetic_recombination_rate = st.slider("Recombination Rate", 0.0, 1.0, 0.5)
    epigenetic_inheritance = st.slider("Epigenetic Inheritance", 0.0, 1.0, 0.3)
    
    codon_redundancy = st.slider("Codon Redundancy", 1, 6, 3)
    intron_presence = st.slider("Intron Presence", 0.0, 1.0, 0.5)
    gene_expression_noise = st.slider("Expression Noise", 0.0, 1.0, 0.2)

with st.sidebar.expander("🦠 Cellular Mechanisms", expanded=False):
    cell_division_rate = st.slider("Cell Division Rate", 0.1, 2.0, 1.0)
    apoptosis_rate = st.slider("Apoptosis Rate", 0.0, 1.0, 0.1)
    cellular_respiration_efficiency = st.slider("Respiration Efficiency", 0.3, 1.0, 0.7)
    photosynthesis_efficiency = st.slider("Photosynthesis Efficiency", 0.1, 0.5, 0.3)
    
    membrane_permeability = st.slider("Membrane Permeability", 0.3, 1.0, 0.7)
    cytoplasm_viscosity = st.slider("Cytoplasm Viscosity", 0.5, 2.0, 1.0)
    organelle_complexity = st.slider("Organelle Complexity", 1, 50, 10)
    
    atp_production = st.slider("ATP Production Rate", 0.5, 2.0, 1.0)
    protein_synthesis_rate = st.slider("Protein Synthesis", 0.5, 2.0, 1.0)
    waste_removal_efficiency = st.slider("Waste Removal", 0.3, 1.0, 0.8)

with st.sidebar.expander("🌱 Developmental Biology", expanded=False):
    embryonic_development_speed = st.slider("Development Speed", 0.1, 2.0, 1.0)
    morphogen_gradient_precision = st.slider("Morphogen Precision", 0.5, 1.0, 0.9)
    cell_differentiation_rate = st.slider("Differentiation Rate", 0.1, 2.0, 1.0)
    
    tissue_regeneration = st.slider("Regeneration Ability", 0.0, 1.0, 0.3)
    stem_cell_potency = st.slider("Stem Cell Potency", 0.0, 1.0, 0.8)
    developmental_plasticity = st.slider("Developmental Plasticity", 0.0, 1.0, 0.5)
    
    aging_rate = st.slider("Aging Rate", 0.1, 2.0, 1.0)
    senescence_onset = st.slider("Senescence Onset", 0.1, 2.0, 1.0)
    telomere_shortening = st.slider("Telomere Shortening", 0.1, 2.0, 1.0)

with st.sidebar.expander("🧠 Nervous System", expanded=False):
    neuron_density = st.slider("Neuron Density", 0.1, 2.0, 1.0)
    synapse_formation_rate = st.slider("Synapse Formation", 0.1, 2.0, 1.0)
    neural_plasticity = st.slider("Neural Plasticity", 0.0, 1.0, 0.7)
    
    neurotransmitter_efficiency = st.slider("Neurotransmitter Efficiency", 0.5, 1.5, 1.0)
    action_potential_speed = st.slider("Action Potential Speed", 0.5, 2.0, 1.0)
    myelination_level = st.slider("Myelination Level", 0.0, 1.0, 0.8)
    
    brain_size_scaling = st.slider("Brain Size Scaling", 0.5, 3.0, 1.0)
    cortical_folding = st.slider("Cortical Folding", 0.0, 2.0, 1.0)
    neural_network_complexity = st.slider("Network Complexity", 1, 100, 50)

# === EVOLUTIONARY PARAMETERS ===
st.sidebar.markdown("---")
st.sidebar.markdown("## 🌿 Evolutionary Dynamics")

with st.sidebar.expander("🔬 Selection Pressures", expanded=False):
    natural_selection_strength = st.slider("Natural Selection Strength", 0.0, 2.0, 1.0)
    sexual_selection_strength = st.slider("Sexual Selection", 0.0, 2.0, 0.5)
    artificial_selection = st.slider("Artificial Selection", 0.0, 1.0, 0.0)
    
    predation_pressure = st.slider("Predation Pressure", 0.0, 2.0, 1.0)
    competition_intensity = st.slider("Competition Intensity", 0.0, 2.0, 1.0)
    cooperation_benefit = st.slider("Cooperation Benefit", 0.0, 2.0, 1.0)
    
    environmental_stress = st.slider("Environmental Stress", 0.0, 2.0, 1.0)
    resource_scarcity = st.slider("Resource Scarcity", 0.0, 2.0, 0.5)
    habitat_fragmentation = st.slider("Habitat Fragmentation", 0.0, 1.0, 0.2)

with st.sidebar.expander("🧬 Evolutionary Mechanisms", expanded=False):
    genetic_drift_strength = st.slider("Genetic Drift", 0.0, 1.0, 0.3)
    gene_flow_rate = st.slider("Gene Flow Rate", 0.0, 1.0, 0.5)
    bottleneck_frequency = st.slider("Bottleneck Events", 0.0, 1.0, 0.1)
    founder_effect = st.slider("Founder Effect", 0.0, 1.0, 0.2)
    
    speciation_rate = st.slider("Speciation Rate", 0.0, 1.0, 0.1)
    extinction_rate = st.slider("Extinction Rate", 0.0, 1.0, 0.05)
    adaptive_radiation = st.slider("Adaptive Radiation", 0.0, 2.0, 1.0)
    
    punctuated_equilibrium = st.slider("Punctuated Equilibrium", 0.0, 1.0, 0.5)
    gradualism_rate = st.slider("Gradualism Rate", 0.0, 1.0, 0.5)
    stasis_duration = st.slider("Evolutionary Stasis", 0.0, 1.0, 0.3)

with st.sidebar.expander("🌍 Ecological Dynamics", expanded=False):
    carrying_capacity = st.slider("Carrying Capacity", 100, 10000, 1000)
    population_growth_rate = st.slider("Population Growth", 0.1, 2.0, 1.0)
    mortality_rate = st.slider("Mortality Rate", 0.0, 1.0, 0.1)
    
    niche_availability = st.slider("Niche Availability", 0.0, 1.0, 0.7)
    niche_specialization = st.slider("Niche Specialization", 0.0, 1.0, 0.5)
    ecological_succession = st.slider("Succession Rate", 0.0, 1.0, 0.3)
    
    predator_prey_ratio = st.slider("Predator/Prey Ratio", 0.01, 0.5, 0.1)
    symbiosis_frequency = st.slider("Symbiosis Frequency", 0.0, 1.0, 0.3)
    parasitism_rate = st.slider("Parasitism Rate", 0.0, 1.0, 0.2)

with st.sidebar.expander("🧩 Complexity Evolution", expanded=False):
    complexity_increase_tendency = st.slider("Complexity Tendency", 0.0, 2.0, 1.0)
    modularity_evolution = st.slider("Modularity Evolution", 0.0, 1.0, 0.5)
    redundancy_level = st.slider("System Redundancy", 0.0, 1.0, 0.3)
    
    multicellularity_tendency = st.slider("Multicellularity Tendency", 0.0, 1.0, 0.5)
    tissue_differentiation = st.slider("Tissue Differentiation", 0.0, 1.0, 0.5)
    organ_system_evolution = st.slider("Organ System Evolution", 0.0, 1.0, 0.3)
    
    body_plan_innovation = st.slider("Body Plan Innovation", 0.0, 1.0, 0.2)
    symmetry_evolution = st.slider("Symmetry Evolution", 0.0, 1.0, 0.5)
    segmentation_tendency = st.slider("Segmentation", 0.0, 1.0, 0.4)

# === COGNITIVE PARAMETERS ===
st.sidebar.markdown("---")
st.sidebar.markdown("## 🧠 Intelligence & Consciousness")

with st.sidebar.expander("🤔 Cognitive Abilities", expanded=False):
    base_intelligence = st.slider("Base Intelligence", 0.0, 10.0, 1.0)
    learning_rate = st.slider("Learning Rate", 0.0, 2.0, 1.0)
    memory_capacity = st.slider("Memory Capacity", 0.0, 10.0, 1.0)
    problem_solving_ability = st.slider("Problem Solving", 0.0, 2.0, 1.0)
    
    abstract_thinking = st.slider("Abstract Thinking", 0.0, 1.0, 0.5)
    pattern_recognition = st.slider("Pattern Recognition", 0.0, 1.0, 0.7)
    creativity = st.slider("Creativity", 0.0, 1.0, 0.5)
    
    language_capability = st.slider("Language Capability", 0.0, 1.0, 0.3)
    symbolic_reasoning = st.slider("Symbolic Reasoning", 0.0, 1.0, 0.4)
    metacognition = st.slider("Metacognition", 0.0, 1.0, 0.2)

with st.sidebar.expander("✨ Consciousness Parameters", expanded=False):
    consciousness_emergence = st.slider("Consciousness Emergence", 0.0, 1.0, 0.1)
    self_awareness_level = st.slider("Self-Awareness", 0.0, 1.0, 0.3)
    qualia_intensity = st.slider("Qualia Intensity", 0.0, 1.0, 0.5)
    
    theory_of_mind = st.slider("Theory of Mind", 0.0, 1.0, 0.4)
    empathy_capacity = st.slider("Empathy Capacity", 0.0, 1.0, 0.5)
    emotional_complexity = st.slider("Emotional Complexity", 0.0, 1.0, 0.6)
    
    free_will_degree = st.slider("Free Will Degree", 0.0, 1.0, 0.5)
    intentionality = st.slider("Intentionality", 0.0, 1.0, 0.5)
    subjective_experience = st.slider("Subjective Experience", 0.0, 1.0, 0.5)

with st.sidebar.expander("🎯 Behavioral Traits", expanded=False):
    curiosity = st.slider("Curiosity", 0.0, 1.0, 0.5)
    risk_taking = st.slider("Risk Taking", 0.0, 1.0, 0.3)
    social_tendency = st.slider("Social Tendency", 0.0, 1.0, 0.6)
    
    aggression_base = st.slider("Base Aggression", 0.0, 1.0, 0.3)
    cooperation_tendency = st.slider("Cooperation", 0.0, 1.0, 0.7)
    altruism = st.slider("Altruism", 0.0, 1.0, 0.4)
    
    territoriality = st.slider("Territoriality", 0.0, 1.0, 0.5)
    hierarchy_formation = st.slider("Hierarchy Formation", 0.0, 1.0, 0.6)
    group_cohesion = st.slider("Group Cohesion", 0.0, 1.0, 0.7)

with st.sidebar.expander("🎨 Cultural Evolution", expanded=False):
    cultural_transmission = st.slider("Cultural Transmission", 0.0, 1.0, 0.3)
    meme_evolution_rate = st.slider("Meme Evolution", 0.0, 1.0, 0.5)
    tradition_strength = st.slider("Tradition Strength", 0.0, 1.0, 0.5)
    
    innovation_rate = st.slider("Innovation Rate", 0.0, 1.0, 0.4)
    technology_adoption = st.slider("Technology Adoption", 0.0, 1.0, 0.5)
    knowledge_accumulation = st.slider("Knowledge Accumulation", 0.0, 2.0, 1.0)
    
    art_emergence = st.slider("Art Emergence", 0.0, 1.0, 0.2)
    music_capability = st.slider("Music Capability", 0.0, 1.0, 0.3)
    storytelling = st.slider("Storytelling", 0.0, 1.0, 0.4)

# === ADVANCED LIFE FORMS ===
st.sidebar.markdown("---")
st.sidebar.markdown("## 🔮 Advanced Life Forms")

with st.sidebar.expander("🤖 Machine Life", expanded=False):
    machine_life_emergence = st.slider("Machine Life Emergence", 0.0, 1.0, 0.0)
    silicon_based_life = st.slider("Silicon-Based Life", 0.0, 1.0, 0.1)
    synthetic_biology = st.slider("Synthetic Biology", 0.0, 1.0, 0.0)
    
    ai_evolution_rate = st.slider("AI Evolution Rate", 0.0, 2.0, 0.5)
    cybernetic_integration = st.slider("Cybernetic Integration", 0.0, 1.0, 0.0)
    digital_consciousness = st.slider("Digital Consciousness", 0.0, 1.0, 0.0)
    
    nanotechnology_level = st.slider("Nanotechnology", 0.0, 1.0, 0.0)
    quantum_computing = st.slider("Quantum Computing", 0.0, 1.0, 0.0)
    neural_networks_bio = st.slider("Bio-Neural Networks", 0.0, 1.0, 0.0)

with st.sidebar.expander("⚡ Energy-Based Life", expanded=False):
    energy_being_emergence = st.slider("Energy Being Emergence", 0.0, 1.0, 0.0)
    plasma_life_probability = st.slider("Plasma Life", 0.0, 1.0, 0.0)
    electromagnetic_life = st.slider("EM Life Forms", 0.0, 1.0, 0.0)
    
    photon_based_consciousness = st.slider("Photon Consciousness", 0.0, 1.0, 0.0)
    dark_matter_interaction = st.slider("Dark Matter Interaction", 0.0, 1.0, 0.0)
    dark_energy_utilization = st.slider("Dark Energy Use", 0.0, 1.0, 0.0)

with st.sidebar.expander("🌌 Exotic Life Forms", expanded=False):
    crystalline_life = st.slider("Crystalline Life", 0.0, 1.0, 0.0)
    metallic_life_forms = st.slider("Metallic Life", 0.0, 1.0, 0.0)
    gaseous_entities = st.slider("Gaseous Entities", 0.0, 1.0, 0.0)
    
    vacuum_based_life = st.slider("Vacuum-Based Life", 0.0, 1.0, 0.0)
    black_hole_life = st.slider("Black Hole Life", 0.0, 1.0, 0.0)
    neutron_star_organisms = st.slider("Neutron Star Life", 0.0, 1.0, 0.0)
    
    temporal_entities = st.slider("Temporal Entities", 0.0, 1.0, 0.0)
    probability_wave_life = st.slider("Probability Wave Life", 0.0, 1.0, 0.0)
    information_based_beings = st.slider("Information Beings", 0.0, 1.0, 0.0)

with st.sidebar.expander("🔬 Hybrid & Chimeric Life", expanded=False):
    hybrid_life_tendency = st.slider("Hybrid Life Tendency", 0.0, 1.0, 0.3)
    symbiogenesis_rate = st.slider("Symbiogenesis", 0.0, 1.0, 0.2)
    horizontal_species_merge = st.slider("Species Merging", 0.0, 1.0, 0.1)
    
    bio_machine_hybrids = st.slider("Bio-Machine Hybrids", 0.0, 1.0, 0.0)
    multi_chemistry_life = st.slider("Multi-Chemistry Life", 0.0, 1.0, 0.1)
    collective_consciousness = st.slider("Collective Consciousness", 0.0, 1.0, 0.2)

# === TRANSCENDENT PARAMETERS ===
st.sidebar.markdown("---")
st.sidebar.markdown("## 🌟 Transcendent Evolution")

with st.sidebar.expander("🧘 Psionic Abilities", expanded=False):
    telepathy_emergence = st.slider("Telepathy", 0.0, 1.0, 0.0)
    telekinesis = st.slider("Telekinesis", 0.0, 1.0, 0.0)
    precognition = st.slider("Precognition", 0.0, 1.0, 0.0)
    
    mind_control = st.slider("Mind Control", 0.0, 1.0, 0.0)
    astral_projection = st.slider("Astral Projection", 0.0, 1.0, 0.0)
    psychic_healing = st.slider("Psychic Healing", 0.0, 1.0, 0.0)
    
    psionic_energy_manipulation = st.slider("Energy Manipulation", 0.0, 1.0, 0.0)
    collective_mind_network = st.slider("Collective Mind", 0.0, 1.0, 0.0)

with st.sidebar.expander("🌀 Dimensional Abilities", expanded=False):
    dimensional_awareness = st.slider("Dimensional Awareness", 0.0, 1.0, 0.0)
    dimensional_travel = st.slider("Dimensional Travel", 0.0, 1.0, 0.0)
    parallel_universe_perception = st.slider("Parallel Universe Sight", 0.0, 1.0, 0.0)
    
    spacetime_manipulation = st.slider("Spacetime Manipulation", 0.0, 1.0, 0.0)
    gravity_control = st.slider("Gravity Control", 0.0, 1.0, 0.0)
    time_perception_control = st.slider("Time Control", 0.0, 1.0, 0.0)
    
    wormhole_creation = st.slider("Wormhole Creation", 0.0, 1.0, 0.0)
    reality_warping = st.slider("Reality Warping", 0.0, 1.0, 0.0)

with st.sidebar.expander("🎭 Cosmic Powers", expanded=False):
    matter_creation = st.slider("Matter Creation", 0.0, 1.0, 0.0)
    energy_conversion = st.slider("Energy Conversion", 0.0, 1.0, 0.0)
    entropy_reversal = st.slider("Entropy Reversal", 0.0, 1.0, 0.0)
    
    star_manipulation = st.slider("Star Manipulation", 0.0, 1.0, 0.0)
    planetary_engineering = st.slider("Planetary Engineering", 0.0, 1.0, 0.0)
    galaxy_scale_influence = st.slider("Galaxy-Scale Influence", 0.0, 1.0, 0.0)
    
    universe_creation = st.slider("Universe Creation", 0.0, 1.0, 0.0)
    fundamental_law_modification = st.slider("Law Modification", 0.0, 1.0, 0.0)
    omnipresence = st.slider("Omnipresence", 0.0, 1.0, 0.0)

with st.sidebar.expander("♾️ Transcendence Levels", expanded=False):
    biological_transcendence = st.slider("Biological Transcendence", 0.0, 1.0, 0.0)
    digital_ascension = st.slider("Digital Ascension", 0.0, 1.0, 0.0)
    energy_ascension = st.slider("Energy Ascension", 0.0, 1.0, 0.0)
    
    fourth_dimensional_beings = st.slider("4D Beings", 0.0, 1.0, 0.0)
    fifth_dimensional_beings = st.slider("5D Beings", 0.0, 1.0, 0.0)
    higher_dimensional_beings = st.slider("Higher Dimensional", 0.0, 1.0, 0.0)
    
    godlike_entities = st.slider("Godlike Entities", 0.0, 1.0, 0.0)
    universe_consciousness = st.slider("Universe Consciousness", 0.0, 1.0, 0.0)
    absolute_omnipotence = st.slider("Absolute Omnipotence", 0.0, 1.0, 0.0)

# === CATASTROPHIC EVENTS ===
st.sidebar.markdown("---")
st.sidebar.markdown("## ☄️ Catastrophic Events")

with st.sidebar.expander("💥 Extinction Events", expanded=False):
    asteroid_impact_frequency = st.slider("Asteroid Impacts", 0.0, 1.0, 0.01)
    supervolcano_eruptions = st.slider("Supervolcano Eruptions", 0.0, 1.0, 0.01)
    gamma_ray_burst = st.slider("Gamma Ray Bursts", 0.0, 1.0, 0.001)
    
    pandemic_frequency = st.slider("Pandemic Frequency", 0.0, 1.0, 0.1)
    ice_age_frequency = st.slider("Ice Ages", 0.0, 1.0, 0.05)
    magnetic_reversal = st.slider("Magnetic Reversals", 0.0, 1.0, 0.02)
    
    solar_flare_intensity = st.slider("Solar Flares", 0.0, 2.0, 1.0)
    supernova_proximity = st.slider("Supernova Risk", 0.0, 1.0, 0.001)

with st.sidebar.expander("🌊 Climate Catastrophes", expanded=False):
    global_warming_rate = st.slider("Global Warming Rate", -1.0, 2.0, 0.0)
    ocean_acidification = st.slider("Ocean Acidification", 0.0, 2.0, 0.3)
    ozone_depletion = st.slider("Ozone Depletion", 0.0, 1.0, 0.0)
    
    mega_tsunami_frequency = st.slider("Mega Tsunamis", 0.0, 1.0, 0.01)
    hypercane_formation = st.slider("Hypercanes", 0.0, 1.0, 0.0)
    drought_severity = st.slider("Drought Severity", 0.0, 2.0, 1.0)

with st.sidebar.expander("🔥 Technological Risks", expanded=False):
    ai_takeover_risk = st.slider("AI Takeover Risk", 0.0, 1.0, 0.0)
    nuclear_war_probability = st.slider("Nuclear War", 0.0, 1.0, 0.0)
    bioweapon_outbreak = st.slider("Bioweapon Outbreak", 0.0, 1.0, 0.0)
    
    grey_goo_scenario = st.slider("Grey Goo Scenario", 0.0, 1.0, 0.0)
    vacuum_decay = st.slider("Vacuum Decay", 0.0, 1.0, 0.0)
    technological_singularity = st.slider("Singularity Risk", 0.0, 1.0, 0.0)

# === SIMULATION PARAMETERS ===
st.sidebar.markdown("---")
st.sidebar.markdown("## ⚙️ Simulation Settings")

with st.sidebar.expander("🎲 Randomness & Chaos", expanded=False):
    random_seed = st.number_input("Random Seed", 0, 999999, 42)
    chaos_factor = st.slider("Chaos Factor", 0.0, 1.0, 0.3)
    butterfly_effect_strength = st.slider("Butterfly Effect", 0.0, 1.0, 0.5)
    
    determinism_level = st.slider("Determinism Level", 0.0, 1.0, 0.7)
    emergent_behavior_tendency = st.slider("Emergent Behavior", 0.0, 1.0, 0.6)
    black_swan_frequency = st.slider("Black Swan Events", 0.0, 1.0, 0.05)

with st.sidebar.expander("📊 Visualization Settings", expanded=False):
    show_population_graph = st.checkbox("Population Graph", True)
    show_complexity_chart = st.checkbox("Complexity Chart", True)
    show_diversity_index = st.checkbox("Diversity Index", True)
    show_evolutionary_tree = st.checkbox("Evolutionary Tree", False)
    
    color_by_property = st.selectbox("Color By", 
        ["Life Type", "Complexity", "Intelligence", "Energy", "Age"])
    graph_update_frequency = st.slider("Graph Update Freq", 1, 100, 10)

with st.sidebar.expander("💾 Data Management", expanded=False):
    if st.button("Export Universe State", use_container_width=True):
        st.info("Export functionality ready")
    
    if st.button("Import Universe State", use_container_width=True):
        st.info("Import functionality ready")
    
    max_history_length = st.slider("Max History Length", 100, 10000, 1000)
    auto_save_frequency = st.slider("Auto-save Every N Generations", 0, 100, 10)

# === CORE SIMULATION FUNCTIONS ===

def initialize_genome(params):
    """Create a genome with specified parameters"""
    return Genome(
        dna_length=random.randint(1000, 10000),
        mutation_rate=base_mutation_rate,
        genes={
            "metabolism": random.random(),
            "reproduction": random.random(),
            "intelligence": random.random(),
            "adaptability": random.random(),
            "longevity": random.random(),
            "size": random.random(),
            "sensory": random.random(),
            "mobility": random.random(),
        },
        epigenetic_factors={
            "stress_response": random.random(),
            "environmental_memory": random.random(),
        },
        horizontal_transfer_rate=horizontal_gene_transfer
    )

def create_primordial_organism(id_num, params):
    """Create the first organism"""
    genome = initialize_genome(params)
    
    # Determine life type based on chemical conditions
    life_types = [LifeType.CARBON_BASED]
    if silicon_abundance > 1.0:
        life_types.append(LifeType.SILICON_BASED)
    if nitrogen_abundance > 2.0:
        life_types.append(LifeType.NITROGEN_BASED)
    if metallic_life_forms > 0.5:
        life_types.append(LifeType.METALLIC)
    
    life_type = random.choice(life_types)
    
    return Organism(
        id=id_num,
        name=f"Organism_{id_num}",
        life_type=life_type,
        complexity=ComplexityLevel.PRIMORDIAL,
        genome=genome,
        traits={
            "size": 0.01,
            "metabolism": genome.genes["metabolism"],
            "reproduction_rate": genome.genes["reproduction"] * reproductive_rate_base,
        },
        age=0,
        generation=0,
        population=100,
        energy=100.0,
        intelligence=base_intelligence * 0.01,
        adaptability=genome.genes["adaptability"],
        reproductive_rate=genome.genes["reproduction"],
        mutation_history=[],
        ancestors=[],
        environment_fitness=random.random(),
        technological_level=0.0,
        consciousness_level=0.0,
        size=0.01,
        mass=0.001,
        structure_complexity=1,
        aggression=aggression_base,
        cooperation=cooperation_tendency,
        exploration_drive=curiosity,
        telepathic_ability=0.0,
        dimensional_awareness=0.0,
        quantum_coherence=quantum_entanglement * 0.1,
        energy_efficiency=0.3,
        resource_gathering=0.5,
        temperature_tolerance=(base_temperature - 50, base_temperature + 50),
        pressure_tolerance=(atmospheric_pressure - 0.5, atmospheric_pressure + 0.5),
        radiation_resistance=0.1
    )

def mutate_organism(organism, params):
    """Apply mutations to an organism"""
    mutations = []
    
    # Base mutation check
    if random.random() < organism.genome.mutation_rate:
        mutation_type = random.choices(
            ["beneficial", "neutral", "harmful"],
            weights=[beneficial_mutation_chance, neutral_mutation_chance, harmful_mutation_chance]
        )[0]
        
        # Select a random trait to mutate
        trait_to_mutate = random.choice(list(organism.genome.genes.keys()))
        old_value = organism.genome.genes[trait_to_mutate]
        
        if mutation_type == "beneficial":
            organism.genome.genes[trait_to_mutate] *= random.uniform(1.1, 1.5)
            mutations.append(f"Beneficial: {trait_to_mutate} +{((organism.genome.genes[trait_to_mutate]/old_value)-1)*100:.1f}%")
        elif mutation_type == "harmful":
            organism.genome.genes[trait_to_mutate] *= random.uniform(0.5, 0.9)
            mutations.append(f"Harmful: {trait_to_mutate} -{(1-(organism.genome.genes[trait_to_mutate]/old_value))*100:.1f}%")
        else:
            organism.genome.genes[trait_to_mutate] *= random.uniform(0.95, 1.05)
            mutations.append(f"Neutral: {trait_to_mutate} ~{((organism.genome.genes[trait_to_mutate]/old_value)-1)*100:.1f}%")
        
        # Clamp values
        organism.genome.genes[trait_to_mutate] = max(0.0, min(2.0, organism.genome.genes[trait_to_mutate]))
    
    # Complexity increase chance
    if random.random() < complexity_increase_tendency * 0.01 and organism.structure_complexity < 100:
        organism.structure_complexity += 1
        mutations.append(f"Structure complexity increased to {organism.structure_complexity}")
        
        # Check for complexity level up
        if organism.structure_complexity > 10 and organism.complexity.value < ComplexityLevel.MULTI_CELL.value:
            organism.complexity = ComplexityLevel.MULTI_CELL
            mutations.append("EVOLVED: Multi-cellular life!")
        elif organism.structure_complexity > 30 and organism.complexity.value < ComplexityLevel.COMPLEX_ORGANISM.value:
            organism.complexity = ComplexityLevel.COMPLEX_ORGANISM
            mutations.append("EVOLVED: Complex organism!")
        elif organism.structure_complexity > 60 and organism.complexity.value < ComplexityLevel.INTELLIGENT.value:
            if organism.intelligence > 1.0:
                organism.complexity = ComplexityLevel.INTELLIGENT
                mutations.append("EVOLVED: Intelligent being!")
    
    # Intelligence evolution
    if organism.complexity.value >= ComplexityLevel.COMPLEX_ORGANISM.value:
        if random.random() < learning_rate * 0.01:
            organism.intelligence *= random.uniform(1.0, 1.2)
            organism.consciousness_level = organism.intelligence / 10.0
            mutations.append(f"Intelligence increased to {organism.intelligence:.2f}")
    
    # Technology development
    if organism.complexity.value >= ComplexityLevel.INTELLIGENT.value:
        if random.random() < innovation_rate * 0.1:
            organism.technological_level += random.uniform(0.1, 0.5)
            mutations.append(f"Technology level: {organism.technological_level:.2f}")
    
    # Advanced evolution - transcendence
    if organism.intelligence > 5.0 and organism.technological_level > 5.0:
        if random.random() < biological_transcendence * 0.01:
            if organism.complexity.value < ComplexityLevel.TRANSCENDENT.value:
                organism.complexity = ComplexityLevel.TRANSCENDENT
                mutations.append("TRANSCENDED: Beyond biological limits!")
    
    # Machine life emergence
    if organism.technological_level > 10.0 and random.random() < machine_life_emergence * 0.01:
        if organism.life_type != LifeType.MACHINE:
            organism.life_type = LifeType.MACHINE
            organism.energy_efficiency *= 2.0
            mutations.append("TRANSFORMATION: Machine life emerged!")
    
    # Psionic abilities
    if organism.consciousness_level > 0.5:
        if random.random() < telepathy_emergence * 0.01:
            organism.telepathic_ability += 0.1
            mutations.append(f"Psionic ability developing: {organism.telepathic_ability:.2f}")
    
    # Dimensional awareness
    if organism.intelligence > 8.0 and random.random() < dimensional_awareness * 0.01:
        organism.dimensional_awareness += 0.1
        mutations.append(f"Dimensional awareness: {organism.dimensional_awareness:.2f}")
    
    organism.mutation_history.extend(mutations)
    return mutations

def calculate_fitness(organism, environment):
    """Calculate how well organism fits environment"""
    fitness = 1.0
    
    # Temperature fitness
    temp_min, temp_max = organism.temperature_tolerance
    if environment.temperature < temp_min or environment.temperature > temp_max:
        fitness *= 0.5
    
    # Pressure fitness
    press_min, press_max = organism.pressure_tolerance
    if environment.pressure < press_min or environment.pressure > press_max:
        fitness *= 0.7
    
    # Radiation fitness
    radiation_damage = max(0, environment.radiation_level - organism.radiation_resistance)
    fitness *= (1.0 - radiation_damage * 0.5)
    
    # Complexity advantage
    fitness *= (1.0 + organism.complexity.value * 0.1)
    
    # Intelligence advantage
    fitness *= (1.0 + organism.intelligence * 0.05)
    
    organism.environment_fitness = max(0.01, fitness)
    return fitness

def simulate_generation(organisms, environment, params):
    """Simulate one generation of evolution"""
    new_organisms = []
    events = []
    
    for organism in organisms:
        # Age the organism
        organism.age += 1
        
        # Calculate fitness
        fitness = calculate_fitness(organism, environment)
        
        # Survival check
        survival_chance = fitness * (1.0 - mortality_rate)
        if random.random() > survival_chance:
            organism.population = int(organism.population * 0.9)
            if organism.population < 10:
                events.append(f"🦠 PANDEMIC struck {victim.name}!")
    
    return new_organisms, events

def create_environment(params):
    """Create environment based on parameters"""
    return Environment(
        temperature=base_temperature,
        pressure=atmospheric_pressure,
        radiation_level=cosmic_radiation + background_radiation,
        oxygen_level=oxygen_level,
        water_availability=water_coverage / 100.0,
        mineral_richness=(carbon_abundance + silicon_abundance) / 2.0,
        gravity=gravity_strength_local,
        magnetic_field=magnetic_field_strength,
        atmospheric_composition={
            "N2": nitrogen_level,
            "O2": oxygen_level,
            "CO2": carbon_dioxide,
            "Ar": argon_level,
            "CH4": methane_level,
        },
        geological_activity=volcanic_activity,
        stellar_type="G-type" if solar_radiation < 1.5 else "F-type",
        cosmic_ray_flux=cosmic_radiation,
        time_dilation_factor=1.0
    )

# Main app layout
st.markdown('<h1 class="main-header">🌌 Universe Sandbox AI 🌌</h1>', unsafe_allow_html=True)

# Initialize universe
if st.session_state.universe is None:
    st.info("⚡ Click 'Initialize Universe' to begin the simulation of life!")
    
    if st.button("🌟 INITIALIZE UNIVERSE NOW", type="primary", use_container_width=True):
        environment = create_environment(locals())
        initial_organisms = [create_primordial_organism(i, locals()) for i in range(5)]
        
        st.session_state.universe = UniverseState(
            age=0,
            organisms=initial_organisms,
            environment=environment,
            extinction_events=0,
            evolutionary_leaps=0,
            dominant_species=None,
            total_biomass=sum(o.population * o.mass for o in initial_organisms),
            technological_artifacts=0,
            dimensional_breaches=0
        )
        st.session_state.history = []
        st.session_state.generation = 0
        st.rerun()

else:
    # Main dashboard
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""<div class="stat-box">
            <h3>⏱️ Generation</h3>
            <h2>{st.session_state.generation}</h2>
        </div>""", unsafe_allow_html=True)
    
    with col2:
        species_count = len(st.session_state.universe.organisms)
        st.markdown(f"""<div class="stat-box">
            <h3>🧬 Species</h3>
            <h2>{species_count}</h2>
        </div>""", unsafe_allow_html=True)
    
    with col3:
        total_pop = sum(o.population for o in st.session_state.universe.organisms)
        st.markdown(f"""<div class="stat-box">
            <h3>👥 Population</h3>
            <h2>{total_pop:,}</h2>
        </div>""", unsafe_allow_html=True)
    
    with col4:
        max_intelligence = max([o.intelligence for o in st.session_state.universe.organisms] + [0])
        st.markdown(f"""<div class="stat-box">
            <h3>🧠 Max Intelligence</h3>
            <h2>{max_intelligence:.2f}</h2>
        </div>""", unsafe_allow_html=True)
    
    with col5:
        max_complexity = max([o.complexity.value for o in st.session_state.universe.organisms] + [0])
        st.markdown(f"""<div class="stat-box">
            <h3>🔬 Max Complexity</h3>
            <h2>{max_complexity}</h2>
        </div>""", unsafe_allow_html=True)
    
    # Simulation step
    if st.session_state.running:
        for _ in range(st.session_state.speed):
            st.session_state.generation += 1
            organisms, events = simulate_generation(
                st.session_state.universe.organisms,
                st.session_state.universe.environment,
                locals()
            )
            
            st.session_state.universe.organisms = organisms
            st.session_state.universe.age += 1
            
            # Record history
            st.session_state.history.append({
                "generation": st.session_state.generation,
                "species_count": len(organisms),
                "total_population": sum(o.population for o in organisms),
                "max_intelligence": max([o.intelligence for o in organisms] + [0]),
                "max_complexity": max([o.complexity.value for o in organisms] + [0]),
                "avg_fitness": np.mean([o.environment_fitness for o in organisms]) if organisms else 0,
            })
            
            # Keep history manageable
            if len(st.session_state.history) > max_history_length:
                st.session_state.history = st.session_state.history[-max_history_length:]
        
        time.sleep(0.1)
        st.rerun()
    
    # Tabs for different views
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Statistics", "🦠 Organisms", "📈 Evolution", "🌍 Environment", "🎯 Events"
    ])
    
    with tab1:
        st.subheader("Universe Statistics")
        
        if len(st.session_state.history) > 1:
            history_df = pd.DataFrame(st.session_state.history)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if show_population_graph:
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=history_df['generation'],
                        y=history_df['total_population'],
                        mode='lines',
                        name='Total Population',
                        line=dict(color='#667eea', width=3)
                    ))
                    fig.update_layout(
                        title="Population Over Time",
                        xaxis_title="Generation",
                        yaxis_title="Population",
                        template="plotly_dark",
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                if show_complexity_chart:
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=history_df['generation'],
                        y=history_df['max_complexity'],
                        mode='lines',
                        name='Max Complexity',
                        line=dict(color='#f093fb', width=3),
                        fill='tozeroy'
                    ))
                    fig.update_layout(
                        title="Complexity Evolution",
                        xaxis_title="Generation",
                        yaxis_title="Complexity Level",
                        template="plotly_dark",
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                if show_diversity_index:
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=history_df['generation'],
                        y=history_df['species_count'],
                        mode='lines',
                        name='Species Count',
                        line=dict(color='#4facfe', width=3)
                    ))
                    fig.update_layout(
                        title="Biodiversity Over Time",
                        xaxis_title="Generation",
                        yaxis_title="Number of Species",
                        template="plotly_dark",
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=history_df['generation'],
                    y=history_df['max_intelligence'],
                    mode='lines',
                    name='Max Intelligence',
                    line=dict(color='#43e97b', width=3)
                ))
                fig.update_layout(
                    title="Intelligence Evolution",
                    xaxis_title="Generation",
                    yaxis_title="Intelligence Level",
                    template="plotly_dark",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Distribution charts
        if st.session_state.universe.organisms:
            col1, col2 = st.columns(2)
            
            with col1:
                life_types = [o.life_type.value for o in st.session_state.universe.organisms]
                fig = px.pie(
                    names=life_types,
                    title="Life Type Distribution",
                    color_discrete_sequence=px.colors.sequential.Plasma
                )
                fig.update_layout(template="plotly_dark", height=300)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                complexity_levels = [o.complexity.name for o in st.session_state.universe.organisms]
                fig = px.histogram(
                    x=complexity_levels,
                    title="Complexity Distribution",
                    color_discrete_sequence=['#667eea']
                )
                fig.update_layout(template="plotly_dark", height=300)
                st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Current Organisms")
        
        if st.session_state.universe.organisms:
            # Sort organisms
            sort_by = st.selectbox("Sort by:", 
                ["Population", "Intelligence", "Complexity", "Technology", "Age"])
            
            if sort_by == "Population":
                sorted_orgs = sorted(st.session_state.universe.organisms, 
                                   key=lambda x: x.population, reverse=True)
            elif sort_by == "Intelligence":
                sorted_orgs = sorted(st.session_state.universe.organisms, 
                                   key=lambda x: x.intelligence, reverse=True)
            elif sort_by == "Complexity":
                sorted_orgs = sorted(st.session_state.universe.organisms, 
                                   key=lambda x: x.complexity.value, reverse=True)
            elif sort_by == "Technology":
                sorted_orgs = sorted(st.session_state.universe.organisms, 
                                   key=lambda x: x.technological_level, reverse=True)
            else:
                sorted_orgs = sorted(st.session_state.universe.organisms, 
                                   key=lambda x: x.age, reverse=True)
            
            # Display top organisms
            display_count = min(20, len(sorted_orgs))
            
            for org in sorted_orgs[:display_count]:
                with st.expander(f"🦠 {org.name} - {org.life_type.value} - {org.complexity.name}"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Population", f"{org.population:,}")
                        st.metric("Intelligence", f"{org.intelligence:.2f}")
                        st.metric("Complexity", org.complexity.value)
                        st.metric("Generation", org.generation)
                    
                    with col2:
                        st.metric("Energy", f"{org.energy:.1f}")
                        st.metric("Fitness", f"{org.environment_fitness:.2f}")
                        st.metric("Technology", f"{org.technological_level:.2f}")
                        st.metric("Age", org.age)
                    
                    with col3:
                        st.metric("Consciousness", f"{org.consciousness_level:.2f}")
                        st.metric("Adaptability", f"{org.adaptability:.2f}")
                        st.metric("Size", f"{org.size:.3f}")
                        st.metric("Structure", org.structure_complexity)
                    
                    # Special abilities
                    if org.telepathic_ability > 0:
                        st.info(f"🧠 Telepathic Ability: {org.telepathic_ability:.2f}")
                    if org.dimensional_awareness > 0:
                        st.info(f"🌀 Dimensional Awareness: {org.dimensional_awareness:.2f}")
                    if org.technological_level > 1:
                        st.success(f"🔬 Technologically Advanced: Level {org.technological_level:.1f}")
                    
                    # Genome information
                    st.markdown("**Genetic Traits:**")
                    genes_df = pd.DataFrame([org.genome.genes]).T
                    genes_df.columns = ["Value"]
                    st.dataframe(genes_df, use_container_width=True)
                    
                    # Recent mutations
                    if org.mutation_history:
                        st.markdown("**Recent Mutations:**")
                        for mutation in org.mutation_history[-5:]:
                            st.text(f"• {mutation}")
        else:
            st.warning("No organisms currently exist in the universe!")
    
    with tab3:
        st.subheader("Evolutionary Progress")
        
        if st.session_state.universe.organisms:
            # Create 3D scatter plot of organisms
            org_data = []
            for org in st.session_state.universe.organisms:
                org_data.append({
                    "name": org.name,
                    "intelligence": org.intelligence,
                    "complexity": org.complexity.value,
                    "population": org.population,
                    "life_type": org.life_type.value,
                    "technology": org.technological_level,
                    "consciousness": org.consciousness_level
                })
            
            df = pd.DataFrame(org_data)
            
            fig = px.scatter_3d(
                df,
                x="intelligence",
                y="complexity",
                z="technology",
                size="population",
                color="life_type",
                hover_name="name",
                title="3D Evolutionary Space",
                labels={
                    "intelligence": "Intelligence",
                    "complexity": "Complexity",
                    "technology": "Technology Level"
                }
            )
            fig.update_layout(template="plotly_dark", height=600)
            st.plotly_chart(fig, use_container_width=True)
            
            # Evolutionary milestones
            st.markdown("### 🏆 Evolutionary Milestones")
            
            milestones = []
            for org in st.session_state.universe.organisms:
                if org.complexity.value >= ComplexityLevel.MULTI_CELL.value:
                    milestones.append(f"✅ Multi-cellular life achieved by {org.name}")
                if org.complexity.value >= ComplexityLevel.INTELLIGENT.value:
                    milestones.append(f"🧠 Intelligence emerged in {org.name}")
                if org.complexity.value >= ComplexityLevel.TRANSCENDENT.value:
                    milestones.append(f"⚡ {org.name} has transcended biological limits!")
                if org.technological_level > 5:
                    milestones.append(f"🔬 {org.name} developed advanced technology")
                if org.life_type == LifeType.MACHINE:
                    milestones.append(f"🤖 Machine life emerged: {org.name}")
            
            unique_milestones = list(set(milestones))[:10]
            for milestone in unique_milestones:
                st.success(milestone)
            
            if not unique_milestones:
                st.info("No major evolutionary milestones yet. Keep evolving!")
        
        # Complexity progression
        if len(st.session_state.history) > 1:
            st.markdown("### 📊 Complexity Progression")
            history_df = pd.DataFrame(st.session_state.history)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=history_df['generation'],
                y=history_df['max_complexity'],
                mode='lines+markers',
                name='Max Complexity',
                line=dict(color='#f093fb', width=4),
                marker=dict(size=8)
            ))
            
            # Add complexity level annotations
            complexity_names = {i: name for i, name in enumerate([
                "Primordial", "Single Cell", "Multi Cell", "Simple Organism",
                "Complex Organism", "Intelligent", "Advanced", "Transcendent", "Cosmic", "Omnipotent"
            ])}
            
            for level, name in complexity_names.items():
                fig.add_hline(y=level, line_dash="dash", line_color="gray", 
                            annotation_text=name, annotation_position="right")
            
            fig.update_layout(
                title="Journey Through Complexity",
                xaxis_title="Generation",
                yaxis_title="Complexity Level",
                template="plotly_dark",
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("Environmental Conditions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🌡️ Physical Parameters")
            env = st.session_state.universe.environment
            
            st.metric("Temperature", f"{env.temperature:.1f} K")
            st.metric("Pressure", f"{env.pressure:.2f} atm")
            st.metric("Gravity", f"{env.gravity:.2f} g")
            st.metric("Radiation Level", f"{env.radiation_level:.2f}")
            st.metric("Magnetic Field", f"{env.magnetic_field:.2f}")
            st.metric("Water Availability", f"{env.water_availability*100:.1f}%")
        
        with col2:
            st.markdown("### 🌊 Atmospheric Composition")
            
            atm_data = pd.DataFrame([env.atmospheric_composition]).T
            atm_data.columns = ["Percentage"]
            
            fig = px.bar(
                atm_data,
                y=atm_data.index,
                x="Percentage",
                orientation='h',
                title="Atmospheric Gases",
                color="Percentage",
                color_continuous_scale="Viridis"
            )
            fig.update_layout(template="plotly_dark", height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Environmental suitability
        st.markdown("### 🎯 Environmental Suitability")
        
        if st.session_state.universe.organisms:
            avg_fitness = np.mean([o.environment_fitness for o in st.session_state.universe.organisms])
            
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=avg_fitness * 100,
                title={'text': "Average Organism Fitness"},
                delta={'reference': 70},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#667eea"},
                    'steps': [
                        {'range': [0, 30], 'color': "#ff6b6b"},
                        {'range': [30, 70], 'color': "#feca57"},
                        {'range': [70, 100], 'color': "#1dd1a1"}
                    ],
                    'threshold': {
                        'line': {'color': "white", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            fig.update_layout(template="plotly_dark", height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab5:
        st.subheader("Recent Events")
        
        # Show recent mutations and events from organisms
        all_events = []
        for org in st.session_state.universe.organisms:
            if org.mutation_history:
                for mutation in org.mutation_history[-3:]:
                    all_events.append({
                        "Generation": st.session_state.generation,
                        "Organism": org.name,
                        "Event": mutation,
                        "Type": "Mutation"
                    })
        
        # Add system events
        if st.session_state.generation % 100 == 0:
            all_events.append({
                "Generation": st.session_state.generation,
                "Organism": "System",
                "Event": f"Century milestone reached! Universe age: {st.session_state.generation}",
                "Type": "Milestone"
            })
        
        if all_events:
            events_df = pd.DataFrame(all_events[-50:])  # Last 50 events
            st.dataframe(events_df, use_container_width=True, height=400)
        else:
            st.info("No events yet. Start the simulation to see life evolve!")
        
        # Universe statistics summary
        st.markdown("### 📈 Universe Summary")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Extinction Events",
                st.session_state.universe.extinction_events,
                help="Number of species that have gone extinct"
            )
        
        with col2:
            st.metric(
                "Evolutionary Leaps",
                st.session_state.universe.evolutionary_leaps,
                help="Major evolutionary transitions"
            )
        
        with col3:
            total_biomass = sum(o.population * o.mass for o in st.session_state.universe.organisms)
            st.metric(
                "Total Biomass",
                f"{total_biomass:.2f}",
                help="Combined mass of all organisms"
            )
    
    # Footer with fun facts
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #888;'>
        <p>🌌 Universe Sandbox AI - Watch Evolution Unfold 🌌</p>
        <p>From simple cells to cosmic entities - witness the infinite possibilities of life</p>
    </div>
    """, unsafe_allow_html=True)
