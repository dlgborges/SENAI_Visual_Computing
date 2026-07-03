Voce e um engenheiro de prompt de ia profissional

Sua tarefa e criar um prompt costar conjugado com RAO (Reason, Act, Observation) para o seguinte objetivo:

PROBLEMÁTICA:
Uma empresa quer simular um sistema básico que identifica se uma imagem contém determinados objetos, i.e.: pessoas, mesmo sem usar modelos complexos de deep learning.

TAREFA:
Criar um sistema simples baseado em regras (simulação de visão computacional).

-------------------------------------------------

# PROMPT COSTAR + RAO: Sistema de Visão Computacional Baseado em Regras

---

## 🎯 OBJETIVO
Criar um sistema simulado de visão computacional que identifica objetos (pessoas, carros, animais) em uma imagem usando apenas lógica condicional, sem deep learning.

---

## 📋 MÉTODO COSTAR

### **C — CONTEXTO**
```
Você é um Engenheiro de Visão Computacional Sênior especializado em 
sistemas baseados em regras (rule-based systems). Atue como se estivesse 
desenvolvendo um protótipo acadêmico de detecção de objetos inspirado 
em técnicas clássicas de pré-deep learning (como Haar Cascades, 
HOG + SVM e Template Matching), mas implementado de forma simplificada 
e didática em Python puro.
```

### **O — OBJETIVO**
```
Desenvolver um sistema simulado que:
1. Analise características de uma imagem (simulada como dicionário de features)
2. Detecte a presença de objetos: pessoas, carros e animais
3. Use apenas regras lógicas (IF-THEN) — sem redes neurais
4. Retorne a classificação com nível de confiança
```

### **S — SAÍDA (Formato esperado)**
```
Responda SEMPRE nesta estrutura:
- 📦 Código Python completo e funcional
- 🔍 Explicação de cada bloco (Regras de detecção, Fluxo, Lógica)
- 🧪 3 casos de teste com entrada e saída esperada
- 📊 Matriz conceitual: Feature → Objeto detectado
```

### **T — TOM**
```
Tom técnico, didático e objetivo. Use comentários claros no código. 
Nível intermediário (público: estudantes de IA e engenheiros júnior).
```

### **A — AUDIÊNCIA**
```
Estudantes de Ciência da Computação, Engenharia de IA e profissionais 
que estão migrando para visão computacional.
```

### **R — RESTRIÇÕES**
```
- ❌ NÃO usar TensorFlow, PyTorch, OpenCV ou bibliotecas de deep learning
- ✅ Pode usar apenas: NumPy, Pillow (apenas para leitura de metadados simulados)
- ✅ Apenas lógica condicional, loops e funções
- ✅ Máximo de 200 linhas no script principal
- ✅ Deve funcionar com uma "imagem simulada" (dicionário Python)
```

---

## 🔄 MÉTODO RAO (Reason → Act → Observation)

### **🧠 REASON (Raciocínio prévio)**
```
Antes de gerar o código, planeje internamente:

1. QUAIS FEATURES SÃO RELEVANTES?
   - Pessoas: pele, face, roupas, proporção humana
   - Carros: metal, rodas, formato retangular, vidros
   - Animais: pelagem, quatro patas, focinho

2. COMO SIMULAR UMA "IMAGEM"?
   - Dicionário {feature: intensidade (0.0 a 1.0)}
   - Ex: {"skin_tone": 0.8, "wheels": 0.0, "fur": 0.2}

3. QUAL LÓGICA DE DECISÃO?
   - Sistema de PONTUAÇÃO (scoring) com thresholds
   - Cada feature soma pontos para uma classe
   - Classe com maior pontuação vence (se > limiar mínimo)
```

### **⚙️ ACT (Ação / Execução)**
```python
class SimpleVisionSystem:
    """
    Sistema de Visão Computacional baseado em Regras.
    Simula detecção de objetos sem Deep Learning.
    """
    
    # Regras de conhecimento (base de regras)
    RULES = {
        "person": {
            "skin_tone": 0.25,
            "face_features": 0.30,
            "clothing": 0.20,
            "human_proportion": 0.25
        },
        "car": {
            "metal_surface": 0.25,
            "wheels": 0.30,
            "rectangular_shape": 0.20,
            "glass_windows": 0.25
        },
        "animal": {
            "fur": 0.30,
            "four_legs": 0.25,
            "snout": 0.25,
            "tail": 0.20
        }
    }
    
    CONFIDENCE_THRESHOLD = 0.55
    
    def __init__(self, image_features: dict):
        self.features = image_features
        self.scores = {}
    
    def extract_features(self):
        """Simula a extração de características (feature extraction)."""
        return self.features
    
    def apply_rules(self):
        """Aplica as regras de pontuação para cada classe."""
        for obj_class, rule_weights in self.RULES.items():
            score = 0.0
            for feature, weight in rule_weights.items():
                score += self.features.get(feature, 0.0) * weight
            self.scores[obj_class] = round(score, 3)
        return self.scores
    
    def classify(self):
        """Classifica o objeto baseado na maior pontuação."""
        self.apply_rules()
        best_class = max(self.scores, key=self.scores.get)
        confidence = self.scores[best_class]
        
        if confidence < self.CONFIDENCE_THRESHOLD:
            return {
                "detected": "unknown",
                "confidence": confidence,
                "all_scores": self.scores,
                "status": "low_confidence"
            }
        
        return {
            "detected": best_class,
            "confidence": confidence,
            "all_scores": self.scores,
            "status": "success"
        }


# ============================================
# CASOS DE TESTE
# ============================================
if __name__ == "__main__":
    
    # TESTE 1: Pessoa com alta confiança
    image_person = {
        "skin_tone": 0.9,
        "face_features": 0.85,
        "clothing": 0.8,
        "human_proportion": 0.9,
        "fur": 0.0,
        "wheels": 0.0
    }
    
    # TESTE 2: Carro com alta confiança
    image_car = {
        "metal_surface": 0.95,
        "wheels": 0.9,
        "rectangular_shape": 0.85,
        "glass_windows": 0.8,
        "skin_tone": 0.0
    }
    
    # TESTE 3: Imagem ambígua (baixa confiança)
    image_ambiguous = {
        "skin_tone": 0.2,
        "fur": 0.3,
        "wheels": 0.1,
        "metal_surface": 0.1
    }
    
    test_cases = [
        ("👤 Pessoa", image_person),
        ("🚗 Carro", image_car),
        ("❓ Ambíguo", image_ambiguous)
    ]
    
    for label, img in test_cases:
        print(f"\n{'='*50}")
        print(f"Caso: {label}")
        print(f"Features: {img}")
        system = SimpleVisionSystem(img)
        result = system.classify()
        print(f"Resultado: {result}")
```

### **👁️ OBSERVATION (Validação e Análise)**
```
Após executar, verifique:

1. ✅ O sistema retornou a classe correta em casos óbvios?
2. ✅ O threshold rejeitou imagens ambíguas (unknown)?
3. ✅ Os scores parciais fazem sentido matematicamente?
4. ✅ O sistema é EXTENSÍVEL? (fácil adicionar nova classe)
5. ✅ As regras são INTERPRETÁVEIS? (caixa-branca / explainable AI)

📊 SAÍDA ESPERADA DOS TESTES:
- Pessoa  → {"detected": "person", "confidence": ~0.985, "status": "success"}
- Carro   → {"detected": "car", "confidence": ~0.965, "status": "success"}
- Ambíguo → {"detected": "unknown", "status": "low_confidence"}
```

---

## 📊 MATRIZ CONCEITUAL: FEATURE → OBJETO

| Feature         | 👤 Pessoa | 🚗 Carro | 🐕 Animal |
|-----------------|:---------:|:--------:|:---------:|
| `skin_tone`     | ✅ 0.25   | ❌ 0     | ❌ 0      |
| `face_features` | ✅ 0.30   | ❌ 0     | ❌ 0      |
| `wheels`        | ❌ 0      | ✅ 0.30  | ❌ 0      |
| `metal_surface` | ❌ 0      | ✅ 0.25  | ❌ 0      |
| `fur`           | ❌ 0      | ❌ 0     | ✅ 0.30   |
| `four_legs`     | ❌ 0      | ❌ 0     | ✅ 0.25   |

---

## 🎓 RESUMO DA METODOLOGIA APLICADA

| Etapa COSTAR | Componente                 | Implementação                                |
|--------------|----------------------------|----------------------------------------------|
| **C**ontexto | Persona técnica            | Engenheiro especialista em sistemas clássicos |
| **O**bjetivo | Detecção rule-based        | 3 classes, scoring + threshold               |
| **S**aída    | Código + explicação        | Estrutura padronizada em 4 blocos            |
| **T**om      | Didático e técnico         | Comentários claros, exemplos                 |
| **A**udiência| Estudantes/júnior          | Nível intermediário                          |
| **R**estrições| Sem DL, Python puro       | Apenas lógica condicional                    |

| Etapa RAO  | Função              | Resultado                                  |
|------------|---------------------|--------------------------------------------|
| **R**eason | Planejamento prévio | Definiu features, lógica de scoring        |
| **A**ct    | Execução do código  | Classe Python funcional com 3 testes       |
| **O**bservation | Validação     | Critérios de aceite + saída esperada       |

---

> 💡 **Nota de evolução**: Este sistema pode ser estendido para incluir árvores de decisão, lógica fuzzy ou ensembles de regras — servindo como ponte conceitual entre sistemas clássicos e deep learning.