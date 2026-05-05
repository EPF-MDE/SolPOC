# Experiment Scheduler

## What is it?

This project is an experiment management tool built around the SolPOC optical optimization library.

It is composed of two main components:

* an Interface used to configure and generate experiment plans,
* a Scheduler responsible for automatically executing the experiments.

The interface generates structured JSON experiment files containing all required simulation and optimization parameters.
The scheduler then reads these files, launches the corresponding SolPOC experiments, manages multiprocessing execution, and organizes the generated outputs.

The tool is designed to simplify large-scale optical optimization campaigns and improve:

* automation,
* reproducibility,
* experiment management,
* result organization.

The scheduler supports several SolPOC workflows, including:

* anti-reflective coatings,
* low-emissivity coatings,
* spectral splitting,
* selective coatings,
* Bragg mirrors,
* fitting experimental optical signals,
* material optimization studies.

---

## How to use

### 1. Create an experiment plan

The interface is used to generate a JSON experiment file containing:

* optical stack definitions,
* optimization parameters,
* algorithms,
* cost functions,
* execution priorities,
* scheduler settings.

Example:

```txt id="4vg31j"
plan_test.json
```

---

### 2. Launch the scheduler

Run the scheduler script:

```bash id="84h7t8"
python projet_test.py
```

The scheduler will:

1. read the experiment plan,
2. select pending experiments according to their priority,
3. launch the optimization processes,
4. save generated outputs,
5. continue until all experiments are completed.

---

### 3. Retrieve generated results

All generated experiment outputs are automatically grouped inside the `runs/` directory.

Example:

```txt id="q2kq1u"
runs/
├── 2026-05-05_11h50m43s/
│   ├── row0_priority3/
│   ├── row1_priority1/
│   ├── row2_priority1/
│   ├── row3_priority2/
│   ├── row4_priority2/
│   └── row5_priority1/
│
└── 2026-05-05_11h57m26s/
    ├── row0_priority3/
    ├── row1_priority1/
    ├── row2_priority1/
    ├── row3_priority2/
    ├── row4_priority2/
    └── row5_priority1/
```

Each experiment folder may contain:

* optimization results,
* convergence plots,
* optical response plots,
* stack visualizations,
* generated text reports.

Failed experiments are automatically stored inside:

```txt id="o6y6yb"
failed_experiments.json
```

---

## Scheduler

The scheduler is responsible for executing experiment campaigns automatically from a JSON experiment plan. 

Main features:

* priority-based experiment execution,
* automatic parameter construction,
* multiprocessing support,
* automatic result generation,
* structured experiment storage,
* failed experiment logging.

The scheduler dynamically converts JSON fields into SolPOC-compatible objects such as:

* optimization algorithms,
* cost functions,
* material stacks,
* wavelength domains,
* optical parameters. 

The execution workflow includes:

1. experiment selection,
2. parameter preparation,
3. optimization execution,
4. result aggregation,
5. automatic plot and report generation.

Generated outputs are automatically organized into global `runs/` directories for easier experiment management and reproducibility.

---

## Interface

To be completed by the Interface team.

