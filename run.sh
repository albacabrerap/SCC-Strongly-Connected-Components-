#!/bin/bash
set -e

echo "Compilando C++..."
g++ -O3 -std=c++17 algorithm/tarjan.cpp -o algorithm/tarjan

echo "Generando traza JSON..."
mkdir -p output/parts
./algorithm/tarjan > output/traza.json

echo "Renderizando Título..."
manim -qh animation/scene_00_title.py S00Title
mv media/videos/scene_00_title/1080p60/S00Title.mp4 output/parts/scene_00_title.mp4

echo "Renderizando Concepto..."
manim -qh animation/scene_01_concept.py S01Concept
mv media/videos/scene_01_concept/1080p60/S01Concept.mp4 output/parts/scene_01_concept.mp4

echo "Renderizando Demo..."
manim -qh animation/scene_02_demo.py S02Demo
mv media/videos/scene_02_demo/1080p60/S02Demo.mp4 output/parts/scene_02_demo.mp4

echo "Uniendo videos..."
cd output/parts
# Aquí corregimos los nombres para que coincidan con los de arriba
echo "file 'scene_00_title.mp4'" > lista.txt
echo "file 'scene_01_concept.mp4'" >> lista.txt
echo "file 'scene_02_demo.mp4'" >> lista.txt

ffmpeg -y -f concat -safe 0 -i lista.txt -c copy ../final.mp4

echo "¡Listo! El video final está en output/final.mp4"