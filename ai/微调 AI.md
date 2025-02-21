# API 微调
来源：[使用 Gemini API 进行微调  |  Google AI for Developers](https://ai.google.dev/gemini-api/docs/model-tuning?hl=zh-cn)
少样本提示等提示设计策略有时可能无法生成 结果。_微调_是一个可以提高模型预测准确率的过程， 或帮助模型遵循特定的输出结果 说明不够充分，并且您有一组示例时的要求 所需的输出结果

本页面从概念上简要介绍了如何微调 Gemini API 文本服务背后的文本模型。准备好开始调优时，请尝试 [微调教程](https://ai.google.dev/gemini-api/docs/model-tuning/tutorial?hl=zh-cn)。如需更全面地了解如何针对特定用例自定义 LLM，请参阅[机器学习速成课程](https://developers.google.com/machine-learning/crash-course/?hl=zh-cn)中的 [LLM：微调、提炼和提示工程](https://developers.google.com/machine-learning/crash-course/llm/tuning?hl=zh-cn)。

## 微调的工作原理

微调的目标是进一步提高模型针对特定任务的效果。通过为模型提供训练 数据集包含该任务的许多示例。对于特定领域的任务，您可以使用适量样本调优模型，以此来显著改善模型性能。这种模型微调有时也称为_监督式微调_，以便与其他类型的微调区分开来。

您的训练数据应构建为包含提示输入和 预期响应输出。您还可以直接在 Google AI Studio 中使用示例数据来调优模型。目标是让模型模仿期望的行为 来说明该行为或任务。

当您运行调参作业时，模型会学习帮助它的其他参数 对必要的信息进行编码，以执行您想要的任务或了解 行为这些参数随后可在推断时使用。此 调优作业是一个新模型，它实际上是新模型 和原始模型之间的差异。

## 准备数据集

在开始微调之前，您需要一个数据集来调优模型。为了获得最佳性能，数据集中的示例应具有高质量、多样化且能代表真实的输入和输出。

### 格式

**注意：**微调仅支持输入-输出对示例。聊天方式 目前不支持多轮对话。

数据集中包含的样本应与您的预期生产流量相匹配。如果您的数据集包含特定的格式、关键字、说明或信息，则生产数据应以相同方式设置格式并包含相同的说明。

例如，如果数据集中的样本包含 `"question:"` 和 `"context:"`，则生产流量的格式也应设置为包含 `"question:"` 和 `"context:"`，其顺序与在数据集样本中的显示顺序相同。如果您排除上下文，模型将无法识别该模式， 即使确切的问题出现在数据集内的样本中。

再举一个例子，这是应用的 Python 训练数据， 生成序列中的下一个数字：

```json
training_data = [
  {"text_input": "1", "output": "2"},
  {"text_input": "3", "output": "4"},
  {"text_input": "-3", "output": "-2"},
  {"text_input": "twenty two", "output": "twenty three"},
  {"text_input": "two hundred", "output": "two hundred one"},
  {"text_input": "ninety nine", "output": "one hundred"},
  {"text_input": "8", "output": "9"},
  {"text_input": "-98", "output": "-97"},
  {"text_input": "1,000", "output": "1,001"},
  {"text_input": "10,100,000", "output": "10,100,001"},
  {"text_input": "thirteen", "output": "fourteen"},
  {"text_input": "eighty", "output": "eighty one"},
  {"text_input": "one", "output": "two"},
  {"text_input": "three", "output": "four"},
  {"text_input": "seven", "output": "eight"},
]
```

为数据集中的每个示例添加提示或前言也可以帮助提升经过调优的模型的性能。请注意，如果数据集中包含提示或前言，则在推理时，对经过调优的模型的提示中也应包含这些内容。

### 限制

**注意**：针对 Gemini 1.5 Flash 微调数据集存在以下限制：

- 每个样本的输入大小上限为 40,000 个字符。
- 每个样本的输出大小上限为 5,000 个字符。

### 训练数据大小

您只需 20 个示例即可微调模型。其他数据 通常可以提高响应的质量。目标为 100 和 500 个样本，具体取决于您的应用。下表显示了针对各种常见任务微调文本模型的建议数据集大小：

|任务|数据集中的示例数量|
|---|---|
|分类|超过 100|
|总结|100 至 500 人以上|
|文档搜索|100 多项|

## 上传您的调参数据集

数据可使用 API 以内嵌方式传递，也可通过上传到 Google AI Studio。

如需使用客户端库，请在 `createTunedModel` 调用中提供数据文件。 文件大小上限为 4 MB。如需开始使用，请参阅[使用 Python 进行微调的快速入门](https://ai.google.dev/gemini-api/docs/model-tuning/tutorial?lang=python&hl=zh-cn)。

要使用 c网址 调用 REST API，请向 `training_data` 参数。如需开始使用，请参阅[使用 cURL 进行调整的快速入门](https://ai.google.dev/gemini-api/docs/model-tuning/tutorial?lang=rest&hl=zh-cn)。

## 高级调参设置

创建调整作业时，您可以指定以下高级设置：

- **周期**：对整个训练集进行一次完整的训练遍历，每次训练时 已经过一次处理。
- **批次大小**：一次训练[迭代](https://developers.google.com/machine-learning/glossary?hl=zh-cn#iteration)中使用的样本集。通过 批次大小决定了一个批次中的样本数量。
- **学习速率**：一个浮点数，告知算法如何 调整每次迭代的模型参数。例如， 将学习速率设为 0.3，就能将权重和偏差调整三倍 这比 0.1 的学习速率要大得多。高学习速率和低学习速率 各有各的利弊，应根据您的用例进行调整。
- **学习速率调节系数**：速率调节系数用于修改模型的原始学习速率。值为 1，表示 模型。值大于 1 时，学习速率会提高；值大于 1 0 则降低学习速率。

### 建议的配置

下表显示了对基础模型进行微调的建议配置：

|超参数|默认值|建议的调整|
|---|---|---|
|纪元|5|如果损失在 5 个 epoch 之前开始趋于稳定，请使用较小的值。<br><br>如果损失收敛且似乎没有趋于稳定，请使用较高的值。|
|批次大小|4||
|学习速率|0.001|对于较小的数据集，请使用较小的值。|

损失曲线显示的是模型预测结果与理想值的偏差 训练样本中的预测。理想情况下，您应在曲线达到平台期之前，在曲线的最低点停止训练。例如： 下面的图表显示了大约第 4-6 个纪元的损失曲线趋于平稳， 您可以将 `Epoch` 参数设置为 4，并获得相同的性能。

![显示模型损失曲线的折线图。该线条在第 1 个和第 2 个时期之间出现峰值，然后急剧下降到几乎为 0，并在第 3 个时期趋于平稳。](https://ai.google.dev/static/docs/images/loss_curve.png?hl=zh-cn)

## 检查调参作业状态

您可以在 Google AI Studio 的**我的库**标签页中检查调优作业的状态，也可以在 Gemini API 中使用经过调优的模型的 `metadata` 属性检查其状态。

## 排查错误

本部分包含一些提示，介绍了如何解决您在 创建经过调整的模型。

### 身份验证

**注意** ：自 2024 年 9 月 30 日起，不再需要 OAuth 身份验证。 新项目应改用 API 密钥身份验证。

使用 API 和客户端库进行调整需要进行身份验证。您可以 使用 API 密钥（推荐）或使用 OAuth 设置身份验证 凭据。有关设置 API 密钥的文档，请参阅 [设置 API 密钥](https://ai.google.dev/gemini-api/docs/quickstart?hl=zh-cn#set-up-api-key)。

如果您看到 `'PermissionDenied: 403 Request had insufficient authentication scopes'` 错误，则可能需要使用 OAuth 设置用户身份验证 凭据。如需为 Python 配置 OAuth 凭据，请参阅我们的 [OAuth 设置教程](https://ai.google.dev/gemini-api/docs/oauth?hl=zh-cn)。

### 已取消的模型

在微调作业完成之前，您可以随时取消该作业。不过， 取消模型的推理性能不可预测，尤其是当 调参作业在训练的早期阶段就被取消了。如果您取消了订阅，原因是： 想要在较早的周期停止训练，则应创建新的调优 并将周期设置为较低的值。

## 经调参的模型的限制

**注意**：经过优化的模型具有以下限制：

- 经调参的 Gemini 1.5 Flash 模型的输入限制为 40,000 个字符。
- 经过调优的模型不支持 JSON 模式。
- 仅支持文本输入。

## 后续步骤

开始学习微调教程：

- [微调教程 (Python)](https://ai.google.dev/gemini-api/docs/model-tuning/tutorial?lang=python&hl=zh-cn)
- [微调教程 (REST)](https://ai.google.dev/gemini-api/docs/model-tuning/tutorial?lang=rest&hl=zh-cn)

# 底层代码微调
该部分基于 [self-llm/models/DeepSeek/04-DeepSeek-7B-chat Lora 微调.md at master · datawhalechina/self-llm · GitHub](https://github.com/datawhalechina/self-llm/blob/master/models/DeepSeek/04-DeepSeek-7B-chat%20Lora%20%E5%BE%AE%E8%B0%83.md)
## 环境配置
前置第三方库
```py
torch
transformers
accelerate
peft
bitsandbytes
swanlab
datasets
tiktoken
transformers_stream_generator
```

微调数据集放置在根目录 [/dataset](../dataset/huanhuan.json)。

## 指令集构建

LLM 的微调一般指指令微调过程。所谓指令微调，是说我们使用的微调数据形如：

```json
{
    "instrution":"回答以下用户问题，仅输出答案。",
    "input":"1+1等于几?",
    "output":"2"
}
```

其中，`instruction` 是用户指令，告知模型其需要完成的任务；`input` 是用户输入，是完成用户指令所必须的输入内容；`output` 是模型应该给出的输出。

即我们的核心训练目标是让模型具有理解并遵循用户指令的能力。因此，在指令集构建时，我们应针对我们的目标任务，针对性构建任务指令集。例如，我们的目标是构建一个能够模拟甄嬛对话风格的个性化 LLM，因此我们构造的指令形如：

```json
{
    "instruction": "现在你要扮演皇帝身边的女人--甄嬛",
    "input":"你是谁？",
    "output":"家父是大理寺少卿甄远道。"
}
```

我们所构造的全部指令数据集在根目录下。

## 数据格式化

`Lora` 训练的数据是需要经过格式化、编码之后再输入给模型进行训练的，如果是熟悉 `Pytorch` 模型训练流程的同学会知道，我们一般需要将输入文本编码为 input_ids，将输出文本编码为 `labels`，编码之后的结果都是多维的向量。我们首先定义一个预处理函数，这个函数用于对每一个样本，编码其输入、输出文本并返回一个编码后的字典：

```python
def process_func(example):
    MAX_LENGTH = 384    # Llama分词器会将一个中文字切分为多个token，因此需要放开一些最大长度，保证数据的完整性
    input_ids, attention_mask, labels = [], [], []
    instruction = tokenizer(f"User: {example['instruction']+example['input']}\n\n", add_special_tokens=False)  # add_special_tokens 不在开头加 special_tokens
    response = tokenizer(f"Assistant: {example['output']}<｜end▁of▁sentence｜>", add_special_tokens=False)
    input_ids = instruction["input_ids"] + response["input_ids"] + [tokenizer.pad_token_id]
    attention_mask = instruction["attention_mask"] + response["attention_mask"] + [1]  # 因为eos token咱们也是要关注的所以 补充为1
    labels = [-100] * len(instruction["input_ids"]) + response["input_ids"] + [tokenizer.pad_token_id]  
    if len(input_ids) > MAX_LENGTH:  # 做一个截断
        input_ids = input_ids[:MAX_LENGTH]
        attention_mask = attention_mask[:MAX_LENGTH]
        labels = labels[:MAX_LENGTH]
    return {
        "input_ids": input_ids,
        "attention_mask": attention_mask,
        "labels": labels
    }
```

这里的格式化输入参考了， [DeepSeek](https://github.com/deepseek-ai/DeepSeek-LLM) 官方github仓库中readme的指令介绍。

```text
User: {messages[0]['content']}

Assistant: {messages[1]['content']}<｜end▁of▁sentence｜>User: {messages[2]['content']}

Assistant:
```

## 加载tokenizer和半精度模型

模型以半精度形式加载，如果你的显卡比较新的话，可以用`torch.bfolat`形式加载。对于自定义的模型一定要指定`trust_remote_code`参数为`True`。

```python
tokenizer = AutoTokenizer.from_pretrained('./deepseek-ai/deepseek-llm-7b-chat/', use_fast=False, trust_remote_code=True)
tokenizer.padding_side = 'right' # padding在右边

model = AutoModelForCausalLM.from_pretrained('./deepseek-ai/deepseek-llm-7b-chat/', trust_remote_code=True, torch_dtype=torch.half, device_map="auto")
model.generation_config = GenerationConfig.from_pretrained('./deepseek-ai/deepseek-llm-7b-chat/')
model.generation_config.pad_token_id = model.generation_config.eos_token_id
```

## 定义LoraConfig

`LoraConfig`这个类中可以设置很多参数，但主要的参数没多少，简单讲一讲，感兴趣的同学可以直接看源码。

- `task_type`：模型类型
- `target_modules`：需要训练的模型层的名字，主要就是`attention`部分的层，不同的模型对应的层的名字不同，可以传入数组，也可以字符串，也可以正则表达式。
- `r`：`lora`的秩，具体可以看`Lora`原理
- `lora_alpha`：`Lora alaph`，具体作用参见 `Lora` 原理 

`Lora`的缩放是啥嘞？当然不是`r`（秩），这个缩放就是`lora_alpha/r`, 在这个`LoraConfig`中缩放就是4倍。

```python
config = LoraConfig(
    task_type=TaskType.CAUSAL_LM, 
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    inference_mode=False, # 训练模式
    r=8, # Lora 秩
    lora_alpha=32, # Lora alaph，具体作用参见 Lora 原理
    lora_dropout=0.1# Dropout 比例
)
```

## 自定义 TrainingArguments 参数

`TrainingArguments`这个类的源码也介绍了每个参数的具体作用，当然大家可以来自行探索，这里就简单说几个常用的。

- `output_dir`：模型的输出路径
- `per_device_train_batch_size`：顾名思义 `batch_size`
- `gradient_accumulation_steps`: 梯度累加，如果你的显存比较小，那可以把 `batch_size` 设置小一点，梯度累加增大一些。
- `logging_steps`：多少步，输出一次`log`
- `num_train_epochs`：顾名思义 `epoch`
- `gradient_checkpointing`：梯度检查，这个一旦开启，模型就必须执行`model.enable_input_require_grads()`，这个原理大家可以自行探索，这里就不细说了。

```python
args = TrainingArguments(
    output_dir="./output/DeepSeek",
    per_device_train_batch_size=8,
    gradient_accumulation_steps=2,
    logging_steps=10,
    num_train_epochs=3,
    save_steps=100,
    learning_rate=1e-4,
    save_on_each_node=True,
    gradient_checkpointing=True
)
```

## 使用 Trainer 训练

```python
trainer = Trainer(
    model=model,
    args=args,
    train_dataset=tokenized_id,
    data_collator=DataCollatorForSeq2Seq(tokenizer=tokenizer, padding=True),
)
trainer.train()
```

## 模型推理

可以用这种比较经典的方式推理：

```python
text = "小姐，别的秀女都在求中选，唯有咱们小姐想被撂牌子，菩萨一定记得真真儿的——"
inputs = tokenizer(f"User: {text}\n\n", return_tensors="pt")
outputs = model.generate(**inputs.to(model.device), max_new_tokens=100)

result = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(result)
```

推理结果：（效果蛮好的，有点出乎我的意料）

```text
User: 小姐，别的秀女都在求中选，唯有咱们小姐想被撂牌子，菩萨一定记得真真儿的——

Assistant: 菩萨也会看错眼的时候。
```