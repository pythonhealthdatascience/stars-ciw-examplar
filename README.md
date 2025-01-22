[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/pythonhealthdatascience/stars-ciw-examplar/HEAD)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10051494.svg)](https://doi.org/10.5281/zenodo.10051494)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Read the Docs](https://readthedocs.org/projects/pip/badge/?version=latest)](https://pythonhealthdatascience.github.io/stars-ciw-examplar/)
[![ORCID: Harper](https://img.shields.io/badge/ORCID-0000--0001--5274--5037-brightgreen)](https://orcid.org/0000-0001-5274-5037)
[![ORCID: Monks](https://img.shields.io/badge/ORCID-0000--0003--2631--4481-brightgreen)](https://orcid.org/0000-0003-2631-4481)
[![ORCID: Heather](https://img.shields.io/badge/ORCID-0000--0002--6596--3479-brightgreen)](https://orcid.org/0000-0002-6596-3479)

#   Towards Sharing Tools and Artefacts for Reusable Simulation: a `ciw` model example

## Overview

The materials and methods in this repository support work towards developing the S.T.A.R.S healthcare framework (**S**haring **T**ools and **A**rtefacts for **R**eusable **S**imulations in healthcare).  The code and written materials here demonstrate the application of S.T.A.R.S' version 1 to sharing a `ciw` discrete-event simuilation model and associated research artefacts.  

* All artefacts in this repository are linked to study researchers via ORCIDs;
* Model code is made available under a GNU Public License version 3;
* Python dependencies are managed through `conda`;
* The code builds a Shiny for Python web application that can be used to run the model (web app);
* The python code itself can be viewed and executed in Jupyter notebooks via [Binder](https://mybinder.org); 
* The model is documented and explained in a quarto website served up by GitHub pages;
* The materials are deposited and made citatable using Zenodo;
* The models are sharable with other researchers and the NHS without the need to install software.

## Author ORCIDs

[![ORCID: Harper](https://img.shields.io/badge/ORCID-0000--0001--5274--5037-brightgreen)](https://orcid.org/0000-0001-5274-5037)
[![ORCID: Monks](https://img.shields.io/badge/ORCID-0000--0003--2631--4481-brightgreen)](https://orcid.org/0000-0003-2631-4481)
[![ORCID: Heather](https://img.shields.io/badge/ORCID-0000--0002--6596--3479-brightgreen)](https://orcid.org/0000-0002-6596-3479)

## Citation

> Monks, T., Harper, A., & Heather, A. (2023). Towards Sharing Tools, Artefacts, and Reproducible Simulation: a ciw model example (v1.0.1). Zenodo. https://doi.org/10.5281/zenodo.10051494

```bibtex
@software{monks_2023_10051495,
  author       = {Monks, Thomas and
                  Harper, Alison and
                  Heather, Amy},
  title        = {{Towards Sharing Tools, Artefacts, and Reproducible 
                   Simulation: a ciw model example}},
  month        = oct,
  year         = 2023,
  publisher    = {Zenodo},
  version      = {v1.0.1},
  url	       = {https://doi.org/10.5281/zenodo.10051494},
  doi          = {10.5281/zenodo.100514954},
}
```

## Funding

This code is part of independent research supported by the National Institute for Health Research Applied Research Collaboration South West Peninsula. The views expressed in this publication are those of the author(s) and not necessarily those of the National Institute for Health Research or the Department of Health and Social Care.

## Case study model

We reuse a stylised urgent care call centre model that we have [previously published](https://openresearch.nihr.ac.uk/articles/3-48). In the model a caller with urgent care needs arrives at randomly to a call centre. The centre is staffed by call operators who answer calls from a first in first out queue. Patients are triaged, and provided a call designation; for example, whether the patient should be allocated an appointment in primary care with a General Practitioner (family doctor) within 48 hours, or if a call back from a nurse is needed.  Callers that are designated as needing a nurse callback enter a first in first out queue until a nurse is available. 

## Shiny web app

The `ciw` model has been given a Shiny for Python interface.  This allows users to easily experiment with the simulation model.  The web app is hosted on a free tier of shinyapps.io.  The app can be access at <https://pythonhealthdatascience.shinyapps.io/stars-ciw-examplar>.

> This is a free service. If the app has not been used for a while it will be "asleep" to save resources. Please be patient while the app "wakes up".  This will be a short time.

🎉 This app has been adapted by [Sammi Rosser](https://github.com/Bergam0t) to incorporate an animation of the model created using the [vidigi](https://github.com/Bergam0t/vidigi) package. Check it our in her repository: <https://github.com/Bergam0t/ciw-example-animation>

## Online Notebooks via Binder

The python code for the model has been setup to run online in Jupyter notebooks via binder [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/pythonhealthdatascience/stars-ciw-examplar/HEAD)

> Binder is a free service.  If it has not been used in a while Binder will need to re-containerise the code repository, and push to binderhub. This will take several minutes. After that the online environment will be quick to load.

## Online documentation produced by Quarto

[![Read the Docs](https://readthedocs.org/projects/pip/badge/?version=latest)](https://pythonhealthdatascience.github.io/stars-ciw-example/)

* Visit our [quarto website](https://pythonhealthdatascience.github.io/stars-ciw-example/) for detailed overview of the project, and code: https://pythonhealthdatascience.github.io/stars-ciw-example

## How to run the model locally

Alternatively you may wish to run the Shiny App locally on your own machine.  

### Downloading the code

Either clone the repository using git or click on the green "code" button and select "Download Zip".

```bash
git clone https://github.com/pythonhealthdatascience/stars-ciw-example
```

### Installing dependencies

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/)

All dependencies can be found in [`binder/environment.yml`]() and are pulled from conda-forge.  To run the code locally, we recommend install [mini-conda](https://docs.conda.io/en/latest/miniconda.html); navigating your terminal (or cmd prompt) to the directory containing the repo and issuing the following command:

```bash
conda env create -f binder/environment.yml
```

To activate the environment issue the following command:

```bash
conda activate stars_pyshiny`
```

### Launching the Shiny Interface

In the directory (folder) containing the code issue the following command via the terminal (or cmd prompt/powershell on windows)

```bash
shiny run app.py
```

The app will run locally on port 8000 and can be accessed using the following URL

```
http://127.0.0.1:8000
```

