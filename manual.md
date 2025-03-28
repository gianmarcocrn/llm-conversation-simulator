## Hardware Requirements
Although there is no specific hardware requirement to run the conversation simulator and LLM-as-a-judge pipeline, a laptoop with at least 16GB of RAM will be necessary to run models that will generate good-quality output.

## Installation and Setup
- Install Conda or Miniconda
- Clone the Git repository
- Create a new Conda environment with all project dependencies running `conda env create -f environment.yml`
- Install LMStudio from https://lmstudio.ai/

## Supported LLMs
- All LLMs supported by LMStudio and by the hardware being used are supported by this project
- Go to the LMStudio client and download the models you'd like to use

## Configuring the Platform
In order to edit the configuration of the simulator, head to the config.py file. Here you can change:
  - The filename that the simulator will use to output simulated conversations
  - The directory that the simulator will use to save conversation history files
  - The directory where persona characteristics will be saved when generated automatically
  - The directory where evaluation reports should be saved
  - Whether the evaluation pipeline should be run on the same model as generation (advised to keep as false to avoid LLM self-preference bias)
  - Whether personas should be generated automatically by the simulator (If set to false, persona characteristics should be specified following the format of the example ones provided in the config file)
  - Whether the conversation topic should be chosen at random from the IBM Project Debater dataset (If set to false, a conversation topic can be defined like the example one provided in the config file)
  - Whether the number of turns of the generated conversations should be fixed or variable
  - The number of fixed or minimum and maximum conversation turns (for variable)

## Running the Conversation Simulator
In order to run the conversation simulator the following scripts from the scripts folder can be run:
- `app_run.bash` to run a single conversation simulation (handles model loading and unloading)
- `app_run_no_load.bash` to run a single conversation simulation (does not handle model loading and unloading) - mainly to be run by batch run script
- `app_run_in_batch.bash` to run any number of conversation simulations with automatic persona generation and random topics from the IBM Project Debater Dataset (handles model loading and unloading)
- `cleanup.bash` to unload all LMStudio models from memory and stop the LMStudio server

## Running the LLM-as-a-judge Pipeline
- `eval_run.bash` runs an LLM-as-a-judge evaluation on a given conversation and persona (handles model loading and unloading)
- `eval_run_no_load.bash` is the same as above but without handling model loading and unloading - mainly to be run by batch eval scripts
- `eval_run_full_directory.bash` runs LLM-as-a-judge evaluations on all conversations and personas in given folders (handles model loading and unloading)
- `eval_run_full_directory_no_load.bash` same as above but without handling model loading and unloading
