import numpy as np
import pytest
from instant_insanity.core.projection import ModelToSceneConversion
from manim.typing import Point3D
from manim import RIGHT, UP, OUT, ORIGIN

SCENE_ORIGIN: Point3D = RIGHT + 2.0 * UP + 3.0 * OUT
SCENE_PER_MODEL: float = 0.5
MODEL_TO_SCENE_CONVERSION: ModelToSceneConversion = ModelToSceneConversion(SCENE_ORIGIN, SCENE_PER_MODEL)

def test_convert_model_to_scene_origin():
    scene_point: Point3D = MODEL_TO_SCENE_CONVERSION.convert_model_to_scene(SCENE_ORIGIN)
    assert np.allclose(scene_point, ORIGIN)

def test_convert_scene_to_model_origin():
    model_point: Point3D = MODEL_TO_SCENE_CONVERSION.convert_scene_to_model(ORIGIN)
    assert np.allclose(model_point, SCENE_ORIGIN)

MODEL_SCENE_PAIRS: list[tuple[Point3D, Point3D]] = [
        (SCENE_ORIGIN,          ORIGIN),
        (SCENE_ORIGIN + RIGHT,  RIGHT * SCENE_PER_MODEL),
        (SCENE_ORIGIN + UP,     UP * SCENE_PER_MODEL),
        (SCENE_ORIGIN + OUT,    OUT * SCENE_PER_MODEL),
    ]

@pytest.mark.parametrize("model_point, expected_scene_point", MODEL_SCENE_PAIRS)
def test_convert_model_to_scene(model_point, expected_scene_point):
    actual_scene_point = MODEL_TO_SCENE_CONVERSION.convert_model_to_scene(model_point)
    assert np.allclose(actual_scene_point, expected_scene_point)

@pytest.mark.parametrize("expected_model_point, scene_point", MODEL_SCENE_PAIRS)
def test_convert_scene_to_model(expected_model_point, scene_point):
    actual_model_point = MODEL_TO_SCENE_CONVERSION.convert_scene_to_model(scene_point)
    assert np.allclose(actual_model_point, expected_model_point)
