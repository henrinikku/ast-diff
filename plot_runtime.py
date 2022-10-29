import argparse
import timeit
from pathlib import Path

import pandas as pd
import plotly.express as px

from astdiff.context import DiffContext
from astdiff.generator.with_move import WithMoveEditScriptGenerator
from astdiff.matcher.gumtree import GumTreeMatcher
from astdiff.parser.base import ParseOptions
from astdiff.parser.builtin import BuiltInASTParser

argparser = argparse.ArgumentParser()
argparser.add_argument("--export-path")
args = argparser.parse_args()

file_paths = [
    (
        "tests/data/runtimetest/django_wsgi_200.py",
        "tests/data/runtimetest/django_asgi_300.py",
    ),
    (
        "tests/data/runtimetest/django_core_validators_600.py",
        "tests/data/runtimetest/django_admin_filters_500.py",
    ),
    (
        "tests/data/runtimetest/django_get_or_create_tests_700.py",
        "tests/data/runtimetest/django_constraints_tests_800.py",
    ),
    (
        "tests/data/runtimetest/django_models_options_1000.py",
        "tests/data/runtimetest/django_postgres_test_array_1400.py",
    ),
    (
        "tests/data/runtimetest/django_aggregation_regress_1800.py",
        "tests/data/runtimetest/django_migrations_test_state_2000.py",
    ),
    (
        "tests/data/runtimetest/django_migrations_test_state_2000.py",
        "tests/data/runtimetest/django_model_fields_init_2700.py",
    ),
]


def plot():
    parser = BuiltInASTParser(ParseOptions(True, True))
    matcher = GumTreeMatcher()
    generator = WithMoveEditScriptGenerator()

    times = []

    for source_path, target_path in file_paths:
        print(f"Comparing {source_path} and {target_path}...")

        source_code = Path(source_path).read_text()
        target_code = Path(target_path).read_text()

        start_time = timeit.default_timer()
        source_ast = parser.parse_code(source_code)
        target_ast = parser.parse_code(target_code)
        context = DiffContext(source_ast, target_ast)
        end_time = timeit.default_timer()
        input_size = max(source_ast.metadata.size, target_ast.metadata.size)
        times.append((input_size, "parsing", end_time - start_time))

        matcher.prepare(context)

        start_time = timeit.default_timer()
        matcher.match_anchors(context.source_root, context.target_root)
        end_time = timeit.default_timer()
        times.append((input_size, "anchor matching", end_time - start_time))

        start_time = timeit.default_timer()
        matcher.match_containers(context.source_root, context.target_root)
        end_time = timeit.default_timer()
        times.append((input_size, "container matching", end_time - start_time))

        start_time = timeit.default_timer()
        context.edit_script = generator.generate_edit_script(context)
        end_time = timeit.default_timer()
        times.append((input_size, "script generation", end_time - start_time))

    df = pd.DataFrame(times, columns=["input size", "phase", "time"])
    fig = px.line(df, x="input size", y="time", color="phase")
    fig.write_image(args.export_path)

    print("Done!")
