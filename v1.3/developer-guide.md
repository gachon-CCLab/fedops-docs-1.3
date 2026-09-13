---
layout: "default"
title: "Federated Task Developer Guide"
nav_order: 7
permalink: "/v1.3/developer-guide/"
docs_version: "1.3"
lang: "ko"
guide_source: "Federated Task Developer Guide 3c95dfbe76bb80ab90c4e62717a778b2.md"
guide_status: "draft"
---

# Federated Task Developer Guide
{: .no_toc }

Federated Task Baseline 작성 가이드
{: .fs-5 .fw-400 }

Federated Task 작성자가 자신의 모델과 로컬 데이터를 FedOps에 연결할 때 필요한 파일 구성과 주요 함수의 작성 기준을 설명합니다.

완성된 구현 예시는 MNIST 예제를 참고할 수 있습니다.

<details markdown="1" class="guide-examples">
<summary>MNIST 완성 예제와 Baseline 코드 보기</summary>

- MNIST/
    - conf/config.yaml
        
        ```bash
        # Completed MNIST example for the Federated Task Baseline 0.16 contract.
        # Only Owner model, data, and local-training values are stored here.
        random_seed: 42
        
        model:
          display_name: MNIST Classifier
          output_size: 10
        
        dataset:
          name: MNIST
          validation_split: 0.2
          # MNIST is public test data, so the aggregation runtime may obtain its
          # server-side validation split without using any participant's local data.
          download: true
        
        local_training:
          learning_rate: 0.001
          epochs: 1
          batch_size: 128
        
        # Aggregation-server Global Model evaluation uses 8 batches (1,024 MNIST
        # samples) so server startup and each round remain responsive.
        server_evaluation:
          max_batches: 8
        ```
        
    - local_training/
        - data_preparation.py
            
            ```python
            """Completed MNIST example of the fixed FedOps local-data contracts.
            
            Function bodies demonstrate editable Task code. Names, arguments, default values,
            keyword-only markers, and return structures marked ``FEDOPS CONTRACT`` are fixed.
            """
            
            from __future__ import annotations
            
            from pathlib import Path
            from typing import Any
            
            import numpy as np
            import torch
            from torch.utils.data import DataLoader, TensorDataset, random_split
            from torchvision import datasets, transforms
            
            # FEDOPS CONTRACT - keep name/signature and return JSON-safe contract metadata.
            def describe_input_features() -> dict[str, Any]:
                """Describe normalized model features and labels without exposing local data."""
                return {
                    "features": [{
                        "name": "image",
                        "shape": [1, 28, 28],
                        "dtype": "float32",
                        "range": [-1.0, 1.0],
                        "normalization": {"mean": [0.5], "std": [0.5]},
                    }],
                    "label": {
                        "name": "digit",
                        "dtype": "int64",
                        "classes": list(range(10)),
                    },
                    "raw_data_upload": False,
                }
            
            # FEDOPS CONTRACT - keep name/signature; adapt the implementation for raw Task rows.
            def preprocess(sample: dict[str, Any]) -> torch.Tensor:
                """Input one raw image mapping; output one `[1, 28, 28]` float32 tensor."""
                image = transforms.ToTensor()(np.array(sample["image"], dtype=np.uint8, copy=True))
                return transforms.Normalize((0.5,), (0.5,))(image)
            
            # FEDOPS CONTRACT - keep name, signature, defaults, and three-loader return order.
            def load_partition(
                dataset: str,
                validation_split: float,
                batch_size: int,
                *,
                data_root: str,
                seed: int = 42,
                download: bool = False,
            ) -> tuple[DataLoader, DataLoader, DataLoader]:
                """Load local MNIST and return `(train, validation, test)` DataLoaders.
            
                `data_root` is a local Agent Studio binding. Its value and samples are never
                included in a Registry Release or Readiness result.
                """
                if dataset.upper() != "MNIST":
                    raise ValueError(f"This starter supports MNIST, received {dataset!r}")
                if not 0 < validation_split < 1:
                    raise ValueError("validation_split must be between 0 and 1")
                if batch_size < 1:
                    raise ValueError("batch_size must be at least 1")
                full_dataset = datasets.MNIST(
                    root=str(Path(data_root)),
                    train=True,
                    download=download,
                    transform=lambda image: preprocess({"image": image}),
                )
                validation_size = max(1, int(validation_split * len(full_dataset)))
                test_size = max(1, int(0.2 * len(full_dataset)))
                train_size = len(full_dataset) - validation_size - test_size
                if train_size < 1:
                    raise ValueError("validation_split leaves no samples for local training")
                generator = torch.Generator().manual_seed(seed)
                train_data, validation_data, test_data = random_split(
                    full_dataset,
                    [train_size, validation_size, test_size],
                    generator=generator,
                )
                return (
                    DataLoader(train_data, batch_size=batch_size, shuffle=True, generator=generator),
                    DataLoader(validation_data, batch_size=batch_size),
                    DataLoader(test_data, batch_size=batch_size),
                )
            
            # FEDOPS CONTRACT - keep name/signature; use no private or downloaded data here.
            def build_smoke_loaders(
                *, sample_count: int = 32, batch_size: int = 8, seed: int = 42
            ) -> tuple[DataLoader, DataLoader]:
                """Return synthetic `(train, validation)` loaders matching real MNIST batches."""
                if sample_count < 8:
                    raise ValueError("sample_count must be at least 8")
                generator = torch.Generator().manual_seed(seed)
                images = (torch.rand(sample_count, 1, 28, 28, generator=generator) * 2.0) - 1.0
                labels = torch.arange(sample_count, dtype=torch.long) % 10
                dataset = TensorDataset(images, labels)
                validation_size = max(2, sample_count // 4)
                train_size = sample_count - validation_size
                train_data, validation_data = random_split(
                    dataset,
                    [train_size, validation_size],
                    generator=torch.Generator().manual_seed(seed),
                )
                return (
                    DataLoader(
                        train_data,
                        batch_size=min(batch_size, train_size),
                        shuffle=True,
                        generator=torch.Generator().manual_seed(seed),
                    ),
                    DataLoader(validation_data, batch_size=min(batch_size, validation_size)),
                )
            
            # FEDOPS CONTRACT - keep name/signature; return model inputs only, without labels.
            def build_contract_probe(batch_size: int = 2) -> torch.Tensor:
                """Return a non-sensitive `[batch, 1, 28, 28]` model input probe."""
                if batch_size < 1:
                    raise ValueError("batch_size must be at least 1")
                return torch.zeros(batch_size, 1, 28, 28, dtype=torch.float32)
            
            # FEDOPS CONTRACT - keep name/signature; use owner-controlled server data only.
            def gl_model_torch_validation(
                batch_size: int,
                *,
                data_root: str,
                download: bool = False,
            ) -> DataLoader:
                """Return the owner-controlled server validation DataLoader."""
                dataset = datasets.MNIST(
                    root=str(Path(data_root)),
                    train=False,
                    download=download,
                    transform=lambda image: preprocess({"image": image}),
                )
                return DataLoader(dataset, batch_size=batch_size)
            ```
            
        - model.py
            
            ```python
            """Completed MNIST example of the fixed FedOps model contracts.
            
            The class name is Task-owned and may change in another Task. The three functions
            marked ``FEDOPS CONTRACT`` are called by the Baseline runtime and must retain their
            names, arguments, and return structures.
            """
            
            from __future__ import annotations
            
            from collections.abc import Mapping
            from typing import Any
            
            import torch
            from torch import nn
            import torch.nn.functional as functional
            
            # USER IMPLEMENTATION - model class name and internals are freely editable.
            class MNISTClassifier(nn.Module):
                def __init__(self, output_size: int = 10):
                    super().__init__()
                    self.conv1 = nn.Conv2d(1, 32, kernel_size=5, stride=1, padding=2)
                    self.conv2 = nn.Conv2d(32, 64, kernel_size=5, stride=1, padding=2)
                    self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
                    # Keep the FedOps 1.2 MNIST architecture checkpoint-compatible.
                    self.fc1 = nn.Linear(64 * 7 * 7, 1000)
                    self.fc2 = nn.Linear(1000, output_size)
            
                def forward(self, inputs: torch.Tensor) -> torch.Tensor:
                    values = self.pool(functional.relu(self.conv1(inputs)))
                    values = self.pool(functional.relu(self.conv2(values)))
                    values = torch.flatten(values, start_dim=1)
                    return self.fc2(functional.relu(self.fc1(values)))
            
            # FEDOPS CONTRACT - keep name/signature; replace the body for another Task model.
            def build_model(config: Mapping[str, Any] | None = None) -> MNISTClassifier:
                """Return a new model with parameters derived only from the model config.
            
                Input: the ``model`` mapping from ``conf/config.yaml``.
                Output: one new ``torch.nn.Module`` with a stable parameter structure.
                """
                model_config = config or {}
                return MNISTClassifier(output_size=int(model_config.get("output_size", 10)))
            
            # FEDOPS CONTRACT - keep name/signature; adapt only the Task input structure.
            def run_model(model: nn.Module, inputs: Any) -> Any:
                """Run a batched input and return raw `[batch, 10]` MNIST logits."""
                return model(inputs)
            
            # FEDOPS CONTRACT - keep name/signature; return JSON-safe metadata, not logits.
            def validate_model_output(output: Any, config: Mapping[str, Any]) -> dict[str, Any]:
                """Reject an invalid MNIST output and summarize the valid output contract."""
                expected_classes = int(config["model"].get("output_size", 10))
                if not isinstance(output, torch.Tensor):
                    raise ValueError("MNIST model output must be a torch.Tensor")
                if output.ndim != 2 or int(output.shape[1]) != expected_classes:
                    raise ValueError("MNIST model output must be [batch, output_size]")
                return {
                    "shape": [int(value) for value in output.shape],
                    "dtype": str(output.dtype).removeprefix("torch."),
                    "semantic": "digit-class-logits",
                }
            ```
            
        - training.py
            
            ```python
            """Completed MNIST local training and evaluation hooks."""
            
            from __future__ import annotations
            
            from collections.abc import Iterable
            
            import torch
            from torch import nn
            
            from ..runtime.progress import emit_evaluation_metrics, emit_training_metrics
            
            # FEDOPS CONTRACT - keep name/signature; update model in place and honor max_batches.
            def train_model(
                model: nn.Module,
                loader: Iterable,
                *,
                epochs: int,
                learning_rate: float,
                device: torch.device,
                max_batches: int | None = None,
            ) -> float:
                """Input model/local batches; output finite mean loss and leave model on CPU."""
                model.to(device)
                model.train()
                criterion = nn.CrossEntropyLoss()
                optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
                total_loss = 0.0
                completed = 0
                try:
                    batches_per_epoch = len(loader)  # type: ignore[arg-type]
                except TypeError:
                    batches_per_epoch = 0
                expected_batches = batches_per_epoch * epochs
                progress_total = min(expected_batches, max_batches) if max_batches and expected_batches else expected_batches
                for epoch_index in range(epochs):
                    for batch_index, (inputs, labels) in enumerate(loader, start=1):
                        inputs, labels = inputs.to(device), labels.to(device)
                        optimizer.zero_grad()
                        loss = criterion(model(inputs), labels)
                        loss.backward()
                        optimizer.step()
                        total_loss += float(loss.item())
                        completed += 1
                        emit_training_metrics(
                            completed_batches=completed,
                            total_batches=progress_total or completed,
                            metrics={"training_loss": total_loss / completed},
                            epoch=epoch_index + 1,
                            epochs=epochs,
                            batch=batch_index,
                            batches_per_epoch=batches_per_epoch or None,
                        )
                        if max_batches is not None and completed >= max_batches:
                            model.to("cpu")
                            return total_loss / completed
                model.to("cpu")
                return total_loss / max(1, completed)
            
            def _weighted_f1(labels: torch.Tensor, predictions: torch.Tensor) -> float:
                labels, predictions = labels.cpu(), predictions.cpu()
                if not labels.numel():
                    return 0.0
                total = 0.0
                for class_id in torch.unique(labels).tolist():
                    expected, predicted = labels == class_id, predictions == class_id
                    true_positive = int((expected & predicted).sum())
                    false_positive = int((~expected & predicted).sum())
                    false_negative = int((expected & ~predicted).sum())
                    support = int(expected.sum())
                    denominator = (2 * true_positive) + false_positive + false_negative
                    total += ((2 * true_positive / denominator) if denominator else 0.0) * support
                return total / int(labels.numel())
            
            # FEDOPS CONTRACT - keep name/signature and `(loss, primary, metrics)` return order.
            def evaluate_model(
                model: nn.Module,
                loader: Iterable,
                *,
                device: torch.device,
                max_batches: int | None = None,
            ) -> tuple[float, float, dict[str, float]]:
                """Return `(mean loss, accuracy, {weighted F1})` as finite Python floats."""
                model.to(device)
                model.eval()
                criterion = nn.CrossEntropyLoss()
                total_loss = 0.0
                total_samples = 0
                correct = 0
                completed = 0
                labels_seen: list[torch.Tensor] = []
                predictions_seen: list[torch.Tensor] = []
                try:
                    evaluation_batches = len(loader)  # type: ignore[arg-type]
                except TypeError:
                    evaluation_batches = 0
                progress_total = min(evaluation_batches, max_batches) if max_batches and evaluation_batches else evaluation_batches
                with torch.no_grad():
                    for batch_index, (inputs, labels) in enumerate(loader, start=1):
                        inputs, labels = inputs.to(device), labels.to(device)
                        outputs = model(inputs)
                        total_loss += float(criterion(outputs, labels).item())
                        predictions = outputs.argmax(dim=1)
                        total_samples += int(labels.size(0))
                        correct += int((predictions == labels).sum().item())
                        completed += 1
                        labels_seen.append(labels)
                        predictions_seen.append(predictions)
                        emit_evaluation_metrics(
                            completed_batches=completed,
                            total_batches=progress_total or completed,
                            metrics={
                                "validation_loss": total_loss / completed,
                                "accuracy": correct / max(1, total_samples),
                            },
                            batch=batch_index,
                        )
                        if max_batches is not None and completed >= max_batches:
                            break
                model.to("cpu")
                labels_tensor = torch.cat(labels_seen) if labels_seen else torch.empty(0, dtype=torch.long)
                predictions_tensor = (
                    torch.cat(predictions_seen) if predictions_seen else torch.empty(0, dtype=torch.long)
                )
                return (
                    total_loss / max(1, completed),
                    correct / max(1, total_samples),
                    {"f1_score": _weighted_f1(labels_tensor, predictions_tensor)},
                )
            ```
            
    - tool_ai/
        - manifest.json
            
            ```python
            {
              "schemaVersion": 2,
              "input": {
                "modality": "image",
                "sources": ["task-data", "manual"]
              },
              "description": "28x28 흑백 손글씨 이미지를 숫자 0부터 9까지 분류합니다.",
              "features": [
                "image"
              ],
              "output": {
                "description": "예측된 숫자 label과 confidence입니다.",
                "labels": [
                  "0",
                  "1",
                  "2",
                  "3",
                  "4",
                  "5",
                  "6",
                  "7",
                  "8",
                  "9"
                ]
              }
            }
            ```
            
        - tool.py
            
            ```python
            """Completed MNIST example of the fixed Agent Builder Tool AI contracts."""
            
            from __future__ import annotations
            
            from pathlib import Path
            import struct
            from typing import Any
            
            import torch
            
            from ..local_training.data_preparation import preprocess
            from ..runtime.model_release import MODEL_PATH, load_released_model
            
            # FEDOPS CONTRACT - keep name/signature and match manifest.json input/output.
            def predict(payload: dict[str, Any], model_path: str | Path | None = None) -> dict[str, Any]:
                """Input MNIST Tool JSON and return JSON-safe label/confidence values."""
                if not isinstance(payload, dict) or "image" not in payload:
                    raise ValueError("input must contain an image")
                selected_path = Path(model_path) if model_path else MODEL_PATH
                model = load_released_model(selected_path)
                model.eval()
                input_tensor = preprocess({"image": payload["image"]}).unsqueeze(0)
                with torch.no_grad():
                    probabilities = torch.softmax(model(input_tensor), dim=1)[0]
                label = int(probabilities.argmax().item())
                return {"label": label, "confidence": float(probabilities[label].item())}
            
            # FEDOPS CONTRACT - keep name/signature; use no local/private sample.
            def build_tool_smoke_payload() -> dict[str, Any]:
                """Return one safe JSON payload matching the Tool manifest input schema."""
                return {"image": [[0 for _ in range(28)] for _ in range(28)]}
            
            # FEDOPS OPTIONAL CONTRACT - keep this signature when Task Data inference is enabled.
            def build_tool_data_sample(data_root: str | Path, index: int = 0) -> dict[str, Any]:
                """Load one real MNIST image from the same folder used for local training."""
                root = Path(data_root)
                raw = next((candidate for candidate in (root / "MNIST" / "raw", root / "raw", root) if candidate.is_dir()), root)
                images = raw / "t10k-images-idx3-ubyte"
                labels = raw / "t10k-labels-idx1-ubyte"
                if not images.is_file():
                    raise FileNotFoundError("Copy the extracted MNIST raw files into the Task Data folder.")
                with images.open("rb") as stream:
                    magic, count, rows, columns = struct.unpack(">IIII", stream.read(16))
                    if magic != 2051 or count <= 0:
                        raise ValueError("The MNIST image file is invalid.")
                    selected = index % count
                    stream.seek(16 + selected * rows * columns)
                    pixels = list(stream.read(rows * columns))
                label = None
                if labels.is_file():
                    with labels.open("rb") as stream:
                        _, label_count = struct.unpack(">II", stream.read(8))
                        if label_count:
                            stream.seek(8 + selected)
                            raw_label = stream.read(1)
                            label = raw_label[0] if raw_label else None
                image = [pixels[offset:offset + columns] for offset in range(0, len(pixels), columns)]
                return {"payload": {"image": image}, "metadata": {"index": selected, "label": label}}
            ```
            
    - README.md
        
        ````markdown
        # Federated Task: MNIST classifier
        
        This starter preserves the FedOps 1.2 client/server execution contract and adds the
        FedOps 1.3 local-development, Registry Release, and Tool AI contracts. It can be
        developed locally, published as one immutable Release, and opened by another user in
        FedOps Agent Studio.
        
        ## How to use this example
        
        This directory is a completed reference for the blank Federated Task Baseline. It is
        not the default Baseline distributed to users. Compare these files in order:
        
        For a fresh Web Draft opened in Agent Studio, keep the Baseline runtime that Studio
        already downloaded. Copy only these MNIST Owner files into the new Workspace:
        
        ```text
        README.md
        requirements.txt
        federated_task/conf/config.yaml
        federated_task/local_training/data_preparation.py
        federated_task/local_training/model.py
        federated_task/local_training/training.py
        federated_task/tool_ai/manifest.json
        federated_task/tool_ai/tool.py
        ```
        
        Do not copy `pyproject.toml`, `uv.lock`, `model_release/`, `federated_learning/`,
        `runtime/`, `task_readiness/`, `main.py`, or `config.py`. Those files are supplied or
        generated by the current FedOps Baseline. This reference keeps them only so the MNIST
        case can also be executed independently.
        
        | Blank Baseline hook                                         | MNIST implementation                        | Fixed part                                             | Editable part                                |
        | ----------------------------------------------------------- | ------------------------------------------- | ------------------------------------------------------ | -------------------------------------------- |
        | `local_training/model.py:build_model`                     | Builds`MNISTClassifier`                   | Function name,`config` argument, module return       | Class name, layers, constructor values       |
        | `local_training/model.py:run_model`                       | Calls`model(inputs)`                      | Function name/arguments                                | How tuple/dict/tensor inputs enter the model |
        | `local_training/model.py:validate_model_output`           | Checks`[batch, 10]` logits                | JSON-safe summary return                               | Task-specific shape and semantic checks      |
        | `local_training/data_preparation.py:load_partition`       | Opens local MNIST and creates three loaders | Signature and`(train, validation, test)` order       | File format, split, Dataset, preprocessing   |
        | `local_training/data_preparation.py:build_smoke_loaders`  | Creates synthetic MNIST-shaped tensors      | No private data; two-loader return                     | Synthetic values for the Task contract       |
        | `local_training/data_preparation.py:build_contract_probe` | Creates`[batch, 1, 28, 28]` zeros         | Inputs-only return                                     | Task input structure, shape, dtype           |
        | `local_training/training.py:train_model`                  | Adam plus cross-entropy                     | Signature, finite loss, in-place update, CPU on return | Loss, optimizer, training loop               |
        | `local_training/training.py:evaluate_model`               | Accuracy and weighted F1                    | Three-value return structure                           | Task metrics and evaluation logic            |
        | `tool_ai/tool.py:predict`                                 | Returns digit label/confidence              | Signature and manifest-compatible JSON                 | Model inference and postprocessing           |
        | `tool_ai/tool.py:build_tool_smoke_payload`                | Returns a zero image                        | Safe manifest-compatible JSON                          | Task-specific example input                  |
        
        In the Python files, `FEDOPS CONTRACT` means the function name and signature are
        fixed. The function body demonstrates what a Task author replaces. `FEDOPS RUNTIME - DO NOT EDIT` marks shared release/FL adapter code. Helper functions and model classes
        without the contract marker may be renamed, added, or reorganized.
        
        The JSON file `federated_task/tool_ai/manifest.json` cannot contain comments. Its
        `features` are keys consumed by `tool.predict()`, while `output.description` and
        `output.labels` explain the result to Agent Builder.
        
        ## Intended use
        
        Classify normalized 28×28 grayscale handwritten digit images into labels 0–9. Replace
        the starter model and data adapter when creating a different Federated Task.
        
        ## Local data setup
        
        Raw data remains on the Agent Studio device. In `Workspace > Task Test`, select
        `Open Data Folder`, copy the prepared `MNIST/` directory into the opened Task-specific
        folder, and select Refresh. Local Train then receives that folder automatically. The
        release packager always excludes raw datasets and local paths.
        
        This repository-local test copy is already prepared at `../datasets/MNIST`. From this
        MNIST project directory, use `--data-root ../datasets` because torchvision appends the
        `MNIST/raw` directory itself.
        
        For the Agent Studio UI flow, copy `../datasets/MNIST` into the opened directory so
        the resulting layout is `dataset/MNIST/raw/*`.
        
        Expected input:
        
        - feature `image`: `float32`, shape `[1, 28, 28]`, normalized to `[-1, 1]`
        - label `digit`: `int64`, values `0`–`9`
        
        ## Local training
        
        ```bash
        uv sync --locked --link-mode copy
        uv run --locked --no-sync fedops-task local-train \
          --data-root "$FEDOPS_LOCAL_DATA_DIR"
        uv run --locked --no-sync fedops-task check-readiness --mode release
        ```
        
        Local training writes the versioned initial model to `model_release/`. It never uploads
        the dataset.
        
        ## Federated participation
        
        After downloading a Published Release, connect local data and run:
        
        ```bash
        uv run --locked --no-sync fedops-task check-readiness \
          --mode participation \
          --data-root "$FEDOPS_LOCAL_DATA_DIR"
        ```
        
        The readiness check constructs the actual FedOps client and uses the same parameter
        contract as `fedops.client.client_fl.FLClient`. Agent Studio enables participation only
        when local training changes that payload and its structure is compatible with the
        Published Release.
        
        The existing FedOps 1.2 entrypoints remain explicit:
        
        ```bash
        uv run --locked --no-sync fedops-task-client
        uv run --locked --no-sync fedops-task-client-manager
        uv run --locked --no-sync fedops-task-server
        ```
        
        FedOps Web and Agent Studio inject Task identity, local-data binding, server-manager
        address, and federated-server endpoint at runtime. Do not hard-code those values in the
        Release.
        
        ## Model use
        
        `federated_task.tool_ai.tool:predict` loads the selected Initial or Global
        Model and applies the same input normalization used by local training.
        
        ## Limitations
        
        The bundled architecture is an MNIST example, not a general-purpose vision model.
        Owners must document task-specific data quality, bias, safety, and evaluation limits
        before publishing a derived task.
        
        ## Privacy
        
        Raw samples, local filesystem paths, model updates, credentials, and signed download
        URLs are never included in a Federated Task Release. Only readiness status and contract
        fingerprints may be sent to FedOps Web.
        ````
        
- baseline/
    - conf/config.yaml
        
        ```yaml
        # Federated Task configuration (Baseline 0.10).
        #
        # Only values marked REQUIRED must be completed before Local Training and
        # Release Readiness. FedOps-owned schema, runtime, federation, and monitoring
        # defaults are supplied by federated_task/config.py and are not repeated here.
        
        # OPTIONAL: reproducible model initialization and data splitting.
        # Example: 42
        random_seed: 42
        
        # REQUIRED: model identity and constructor values.
        model:
          # REQUIRED: model name shown on the Registry card.
          # Example: MNIST Classifier
          display_name: replace-with-primary-model-name
        
          # OPTIONAL: values consumed by local_training/model.py build_model(config).
          # Add any Task-specific keys here. Example:
          # input_channels: 1
          # output_size: 10
        
        # REQUIRED: local-only participant data contract. Never put a filesystem path here.
        # Agent Studio creates and injects this Task's private directory at runtime:
        #   .local-data/federated-tasks/<local-project>/dataset/
        # Use Workspace > Task Test > Open Data Folder to place local files there.
        dataset:
          # REQUIRED: logical dataset or input-contract name.
          # Example: MNIST
          name: replace-with-dataset-name
        
          # REQUIRED: value greater than 0 and less than 1.
          # Example: 0.2 means 80% training and 20% validation.
          validation_split: 0.2
        
          # REQUIRED: whether data_preparation.py may download data when explicitly run.
          download: false
        
        # REQUIRED: defaults used by Local Training and each participant's local epoch.
        local_training:
          # Examples: 0.001, 1, 32
          learning_rate: 0.001
          epochs: 1
          batch_size: 32
        
        # OPTIONAL ADVANCED: cap aggregation-server Global Model evaluation for a
        # responsive server start and shorter rounds. The default is 8 batches.
        # Use `max_batches: null` only when every server evaluation must scan the
        # complete owner-controlled validation loader.
        # server_evaluation:
        #   max_batches: 8
        ```
        
    - local_training
        - data_preparation.py
            
            ```yaml
            """User-owned local-data adapter with fixed FedOps integration hooks.
            
            Raw data remains on the Agent Studio device. Keep every ``FEDOPS CONTRACT``
            function name, argument, default value, keyword-only marker, and return structure.
            Real and synthetic loaders must yield the same ``(inputs, targets)`` batch shape.
            """
            
            from __future__ import annotations
            
            from collections.abc import Mapping
            from typing import Any
            
            from torch.utils.data import DataLoader
            
            # FEDOPS CONTRACT - DO NOT RENAME OR CHANGE ARGUMENTS/RETURN TYPE.
            # EDIT HERE - document the exact feature and label contract as JSON-safe metadata.
            def describe_input_features() -> dict[str, Any]:
                """Describe model features, labels, shape, dtype, and preprocessing.
            
                Returns:
                    A JSON-serializable dictionary with at least ``features``, ``label``,
                    and ``raw_data_upload``. ``raw_data_upload`` must remain ``False``.
            
                Example implementation shape only::
            
                    {
                        "features": [{"name": "feature", "shape": [8], "dtype": "float32"}],
                        "label": {"name": "target", "dtype": "int64", "classes": [0, 1]},
                        "raw_data_upload": False,
                    }
                """
                raise NotImplementedError(
                    "Implement federated_task.local_training.data_preparation.describe_input_features()"
                )
            
            # FEDOPS CONTRACT - DO NOT RENAME OR CHANGE ARGUMENTS/RETURN TYPE.
            # EDIT HERE - convert one raw sample; never upload or report the source path.
            def preprocess(sample: Mapping[str, Any]) -> Any:
                """Convert one raw sample into the input structure expected by the model.
            
                Args:
                    sample: One sample read from the owner's or participant's local data.
            
                Returns:
                    A tensor, tuple/list of tensors, or mapping of tensors accepted by
                    ``run_model()`` and the training implementation.
            
                Example implementation for numeric features::
            
                    return torch.tensor(sample["features"], dtype=torch.float32)
                """
                del sample
                raise NotImplementedError(
                    "Implement federated_task.local_training.data_preparation.preprocess()"
                )
            
            # FEDOPS CONTRACT - DO NOT RENAME OR CHANGE ARGUMENTS/DEFAULTS/KEYWORD-ONLY MARKER.
            # EDIT HERE - open only the user-selected local data binding and create three loaders.
            def load_partition(
                dataset: str,
                validation_split: float,
                batch_size: int,
                *,
                data_root: str,
                seed: int = 42,
                download: bool = False,
            ) -> tuple[DataLoader, DataLoader, DataLoader]:
                """Load local data and return train, validation, and test loaders.
            
                Args:
                    dataset: Logical dataset name from ``conf/config.yaml``.
                    validation_split: Fraction reserved for local validation.
                    batch_size: Batch size for all returned loaders.
                    data_root: Agent Studio's Task-specific ``.local-data`` directory.
                        Treat this argument as the only dataset root; do not replace it with
                        a user-specific absolute path or a path inside the releaseable source.
                    seed: Deterministic split/shuffle seed.
                    download: Whether this Task explicitly permits downloading public data.
            
                Returns:
                    Exactly ``(train_loader, validation_loader, test_loader)``. Every batch
                    must have the form ``(inputs, targets)`` expected by ``training.py``.
            
                Example implementation outline::
            
                    # The user placed files with Workspace > Task Test > Open Data Folder.
                    # For example: Path(data_root) / "train.csv"
                    rows = read_local_rows(data_root)
                    dataset_object = TaskDataset(rows, transform=preprocess)
                    train_data, validation_data, test_data = deterministic_split(
                        dataset_object, validation_split, seed
                    )
                    return (
                        DataLoader(train_data, batch_size=batch_size, shuffle=True),
                        DataLoader(validation_data, batch_size=batch_size),
                        DataLoader(test_data, batch_size=batch_size),
                    )
                """
                del dataset, validation_split, batch_size, data_root, seed, download
                raise NotImplementedError(
                    "Implement federated_task.local_training.data_preparation.load_partition() with local-only data"
                )
            
            # FEDOPS CONTRACT - DO NOT RENAME OR CHANGE ARGUMENTS/DEFAULTS/KEYWORD-ONLY MARKER.
            # EDIT HERE - create non-sensitive fake data with the exact real batch contract.
            def build_smoke_loaders(
                *,
                sample_count: int = 32,
                batch_size: int = 8,
                seed: int = 42,
            ) -> tuple[DataLoader, DataLoader]:
                """Build non-sensitive synthetic loaders for Release Readiness.
            
                Returns:
                    Exactly ``(train_loader, validation_loader)`` with the same batch
                    structure, dtypes, and shapes as :func:`load_partition`.
            
                Do not read private data here. This hook proves the executable contract
                before a participant connects their own local dataset.
            
                Example outline: construct tensors with the same input/target shape and
                dtype as ``load_partition()``, wrap them in ``TensorDataset``, and return
                separate training and validation ``DataLoader`` objects.
                """
                del sample_count, batch_size, seed
                raise NotImplementedError(
                    "Implement federated_task.local_training.data_preparation.build_smoke_loaders()"
                )
            
            # FEDOPS CONTRACT - DO NOT RENAME OR CHANGE ARGUMENTS/DEFAULT VALUE.
            # EDIT HERE - return model inputs only, not labels and not private data.
            def build_contract_probe(batch_size: int = 2) -> Any:
                """Build one batched model input without reading real user data.
            
                Returns:
                    The exact input structure accepted by ``model.run_model()``. The first
                    dimension of tensor values should equal ``batch_size``.
            
                Example implementation for eight numeric features::
            
                    return torch.zeros(batch_size, 8, dtype=torch.float32)
                """
                del batch_size
                raise NotImplementedError(
                    "Implement federated_task.local_training.data_preparation.build_contract_probe()"
                )
            
            # FEDOPS CONTRACT - DO NOT RENAME OR CHANGE ARGUMENTS/DEFAULTS/KEYWORD-ONLY MARKER.
            # EDIT HERE - use only owner-controlled/licensed server validation data.
            def gl_model_torch_validation(
                batch_size: int,
                *,
                data_root: str,
                download: bool = False,
            ) -> DataLoader:
                """Load the aggregation server's permitted global-validation dataset.
            
                Returns:
                    One ``DataLoader`` with the same ``(inputs, targets)`` batch contract.
            
                This must not depend on a participant's private dataset. Use only an
                owner-controlled or explicitly licensed central validation source.
            
                Example outline: open the permitted validation dataset below ``data_root``,
                apply the same preprocessing, and return one non-shuffled ``DataLoader``.
                """
                del batch_size, data_root, download
                raise NotImplementedError(
                    "Implement federated_task.local_training.data_preparation.gl_model_torch_validation()"
                )
            ```
            
        - model.py
            
            ```yaml
            """User-owned model definition with fixed FedOps integration hooks.
            
            Add model classes and helpers freely. Functions marked ``FEDOPS CONTRACT`` are
            imported by local training, Readiness, clients, servers, and Tool inference; keep
            their names, arguments, and return structures and replace only their bodies.
            """
            
            from __future__ import annotations
            
            from collections.abc import Mapping
            from typing import Any
            
            from torch import nn
            
            # USER IMPLEMENTATION ---------------------------------------------------------
            # Add the Task's torch.nn.Module class above or below this marker.
            # Example only:
            #
            # class TaskModel(nn.Module):
            #     def __init__(self, input_size: int, output_size: int):
            #         super().__init__()
            #         self.network = nn.Linear(input_size, output_size)
            #
            #     def forward(self, inputs):
            #         return self.network(inputs)
            
            # FEDOPS CONTRACT - DO NOT RENAME OR CHANGE ARGUMENTS/RETURN TYPE.
            # EDIT HERE - replace only this implementation body and add helpers as needed.
            def build_model(config: Mapping[str, Any] | None = None) -> nn.Module:
                """Build a new model instance with the Federated Task architecture.
            
                Args:
                    config: The ``model`` object from ``conf/config.yaml``.
            
                Returns:
                    A new ``torch.nn.Module``. Every owner, participant, and aggregation
                    server must construct the same parameter names, shapes, and dtypes.
            
                Implementation guidance:
                    Define the model class in this file (or import it from another source
                    file) and return it here. Do not load participant data or contact the
                    FedOps server in this function.
            
                Example implementation::
            
                    values = config or {}
                    return TaskModel(
                        input_size=int(values.get("input_size", 8)),
                        output_size=int(values.get("output_size", 2)),
                    )
                """
                del config
                raise NotImplementedError(
                    "Implement federated_task.local_training.model.build_model() with the Task model architecture"
                )
            
            # FEDOPS CONTRACT - DO NOT RENAME OR CHANGE ARGUMENTS/RETURN TYPE.
            # EDIT HERE - adapt only how this Task passes its input structure to the model.
            def run_model(model: nn.Module, inputs: Any) -> Any:
                """Run one forward pass for readiness and Tool-compatible validation.
            
                Args:
                    model: A model returned by :func:`build_model`.
                    inputs: One batched value returned by ``build_contract_probe()``.
            
                Returns:
                    The raw model output. For one tensor input this is normally
                    ``model(inputs)``. For multiple inputs it may be
                    ``model(*inputs)`` or ``model(**inputs)``.
            
                Example implementation for one tensor input::
            
                    return model(inputs)
                """
                del model, inputs
                raise NotImplementedError(
                    "Implement federated_task.local_training.model.run_model() for the Task input structure"
                )
            
            # FEDOPS CONTRACT - DO NOT RENAME OR CHANGE ARGUMENTS/RETURN TYPE.
            # EDIT HERE - validate the Task-specific output without returning tensor values.
            def validate_model_output(output: Any, config: Mapping[str, Any]) -> dict[str, Any]:
                """Validate a probe output and return a JSON-serializable summary.
            
                Args:
                    output: The result of :func:`run_model` for a batched contract probe.
                    config: The complete Task configuration.
            
                Returns:
                    A JSON-serializable dictionary describing the verified output, for
                    example ``{"shape": [2, 10], "dtype": "float32"}``.
            
                Raise ``ValueError`` when the output cannot satisfy the Task's documented
                output contract.
            
                Example implementation for ``[batch, classes]`` logits::
            
                    expected = int(config["model"]["output_size"])
                    if output.ndim != 2 or output.shape[1] != expected:
                        raise ValueError("model output must be [batch, output_size]")
                    return {"shape": list(output.shape), "dtype": str(output.dtype)}
                """
                del output, config
                raise NotImplementedError(
                    "Implement federated_task.local_training.model.validate_model_output() for readiness"
                )
            ```
            
        - training.py
            
            ```yaml
            """Task-owner local training and evaluation hooks."""
            
            from __future__ import annotations
            
            from collections.abc import Iterable
            
            import torch
            from torch import nn
            
            from ..runtime.progress import emit_evaluation_metrics, emit_training_metrics
            
            # Add Task-specific losses, metrics, and optimizer helpers in this file.
            
            # FEDOPS CONTRACT - DO NOT RENAME OR CHANGE ARGUMENTS/RETURN TYPE.
            # EDIT HERE - update ``model`` in place and honor ``max_batches`` when provided.
            def train_model(
                model: nn.Module,
                loader: Iterable,
                *,
                epochs: int,
                learning_rate: float,
                device: torch.device,
                max_batches: int | None = None,
            ) -> float:
                """Train ``model`` with local batches and return the mean training loss.
            
                Args:
                    model: The local model to update in place.
                    loader: Batches shaped as ``(inputs, targets)``.
                    epochs: Number of local epochs.
                    learning_rate: Effective local learning rate.
                    device: Selected CPU, CUDA, or accelerator device.
                    max_batches: Optional readiness-only limit; honor it when provided.
            
                Returns:
                    One finite ``float`` representing mean training loss. Move the model
                    back to CPU before returning so FedOps can serialize its parameters.
            
                Example implementation outline::
            
                    model.to(device).train()
                    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
                    for epoch_index in range(epochs):
                        for batch_index, (inputs, targets) in enumerate(loader, start=1):
                            # move values to device, compute loss, backward, and optimizer.step()
                            # stop once max_batches is reached when it is not None
                            # Optionally publish live metrics without changing this hook:
                            # emit_training_metrics(
                            #     completed_batches=completed,
                            #     total_batches=expected_batches,
                            #     metrics={"training_loss": float(mean_loss)},
                            #     epoch=epoch_index + 1,
                            #     epochs=epochs,
                            #     batch=batch_index,
                            # )
                            ...
                    model.to("cpu")
                    return float(mean_loss)
                """
                del model, loader, epochs, learning_rate, device, max_batches
                raise NotImplementedError(
                    "Implement federated_task.local_training.training.train_model() with the Task loss and optimizer"
                )
            
            # FEDOPS CONTRACT - DO NOT RENAME OR CHANGE ARGUMENTS/RETURN TYPE.
            # EDIT HERE - use the Task's loss and documented primary/additional metrics.
            def evaluate_model(
                model: nn.Module,
                loader: Iterable,
                *,
                device: torch.device,
                max_batches: int | None = None,
            ) -> tuple[float, float, dict[str, float]]:
                """Evaluate a model and return the fixed FedOps evaluation tuple.
            
                Returns:
                    Exactly ``(loss, primary_metric, additional_metrics)`` where the first
                    two values are finite floats and ``additional_metrics`` is a mapping of
                    metric names to finite float values. The primary metric may be accuracy,
                    F1, MAE, RMSE, or another Task-appropriate measure documented in README.
            
                Example return::
            
                    return float(mean_loss), float(accuracy), {"weighted_f1": float(f1)}
            
                During the evaluation loop, ``emit_evaluation_metrics(...)`` may be used
                to show live validation loss and primary-metric graphs in Agent Studio.
                """
                del model, loader, device, max_batches
                raise NotImplementedError(
                    "Implement federated_task.local_training.training.evaluate_model() with Task metrics"
                )
            ```
            
    - tool_ai
        - manifest.json
            
            ```yaml
            {
              "schemaVersion": 2,
              "input": {
                "modality": "replace_with_modality",
                "sources": ["task-data", "manual"]
              },
              "description": "Initial 또는 Global Model을 Tool AI로 사용할 때의 동작을 설명하세요.",
              "features": [
                "replace_with_feature_name"
              ],
              "output": {
                "description": "모델이 반환하는 값의 의미를 설명하세요.",
                "labels": []
              }
            }
            ```
            
        - tool.py
            
            ```yaml
            """User-owned Agent Builder Tool AI hooks with fixed JSON contracts."""
            
            from __future__ import annotations
            
            from pathlib import Path
            from typing import Any
            
            # FEDOPS CONTRACT - DO NOT RENAME OR CHANGE ARGUMENTS/RETURN TYPE.
            # EDIT HERE - keep implementation consistent with manifest.json and local training.
            def predict(payload: dict[str, Any], model_path: str | Path | None = None) -> dict[str, Any]:
                """Run one inference with an Initial or Global Model release.
            
                Args:
                    payload: JSON object containing every feature named in ``manifest.json``.
                    model_path: Optional selected model artifact. When omitted, load the
                    Task's local ``model_release/model.safetensors`` artifact.
            
                Returns:
                    A JSON-serializable dictionary matching the Tool manifest output.
            
                Use ``data_preparation.preprocess()`` and
                ``training.load_released_model()`` so local training, federated learning,
                and Agent Builder inference use one model and preprocessing contract.
            
                Example implementation outline::
            
                    model = load_released_model(Path(model_path) if model_path else MODEL_PATH)
                    inputs = preprocess(payload)
                    output = run_model(model, add_batch_dimension(inputs))
                    return {"prediction": convert_to_json_value(output)}
                """
                del payload, model_path
                raise NotImplementedError(
                    "Implement federated_task.tool_ai.tool.predict() and match manifest.json"
                )
            
            # FEDOPS CONTRACT - DO NOT RENAME OR CHANGE ARGUMENTS/RETURN TYPE.
            # EDIT HERE - return safe example JSON matching manifest.json input.
            def build_tool_smoke_payload() -> dict[str, Any]:
                """Return one non-sensitive JSON payload accepted by :func:`predict`.
            
                Example implementation::
            
                    return {"features": [0.0] * 8}
                """
                raise NotImplementedError(
                    "Implement federated_task.tool_ai.tool.build_tool_smoke_payload()"
                )
            
            # FEDOPS OPTIONAL CONTRACT - keep this signature to use Task Data in Agent Builder.
            # EDIT HERE - read one record from data_root and return the exact predict() payload.
            def build_tool_data_sample(data_root: str | Path, index: int = 0) -> dict[str, Any]:
                """Convert one local training-data record into a Tool AI inference payload.
            
                Return ``{"payload": {...}, "metadata": {...}}``. The payload must match
                ``manifest.json`` and :func:`predict`. Metadata may contain an index or
                label for local inspection, but is never sent to FedOps Web.
                """
                del data_root, index
                raise NotImplementedError(
                    "Implement build_tool_data_sample(data_root, index) to connect Task Data inference"
                )
            ```
            
    - README.md
        
        ````yaml
        # Federated Task: replace with Task name
        
        This Workspace is a contract template, not a runnable MNIST example. Replace only the
        documented user-editable parts. FedOps Web, Agent Studio, the aggregation server, and
        participants call the fixed names and arguments exactly as shown below.
        
        ## Start here
        
        For a new model and dataset, edit in this order:
        
        1. In Agent Studio `Workspace > Task Test`, select `Open Data Folder` and place the
           private dataset in the automatically prepared Task directory. This directory is
           outside the releaseable source tree.
        2. `federated_task/conf/config.yaml`: complete the clearly marked model, data-contract,
           and local-training values. FedOps supplies fixed runtime defaults, while Web Server
           Management supplies the actual rounds/clients/strategy for each Campaign.
        3. `requirements.txt`: list each Python library as `library==version`.
        4. `federated_task/local_training/model.py`: define the one Task model shared by local
           training, federated learning, and Tool AI.
        5. `federated_task/local_training/data_preparation.py`: bind local data and create identical batch
           structures for real data and non-sensitive readiness probes.
        6. `federated_task/local_training/training.py`: implement local training, loss, and evaluation metrics.
           The FedOps runtime always reports batch progress. Call the documented
           `emit_training_metrics(...)` and `emit_evaluation_metrics(...)` helpers inside
           your loops to add live loss and accuracy graphs without changing hook signatures.
        7. `federated_task/tool_ai/manifest.json` and `federated_task/tool_ai/tool.py`: define and implement
           Agent Builder Tool inference.
        8. `README.md`: replace this guide with the Registry Task Card while retaining the
           required Registry sections listed below.
        
        Search the Python files for these markers:
        
        - `FEDOPS CONTRACT - DO NOT RENAME`: keep the function name, arguments, and return
          structure. Replace only its implementation body.
        - `USER IMPLEMENTATION`: model/data/training/Tool code that the Task author owns.
        - Files under `federated_learning/`, `task_readiness/`, and `runtime/` are FedOps-managed
          integration code. Normal Task development must not modify them.
        
        You may add helper classes, helper functions, and new source files. Do not rename or
        remove the fixed hooks because local training, Readiness, the FL client/server, and
        Agent Builder import them directly.
        
        ## Directory ownership
        
        ```text
        federated_task/
        ├── conf/                 # EDIT: Task configuration values
        ├── local_training/       # EDIT: model, local data, training, evaluation
        ├── tool_ai/              # EDIT: Tool description and inference
        ├── federated_learning/   # DO NOT EDIT: FedOps client/manager/server adapters
        ├── task_readiness/       # DO NOT EDIT: Release/Participation checks
        ├── runtime/              # DO NOT EDIT: Model Release and callback adapters
        ├── config.py             # DO NOT EDIT: config and Campaign overlay loader
        └── main.py               # DO NOT EDIT: Task CLI
        ````
        
        The model lives under `local_training/` because that is where the Owner implements it;
        it is not local-only. The same model definition is imported by local training, the
        federated client/server, Readiness, and Tool AI. Do not create a second federated or
        Tool-specific model definition.
        
        ## What can be edited
        
        | File | User action | Fixed boundary |
        | --- | --- | --- |
        | `README.md` | Replace Task description and usage | Keep `Intended use`, `Local data setup`, `Federated participation`, `Limitations`, and `Privacy` headings |
        | `conf/config.yaml` | Replace Primary Model, dataset contract, and local-training defaults | Keep required keys; runtime Campaign and local paths are injected |
        | `requirements.txt` | Add or change exact Task library versions using `library==version` | Keep one dependency contract for every Python Environment |
        | `local_training/model.py` | Add model class and implement three hooks | Hook names, arguments, and return contracts |
        | `local_training/data_preparation.py` | Implement feature description, local loaders, probes, and server validation loader | Six hook names, arguments, local-data boundary, and batch contract |
        | `local_training/training.py` | Implement `train_model` and `evaluate_model` | Function names, signatures, and return contracts |
        | `tool_ai/manifest.json` | Replace Tool description, feature names, output description, and labels | `description`, `features`, and `output` JSON structure |
        | `tool_ai/tool.py` | Implement Tool inference and one smoke input | Two hook names, arguments, and JSON-compatible returns |
        | `pyproject.toml` | No normal Task edits | FedOps package metadata, scripts, dependency hook, and `[tool.fedops.task]` paths |
        | `uv.lock` | Regenerate through Agent Studio Environment Sync | Never edit manually |
        | `model_release/manifest.json` | No manual editing | Generated by `local-train` together with `model.safetensors` |
        | `federated_learning/`, `task_readiness/`, `runtime/`, `main.py`, `config.py` | No normal Task edits | FedOps runtime integration |
        
        ## Fixed Python contracts
        
        The examples below describe shape only; complete annotated examples are also placed
        directly above each implementation gap in the corresponding Python file.
        
        | Function | Input | Required output |
        | --- | --- | --- |
        | `build_model(config)` | `model` mapping from YAML | A new `torch.nn.Module` with the same parameter names/shapes/dtypes on every device |
        | `run_model(model, inputs)` | Model plus one batched input structure | Raw model output |
        | `validate_model_output(output, config)` | Raw probe output plus full config | JSON-serializable output summary; raise `ValueError` on mismatch |
        | `describe_input_features()` | None | JSON-serializable feature/label description with `raw_data_upload: false` |
        | `preprocess(sample)` | One raw sample mapping | Tensor, tuple/list of tensors, or tensor mapping accepted by the model |
        | `load_partition(dataset, validation_split, batch_size, *, data_root, seed=42, download=False)` | Local data binding and split settings | Exactly `(train_loader, validation_loader, test_loader)` |
        | `build_smoke_loaders(*, sample_count=32, batch_size=8, seed=42)` | Non-sensitive sample settings | Exactly `(train_loader, validation_loader)` with the real batch format |
        | `build_contract_probe(batch_size=2)` | Probe batch size | One non-sensitive batched model input |
        | `gl_model_torch_validation(batch_size, *, data_root, download=False)` | Owner-controlled server data binding | Server validation `DataLoader` |
        | `train_model(model, loader, *, epochs, learning_rate, device, max_batches=None)` | Model and local batches | Finite mean loss `float`; update model in place and return it to CPU |
        | `evaluate_model(model, loader, *, device, max_batches=None)` | Model and evaluation batches | Exactly `(loss, primary_metric, additional_metrics)` with finite floats |
        | `predict(payload, model_path=None)` | Tool JSON payload and optional Model Release | JSON object matching `manifest.json` output |
        | `build_tool_smoke_payload()` | None | Non-sensitive JSON input accepted by `predict` |
        
        Keyword-only markers (`*`) are part of the signature. Do not remove them. Default
        values may not be changed because Agent Studio and Readiness call these functions
        without inspecting Task-specific code.
        
        ## Contracts that must agree
        
        One edit often affects several files:
        
        - `build_model()` defines the authoritative parameters transported by FedOps. Do not
          implement separate parameter packing in this Workspace.
        - A batch from `load_partition()` must be `(inputs, targets)`. `inputs` must have the
          same structure as `build_contract_probe()` and be accepted by `run_model()` and the
          training implementation.
        - `build_smoke_loaders()` must use the same shapes and dtypes as real local data but
          must not read or copy participant data.
        - `predict()` must apply the same preprocessing and load the same model architecture
          used by local and federated training.
        - Every name in `tool_ai/manifest.json` `features` must exist in the payload consumed by
          `predict()`. `output.description` and `output.labels` describe its result to Agent Builder.
        - Model constructor settings in `conf/config.yaml` must match `build_model(config)`.
        - `model.display_name` is the Registry-facing Primary Model name. It is not a global
          identifier; `@owner/task-slug` identifies the Federated Task.
        - Do not add local data paths, Task IDs, ports, server endpoints, or credentials to
          `config.yaml`. Agent Studio and Web inject those values at execution time.
        
        ## Intended use
        
        TODO: Describe the problem, intended users, Initial/Global Model behavior, and the
        primary evaluation metric.
        
        ## Local data setup
        
        TODO: Document expected local files, columns/features, labels, shapes, dtypes,
        preprocessing, and train/validation/test split. Raw data must remain on the Agent
        Studio device and is supplied through `--data-root` or `FEDOPS_LOCAL_DATA_DIR`.
        
        Agent Studio prepares the physical directory automatically when this Task is opened:
        
        ```text
        <fedops-workspace>/accounts/<account-key>/.local-data/
        └── federated-tasks/<local-project>/dataset/   # Open Data Folder
        ```
        
        Do not create a `dataset/` or `datasets/` directory inside this Baseline. Local Train
        and Participation Readiness receive the prepared directory as `data_root`, and
        `local_training/data_preparation.py` must read only from that argument. In this Task
        Card, replace the example below with the layout users must place inside the opened
        folder:
        
        ```text
        dataset/
        ├── train.csv       # example only
        └── test.csv        # example only
        ```
        
        Do not include raw data, credentials, or a user-specific absolute path in a Registry
        Release.
        
        ## Local development
        
        Add Task dependencies to `requirements.txt` using one `library==version` entry per
        line. Agent Studio Environment Sync reads that single file and updates `uv.lock` for
        the selected Python Environment. Do not edit `pyproject.toml` or `uv.lock` by hand.
        
        After implementing all marked contracts:
        
        ```bash
        uv sync --link-mode copy
        uv run fedops-task local-train --data-root "$FEDOPS_LOCAL_DATA_DIR"
        uv run fedops-task tool-test
        uv run fedops-task check-readiness --mode release
        ```
        
        Unimplemented contracts stop with a specific `NotImplementedError`; a blank starter
        cannot accidentally pass Release Readiness.
        
        ## Federated participation
        
        After opening a Published Release, a participant binds their own local data and runs:
        
        ```bash
        uv run --locked --no-sync fedops-task check-readiness \
          --mode participation \
          --data-root "$FEDOPS_LOCAL_DATA_DIR"
        ```
        
        Participation Readiness verifies the actual local loader, local training update,
        FedOps parameter signature, model input/output contract, and Tool inference without
        uploading raw data or parameter values.
        
        ## Model and Tool release
        
        `local-train` writes `model_release/model.safetensors` and replaces the draft model
        manifest with checksum, size, parameter signature, provenance, and evaluation metrics.
        Agent Studio shows fixed-stage progress automatically. Task training code may emit
        live named metrics through `runtime.progress`; these machine-readable events are kept
        out of the normal log and rendered as metric cards and charts.
        Update `federated_task/tool_ai/manifest.json` and `tool.py` together so Agent Builder
        receives the same feature names and output meaning implemented by the Tool adapter.
        
        ## Limitations
        
        TODO: Document known model, population, data-quality, bias, safety, latency, hardware,
        and out-of-distribution limitations.
        
        ## Privacy
        
        Raw samples, local filesystem paths, credentials, signed download URLs, and model
        parameter values must not be included in the Federated Task Release or readiness
        metadata. Only source/model checksums, parameter-structure fingerprints, metrics, and
        pass/fail status may leave the local device.
        
        ````
        
            - requirements.txt
        
        ```yaml
        # Federated Task Python dependencies.
        #
        # Use one `library==version` entry per line. Agent Studio validates this file,
        # resolves transitive dependencies into uv.lock, and installs the same contract
        # into every selected Python Environment.
        fedops==1.1.30.15
        fastapi==0.116.1
        hydra-core==1.3.2
        numpy==1.26.4
        omegaconf==2.3.0
        packaging==25.0
        pyyaml==6.0.2
        requests==2.32.4
        safetensors==0.6.2
        torch==2.8.0
        torchvision==0.23.0
        uvicorn==0.35.0
        ````
        


</details>

![image.png]({{ '/assets/images/v1.3/developer-guide/image.png' | relative_url }})

## 1. 수정할 파일

Federated Task를 작성할 때 주로 수정하는 파일은 다음과 같습니다.

| 파일 | 작성 내용 |
| --- | --- |
| federated_task/conf/config.yaml | 모델 생성값, 데이터 설정, 로컬 학습 기본값 |
| federated_task/local_training/data_preparation.py | 로컬 데이터 로드와 전처리 관련 함수 |
| federated_task/local_training/model.py | PyTorch 모델과 모델 관련 함수 |
| federated_task/local_training/training.py | 로컬 학습과 평가 함수 |
| federated_task/tool_ai/manifest.json | Agent Builder에서 사용할 Tool AI의 입력·출력 정보 |
| federated_task/tool_ai/tool.py | Model Release를 이용한 추론 함수 |
| requirements.txt | 필요한 라이브러리와 버전 |
| README.md | Registry에 표시할 Task 설명과 데이터 배치 방법 |

다음 파일과 디렉터리는 FedOps에서 관리하므로 직접 수정하지 않습니다.

```
federated_task/federated_learning/
federated_task/runtime/
federated_task/task_readiness/
federated_task/main.py
federated_task/config.py
pyproject.toml
uv.lock
model_release/
```

FEDOPS CONTRACT로 표시된 함수는 함수 이름, 인자 순서, 기본값, 키워드 전용 인자를 구분하는 *, 반환 형식을 변경하지 않습니다.

함수 내부 구현과 사용자 모델 클래스의 이름 및 내부 구조는 Task에 맞게 작성할 수 있습니다.

## 2. 로컬 데이터 준비

Agent Studio에서 다음 메뉴를 선택하여 해당 Task의 데이터 폴더를 엽니다.

```
Workspace > Task Test > Open Data Folder
```

이 폴더는 Task 코드와 분리된 계정별 로컬 영역에 위치합니다.

```
<fedops-workspace>/accounts/<account>/.local-data/
└── federated-tasks/<project>/dataset/
```

사용자는 dataset 폴더 안에 Task에서 요구하는 데이터를 배치합니다.

예를 들어 train.csv와 test.csv를 사용하는 Task라면 다음과 같이 구성할 수 있습니다.

```
dataset/
├── train.csv
└── test.csv
```

필요한 데이터 구조는 README.md에 작성하고, 실제 파일 로드는 local_training/data_preparation.py의 load_partition 함수에서 구현합니다.

```python
def load_partition(..., *, data_root: str, ...):
    root = Path(data_root)

    train_file = root / "train.csv"
    test_file = root / "test.csv"

    # 파일 읽기
    # 전처리
    # Dataset 생성
    # DataLoader 생성
```

Agent Studio가 선택된 Data Folder를 data_root로 전달하므로 로컬 데이터의 절대경로를 코드나 config.yaml에 직접 작성하지 않습니다.

같은 load_partition 함수는 다음 작업에서 사용됩니다.

```
Local Train
Participation Readiness
Federated Learning Client
```

원본 데이터와 로컬 경로는 Web, Registry 또는 Release에 포함되지 않아야 합니다.

## 3. config.yaml

![image.png]({{ '/assets/images/v1.3/developer-guide/image-1.png' | relative_url }})

다음 키는 유지하고 값만 Task에 맞게 작성합니다.

```yaml
random_seed: 42

model:
  display_name: My Model
  # build_model()에 필요한 값을 추가
  input_size: 8
  output_size: 2

dataset:
  name: My Dataset
  validation_split: 0.2
  download: false

local_training:
  learning_rate: 0.001
  epochs: 1
  batch_size: 32
```

- model의 추가 값은 build_model(config)가 사용합니다.
- dataset.name은 논리적인 데이터 이름입니다. 파일 경로가 아닙니다.
- 참여 클라이언트 수, FL Round, 집계 전략은 여기 적지 않습니다. FedOps Web의 Campaign/Server Management에서 설정합니다.
- Task ID, 서버 주소, 포트, 로컬 절대경로, 인증정보를 넣지 않습니다.

## 4. data_preparation.py

![image.png]({{ '/assets/images/v1.3/developer-guide/image-2.png' | relative_url }})

| 고정 함수 | 반드시 지킬 계약 |
| --- | --- |
| describe_input_features() -> dict | feature·label·shape·dtype을 JSON dict로 반환하고 raw_data_upload는 False |
| preprocess(sample) -> Any | 원본 샘플 하나를 모델 입력 Tensor/tuple/dict로 변환 |
| load_partition(dataset, validation_split, batch_size, *, data_root, seed=42, download=False) | data_root만 읽고 정확히 (train, validation, test) DataLoader 반환 |
| build_smoke_loaders(*, sample_count=32, batch_size=8, seed=42) | 실제 데이터 없이 같은 shape·dtype의 (train, validation) DataLoader 반환 |
| build_contract_probe(batch_size=2) -> Any | label 없는 비민감 배치 입력 반환 |
| gl_model_torch_validation(batch_size, *, data_root, download=False) | Owner가 허용한 서버 검증 데이터의 DataLoader 반환 |

모든 DataLoader 배치는 기본적으로 다음 형식이어야 합니다.

```python
(inputs, targets)
```

inputs의 구조는 preprocess(), build_contract_probe(), run_model()에서 모두 같아야 합니다. build_smoke_loaders()에는 실제 참여자 데이터를 사용하지 않습니다.

gl_model_torch_validation()도 참여자의 비공개 데이터가 아니라 Owner가 통제하거나 사용 허가를 받은 집계 서버 측 검증 데이터만 사용합니다. 참여자 Data Folder는 집계 서버로 전달되지 않습니다.

## 5. model.py

![image.png]({{ '/assets/images/v1.3/developer-guide/image-3.png' | relative_url }})

모델 클래스 이름과 내부 구조는 자유롭게 작성합니다. 아래 함수 3개는 고정입니다.

| 함수 | 입력 | 반드시 반환할 값 |
| --- | --- | --- |
| build_model(config=None) | config.yaml의 model 객체 | 새 torch.nn.Module |
| run_model(model, inputs) | 모델과 배치 입력 | 모델의 원시 출력(logits 등) |
| validate_model_output(output, config) | 원시 출력과 전체 설정 | JSON으로 변환 가능한 출력 요약 dict |

중요한 조건

- Owner, 참여자, 집계 서버가 만든 모델의 파라미터 이름·shape·dtype이 모두 같아야 합니다.
- build_model()에서 데이터를 읽거나 서버에 접속하지 않습니다.
- 입력이 여러 개라면 run_model()에서 model(*inputs) 또는 model(**inputs)처럼 연결합니다.
- validate_model_output()은 출력 shape가 계약과 다르면 ValueError를 발생시킵니다.

## 6. training.py

![image.png]({{ '/assets/images/v1.3/developer-guide/image-4.png' | relative_url }})

```python
train_model(
    model, loader, *, epochs, learning_rate, device, max_batches=None
) -> float
```

- 전달받은 model을 제자리에서 학습합니다.
- max_batches가 있으면 반드시 그 수에서 중단합니다.
- 종료 전에 모델을 CPU로 옮깁니다.
- 유한한 평균 학습 loss 한 개를 Python float로 반환합니다.

```python
evaluate_model(
    model, loader, *, device, max_batches=None
) -> tuple[float, float, dict[str, float]]
```

정확히 다음 순서로 반환합니다.

```python
(평균_loss, primary_metric, 추가_metric_dict)
```

예: (0.12, 0.95, {"f1_score": 0.94}). 모든 값은 유한한 Python float여야 합니다. 학습 진행 그래프가 필요하면 기존 emit_training_metrics()와 emit_evaluation_metrics() 호출을 학습·평가 반복문 안에 둡니다.

## 7. Manifest.json

![image.png]({{ '/assets/images/v1.3/developer-guide/image-5.png' | relative_url }})

tool_ai/manifest.json에는 Agent Builder가 모델을 호출하는 데 필요한 정보를 작성합니다.

```json
{
  "schemaVersion": 2,
  "input": {"modality": "tabular", "sources": ["task-data", "manual"]},
  "description": "이 모델이 하는 일",
  "features": ["feature_a", "feature_b"],
  "output": {"description": "예측값의 의미", "labels": []}
}
```

## 8. Tool.py

![image.png]({{ '/assets/images/v1.3/developer-guide/image-6.png' | relative_url }})

tool.py의 고정 계약:

| 함수 | 계약 |
| --- | --- |
| predict(payload, model_path=None) | manifest의 feature를 입력받아 JSON dict 반환 |
| build_tool_smoke_payload() | 실제 데이터가 아닌 안전한 테스트 payload 반환 |
| build_tool_data_sample(data_root, index=0) | 선택한 로컬 데이터 한 건을 {"payload": {...}, "metadata": {...}}로 변환하는 선택 계약 |

predict()는 로컬학습과 같은 preprocess()와 같은 모델 구조를 사용해야 합니다.

학습용 모델과 Tool 전용 모델을 따로 만들지 않습니다. manifest의 sources에 task-data를 두고 로컬 데이터 기반 추론을 제공하려면 build_tool_data_sample()도 구현합니다.

## 9. requirements.txt

requirements.txt는 한 줄에 하나씩 정확한 버전을 적습니다.

```
torch==2.8.0
numpy==1.26.4
```

환경 설치는 Agent Studio의 Sync Environment가 담당합니다. uv.lock과 pyproject.toml은 직접 수정하지 않습니다.

## 10. Readme.md

README.md에는 최소한 다음 내용을 작성합니다.

- 모델의 목적과 주요 성능 지표
- 사용자가 Data Folder에 넣을 정확한 파일·디렉터리 구조
- feature, label, shape, dtype과 전처리 방식
- 로컬학습 및 연합학습 참여 방법
- 모델의 한계와 개인정보 보호 주의사항

README.md 파일은 반드시 아래의 제목을 포함한 구조로 작성되어야합니다.

(작성하지 않고 진행시, Check Release Readiness에서 진행 불가능)

```markdown
## Federated participation, 
## Intended use, 
## Limitations, 
## Local data setup, 
## Privacy
```

## 11. 작성 후 확인

Federated Task 작성이 완료되면 다음 항목을 확인합니다.

| 항목 | 확인 내용 |
| --- | --- |
| 함수 계약 | 고정 함수의 이름, 인자, 반환 형식을 유지했는지 확인합니다. |
| 입력 구조 | 실제 데이터와 smoke/probe 데이터의 입력 구조가 동일한지 확인합니다. |
| 데이터 경로 | load_partition이 전달받은 data_root만 사용하는지 확인합니다. |
| 모델 구조 | 모델의 파라미터 구조가 모든 실행 환경에서 동일한지 확인합니다. |
| Tool AI | Tool manifest, predict, preprocess의 입력 계약이 일치하는지 확인합니다. |
| 라이브러리 | requirements.txt에 사용하는 모든 라이브러리의 버전을 지정했는지 확인합니다. |
| Release | 원본 데이터, 절대경로, 인증정보가 Release에 포함되지 않았는지 확인합니다. |
| Readiness | Local Train과 Release/Participation Readiness가 정상적으로 통과하는지 확인합니다. |
