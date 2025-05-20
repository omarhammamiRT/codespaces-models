import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import (
    SystemMessage,
    UserMessage,
    TextContentItem,
    ImageContentItem,
    ImageUrl,
    ImageDetailLevel,
)
from azure.core.credentials import AzureKeyCredential

token = os.environ["GITHUB_TOKEN"]
endpoint = "https://models.github.ai/inference"
model_name = "meta/Llama-3.2-11B-Vision-Instruct"

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

response = client.complete(
    messages=[
        SystemMessage("You are a highly efficient and precise JSON extraction assistant. Your sole purpose is to extract specific information from provided medical documents and output it strictly in the requested JSON format, with no additional text or conversational filler."),
        UserMessage(
            content=[
                TextContentItem(text='''Extrayez les informations suivantes du document fourni, au format JSON. Votre réponse DOIT contenir UNIQUEMENT l'objet JSON, et aucun autre texte ou remplissage conversationnel.

{
 "date_examen": "jj/mm/aaaa",
 "type_document": "",
 "specialite_medecin": "",
 "conclusions": ""
}

Instructions:
- **date_examen**: Extraire la date de l'examen (jj/mm/aaaa). Si la date n'est pas mentionnée explicitement dans le document (y compris les dates manuscrites), la valeur doit être "inconnu".
- **type_document**: Déterminez le type de document médical. Cela peut être un type d'IRM, un Scanner (mentionnez le nom complet du document). Si le type n'est pas explicitement mentionné, déduisez-le du contexte médical ou, s'il est manuscrit, identifiez-le comme une ordonnance médicale ou une lettre médicale. Si aucune déduction n'est possible, la valeur doit être "inconnu".
- **specialite_medecin**: Déterminez la spécialité du médecin. Si la spécialité n'est pas mentionnée explicitement, essayez de la déduire du contexte médical. Si aucune déduction n'est possible, la valeur doit être "inconnu".
- **conclusions**: Extraire les conclusions de l'examen si elles sont clairement mentionnées dans le document. Si aucune conclusion claire n'est présente, ou si le type de document est une ordonnance médicale ou une lettre médicale, la valeur doit être "inconnu".'''),
                ImageContentItem(
                    image_url=ImageUrl.load(
                        image_file=os.path.join(os.path.dirname(__file__), "f1.jpg"),
                        image_format="jpg",
                        detail=ImageDetailLevel.LOW)
                ),
            ],
        ),
    ],
    model=model_name,
)

print(response.choices[0].message.content)