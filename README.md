# Application Flask pour Payer en Lightning Network

## Description Générale

Ce projet illustre comment proposer un paiement via **Lightning Network** sur une page web.  
L’application, écrite en **Python/Flask**, se connecte à un nœud **Core Lightning (c-lightning)** local afin de :

- **Créer des factures** (BOLT11) en fonction d’un montant saisi par l’utilisateur.  
- **Fournir un lien de vérification** pour confirmer si la facture a bien été payée.

Ainsi, en quelques étapes, vous pouvez tester et démontrer un paiement Lightning sur un simple site web.

---

## Prérequis et Installation

1. **Avoir un nœud Lightning fonctionnel en local**

   - **Bitcoin Core** :  
     - Installer, synchroniser et configurer **Bitcoin Core (bitcoind)**.  
     - Vous pouvez choisir :  
       - **Réseau principal (mainnet)** pour des paiements réels,  
       - **Testnet**, **Signet**, ou **Regtest** pour des tests et de l’expérimentation plus sécurisés et moins coûteux.

   - **Core Lightning (c-lightning)** :  
     - Installer **c-lightning** et le configurer pour qu’il se connecte à votre Bitcoin Core.  
     - Vérifier que `lightningd` tourne et qu’il crée bien le fichier `lightning-rpc`.  
     - Exemple de chemin par défaut sous Linux : `~/.lightning/bitcoin/lightning-rpc`.

2. **Installer les dépendances Python**

   - **Cloner ou télécharger** ce projet.  
   - **Créer un environnement virtuel Python** (recommandé) :
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - **Installer Flask et pylightning** :
     ```bash
     pip install flask pylightning
     ```
   - **Configurer le chemin vers votre socket `lightning-rpc`** :
     - Dans le code (`app.py`), modifier la variable `LIGHTNING_RPC_PATH` pour pointer vers le fichier `lightning-rpc` de votre installation c-lightning.

---

## Lancement de l’application

- **Vérifier** que votre nœud **Bitcoin** et votre nœud **Lightning** sont démarrés et prêts à recevoir des commandes.
- **Lancer le serveur Flask** :  python app.py
- Par défaut, l’application écoute sur le port 5000. Rendez-vous sur http://127.0.0.1:5000 pour accéder à la page d’accueil.

---

## Utilisation

- Page d’accueil :  
  - Affiche un formulaire pour saisir un montant en satoshis.   
  - En validant le formulaire, vous envoyez la requête à l’URL /create_invoice.   
- Génération d’une facture (BOLT11) :       
  - L’application appelle lightning.invoice() via pylightning pour créer une facture.    
  - Le résultat est un code BOLT11 (commençant souvent par lnbc…), que vous pouvez copier ou scanner avec un portefeuille Lightning compatible (Phoenix, Muun, BlueWallet, etc.).   
- Paiement de la facture :   
  - Utilisez un wallet Lightning pour payer la facture.   
  - Si vous êtes sur regtest ou signet, veillez à avoir un canal ouvert et des fonds disponibles dans votre nœud.   
- Vérification du paiement :     
  - L’application propose un lien /check_invoice/<label> pour afficher le statut de la facture.  
  - Le code interroge lightning.listinvoices(label) et renvoie le statut :    
    - paid : la facture a été réglée,   
    - unpaid : la facture n’est pas encore payée (et n’est pas expirée),   
    - expired : délai dépassé, aucun paiement effectué.   

