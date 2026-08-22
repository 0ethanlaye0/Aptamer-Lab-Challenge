# Aptamer Lab Report

## Approach and Workflow

- For each of the models, I read through the repos and tried to follow steps on installation, set-up and running.
- Whenever I ran into an issue I could not fix on my own, I first tried finding a solution online, then resorted to claude AI if I still found myself stuck.
- Claude AI was used mainly to generate scripts for SLURM, data fetching, and file creation.
- Claude AI, also helped by providing useful shell commands to navigate the cluster quickly, create necessary environments, and edit code files.
- After both models were tested and run on their respective input files (created from the database using AI-generated scripts), their outputs were recorded then the results were extracted and recorded on spreadsheets for each of the models with the help of other scripts made for this purpose.
- Finally another script was used to access these spreadsheets and calculate the spearman correlation for each model

## Technical Challenges

### Singularity Container Issues
- I could not find a singularity container to run Alphafold3 that worked for the examples(json 4 files). As a result, I tried running Alphafold3 without one by installing every dependency needed which resulted in a lot of errors.
- I modified one of the examples by changing the json version from 4 to 1 and took out the "description" metric in order to force it to work with a container which solved the issue.

### Database Issue
- The MSA database needed to run Alphafold 3 was too large so when generating the slurm scripts I found out through Claude AI that installing the database can be skipped. However, running alphafold without MSA raised errors for missing metrics.
- I added "pairedMSA", "unpairedMSA", and "templates" metrics in the input files before it would run properly without the database.

### Boltz-2 aptamer affinity prediction
- Trying to modify the code for Boltz to produce affinity predictions for aptamer complexes was the hardest challenge I faced. I was able to locate where the code that restricted DNA/RNA aptamers from getting an affinity prediction was with one of the shell commands Claude AI provided but had trouble modifying it myself.
- I passed the code section into Claude AI and explained what I intended to do and it provided the correct changes that allowed them to get an affinity prediction.
- Due to how messy things were getting from this, I decided to skip the bonus section in order to avoid messing with code too much.

## Affinity Analysis

- Alphafold3 showed weak but statistically significant negative correlation between iPTM and Kd(r = -.26, p = 0.02).
- Boltz2 did not show a significant correlation (r = -0.05, p = 0.67), probably because the affinity module is not designed to work with aptamer-protein complexes.
- These results were greatly influenced by choices I made due to limitations I faced.

## Limitations

- The UTexas Dataset was hard to deal with because many of the aptamer sequences provided raised some errors and the target(protein) sequences were also not provided.
- The script I used to make some of these complexes usable by the models shrunk the dataset down to 80 inputs. This is because only those with working aptamer sequences that were binded with proteins found on 'Uniprot' were used as inputs for the models.
- Another limitation was that the 'Uniprot' search for some targets which were NOT proteins still returned a sequence, resulting in 'valid' input files being created for them..

## Next Steps

- It would be better to use a more fitting dataset for these models that contains all the necessary information in order to ensure smooth running and predictions.
- Given enough space and time, I would run the models on well organized data with databases fully in use in order to use the models to their fullest potential.
