#!/bin/bash
#SBATCH --job-name=boltz-all
#SBATCH --output=/projects/bentosprg6/Ethan_Njamnshi/boltz2/boltz_logs/%x_%j.out
#SBATCH --error=/projects/bentosprg6/Ethan_Njamnshi/boltz2/boltz_logs/%x_%j.err
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --gpus-per-task=1
#SBATCH --mem=32GB
#SBATCH --time=12:00:00
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=njamnshi@bc.edu
#SBATCH --partition=short

source /m31/modules/miniconda/3/etc/profile.d/conda.sh
conda activate /projects/bentosprg6/Ethan_Njamnshi/conda/envs/boltz2

export NUMBA_CACHE_DIR=/projects/bentosprg6/Ethan_Njamnshi/boltz2/numba_cache
mkdir -p $NUMBA_CACHE_DIR

boltz predict /projects/bentosprg6/Ethan_Njamnshi/boltz2/boltz_inputs \
  --out_dir /projects/bentosprg6/Ethan_Njamnshi/boltz2/boltz_output \
  --cache /projects/bentosprg6/Ethan_Njamnshi/boltz2/weights \
  --use_msa_server
