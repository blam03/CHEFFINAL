import google.generativeai as genai
genai.configure(api_key="AIzaSyCzy5thLA2G1bcOJucI0SOIhN1LCbLNfiU")
models = genai.list_models()
for m in models:
    print(m.name)
