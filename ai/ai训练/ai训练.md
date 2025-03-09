## 所需显存
所需显存 = 模型大小 + KV 缓存 + 激活所需显存
其中：
模型大小

检测是否能使用 cuda
```py
import torch
print(torch.cuda.is_available())
```

加载模型
```python
model = AutoModelForCausalLM.from_pretrained("gpt2")
# huggingface上的
model = AutoModelForCausalLM.from_pretrained("./my_local_model")
# 本地的
```

