from dataclasses import dataclass
import yaml

@dataclass
class AppConfig:
    model_path: str
    model_name: str
    model_version: str
    api_key: str
    cors_origins: list
    feature_count: int
    class_labels: list


# 2. Function to load YAML file
def load_config(path: str = "config/settings.yaml") -> AppConfig:
    """
    Reads the YAML file and returns an AppConfig object.
    Keeping configuration loading separate helps in testing and readability.
    """
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    # Create and return an AppConfig object
    config = AppConfig(
        model_path=data["model_path"],
        model_name=data["model_name"],
        model_version=data["model_version"],
        api_key=data["api_key"],
        cors_origins=data.get("cors_origins", ["*"]),
        feature_count=int(data["feature_count"]),
        class_labels=list(data["class_labels"]),
    )
    return config
