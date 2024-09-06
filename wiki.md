---

## 🎟 **Wiki - Billetterie Esport : Scénarios BDD**

### Introduction :
Bienvenue sur la page Wiki de la billetterie Esport. Cette page présente les **use cases** clés de notre projet et les scénarios BDD associés. Ces scénarios décrivent le comportement attendu des différentes fonctionnalités en langage naturel, facilitant la compréhension par toutes les parties prenantes.

---

### 1. **Billetterie Nominative :**

Chaque E-Billet est nominatif, associé à une personne physique et une journée d'événement spécifique. L'achat se fait exclusivement en ligne, et chaque billet doit contenir le nom, le prénom et une adresse e-mail.

#### 📝 **Scénario BDD : Achat d'un billet nominatif**
```
Feature: Achat d'un billet nominatif pour un tournoi Esport

  Scenario: Achat d'un E-Billet individuel
    Given un utilisateur "John Doe" n'a pas encore acheté de billet
    When il achète un billet pour le "premier jour" du "Tournoi Esport"
    Then le billet doit être enregistré avec les informations de "John Doe"
    And un e-mail de confirmation est envoyé à "john.doe@example.com"
```

---

### 2. **Achats Groupés :**

Un utilisateur peut acheter plusieurs E-Billets pour le même jour, en attribuant une identité différente à chaque billet, mais avec une seule adresse e-mail pour l'ensemble de la commande.

#### 📝 **Scénario BDD : Achat groupé de billets**
```
Feature: Achat groupé de plusieurs billets pour un tournoi Esport

  Scenario: Achat de plusieurs E-Billets pour la même journée
    Given l'utilisateur "Jane Smith" souhaite acheter plusieurs billets pour le "dernier jour"
    When elle achète 3 billets pour le même événement
    And elle fournit l'identité de chaque détenteur de billet ("John Doe", "Emma Doe", "Mark Doe")
    Then les billets doivent être enregistrés avec les noms fournis
    And un e-mail de confirmation est envoyé à "jane.smith@example.com"
```

---

### 3. **Prix Variable Selon le Jour de l'Événement :**

Le prix des billets varie en fonction du jour choisi. Par exemple, le dernier jour d'un événement, qui inclut la finale, est plus cher que le premier jour.

#### 📝 **Scénario BDD : Achat de billet à prix variable**
```
Feature: Achat de billets avec un prix variable selon le jour

  Scenario: Achat d'un billet pour la finale
    Given un utilisateur "John Doe" n'a pas encore acheté de billet
    When il achète un billet pour le "dernier jour" du "Tournoi Esport"
    Then le prix du billet doit être de "50€"
    And le billet est enregistré pour "John Doe"
    And un e-mail de confirmation est envoyé à "john.doe@example.com"
    
  Scenario: Achat d'un billet pour le premier jour
    Given un utilisateur "Jane Smith" souhaite acheter un billet
    When elle achète un billet pour le "premier jour" du "Tournoi Esport"
    Then le prix du billet doit être de "30€"
    And le billet est enregistré pour "Jane Smith"
    And un e-mail de confirmation est envoyé à "jane.smith@example.com"
```

---

### 4. **Multipass :**

Le **Multipass** est un billet donnant accès à toutes les dates de l'événement, avec un prix unique (ex. 30€ pour les trois jours). Ce billet est nominatif et peut également faire l'objet d'un achat groupé.

#### 📝 **Scénario BDD : Achat d'un Multipass**
```
Feature: Achat de billets Multipass pour plusieurs jours

  Scenario: Achat d'un Multipass individuel
    Given un utilisateur "John Doe" souhaite accéder à tous les jours de l'événement
    When il achète un Multipass pour le "Tournoi Esport"
    Then le billet doit être enregistré avec un prix total de "30€"
    And le billet est enregistré pour "John Doe"
    And un e-mail de confirmation est envoyé à "john.doe@example.com"
  
  Scenario: Achat groupé de Multipass
    Given l'utilisateur "Jane Smith" souhaite acheter plusieurs Multipass
    When elle achète 3 Multipass pour l'événement
    And elle fournit l'identité des détenteurs ("Jane Smith", "Mark Doe", "Emma Doe")
    Then chaque Multipass est enregistré pour les noms donnés
    And un e-mail de confirmation est envoyé à "jane.smith@example.com"
```

---

### Conclusion :
Cette page Wiki présente les principaux cas d'utilisation de la billetterie Esport, avec des scénarios **BDD** décrivant les comportements attendus des fonctionnalités. Ces scénarios permettent à l'équipe technique et aux parties prenantes non techniques de **collaborer efficacement** et d'assurer que les besoins métiers sont respectés tout au long du projet.

--- 
