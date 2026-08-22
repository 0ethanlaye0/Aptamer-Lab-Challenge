#!/bin/bash

INPUT_DIR="/projects/bentosprg6/Ethan_Njamnshi/alphafold3/af3_inputs"
OUTPUT_DIR="/projects/bentosprg6/Ethan_Njamnshi/alphafold3/af3_output"
MODEL_DIR="/projects/bentosprg6/Ethan_Njamnshi/alphafold3/models"
SIF="/projects/bentosprg6/Ethan_Njamnshi/alphafold3/image/alphafold3.sif"
LOGS="/projects/bentosprg6/Ethan_Njamnshi/alphafold3/af3_logs"

count=0
for json_file in $INPUT_DIR/*.json; do
    name=$(basename "$json_file" .json)
    sbatch --job-name="af3-$name" \
           --output="$LOGS/${name}_%j.out" \
           --error="$LOGS/${name}_%j.err" \
           --nodes=1 --ntasks=1 --cpus-per-task=8 \
           --gpus-per-task=1 --mem=32GB --time=01:00:00 \
           --mail-type=FAIL --mail-user=njamnshi@bc.edu \
           --partition=short \
           --wrap="export XLA_FLAGS='--xla_disable_hlo_passes=custom-kernel-fusion-rewriter'; singularity exec --nv --bind $MODEL_DIR:/root/models --bind $INPUT_DIR:/root/af_input --bind $OUTPUT_DIR:/root/af_output $SIF python /app/alphafold/run_alphafold.py --json_path=/root/af_input/$(basename $json_file) --model_dir=/root/models --output_dir=/root/af_output --flash_attention_implementation=xla --run_data_pipeline=false --run_inference=true"
    count=$((count + 1))
    if [ $count -ge 88 ]; then
        break
    fi
done
echo "Submitted $count jobs"
