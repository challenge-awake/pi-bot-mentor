const steps = [
  "Étape 1 : Ouvre PowerShell.",
  "Étape 2 : Tape 'cd Documents'",
  "Étape 3 : Crée un nouveau projet avec 'npm create vite@latest'",
  "Étape 4 : Installe Git si ce n'est pas fait",
  "Étape 5 : Connecte-toi à GitHub"
];

let currentStep = -1;
const stepElement = document.getElementById('step');
const nextBtn = document.getElementById('nextBtn');

nextBtn.addEventListener('click', () => {
  currentStep++;
  if (currentStep >= steps.length) {
    stepElement.innerHTML = "<p style='color:#A0E7A5'>🎉 Félicitations ! Tu es prêt à coder sur Pi Network.</p>";
    nextBtn.textContent = "✅ Terminé";
    nextBtn.disabled = true;
  } else {
    stepElement.innerHTML = `<p>${steps[currentStep]}</p>`;
    nextBtn.textContent = "➡️ Suivant";
  }
});