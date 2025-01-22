# plugins/plugin_loader.py
import os
import yaml
import importlib.util
from src.apps.core.certificates import verify_signature

def load_plugins(app):
    plugins_dir = os.path.join(os.path.dirname(__file__))
    for plugin_name in os.listdir(plugins_dir):
        plugin_path = os.path.join(plugins_dir, plugin_name)
        if os.path.isdir(plugin_path) and plugin_name != '__pycache__':
            load_plugin(app, plugin_path, plugin_name)

def load_plugin(app, plugin_path, plugin_name):
    manifest_path = os.path.join(plugin_path, 'manifest.yaml')
    if os.path.exists(manifest_path):
        manifest_data, manifest = read_manifest(manifest_path)
        signature = manifest.get('signature')
        if signature and verify_signature(manifest_data, bytes.fromhex(signature)):
            load_plugin_pages(app, plugin_path, plugin_name)
        else:
            print(f"Plugin '{plugin_name}' failed signature verification.")

def read_manifest(manifest_path):
    with open(manifest_path, 'rb') as f:
        manifest_data = f.read()
    with open(manifest_path, 'r') as f:
        manifest = yaml.safe_load(f)
    return manifest_data, manifest

def load_plugin_pages(app, plugin_path, plugin_name):
    pages_dir = os.path.join(plugin_path, 'pages')
    if os.path.exists(pages_dir):
        for page_file in os.listdir(pages_dir):
            if page_file.endswith('.py'):
                module_name = f"plugins.{plugin_name}.pages.{page_file[:-3]}"
                spec = importlib.util.spec_from_file_location(module_name, os.path.join(pages_dir, page_file))
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                app.include_router(module.router)