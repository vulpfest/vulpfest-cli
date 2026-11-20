"""Pengaturan lokal vulpfest: folder hasil dan status cek versi. Disimpan di ~/.vulpfest/."""
import json
import os
from pathlib import Path


def home_dir():
    return Path(os.environ.get("VULPFEST_HOME") or (Path.home() / ".vulpfest")).expanduser()


def _read(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _write(path, data):
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    except Exception:
        pass


def default_out_dir():
    docs = Path.home() / "Documents"
    return (docs if docs.is_dir() else Path.home()) / "Vulpfest"


def out_dir():
    env = os.environ.get("VULPFEST_OUT")
    if env:
        return Path(env).expanduser()
    value = _read(home_dir() / "config.json").get("out_dir")
    return Path(value).expanduser() if value else default_out_dir()


def set_out_dir(path):
    cfg = _read(home_dir() / "config.json")
    cfg["out_dir"] = str(Path(path).expanduser().resolve())
    _write(home_dir() / "config.json", cfg)
    return cfg["out_dir"]


def state():
    return _read(home_dir() / "state.json")


def save_state(data):
    current = state()
    current.update(data)
    _write(home_dir() / "state.json", current)


def resolve_out(value):
    """Nama file tanpa folder disimpan di folder hasil. Jalur yang menyebut folder dibiarkan apa adanya."""
    path = Path(value).expanduser()
    if path.is_absolute() or path.parent != Path("."):
        return str(path)
    folder = out_dir()
    folder.mkdir(parents=True, exist_ok=True)
    return str(folder / path.name)
