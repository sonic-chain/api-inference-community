from transformers import pipeline


captioner = pipeline(model="ydshieh/vit-gpt2-coco-en")
result = captioner(images="https://huggingface.co/datasets/Narsil/image_dummy/raw/main/parrots.png")
print(result)
