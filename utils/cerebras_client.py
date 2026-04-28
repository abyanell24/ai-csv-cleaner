import json
from cerebras.cloud.sdk import Cerebras


class CerebrasClient:
    def __init__(self, model: str = "llama-3.1-8b"):
        self.client = Cerebras(api_key="csk-e6kxn3e56cfcmk93wtw2jet2446f9xv8m44xkxc3df3hwx4p")
        self.model = model
    
    def generate(self, prompt: str, system_prompt: str = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.5,
            max_tokens=4096
        )
        return response.choices[0].message.content
    
    def generate_batch(self, data: list, system_prompt: str, batch_size: int = 50, progress_callback=None) -> str:
        total_cleaned = []
        total_batches = (len(data) + batch_size - 1) // batch_size
        step = batch_size
        
        for start in range(0, len(data), step):
            batch = data[start:start+batch_size]
            batch_json = json.dumps(batch)
            
            prompt = f"""{system_prompt}

Data to clean:
{batch_json}

Return ONLY the cleaned data in the same JSON format as input. No explanation."""

            try:
                result = self.generate(prompt, "")
                cleaned_batch = json.loads(result)
                total_cleaned.extend(cleaned_batch)
            except json.JSONDecodeError:
                total_cleaned.extend(batch)
            
            if progress_callback:
                current_batch = (start // batch_size) + 1
                progress_callback(current_batch, total_batches)
        
        return json.dumps(total_cleaned)
    
    def chat(self, messages: list) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.5,
            max_tokens=4096
        )
        return response.choices[0].message.content
    
    def is_available(self) -> bool:
        try:
            test_msg = [{"role": "user", "content": "hi"}]
            self.chat(test_msg)
            return True
        except:
            return False