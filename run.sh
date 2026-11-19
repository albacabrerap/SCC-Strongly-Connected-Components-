#!/bin/bash
set -e

echo "Compilando C++..."
g++ -O3 -std=c++17 algorithm/tarjan.cpp -o algorithm/tarjan

echo "Generando trazas JSON..."
mkdir -p output/parts
./algorithm/tarjan inputs/demo.txt     > output/traza.json
./algorithm/tarjan inputs/mini.txt     > output/traza_mini.json
./algorithm/tarjan inputs/empty.txt    > output/traza_empty.json
./algorithm/tarjan inputs/single.txt   > output/traza_single.json
./algorithm/tarjan inputs/dag.txt      > output/traza_dag.json
./algorithm/tarjan inputs/complete.txt > output/traza_complete.json

SCENES=(
  "scene_00_title S00Title"
  "scene_01_motivation S01Motivation"
  "scene_02_concept S02Concept"
  "scene_03_algorithm S03Algorithm"
  "scene_04_demo S04Demo"
  "scene_05_edgecases S05EdgeCases"
  "scene_06_complexity S06Complexity"
  "scene_07_credits S07Credits"
)

: > output/parts/lista.txt
for item in "${SCENES[@]}"; do
  read -r file cls <<< "$item"
  echo "Renderizando $cls..."
  manim -qh animation/$file.py $cls
  mv media/videos/$file/1080p60/$cls.mp4 output/parts/$file.mp4
  echo "file '$file.mp4'" >> output/parts/lista.txt
done

echo "Uniendo videos..."
(cd output/parts && ffmpeg -y -f concat -safe 0 -i lista.txt -c copy ../final.mp4)

dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 output/final.mp4)
echo "Duración total: ${dur}s"
awk -v d="$dur" 'BEGIN { if (d > 300) print "AVISO: excede 5 minutos"; else print "OK: dentro del límite de 5 minutos" }'
echo "¡Listo! output/final.mp4"