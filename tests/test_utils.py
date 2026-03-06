import torch

from loom.geometry.randomizer import generate_random_so3


def test_generate_random_so3_shape():
    matrix = generate_random_so3()
    assert matrix.shape == (1, 3, 3)


def test_generate_random_so3_orthogonal():
    matrix = generate_random_so3(4)
    result = matrix @ matrix.transpose(2, 1)
    identity = torch.eye(3, dtype=matrix.dtype, device=matrix.device)
    assert torch.allclose(result, identity, atol=1e-6)


def test_generate_random_so3_determinant():
    matrix = generate_random_so3(2)
    det = torch.linalg.det(matrix)
    assert torch.allclose(det, torch.tensor(1.0), atol=1e-3)


def test_generate_random_so3_randomness():
    matrix1 = generate_random_so3()
    matrix2 = generate_random_so3()
    assert not torch.allclose(matrix1, matrix2, atol=1e-6)


def test_generate_random_so3_preserves_norm():
    matrix = generate_random_so3()
    vector = torch.tensor([1.0, 2.0, 3.0])
    rotated = matrix @ vector

    original_norm = torch.linalg.norm(vector)
    rotated_norm = torch.linalg.norm(rotated)

    assert torch.allclose(original_norm, rotated_norm, atol=1e-6)
