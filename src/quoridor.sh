#!/bin/bash
strategie0=0
strategie1=1
compteur0=0
compteur1=0

for i in {1..100}; do
    if python3 main.py $strategie0 $strategie1; then
        ((compteur0++))
    else
        ((compteur1++))
    fi
done 

echo "Le joueur 0 a gagné $compteur0 fois et le joueur 1 $compteur1 fois."
if [ $compteur0 -ne 0 ]; then
    pourcentage=$(echo "scale=2; $compteur1/100*100" | bc)
    echo "Le pourcentage est de $pourcentage %."
else
    echo "Le pourcentage est de 100%"
fi