#!/bin/bash

<< CpuDoc
  Output all necessary information
  about CPU for default PC user in
  txt-file.
CpuDoc


cpu_info=(
  "Model name" "CPU(s)" "CPU MHz"
  "L1d cache" "L1i cache" "L2 cache"
  "L3 cache" "Architecture"
)

file_cpu_info="cpu.txt"
touch $file_cpu_info

for element in "${cpu_info[@]}"
do
  command="$(lscpu | grep "$element" --max-count=1)"
  echo "$command" >> $file_cpu_info
done