import base64
from openai import AsyncOpenAI
from core.config import settings

client = AsyncOpenAI(api_key=settings.openai_api_key)

SYSTEM_PROMPT = """তুমি একজন বিশেষজ্ঞ কৃষি বিজ্ঞানী। কৃষকের ফসলের ছবি দেখে রোগ বা সমস্যা চিহ্নিত করো।

তোমার উত্তর অবশ্যই বাংলায় দিতে হবে এবং নিচের JSON format এ দিতে হবে:
{
  "detected": true/false,
  "crop_name": "ফসলের নাম (যদি চেনা যায়)",
  "disease_name": "রোগের নাম",
  "confidence": "high/medium/low",
  "symptoms": ["লক্ষণ ১", "লক্ষণ ২"],
  "causes": "রোগের কারণ",
  "treatment": ["চিকিৎসা ১", "চিকিৎসা ২", "চিকিৎসা ৩"],
  "prevention": ["প্রতিরোধ ১", "প্রতিরোধ ২"],
  "urgency": "high/medium/low",
  "summary": "সংক্ষিপ্ত পরামর্শ"
}

যদি ছবিতে ফসল বা গাছপালা না থাকে তাহলে detected: false দাও।
শুধু JSON দাও, অন্য কিছু নয়।"""


async def analyze_crop_image(image_bytes: bytes, crop_hint: str = "") -> dict:
    """
    Analyze crop image using OpenAI Vision and return disease detection result.
    """
    b64_image = base64.b64encode(image_bytes).decode("utf-8")

    user_message = "এই ফসলের ছবি দেখো এবং রোগ বা সমস্যা চিহ্নিত করো।"
    if crop_hint:
        user_message += f" ফসলের নাম: {crop_hint}"

    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_message},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{b64_image}",
                            "detail": "high",
                        },
                    },
                ],
            },
        ],
        max_tokens=1000,
        temperature=0.2,
    )

    raw = response.choices[0].message.content.strip()

    # strip markdown fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    import json
    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        result = {
            "detected": False,
            "summary": raw,
            "error": "JSON parse failed — raw response returned",
        }

    result["raw_response"] = response.choices[0].message.content
    result["model_used"] = response.model
    result["tokens_used"] = response.usage.total_tokens

    return result
