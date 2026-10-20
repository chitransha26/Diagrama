"""Builds the curriculum map (coverage ledger, PRD §03) as coverage.csv and summary counts.

Each diagram is mapped to the NGSS performance expectation it supports (or an AP course); undergraduate
diagrams to an OpenStax textbook section and, where it applies, an MCAT content category.
Mappings are proposed and need teacher review before a lesson is advertised as covering a
standard. Run: python3 curriculum/build_map.py
"""
import csv
import os
from collections import Counter

# (grade, subject, diagram, standard, interaction)
# interaction: trace = trace + label; process = cycle/flow with arrows; graph = draw axes and
# curve; build = draw a structure from rules (e.g. Lewis); compare = two diagrams side by side
D = [
    # ---- Kindergarten ----
    ("K", "Life", "Parts of a plant: root, stem, leaf, flower", "K-LS1-1", "trace"),
    ("K", "Life", "Parts of a tree", "K-LS1-1", "trace"),
    ("K", "Life", "A seed sprouting", "K-LS1-1", "process"),
    ("K", "Life", "A plant growing toward light", "K-LS1-1", "compare"),
    ("K", "Earth & Space", "A bird building a nest", "K-ESS2-2", "trace"),
    ("K", "Earth & Space", "A beaver dam changing a stream", "K-ESS2-2", "trace"),
    ("K", "Earth & Space", "Weather symbols: sun, cloud, rain, snow", "K-ESS2-1", "trace"),
    ("K", "Physical", "Sunlight warming the ground", "K-PS3-1", "compare"),
    ("K", "Physical", "A shade structure blocking the sun", "K-PS3-2", "trace"),
    ("K", "Physical", "Pushes and pulls on a wagon", "K-PS2-1", "trace"),
    # ---- Grade 1 ----
    ("1", "Life", "Turtle shell: built for protection", "1-LS1-1", "trace"),
    ("1", "Life", "Cactus: spines and a thick stem", "1-LS1-1", "trace"),
    ("1", "Life", "Bird beaks and the food they eat", "1-LS1-1", "compare"),
    ("1", "Life", "Burr and hook-and-loop fastener (biomimicry)", "1-LS1-1", "compare"),
    ("1", "Life", "A bird feeding its chicks", "1-LS1-2", "trace"),
    ("1", "Life", "Parent and young plant: alike and different", "1-LS3-1", "compare"),
    ("1", "Life", "Dog and puppies: inherited features", "1-LS3-1", "compare"),
    ("1", "Physical", "A vibrating drum makes sound", "1-PS4-1", "trace"),
    ("1", "Physical", "Light from a flashlight lets us see", "1-PS4-2", "process"),
    ("1", "Physical", "Transparent, translucent and opaque", "1-PS4-3", "compare"),
    ("1", "Physical", "A string-and-cup telephone", "1-PS4-4", "trace"),
    ("1", "Earth & Space", "The sun's path across the sky", "1-ESS1-1", "process"),
    ("1", "Earth & Space", "Shapes of the moon over a month", "1-ESS1-1", "process"),
    ("1", "Earth & Space", "Daylight in winter vs summer", "1-ESS1-2", "compare"),
    # ---- Grade 2 ----
    ("2", "Life", "What plants need: light and water test", "2-LS2-1", "compare"),
    ("2", "Life", "A bee pollinating a flower", "2-LS2-2", "trace"),
    ("2", "Life", "Seed dispersal: wind, water, animals", "2-LS2-2", "compare"),
    ("2", "Life", "Pond habitat", "2-LS4-1", "trace"),
    ("2", "Life", "Desert habitat", "2-LS4-1", "trace"),
    ("2", "Life", "Rainforest layers", "2-LS4-1", "trace"),
    ("2", "Physical", "Water as ice, liquid and vapor", "2-PS1-1", "compare"),
    ("2", "Physical", "Building something from small pieces", "2-PS1-3", "trace"),
    ("2", "Physical", "Melting and freezing: reversible changes", "2-PS1-4", "process"),
    ("2", "Earth & Space", "Fast and slow land changes: volcano vs canyon", "2-ESS1-1", "compare"),
    ("2", "Earth & Space", "A simple map of land and water", "2-ESS2-2", "trace"),
    ("2", "Earth & Space", "Where water is found: glacier, river, ocean", "2-ESS2-3", "trace"),
    ("2", "Earth & Space", "A windbreak slowing erosion", "2-ESS2-1", "trace"),
    # ---- Grade 3 ----
    ("3", "Life", "Butterfly life cycle", "3-LS1-1", "process"),
    ("3", "Life", "Frog life cycle", "3-LS1-1", "process"),
    ("3", "Life", "Flowering plant life cycle", "3-LS1-1", "process"),
    ("3", "Life", "Chicken life cycle", "3-LS1-1", "process"),
    ("3", "Life", "Animals in groups: a school of fish", "3-LS2-1", "trace"),
    ("3", "Life", "Inherited traits: flower color in a family", "3-LS3-1", "compare"),
    ("3", "Life", "Environment changes traits: plant in light vs dark", "3-LS3-2", "compare"),
    ("3", "Life", "How a fossil forms", "3-LS4-1", "process"),
    ("3", "Life", "Variation: beetles of different colors", "3-LS4-2", "compare"),
    ("3", "Life", "Camouflage: peppered moths on bark", "3-LS4-3", "compare"),
    ("3", "Life", "When a dam blocks salmon: a fish ladder", "3-LS4-4", "trace"),
    ("3", "Physical", "Balanced and unbalanced forces: tug of war", "3-PS2-1", "trace"),
    ("3", "Physical", "A pendulum's swing", "3-PS2-2", "process"),
    ("3", "Physical", "Magnets attract and repel", "3-PS2-3", "compare"),
    ("3", "Physical", "Design problem: sorting cans with a magnet", "3-PS2-4", "trace"),
    ("3", "Earth & Space", "Graphing a week of temperatures", "3-ESS2-1", "graph"),
    ("3", "Earth & Space", "Climate zones of the world", "3-ESS2-2", "trace"),
    ("3", "Earth & Space", "Structure of a hurricane", "3-ESS3-1", "trace"),
    # ---- Grade 4 ----
    ("4", "Life", "Parts of a flower", "4-LS1-1", "trace"),
    ("4", "Life", "The human heart (simple)", "4-LS1-1", "trace"),
    ("4", "Life", "Fish external anatomy", "4-LS1-1", "trace"),
    ("4", "Life", "Bird external anatomy", "4-LS1-1", "trace"),
    ("4", "Life", "The human skeleton: major bones", "4-LS1-1", "trace"),
    ("4", "Life", "The human lungs", "4-LS1-1", "trace"),
    ("4", "Life", "The digestive system (simple)", "4-LS1-1", "trace"),
    ("4", "Life", "Earthworm external anatomy", "4-LS1-1", "trace"),
    ("4", "Life", "The human eye (simple)", "4-LS1-2", "trace"),
    ("4", "Life", "The human ear (simple)", "4-LS1-2", "trace"),
    ("4", "Physical", "A simple circuit: battery, wire, bulb", "4-PS3-2", "trace"),
    ("4", "Physical", "A wind turbine making electricity", "4-PS3-4", "process"),
    ("4", "Physical", "Parts of a wave: crest, trough, wavelength", "4-PS4-1", "trace"),
    ("4", "Physical", "Light reflecting into the eye", "4-PS4-2", "process"),
    ("4", "Physical", "Sending a message in code", "4-PS4-3", "process"),
    ("4", "Earth & Space", "Rock layers with fossils", "4-ESS1-1", "trace"),
    ("4", "Earth & Space", "Weathering by ice wedging", "4-ESS2-1", "process"),
    ("4", "Earth & Space", "Map of volcanoes and earthquakes: Ring of Fire", "4-ESS2-2", "trace"),
    ("4", "Earth & Space", "Renewable and nonrenewable energy sources", "4-ESS3-1", "compare"),
    ("4", "Earth & Space", "An earthquake-resistant building", "4-ESS3-2", "trace"),
    # ---- Grade 5 ----
    ("5", "Physical", "Particles in a solid, liquid and gas", "5-PS1-1", "compare"),
    ("5", "Physical", "Conservation of mass on a balance", "5-PS1-2", "compare"),
    ("5", "Physical", "Salt dissolving in water", "5-PS1-4", "process"),
    ("5", "Physical", "Gravity pulls toward Earth's center", "5-PS2-1", "trace"),
    ("5", "Life", "Energy flow: sun to plant to animal", "5-PS3-1", "process"),
    ("5", "Life", "What a plant takes in and gives out", "5-LS1-1", "process"),
    ("5", "Life", "Forest food web", "5-LS2-1", "process"),
    ("5", "Life", "Ocean food chain", "5-LS2-1", "process"),
    ("5", "Life", "Decomposers return nutrients to soil", "5-LS2-1", "process"),
    ("5", "Earth & Space", "The water cycle", "5-ESS2-1", "process"),
    ("5", "Earth & Space", "Earth's four spheres", "5-ESS2-1", "trace"),
    ("5", "Earth & Space", "Where Earth's water is", "5-ESS2-2", "graph"),
    ("5", "Earth & Space", "The sun compared with other stars", "5-ESS1-1", "compare"),
    ("5", "Earth & Space", "Shadow length through the day", "5-ESS1-2", "process"),
    ("5", "Earth & Space", "Earth's rotation: day and night", "5-ESS1-2", "process"),
    ("5", "Earth & Space", "Seasonal constellations", "5-ESS1-2", "compare"),
    ("5", "Earth & Space", "A community recycling loop", "5-ESS3-1", "process"),
    # ---- Middle school: life science (often grade 7) ----
    ("7", "Life", "The compound light microscope", "MS-LS1-1", "trace"),
    ("7", "Life", "Animal cell", "MS-LS1-2", "trace"),
    ("7", "Life", "Plant cell", "MS-LS1-2", "trace"),
    ("7", "Life", "Bacterial cell (prokaryote)", "MS-LS1-1", "trace"),
    ("7", "Life", "Mitochondrion (simple)", "MS-LS1-2", "trace"),
    ("7", "Life", "Diffusion across a membrane", "MS-LS1-2", "process"),
    ("7", "Life", "Plant vs animal cell", "MS-LS1-2", "compare"),
    ("7", "Life", "Levels of organization: cell to organism", "MS-LS1-3", "process"),
    ("7", "Life", "The circulatory system", "MS-LS1-3", "trace"),
    ("7", "Life", "The respiratory system", "MS-LS1-3", "trace"),
    ("7", "Life", "The digestive system", "MS-LS1-3", "trace"),
    ("7", "Life", "The nervous system", "MS-LS1-3", "trace"),
    ("7", "Life", "Muscles moving the arm: biceps and triceps", "MS-LS1-3", "trace"),
    ("7", "Life", "The urinary system and kidney", "MS-LS1-3", "trace"),
    ("7", "Life", "Pollination and the pollen tube", "MS-LS1-4", "process"),
    ("7", "Life", "Inside a bean seed", "MS-LS1-4", "trace"),
    ("7", "Life", "Graphing plant growth", "MS-LS1-5", "graph"),
    ("7", "Life", "Photosynthesis in a leaf", "MS-LS1-6", "process"),
    ("7", "Life", "Leaf cross-section", "MS-LS1-6", "trace"),
    ("7", "Life", "Cellular respiration overview", "MS-LS1-7", "process"),
    ("7", "Life", "A reflex arc", "MS-LS1-8", "process"),
    ("7", "Life", "Predator-prey population graph", "MS-LS2-1", "graph"),
    ("7", "Life", "Symbiosis: clownfish and anemone", "MS-LS2-2", "compare"),
    ("7", "Life", "The carbon cycle", "MS-LS2-3", "process"),
    ("7", "Life", "The nitrogen cycle", "MS-LS2-3", "process"),
    ("7", "Life", "Ecological succession", "MS-LS2-4", "process"),
    ("7", "Life", "DNA, genes and chromosomes", "MS-LS3-1", "trace"),
    ("7", "Life", "A Punnett square", "MS-LS3-2", "graph"),
    ("7", "Life", "Asexual reproduction: budding and fission", "MS-LS3-2", "compare"),
    ("7", "Life", "The geologic time scale", "MS-LS4-1", "graph"),
    ("7", "Life", "Homologous forelimbs", "MS-LS4-2", "compare"),
    ("7", "Life", "Vertebrate embryos compared", "MS-LS4-3", "compare"),
    ("7", "Life", "Natural selection in finch beaks", "MS-LS4-4", "compare"),
    ("7", "Life", "Artificial selection: wild mustard to broccoli", "MS-LS4-5", "process"),
    ("7", "Zoology", "Frog internal anatomy", "MS-LS1-3", "trace"),
    ("7", "Zoology", "Earthworm internal anatomy", "MS-LS1-3", "trace"),
    ("7", "Zoology", "Fish internal anatomy", "MS-LS1-3", "trace"),
    ("7", "Zoology", "Insect body plan", "MS-LS1-3", "trace"),
    ("7", "Zoology", "The five vertebrate classes", "MS-LS4-2", "compare"),
    # ---- Middle school: physical science (often grade 8) ----
    ("8", "Chemistry", "Bohr model of an atom", "MS-PS1-1", "build"),
    ("8", "Chemistry", "Water molecule, ball-and-stick", "MS-PS1-1", "build"),
    ("8", "Chemistry", "Simple molecules: O2, CO2, CH4", "MS-PS1-1", "build"),
    ("8", "Chemistry", "Particles before and after a reaction", "MS-PS1-2", "compare"),
    ("8", "Chemistry", "Heating curve of water", "MS-PS1-4", "graph"),
    ("8", "Chemistry", "Particle motion in each state", "MS-PS1-4", "compare"),
    ("8", "Chemistry", "Balancing a reaction with atoms", "MS-PS1-5", "build"),
    ("8", "Chemistry", "Exothermic vs endothermic energy diagrams", "MS-PS1-6", "graph"),
    ("8", "Physics", "Action and reaction: a rocket", "MS-PS2-1", "trace"),
    ("8", "Physics", "Free-body diagram: pushing a box", "MS-PS2-2", "build"),
    ("8", "Physics", "An electromagnet", "MS-PS2-3", "trace"),
    ("8", "Physics", "Series vs parallel circuits", "MS-PS2-3", "compare"),
    ("8", "Physics", "Gravity between Earth and Moon", "MS-PS2-4", "trace"),
    ("8", "Physics", "Magnetic field of a bar magnet", "MS-PS2-5", "trace"),
    ("8", "Physics", "Kinetic energy and speed", "MS-PS3-1", "graph"),
    ("8", "Physics", "Roller coaster: potential and kinetic energy", "MS-PS3-2", "process"),
    ("8", "Physics", "Conduction, convection and radiation", "MS-PS3-3", "compare"),
    ("8", "Physics", "Transverse and longitudinal waves", "MS-PS4-1", "compare"),
    ("8", "Physics", "Reflection and refraction of light", "MS-PS4-2", "trace"),
    ("8", "Physics", "The electromagnetic spectrum", "MS-PS4-2", "trace"),
    ("8", "Physics", "Analog vs digital signals", "MS-PS4-3", "graph"),
    # ---- Middle school: Earth and space science (often grade 6) ----
    ("6", "Earth & Space", "Phases of the moon", "MS-ESS1-1", "process"),
    ("6", "Earth & Space", "Why we have seasons", "MS-ESS1-1", "trace"),
    ("6", "Earth & Space", "Solar and lunar eclipses", "MS-ESS1-1", "compare"),
    ("6", "Earth & Space", "The solar system", "MS-ESS1-2", "trace"),
    ("6", "Earth & Space", "The Milky Way and our sun", "MS-ESS1-2", "trace"),
    ("6", "Earth & Space", "Reading rock layers and geologic history", "MS-ESS1-4", "trace"),
    ("6", "Earth & Space", "The rock cycle", "MS-ESS2-1", "process"),
    ("6", "Earth & Space", "Erosion and deposition: a river delta", "MS-ESS2-2", "process"),
    ("6", "Earth & Space", "Plate boundaries", "MS-ESS2-3", "compare"),
    ("6", "Earth & Space", "Pangaea and continental drift", "MS-ESS2-3", "compare"),
    ("6", "Earth & Space", "The water cycle in detail", "MS-ESS2-4", "process"),
    ("6", "Earth & Space", "A cold front", "MS-ESS2-5", "trace"),
    ("6", "Earth & Space", "Global wind belts", "MS-ESS2-6", "trace"),
    ("6", "Earth & Space", "An aquifer cross-section", "MS-ESS3-1", "trace"),
    ("6", "Earth & Space", "Inside a volcano", "MS-ESS3-2", "trace"),
    ("6", "Earth & Space", "The greenhouse effect", "MS-ESS3-5", "process"),
    # ---- High school biology (often grades 9-10) ----
    ("9-10", "Life", "DNA double helix", "HS-LS1-1", "trace"),
    ("9-10", "Life", "Transcription and translation", "HS-LS1-1", "process"),
    ("9-10", "Life", "Levels of protein structure", "HS-LS1-1", "compare"),
    ("9-10", "Life", "The human heart and double circulation", "HS-LS1-2", "trace"),
    ("9-10", "Life", "The nephron", "HS-LS1-2", "trace"),
    ("9-10", "Life", "The neuron", "HS-LS1-2", "trace"),
    ("9-10", "Life", "Alveoli and gas exchange", "HS-LS1-2", "trace"),
    ("9-10", "Life", "Negative feedback: blood glucose", "HS-LS1-3", "process"),
    ("9-10", "Life", "The cell cycle", "HS-LS1-4", "process"),
    ("9-10", "Life", "Stages of mitosis", "HS-LS1-4", "process"),
    ("9-10", "Life", "Chloroplast structure", "HS-LS1-5", "trace"),
    ("9-10", "Life", "Light reactions and the Calvin cycle", "HS-LS1-5", "process"),
    ("9-10", "Life", "Amino acids and the peptide bond", "HS-LS1-6", "build"),
    ("9-10", "Life", "Glucose ring structure", "HS-LS1-6", "build"),
    ("9-10", "Life", "Mitochondrion structure", "HS-LS1-7", "trace"),
    ("9-10", "Life", "Glycolysis, Krebs cycle and electron transport", "HS-LS1-7", "process"),
    ("9-10", "Life", "Energy pyramid and the 10% rule", "HS-LS2-4", "graph"),
    ("9-10", "Life", "Carbon cycle with reservoirs", "HS-LS2-5", "process"),
    ("9-10", "Life", "Chromosome structure and karyotype", "HS-LS3-1", "trace"),
    ("9-10", "Life", "Meiosis and crossing over", "HS-LS3-2", "process"),
    ("9-10", "Life", "A pedigree chart", "HS-LS3-3", "build"),
    ("9-10", "Life", "Dihybrid Punnett square", "HS-LS3-3", "graph"),
    ("9-10", "Life", "A cladogram", "HS-LS4-1", "build"),
    ("9-10", "Life", "Darwin's finches and adaptive radiation", "HS-LS4-4", "compare"),
    ("AP Bio", "Life", "Fluid mosaic model of the membrane", "AP Biology", "trace"),
    ("AP Bio", "Life", "Enzyme and substrate: induced fit", "AP Biology", "process"),
    ("AP Bio", "Life", "Dicot root cross-section", "AP Biology", "trace"),
    ("AP Bio", "Life", "Monocot vs dicot stem cross-sections", "AP Biology", "compare"),
    ("AP Bio", "Life", "Flower longitudinal section", "AP Biology", "trace"),
    ("AP Bio", "Life", "Bacteriophage virus structure", "AP Biology", "trace"),
    ("9-10", "Zoology", "Animal tissue types", "HS-LS1-2", "compare"),
    ("9-10", "Zoology", "The human eye in detail", "HS-LS1-2", "trace"),
    ("9-10", "Zoology", "The human ear in detail", "HS-LS1-2", "trace"),
    ("9-10", "Zoology", "Skin cross-section", "HS-LS1-2", "trace"),
    ("9-10", "Zoology", "Fish, amphibian and mammal hearts compared", "HS-LS4-1", "compare"),
    # ---- High school chemistry (often grades 10-11) ----
    ("10-11", "Chemistry", "Atomic structure: protons, neutrons, electrons", "HS-PS1-1", "build"),
    ("10-11", "Chemistry", "Periodic table: groups, periods and blocks", "HS-PS1-1", "trace"),
    ("10-11", "Chemistry", "Orbital diagram for oxygen", "HS-PS1-1", "build"),
    ("10-11", "Chemistry", "Water: Lewis structure", "HS-PS1-1", "build"),
    ("10-11", "Chemistry", "Ammonia: Lewis structure", "HS-PS1-2", "build"),
    ("10-11", "Chemistry", "Methane: Lewis structure", "HS-PS1-2", "build"),
    ("10-11", "Chemistry", "Carbon dioxide: double bonds", "HS-PS1-2", "build"),
    ("10-11", "Chemistry", "Ionic bonding: sodium chloride", "HS-PS1-2", "build"),
    ("10-11", "Chemistry", "Sodium chloride crystal lattice", "HS-PS1-3", "trace"),
    ("10-11", "Chemistry", "Hydrogen bonds between water molecules", "HS-PS1-3", "build"),
    ("10-11", "Chemistry", "Molecular shapes (VSEPR)", "HS-PS1-3", "compare"),
    ("10-11", "Chemistry", "Reaction energy diagram and activation energy", "HS-PS1-4", "graph"),
    ("10-11", "Chemistry", "Collision theory and reaction rate", "HS-PS1-5", "compare"),
    ("10-11", "Chemistry", "Reaching equilibrium", "HS-PS1-6", "graph"),
    ("10-11", "Chemistry", "Combustion of methane, atom by atom", "HS-PS1-7", "build"),
    ("10-11", "Chemistry", "Alpha, beta and gamma decay", "HS-PS1-8", "compare"),
    ("10-11", "Chemistry", "A fission chain reaction", "HS-PS1-8", "process"),
    ("10-11", "Chemistry", "Phase diagram of water", "HS-PS1-3", "graph"),
    ("10-11", "Chemistry", "The pH scale", "HS-PS1-2", "graph"),
    ("AP Chem", "Chemistry", "Titration setup and curve", "AP Chemistry", "graph"),
    ("AP Chem", "Chemistry", "Simple distillation apparatus", "AP Chemistry", "trace"),
    ("AP Chem", "Chemistry", "Galvanic (electrochemical) cell", "AP Chemistry", "trace"),
    # ---- High school physics (often grades 11-12) ----
    ("11-12", "Physics", "Free-body diagram on an incline", "HS-PS2-1", "build"),
    ("11-12", "Physics", "Velocity-time graph", "HS-PS2-1", "graph"),
    ("11-12", "Physics", "Momentum in a collision", "HS-PS2-2", "compare"),
    ("11-12", "Physics", "Electric field lines of charges", "HS-PS2-4", "trace"),
    ("11-12", "Physics", "Magnetic field around a current", "HS-PS2-5", "trace"),
    ("11-12", "Physics", "An electric motor", "HS-PS2-5", "trace"),
    ("11-12", "Physics", "A generator and induction", "HS-PS2-5", "trace"),
    ("11-12", "Physics", "Energy flow in a power plant", "HS-PS3-1", "process"),
    ("11-12", "Physics", "Circuit schematic with resistors", "HS-PS3-3", "build"),
    ("11-12", "Physics", "Wave interference", "HS-PS4-1", "compare"),
    ("11-12", "Physics", "Standing waves on a string", "HS-PS4-1", "trace"),
    ("11-12", "Physics", "The Doppler effect", "HS-PS4-1", "compare"),
    ("11-12", "Physics", "The photoelectric effect", "HS-PS4-3", "process"),
    ("11-12", "Physics", "Convex lens ray diagram", "HS-PS4-5", "build"),
    ("11-12", "Physics", "Concave mirror ray diagram", "HS-PS4-5", "build"),
    # ---- High school Earth and space science (often grade 9) ----
    ("9", "Earth & Space", "Layers of the sun", "HS-ESS1-1", "trace"),
    ("9", "Earth & Space", "Hertzsprung-Russell diagram", "HS-ESS1-1", "graph"),
    ("9", "Earth & Space", "Big Bang evidence: redshift", "HS-ESS1-2", "compare"),
    ("9", "Earth & Space", "Life cycle of stars", "HS-ESS1-3", "process"),
    ("9", "Earth & Space", "Kepler's elliptical orbits", "HS-ESS1-4", "trace"),
    ("9", "Earth & Space", "Earth's interior layers", "HS-ESS2-1", "trace"),
    ("9", "Earth & Space", "Subduction zone cross-section", "HS-ESS2-3", "trace"),
    ("9", "Earth & Space", "Layers of the atmosphere", "HS-ESS2-4", "trace"),
    ("9", "Earth & Space", "Groundwater and the water table", "HS-ESS2-5", "trace"),
    ("9", "Earth & Space", "Ocean conveyor belt circulation", "HS-ESS2-6", "trace"),
    ("9", "Earth & Space", "Ice-albedo climate feedback", "HS-ESS3-6", "process"),
    ("9", "Earth & Space", "Seismic waves and the shadow zone", "HS-ESS2-1", "trace"),
]

# ---- Undergraduate ----
# Mapped to a section of an OpenStax textbook (free, peer-reviewed, CC BY, so their art can be
# adapted with credit) and, where it applies, an MCAT content category (AAMC outline). Both are
# checked below against the saved tables of contents in curriculum/sources.
# (subject, diagram, book, section, MCAT category or None, interaction)
UG = [
    # Cell and molecular biology
    ("Life", "Prokaryotic cell structure", "Biology 2e", "4.2", "2B", "trace"),
    ("Life", "Eukaryotic animal cell, organelle by organelle", "Biology 2e", "4.3", "2A", "trace"),
    ("Life", "The endomembrane system: ER to Golgi to membrane", "Biology 2e", "4.4", "2A", "process"),
    ("Life", "The cytoskeleton: three kinds of fibers", "Biology 2e", "4.5", "2A", "compare"),
    ("Life", "Cell junctions: tight, gap and desmosome", "Biology 2e", "4.6", "2A", "compare"),
    ("Life", "Fluid mosaic model of the plasma membrane", "Biology 2e", "5.1", "2A", "trace"),
    ("Life", "Passive transport: diffusion, channels and carriers", "Biology 2e", "5.2", "2A", "compare"),
    ("Life", "The sodium-potassium pump cycle", "Biology 2e", "5.3", "2A", "process"),
    ("Life", "Endocytosis and exocytosis", "Biology 2e", "5.4", "2A", "process"),
    ("Life", "Cell signaling: a G-protein-coupled receptor", "Biology 2e", "9.2", "3A", "process"),
    ("Life", "Cell signaling: a receptor tyrosine kinase cascade", "Biology 2e", "9.2", "3A", "process"),
    ("Life", "Cell cycle checkpoints and cyclins", "Biology 2e", "10.3", "2C", "process"),
    ("Life", "Meiosis I and II with crossing over", "Biology 2e", "11.1", "1C", "process"),
    ("Life", "Gene linkage and recombination frequency", "Biology 2e", "13.1", "1C", "compare"),
    ("Life", "Nondisjunction in meiosis", "Biology 2e", "13.2", "1C", "process"),
    ("Life", "DNA structure: antiparallel strands and base pairing", "Biology 2e", "14.2", "1B", "build"),
    ("Life", "The DNA replication fork", "Biology 2e", "14.3", "1B", "trace"),
    ("Life", "Eukaryotic transcription", "Biology 2e", "15.3", "1B", "process"),
    ("Life", "mRNA processing: cap, tail and splicing", "Biology 2e", "15.4", "1B", "process"),
    ("Life", "Translation at the ribosome", "Biology 2e", "15.5", "1B", "process"),
    ("Life", "The lac operon", "Biology 2e", "16.2", "1B", "compare"),
    ("Life", "Chromatin and epigenetic regulation", "Biology 2e", "16.3", "1B", "compare"),
    ("Life", "The PCR cycle", "Biology 2e", "17.1", "1B", "process"),
    ("Life", "Gel electrophoresis", "Biology 2e", "17.1", "5C", "trace"),
    ("Life", "Stabilizing, directional and disruptive selection", "Biology 2e", "19.3", "1C", "graph"),
    ("Life", "Reading a phylogenetic tree", "Biology 2e", "20.2", None, "compare"),
    ("Life", "Viral replication: lytic and lysogenic cycles", "Biology 2e", "21.2", "2B", "process"),
    ("Life", "Stem cross-section: xylem and phloem", "Biology 2e", "30.2", None, "trace"),
    ("Life", "Root cross-section: endodermis and Casparian strip", "Biology 2e", "30.3", None, "trace"),
    ("Life", "Double fertilization in flowering plants", "Biology 2e", "32.2", None, "process"),
    ("Life", "Human eye anatomy", "Biology 2e", "36.5", "6A", "trace"),
    ("Life", "Human ear anatomy", "Biology 2e", "36.4", "6A", "trace"),
    # Biochemistry and metabolism
    ("Biochemistry", "ATP structure and hydrolysis", "Biology 2e", "6.4", "1D", "build"),
    ("Biochemistry", "Enzyme energy diagram: with and without a catalyst", "Biology 2e", "6.5", "1A", "graph"),
    ("Biochemistry", "Competitive and noncompetitive inhibition", "Biology 2e", "6.5", "1A", "compare"),
    ("Biochemistry", "Glycolysis overview", "Biology 2e", "7.2", "1D", "process"),
    ("Biochemistry", "The citric acid cycle", "Biology 2e", "7.3", "1D", "process"),
    ("Biochemistry", "Electron transport chain and ATP synthase", "Biology 2e", "7.4", "1D", "trace"),
    ("Biochemistry", "Fermentation: lactic acid and alcohol", "Biology 2e", "7.5", "1D", "compare"),
    ("Biochemistry", "Light-dependent reactions: the Z-scheme", "Biology 2e", "8.2", None, "process"),
    ("Biochemistry", "The Calvin cycle", "Biology 2e", "8.3", None, "process"),
    ("Biochemistry", "Amino acid charge at different pH", "Organic Chemistry", "26.2", "1A", "build"),
    ("Biochemistry", "Four levels of protein structure", "Organic Chemistry", "26.9", "1A", "compare"),
    ("Biochemistry", "Nucleotides and the phosphodiester bond", "Organic Chemistry", "28.1", "1B", "build"),
    ("Biochemistry", "Beta-oxidation of fatty acids", "Organic Chemistry", "29.3", "1D", "process"),
    ("Biochemistry", "Gluconeogenesis and glycolysis compared", "Organic Chemistry", "29.8", "1D", "compare"),
    # Anatomy and physiology
    ("Anatomy & Physiology", "Layers of the skin", "Anatomy and Physiology 2e", "5.1", "3B", "trace"),
    ("Anatomy & Physiology", "Long bone and the osteon", "Anatomy and Physiology 2e", "6.3", "3B", "trace"),
    ("Anatomy & Physiology", "A synovial joint", "Anatomy and Physiology 2e", "9.4", "3B", "trace"),
    ("Anatomy & Physiology", "The neuromuscular junction", "Anatomy and Physiology 2e", "10.2", "3B", "trace"),
    ("Anatomy & Physiology", "The sarcomere and sliding filaments", "Anatomy and Physiology 2e", "10.3", "3B", "compare"),
    ("Anatomy & Physiology", "The action potential", "Anatomy and Physiology 2e", "12.4", "3A", "graph"),
    ("Anatomy & Physiology", "Synaptic transmission", "Anatomy and Physiology 2e", "12.5", "3A", "process"),
    ("Anatomy & Physiology", "Regions of the brain", "Anatomy and Physiology 2e", "13.2", "3A", "trace"),
    ("Anatomy & Physiology", "The spinal reflex arc", "Anatomy and Physiology 2e", "14.3", "3A", "process"),
    ("Anatomy & Physiology", "The hypothalamus-pituitary axis", "Anatomy and Physiology 2e", "17.3", "3A", "process"),
    ("Anatomy & Physiology", "Blood glucose regulation by insulin and glucagon", "Anatomy and Physiology 2e", "17.9", "3A", "process"),
    ("Anatomy & Physiology", "Formed elements of the blood", "Anatomy and Physiology 2e", "18.2", "3B", "compare"),
    ("Anatomy & Physiology", "ABO blood types", "Anatomy and Physiology 2e", "18.6", "3B", "compare"),
    ("Anatomy & Physiology", "Heart chambers, valves and great vessels", "Anatomy and Physiology 2e", "19.1", "3B", "trace"),
    ("Anatomy & Physiology", "The cardiac conduction system", "Anatomy and Physiology 2e", "19.2", "3B", "trace"),
    ("Anatomy & Physiology", "The cardiac cycle: pressures and volumes", "Anatomy and Physiology 2e", "19.3", "3B", "graph"),
    ("Anatomy & Physiology", "Capillary exchange", "Anatomy and Physiology 2e", "20.3", "4B", "process"),
    ("Anatomy & Physiology", "The lymphatic system", "Anatomy and Physiology 2e", "21.1", "3B", "trace"),
    ("Anatomy & Physiology", "Antibody structure", "Anatomy and Physiology 2e", "21.4", "3B", "trace"),
    ("Anatomy & Physiology", "The respiratory tree and the alveolus", "Anatomy and Physiology 2e", "22.1", "3B", "trace"),
    ("Anatomy & Physiology", "The oxygen-hemoglobin dissociation curve", "Anatomy and Physiology 2e", "22.5", "4B", "graph"),
    ("Anatomy & Physiology", "The digestive tract", "Anatomy and Physiology 2e", "23.1", "3B", "trace"),
    ("Anatomy & Physiology", "A villus of the small intestine", "Anatomy and Physiology 2e", "23.5", "3B", "trace"),
    ("Anatomy & Physiology", "The nephron and its blood supply", "Anatomy and Physiology 2e", "25.4", "3B", "trace"),
    ("Anatomy & Physiology", "Reabsorption along the nephron", "Anatomy and Physiology 2e", "25.6", "3B", "process"),
    ("Anatomy & Physiology", "Spermatogenesis in the seminiferous tubule", "Anatomy and Physiology 2e", "27.1", "2C", "trace"),
    ("Anatomy & Physiology", "The ovarian and uterine cycles", "Anatomy and Physiology 2e", "27.2", "3B", "graph"),
    ("Anatomy & Physiology", "Fertilization to blastocyst", "Anatomy and Physiology 2e", "28.2", "2C", "process"),
    # Microbiology
    ("Microbiology", "Parts of a light microscope", "Microbiology", "2.3", None, "trace"),
    ("Microbiology", "The Gram stain, step by step", "Microbiology", "2.4", "2B", "process"),
    ("Microbiology", "Gram-positive and gram-negative cell walls", "Microbiology", "3.3", "2B", "compare"),
    ("Microbiology", "Enveloped and naked viruses", "Microbiology", "6.1", "2B", "compare"),
    ("Microbiology", "The bacterial growth curve", "Microbiology", "9.1", "2B", "graph"),
    ("Microbiology", "Conjugation, transformation and transduction", "Microbiology", "11.6", "2B", "compare"),
    ("Microbiology", "Phagocytosis", "Microbiology", "17.4", "3B", "process"),
    ("Microbiology", "Inflammation", "Microbiology", "17.5", "3B", "process"),
    ("Microbiology", "Humoral and cell-mediated immunity", "Microbiology", "18.1", "3B", "compare"),
    # General chemistry
    ("Chemistry", "The Bohr model and emission lines", "Chemistry 2e", "6.2", "4E", "process"),
    ("Chemistry", "Shapes of s, p and d orbitals", "Chemistry 2e", "6.3", "4E", "trace"),
    ("Chemistry", "Orbital diagrams and electron configuration", "Chemistry 2e", "6.4", "4E", "build"),
    ("Chemistry", "Periodic trends", "Chemistry 2e", "6.5", "4E", "graph"),
    ("Chemistry", "Formal charge and resonance: carbonate", "Chemistry 2e", "7.4", "5B", "build"),
    ("Chemistry", "VSEPR molecular geometries", "Chemistry 2e", "7.6", "5B", "compare"),
    ("Chemistry", "Hybrid orbitals: sp3, sp2 and sp", "Chemistry 2e", "8.2", "5B", "compare"),
    ("Chemistry", "Molecular orbital diagram of O2", "Chemistry 2e", "8.4", "5B", "build"),
    ("Chemistry", "Intermolecular forces", "Chemistry 2e", "10.1", "5B", "compare"),
    ("Chemistry", "Phase diagram of carbon dioxide", "Chemistry 2e", "10.4", "5E", "graph"),
    ("Chemistry", "Cubic unit cells", "Chemistry 2e", "10.6", None, "trace"),
    ("Chemistry", "A two-step mechanism's energy profile", "Chemistry 2e", "12.6", "5E", "graph"),
    ("Chemistry", "Le Chatelier's principle", "Chemistry 2e", "13.3", "5E", "compare"),
    ("Chemistry", "How a buffer resists pH change", "Chemistry 2e", "14.6", "5A", "process"),
    ("Chemistry", "Weak acid titration curve and the buffer region", "Chemistry 2e", "14.7", "5A", "graph"),
    ("Chemistry", "Free energy and spontaneity", "Chemistry 2e", "16.4", "5E", "graph"),
    ("Chemistry", "An electrolytic cell", "Chemistry 2e", "17.7", "4C", "trace"),
    # Organic chemistry
    ("Organic Chemistry", "Skeletal (line-angle) structures", "Organic Chemistry", "1.12", "5D", "build"),
    ("Organic Chemistry", "Newman projections of butane", "Organic Chemistry", "3.7", "5D", "build"),
    ("Organic Chemistry", "The cyclohexane chair", "Organic Chemistry", "4.5", "5D", "build"),
    ("Organic Chemistry", "Assigning R and S", "Organic Chemistry", "5.5", "5D", "build"),
    ("Organic Chemistry", "Enantiomers and diastereomers", "Organic Chemistry", "5.6", "5D", "compare"),
    ("Organic Chemistry", "Curved arrows: HBr adding to ethylene", "Organic Chemistry", "6.5", "5D", "build"),
    ("Organic Chemistry", "Transition states and intermediates", "Organic Chemistry", "6.9", "5E", "graph"),
    ("Organic Chemistry", "Carbocation stability and Markovnikov's rule", "Organic Chemistry", "7.9", "5D", "compare"),
    ("Organic Chemistry", "The SN2 reaction", "Organic Chemistry", "11.2", "5D", "build"),
    ("Organic Chemistry", "The SN1 reaction", "Organic Chemistry", "11.4", "5D", "build"),
    ("Organic Chemistry", "The E2 reaction", "Organic Chemistry", "11.8", "5D", "build"),
    ("Organic Chemistry", "Reading an IR spectrum", "Organic Chemistry", "12.7", "4D", "graph"),
    ("Organic Chemistry", "Spin-spin splitting in 1H NMR", "Organic Chemistry", "13.6", "4D", "graph"),
    ("Organic Chemistry", "Benzene: resonance and aromaticity", "Organic Chemistry", "15.2", None, "build"),
    # Physics
    ("Physics", "Free-body diagrams with tension and friction", "University Physics Volume 1", "5.7", "4A", "build"),
    ("Physics", "Buoyancy and Archimedes' principle", "University Physics Volume 1", "14.4", "4B", "compare"),
    ("Physics", "Bernoulli's equation in a narrowing pipe", "University Physics Volume 1", "14.6", "4B", "trace"),
    ("Physics", "Energy in simple harmonic motion", "University Physics Volume 1", "15.2", "4A", "graph"),
    ("Physics", "Standing waves in open and closed pipes", "University Physics Volume 1", "17.4", "4D", "compare"),
    ("Physics", "Thermodynamic processes on a PV diagram", "University Physics Volume 2", "3.4", "5E", "graph"),
    ("Physics", "The electric dipole field", "University Physics Volume 2", "5.7", "4C", "trace"),
    ("Physics", "Kirchhoff's rules in a two-loop circuit", "University Physics Volume 2", "10.3", "4C", "build"),
    ("Physics", "Charging an RC circuit", "University Physics Volume 2", "10.5", "4C", "graph"),
    ("Physics", "A charged particle in a magnetic field", "University Physics Volume 2", "11.3", "4C", "trace"),
    ("Physics", "The electromagnetic spectrum: wavelength, frequency and energy", "University Physics Volume 2", "16.5", "4D", "compare"),
    ("Physics", "The eye: correcting near- and farsightedness", "University Physics Volume 3", "2.5", "4D", "build"),
    ("Physics", "The compound microscope", "University Physics Volume 3", "2.8", "4D", "build"),
    ("Physics", "Young's double-slit interference", "University Physics Volume 3", "3.1", "4D", "compare"),
    ("Physics", "Nuclear binding energy per nucleon", "University Physics Volume 3", "10.2", "4E", "graph"),
    ("Physics", "Radioactive decay and half-life", "University Physics Volume 3", "10.3", "4E", "graph"),
]

SOURCES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sources")


def _sections(book):
    """Section number -> title, from the table of contents saved from openstax.org."""
    path = os.path.join(SOURCES, "openstax", book.lower().replace(" ", "-") + ".toc")
    out = {}
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if line[:1].isdigit():
            num, _, title = line.partition(" ")
            out[num] = title
    return out


_mcat = {line.split(".")[0] for line in open(os.path.join(SOURCES, "mcat-content-categories.txt"), encoding="utf-8") if line.strip()}
for subject, diagram, book, section, mcat, interaction in UG:
    title = _sections(book).get(section)
    assert title, f"{diagram}: {book} has no section {section}"
    assert mcat is None or mcat in _mcat, f"{diagram}: no MCAT content category {mcat}"
    standard = f"OpenStax {book} §{section} {title}" + (f"; MCAT {mcat}" if mcat else "")
    D.append(("UG", subject, diagram, standard, interaction))

import glob
import json

# A diagram is live once a lesson with the same title ships (Swift lessons, or files in Content/Lessons).
LIVE = {"Plant cell", "Leaf cross-section", "Water: Lewis structure"} | {
    json.load(open(f))["title"]
    for f in glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Diagrama", "Content", "Lessons", "lesson-*.json"))
}

BAND = {"K": "K-2", "1": "K-2", "2": "K-2", "3": "3-5", "4": "3-5", "5": "3-5",
        "6": "Middle school", "7": "Middle school", "8": "Middle school", "UG": "Undergraduate"}


def band(grade):
    return BAND.get(grade, "High school")


here = os.path.dirname(os.path.abspath(__file__))
rows = []
for i, (grade, subject, diagram, standard, interaction) in enumerate(D, 1):
    rows.append({
        "id": f"D{i:03d}", "grade": grade, "band": band(grade), "subject": subject,
        "diagram": diagram, "standard": standard, "interaction": interaction,
        # K-2 is deferred until read-aloud audio exists: young children can't read the notes.
        "status": "live" if diagram in LIVE else ("deferred" if band(grade) == "K-2" else "planned"),
        "mapping": "proposed - needs instructor review" if grade == "UG" else "proposed - needs teacher review",
    })

titles = [r["diagram"] for r in rows]
assert len(titles) == len(set(titles)), "duplicate diagram"

with open(os.path.join(here, "coverage.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

order = ["K-2", "3-5", "Middle school", "High school", "Undergraduate"]
print(f"{len(rows)} diagrams: " + ", ".join(f"{v} {k}" for k, v in Counter(r["status"] for r in rows).items()))
for b in order:
    c = Counter(r["subject"] for r in rows if r["band"] == b)
    print(f"  {b:14} {sum(c.values()):3}  " + ", ".join(f"{k} {v}" for k, v in sorted(c.items())))
print("  by interaction:", dict(Counter(r["interaction"] for r in rows)))
