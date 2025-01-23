from flask import Flask, request, jsonify
from lightning import LightningRpc
import os

app = Flask(__name__)

# Indiquez le chemin exact de votre socket lightning-rpc
# Exemple : "/home/votre_user/.lightning/bitcoin/lightning-rpc"
LIGHTNING_RPC_PATH = "/mnt/d/Programation/lightning/lightning-rpc"

# Initialisation de la connexion RPC
lightning = LightningRpc(LIGHTNING_RPC_PATH)

@app.route("/")
def index():
    """
    Page d'accueil.
    On propose à l'utilisateur d'entrer un montant en satoshis pour générer une facture.
    """
    return """
    <h1>Accepter un paiement Lightning</h1>
    <form action="/create_invoice" method="POST">
      Montant (en satoshis): <input type="text" name="amount">
      <input type="submit" value="Créer une facture">
    </form>
    """

@app.route("/create_invoice", methods=["POST"])
def create_invoice():
    """
    Crée une facture Lightning (BOLT11) à partir du montant en satoshis fourni par l'utilisateur.
    Retourne un BOLT11 qui pourra être scanné/payant via un wallet LN.
    """
    amount_sats = request.form.get("amount", "1000")  # par défaut 1000 sats si vide
    label = "facture_" + os.urandom(4).hex()  # un label unique obligatoire pour c-lightning
    description = "Paiement de test depuis Flask"

    # L'argument msatoshi attend des millisatoshis => multiplier par 1000
    invoice = lightning.invoice(
        msatoshi=int(amount_sats) * 1000,
        label=label,
        description=description
    )

    bolt11 = invoice["bolt11"]

    return f"""
    <h2>Voici votre facture :</h2>
    <p><strong>BOLT11 : </strong>{bolt11}</p>
    <p>Utilisez un portefeuille Lightning pour scanner ou payer ce BOLT11.</p>
    <hr>
    <a href="/check_invoice/{label}">Vérifier le statut de la facture</a>
    """

@app.route("/check_invoice/<label>", methods=["GET"])
def check_invoice(label):
    """
    Vérifie le statut d'une facture via son label unique.
    """
    invoices = lightning.listinvoices(label)["invoices"]
    if not invoices:
        return "Aucune facture trouvée avec ce label."

    invoice = invoices[0]
    status = invoice["status"]  # "unpaid" (ou "expired") / "paid"

    if status == "paid":
        return f"<h3>La facture {label} est payée !</h3>"
    else:
        return f"Statut de la facture {label} : {status}"

if __name__ == "__main__":
    # Lancement de l'app Flask en mode debug
    app.run(debug=True, host="0.0.0.0", port=5000)
