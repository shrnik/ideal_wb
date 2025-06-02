import os
import json
import pandas as pd


def get_system_prompt() -> str:
    return (
        "You are an expert at analysing research paper for impact in development economics.\nFoe a given title, abstract and DOI, you need to find intervention used in the study\n\nList of interventions\n- Conditional Cash Transfers (CCTs)\n- Environmental regulation\n- Nutrient supplementation\n- Nutrition education and behaviour change\n- Other intervention\n- Unconditional Cash Transfers (UCTs)\n- Health worker training\n- Access to microcredit\n- Introduction of agricultural extension services\n- General health education and behaviour change\n- Nutrient fortification in foods\n- Maternal and infant nutrition care\n- Awareness campaigns about STI/HIV transmission, prevention, and treatment\n- HIV counselling\n- Forest conservation policy\n- Improved inputs for agriculture\n- Entrepreneurship training\n- Food transfers\n- General health counselling\n- Ecosystem conservation\n- Crop management training\n- Mental health and psychosocial support (MHPSS)\n- mHealth\n- Reproductive health education and behaviour change\n- Sexual and gender-based violence (SGBV) - prevention\n- STI/HIV testing\n- Land titling and certification\n- Antenatal care\n- Exclusive breastfeeding\n- Government tax policy\n- Other life skills\n- Gender equality behavioural-change communications\n- Sustainable land management\n- Access and participation\n- Other pedagogical intervention\n- Social health insurance\n- Financial regulation\n- Organisational contract farming (agriculture)\n- Community involvement in health information\n- Irrigation infrastructure\n- Agricultural extension worker training\n- Land management and reform\n- Behavioural change and public awareness campaign\n- Provision of contraception\n- School feeding programmes\n- Antiretroviral therapy (ART)\n- Participatory forest management\n- Community mobilization in health\n- Fertiliser subsidies\n- Decentralisation\n- Information dissemination - political processes\n- Parasite prevention\n- Pay for performance\n- Mass health communications\n- Cooking appliances\n- Reminder systems for healthcare\n- Rotating/Accumulated savings and credit associations\n- Community-driven Development & Reconstruction (CDD & CDR)\n- Agricultural research and development\n- Cash for work\n- Agricultural market information\n- Outreach services of care\n- Livestock management training\n- Railway construction\n- Energy subsidies\n- Financial literacy\n- Behavioural sanitation promotion\n- Educational hand hygiene promotion\n- Farmer field schools\n- Civic engagement initiatives\n- Insecticide Treated Nets (ITNs)\n- Continuing education for educators\n- Technical and Vocational Education and Training (TVET)\n- Formal credit to farmers\n- Establishing farmer-based organisations\n- Old-age and pension schemes\n- ICT in agricultural extension\n- Behavioural hand hygiene promotion\n- Representation of women & minorities\n- Seed grants\n- Access to output markets for smallholder farmers\n- Immunisation campaigns\n- Agricultural marketing training\n- Civil society capacity building\n- Individual health communications\n- Postnatal care\n- Seed subsidies\n- Infrastructure development and reconstruction\n- Educational sanitation promotion\n- Crop insurance\n- Family counselling\n- Index insurance\n- Promotion of contraceptive use\n- Technical and vocational education and training (TVET)\n- Water supply management\n- Early childhood care\n- Other in-kind transfers\n- Voucher schemes for health\n- Asset transfers\n- Sexual and reproductive health education in school\n\nThere could be one or more interventions but no more than 3\noutput should be valid json of the format\n\n{\"interventions\": [\"Seed grants\", \" Asset transfers\"] }"

    )


def get_user_prompt(abstract: str, title: str, doi) -> str:
    prompt_parts = []
    if title:
        prompt_parts.append(f"Title: {title}")
    if abstract:
        prompt_parts.append(f"Abstract: {abstract}")
    if doi:
        prompt_parts.append(f"DOI: {doi}")
    return "\n".join(prompt_parts)


csv = "data/initial_data.csv"


def get_csv_data(csv: str):
    df = pd.read_csv(csv)
    return df


def replace_nbsp(text):
    return text.replace('\u00a0', ' ').replace('\u2011', '-').replace('\u2014', '--')


def get_input_data(df: pd.DataFrame):
    input_data = []
    for index, row in df.iterrows():
        title = row["Title"]
        abstract = row["Abstract"]
        doi = row["DOI"]
        api_input = {
            "custom_id": f"row-{index}",
            "url": "/v1/chat/completions",
            "method": "POST",
            "body": {
                "model": "gpt-4.1",
                "messages": [
                    {"role": "system", "content": [{
                        "type": "text",
                        "text": get_system_prompt()
                    }]},
                    {"role": "user", "content": [{
                        "type": "text",
                        "text": replace_nbsp(get_user_prompt(
                            abstract, title, doi))}
                    ]},
                ],
                "response_format": {
                    "type": "text"
                },
                "temperature": 1,
                "max_completion_tokens": 200,
                "top_p": 1,
                "frequency_penalty": 0,
                "presence_penalty": 0
            },
        }
        input_data.append(api_input)
    return input_data


def get_batch_file():
    df = get_csv_data(csv)
    input_data = get_input_data(df[:2000])
    batch_file = "data/batch_input_interventions.jsonl"
    os.makedirs(os.path.dirname(batch_file), exist_ok=True)

    with open(batch_file, "w") as f:
        for item in input_data:
            f.write(json.dumps(item) + "\n")


get_batch_file()
