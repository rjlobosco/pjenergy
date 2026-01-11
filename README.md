
![alt text](/tutorials/images/Pasted%20image%2020250308162026.png)

# Pjenergy

**Pjenergy** is a research project focused on the quantification and characterization of offshore wind energy potential in the Campos Basin, with particular emphasis on areas currently occupied by oil and gas platforms undergoing decommissioning. The project aims to provide scientifically robust support for the assessment of repurposing strategies and the potential deployment of offshore wind turbines, contributing to energy transition pathways in mature offshore basins.

The analysis is based on reanalysis data obtained from [Climate Data Store (CDS)](https://cds.climate.copernicus.eu/), a European repository of climate and atmospheric data. Specifically, the project employs the dataset:

ERA5 hourly data on pressure levels from 1940 to present (https://cds.climate.copernicus.eu/datasets/reanalysis-era5-pressure-levels?tab=overview)

ERA5 provides hourly, physically consistent atmospheric fields derived from the assimilation of in situ and remote-sensing observations into a global numerical weather prediction model.

For the present study, a total of 250 variable–level–time combinations were extracted, comprising:

**Five atmospheric variables**: zonal wind component (u), meridional wind component (v), relative humidity, air temperature, and geopotential height;

**Five pressure levels**: 900, 925, 950, 975, and 1000 hPa, representing the lower troposphere relevant for offshore wind resource assessment and vertical wind extrapolation;

**A 10-year period (2015–2024)**, ensuring statistical robustness while capturing interannual variability.

All datasets provide complete temporal coverage, including all days of the year with hourly temporal resolution, enabling detailed analyses of wind climatology, variability, extreme events, and derived quantities such as wind speed, wind direction, shear profiles, and energy density.


---


## Prerequisites

- [Anaconda](https://anaconda.org/anaconda/anaconda-navigator): Includes Conda, a package and environment manager that facilitates package installation, the creation of isolated environments (thus avoiding dependency conflicts) and, most importantly, enables smooth sharing of environment configurations among team members.

- [Git](https://git-scm.com/downloads): For using and contributing to the code.

- An account on the [Climate Data Store](https://cds.climate.copernicus.eu/): The platform from which the datasets used are retrieved. This step is optional, since the required datasets are already included in the repository.



---


Getting Started

1 - Clone the repository

While in the directory where you want to clone the project, type in the terminal:

    git clone https://github.com/cff100/pjenergy.git

2 - Install the project locally

This makes the project usable as a package (essential for imports) and ensures the installation of dependencies in a virtual environment with standardized settings.

Create the virtual environment with:

    conda env create -f environment.yml

And activate it:

    conda activate pjenergy

The installed packages are organized in the environment file.

When necessary: Whenever you or someone else working on the project makes changes to this file, an update is required if you want to stay up to date with the changes. To do so, use:

    conda env update -f environment.yml


### 3 - (Optional) Save the personal token to retrieve data from the Climate Data Store API

This step is intended to keep the code generic, avoiding the use of a single person’s account to retrieve the datasets.

After registering an account on the CDS, simply go to the [CDSAPI setup](https://cds.climate.copernicus.eu/how-to-api) page and copy the code containing the *url* and *key*.

Now create a file in your **user home directory** named `.cdsapirc` (for example, using the command below) and paste the url and key into it.

    notepad $env:USERPROFILE\.cdsapirc


**OBS.:** As expected, the .cdsapirc file will not be pushed to GitHub.


---


## Data Acquisition

Since this is an extremely computationally expensive process, the datasets were obtained via the CDS API and stored in the [NetCDF data folder](data/datasets/originais) of the repository. Nevertheless, the structure required to obtain these data is included in the repository for eventual use. The parameters used are defined in the `ParametrosObtencaoDados` class ([in this file](src/config/constants.py)), which centralizes and organizes the combinations required for data retrieval.

The process takes several tens of hours; however, the code structure was designed using a file-naming pattern that allows the download process to be interrupted and resumed as many times as necessary, without having to restart the acquisition from the beginning. The main function responsible for data acquisition is available [here](src/main/obtem_datasets_originais.py).

Using the same function, it is also possible to retrieve a single dataset with a user-selected combination of variable, year, and pressure level. This type of usage can be tested with [this test file](tests/tests_geracoes/test_requisicao_dados_nc.py). Simply run:


    pytest -s .\tests\tests_geracoes\test_requisicao_dados_nc.py

---

Data Assembly (UNDER DEVELOPMENT...)

This stage involves several sub-steps, including merging the obtained datasets, editing and mapping them to platform coordinates, and generating the corresponding dataframes.

The main function for this stage is available [here](src/main/montagem_dados.py).

Expected Folder Structure (dynamically generated)

- **Merged dataset**: Location of the dataset formed by merging the datasets obtained from the CDS.

- **Specific-coordinate datasets**
    - **Platform datasets**: Datasets specific to the coordinates of each studied platform.
    - **Non-platform point datasets**: Dataset for any other coordinate of interest.

- **Specific-coordinate dataframes**
    - **Platform dataframes**: Dask dataframes specific to the coordinates of each studied platform.
    - **Non-platform point dataframes**: Dask dataframe for any other coordinate of interest.


Design Decisions

Several technical decisions were made to balance performance, readability, and scalability. Some of the main choices are outlined below:

Why Dask?

The data volume involved in the project (hourly data, 10 years, 250 variable combinations) is large enough to make the use of pandas inefficient or even infeasible on standard machines. Dask allows the manipulation of datasets larger than the available RAM by splitting them into multiple partitions.

Why Parquet?

The Parquet format was chosen because:

    It is a columnar and compressed format, efficient for selective reads.
    It is highly compatible with Dask, optimizing read/write performance.
    It significantly reduces storage usage compared to CSV, despite the drawback of not being directly human-readable.
        However, this limitation can be easily mitigated by using Parquet file visualization tools or by converting the data, partially or entirely, to other formats such as CSV whenever necessary.

