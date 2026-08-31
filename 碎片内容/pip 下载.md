旧版
```sh
python -m pip download numpy==2.2.0 --platform manylinux2014_x86_64 --python-version 310 --implementation cp --abi cp310 --only-binary=:all:
```

新版
```sh
python -m pip download vllm==0.22.0 --platform manylinux_2_28_x86_64 --python-version 310 --implementation cp --only-binary=:all: 
```

`pip install` 时添加 `--no-index --find-links=/app/models/whl`